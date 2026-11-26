#!/usr/bin/env python3
"""Build the GitHub Pages landing page and HTML reading edition from the pandoc HTML."""
from __future__ import annotations

import re
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
PAPER = ROOT / "paper"
RAW = Path("/tmp/essay-raw.html")

CITE_ORDER = [
    "mithen1996",
    "gamble2013",
    "diamond1997",
    "arthur2009",
    "wrangham2009",
    "perez2002",
    "pomeranz2000",
    "landes1998",
    "acemoglu2012",
    "kelly2010",
    "russell2020",
    "tegmark2017",
    "bls2025sd",
    "oliss2023",
    "nasem2024",
    "tiktokusds2026",
    "forristal2026",
    "miller2022",
    "oecd2023",
    "mazzucato2013",
]
CITE_NUM = {k: i + 1 for i, k in enumerate(CITE_ORDER)}

TABLE_CAPTIONS = {
    1: "Selected technological transitions and associated civilizational patterns.",
    2: "Illustrative division of cognitive labor in a large-scale AI or platform organization.",
    3: "STEM graduate volume (CSET, 2020 data, where available) and a qualitative assessment of system-building capacity. Counts follow CSET’s tertiary STEM definition and are not a measure of quality.",
    4: "Stylized comparison of Douyin (China) and TikTok (U.S. and global), updated to reflect the January 2026 U.S. joint venture.",
    5: "Revised technological world order, distinguishing general system-builders from specialized chokepoint builders. Examples are indicative, not exhaustive.",
}

FIG_SRC = {
    "figures/fig1-niche.pdf": "figures/fig1-niche.svg",
    "figures/fig2-chain.pdf": "figures/fig2-chain.svg",
    "figures/fig3-pyramid.pdf": "figures/fig3-pyramid.svg",
    "figures/fig4-layers.pdf": "figures/fig4-layers.svg",
    "figures/fig5-sovereignty.pdf": "figures/fig5-sovereignty.svg",
}

LABEL_TO_NUM = {
    "tab:transitions": "1",
    "tab:labor": "2",
    "tab:stem": "3",
    "tab:douyin": "4",
    "tab:tiers": "5",
    "fig:niche": "1",
    "fig:chain": "2",
    "fig:layers": "3",
    "fig:pyramid": "4",
    "fig:sovereignty": "5",
    "sec:anthro": "2",
    "sec:credit": "3",
    "sec:complexity": "4",
    "sec:stem": "5",
    "sec:platforms": "6",
    "sec:tiers": "7",
    "sec:counter": "8",
    "sec:policy": "9",
}


def strip_tags(html: str) -> str:
    return unescape(re.sub(r"<[^>]+>", "", html))


def parse_tabularx(block: str, number: int) -> str:
    inner = re.sub(r"^<div class=\"tabularx\">\s*<p>", "", block)
    inner = re.sub(r"</p>\s*</div>$", "", inner)
    # drop latex column-spec junk (nested spans) before the header
    inner = re.sub(r"^.*?(?=<strong>)", "", inner, flags=re.S)
    inner = re.sub(r"\s+", " ", inner).strip()
    # rows split by <br />
    rows = [r.strip() for r in re.split(r"<br\s*/?>", inner) if r.strip()]
    parsed = []
    for row in rows:
        cells = [c.strip() for c in row.split("&amp;")]
        parsed.append(cells)
    if not parsed:
        return block
    header, body = parsed[0], parsed[1:]
    # pad
    ncols = max(len(r) for r in parsed)
    def pad(r):
        return r + [""] * (ncols - len(r))
    html = [f'<table id="tab-{number}">', "<thead><tr>"]
    for c in pad(header):
        html.append(f"<th>{c}</th>")
    html.append("</tr></thead><tbody>")
    for r in body:
        html.append("<tr>")
        for c in pad(r):
            html.append(f"<td>{c}</td>")
        html.append("</tr>")
    html.append("</tbody></table>")
    cap = TABLE_CAPTIONS[number]
    return (
        f'<figure class="table-wrap" id="table-{number}">'
        f'<figcaption><span class="fig-label">Table {number}.</span> {cap}</figcaption>'
        + "".join(html)
        + "</figure>"
    )


def convert_citations(html: str) -> str:
    def repl(m: re.Match) -> str:
        keys = m.group(1).split()
        nums = []
        for k in keys:
            if k not in CITE_NUM:
                return m.group(0)
            nums.append(CITE_NUM[k])
        # collapse consecutive? keep simple
        links = []
        for n, k in zip(nums, keys):
            links.append(f'<a class="cite" href="#ref-{k}">[{n}]</a>')
        if len(links) == 1:
            return links[0]
        return "".join(links) if False else '<span class="cites">' + "".join(links) + "</span>"

    return re.sub(
        r'<span class="citation" data-cites="([^"]+)">.*?</span>',
        repl,
        html,
        flags=re.S,
    )


def convert_internal_refs(html: str) -> str:
    def repl(m: re.Match) -> str:
        typ, lab, text = m.group(1), m.group(2), m.group(3)
        num = LABEL_TO_NUM.get(lab)
        display = num if num else strip_tags(text)
        return f'<a href="#{lab}" class="xref">{display}</a>'

    html = re.sub(
        r'<a\s+href="#([^"]+)"\s+data-reference-type="ref"\s+data-reference="([^"]+)">(.*?)</a>',
        repl,
        html,
        flags=re.S,
    )
    # leftover pandoc placeholders such as [tab:transitions]
    html = re.sub(r"\[(tab|fig|sec):[^\]]+\]", "", html)
    return html


def convert_figures(html: str) -> str:
    def repl(m: re.Match) -> str:
        block = m.group(0)
        fid = m.group(1)
        src = m.group(2)
        cap = m.group(3)
        svg = FIG_SRC.get(src, src.replace(".pdf", ".svg"))
        num = LABEL_TO_NUM.get(fid, "")
        cap_text = re.sub(r"\s+", " ", cap).strip()
        wide = " wide" if "pyramid" in svg or "chain" in svg or "layers" in svg else ""
        return (
            f'<figure class="diagram{wide}" id="{fid}">'
            f'<img src="{svg}" alt="{strip_tags(cap_text)}" />'
            f'<figcaption><span class="fig-label">Figure {num}.</span> {cap_text}</figcaption>'
            f"</figure>"
        )

    return re.sub(
        r'<figure id="(fig:[^"]+)"[^>]*>\s*<embed src="([^"]+)"[^>]*/?>\s*<figcaption>(.*?)</figcaption>\s*</figure>',
        repl,
        html,
        flags=re.S,
    )


def convert_tables(html: str) -> str:
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        n += 1
        return parse_tabularx(m.group(0), n)

    return re.sub(r'<div class="tabularx">.*?</div>', repl, html, flags=re.S)


def extract_body(html: str) -> str:
    m = re.search(r"<body[^>]*>(.*)</body>", html, re.S)
    body = m.group(1)
    # drop pandoc title header
    body = re.sub(r'<header id="title-block-header">.*?</header>', "", body, flags=re.S)
    return body.strip()


def number_sections(html: str) -> str:
    # Add visible section numbers to h1s (except abstract/refs). Already have ids.
    # Leave headings as authored; TOC will number them.
    return html


def build_toc(html: str) -> str:
    items = []
    for m in re.finditer(r"<h([12])\b([^>]*)>(.*?)</h\1>", html, re.S):
        attrs, title_html = m.group(2), m.group(3)
        idm = re.search(r'id="([^"]+)"', attrs)
        if not idm:
            continue
        level, hid = m.group(1), idm.group(1)
        title = re.sub(r"\s+", " ", strip_tags(title_html)).strip()
        if hid in {"title-block-header"}:
            continue
        items.append((level, hid, title))
    parts = ['<nav class="toc" aria-label="Table of contents">', "<h2>Contents</h2>", "<ol>"]
    open_sub = False
    for level, hid, title in items:
        if level == "1":
            if open_sub:
                parts.append("</ol></li>")
                open_sub = False
            parts.append(f'<li><a href="#{hid}">{title}</a>')
            # may open sub
            open_sub = False
            parts.append("")  # placeholder, we'll handle on the fly
        else:
            if not open_sub:
                # remove the dangling empty and open
                if parts[-1] == "":
                    parts.pop()
                parts.append("<ol>")
                open_sub = True
            else:
                if parts[-1] == "":
                    parts.pop()
            parts.append(f'<li><a href="#{hid}">{title}</a></li>')
    if open_sub:
        parts.append("</ol></li>")
    # close any unclosed li from h1 without sub
    # cleanup empty placeholders
    cleaned = []
    for p in parts:
        if p == "":
            cleaned.append("</li>")
        else:
            cleaned.append(p)
    # The logic is messy. Simpler approach:
    parts = ['<nav class="toc" aria-label="Table of contents">', "<h2>Contents</h2>", "<ol class=\"toc-list\">"]
    for level, hid, title in items:
        cls = "toc-h1" if level == "1" else "toc-h2"
        parts.append(f'<li class="{cls}"><a href="#{hid}">{title}</a></li>')
    parts.append("</ol></nav>")
    return "\n".join(parts)


def add_ref_ids(html: str) -> str:
    # pandoc citeproc uses id="ref-key"
    # already present as id="ref-mithen1996"
    # Add a heading if missing
    if 'id="refs"' in html and "<h1" not in html[html.find('id="refs"') - 80 : html.find('id="refs"') + 20]:
        html = html.replace(
            '<div id="refs"',
            '<h1 id="references">References</h1>\n<div id="refs"',
            1,
        )
    return html


ESSAY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>The Oldest Law of Power — Javed Alam</title>
  <meta name="description" content="A monograph on how engineering capacity shapes human hierarchy and the emerging global order, by Javed Alam. Version 0.2." />
  <meta name="author" content="Javed Alam" />
  <meta property="og:title" content="The Oldest Law of Power: Technology, Human Hierarchy, and the Architecture of the Emerging Global Order" />
  <meta property="og:description" content="A monograph by Javed Alam on engineering capacity, technological sovereignty, and geopolitical hierarchy. Version 0.2." />
  <meta property="og:type" content="article" />
  <meta property="og:image" content="assets/social-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="stylesheet" href="css/style.css" />
  <link rel="canonical" href="essay.html" />
</head>
<body class="essay-page">
  <a class="skip" href="#main">Skip to the essay</a>
  <header class="site-header">
    <div class="inner">
      <a class="wordmark" href="index.html">The Oldest Law of Power</a>
      <nav>
        <a href="index.html">Home</a>
        <a href="essay.html" aria-current="page">Read</a>
        <a href="The-Oldest-Law-of-Power-v0.2.pdf">PDF</a>
        <a href="essay.html#references">Cite</a>
      </nav>
    </div>
  </header>
  <article id="main" class="essay">
    <header class="essay-hero">
      <p class="eyebrow">A monograph · Version 0.2</p>
      <h1>The Oldest Law of Power</h1>
      <p class="subtitle">Technology, Human Hierarchy, and the Architecture of the Emerging Global Order</p>
      <p class="byline">Javed Alam</p>
      <p class="dateline">December 2025; revised November 2026</p>
    </header>
    <section class="abstract-block" id="abstract">
      <h2>Abstract</h2>
      <p>Technology has always been the primary driver of hierarchy within human societies. From the earliest stone tools to modern artificial intelligence systems, the capacity to create and wield technical innovations has consistently determined which groups ascend and which decline. Although contemporary discourse often frames technological disruption as a novel phenomenon, the historical record shows that technological capacity has consistently structured civilizational hierarchy. The twenty-first century magnifies this pattern: modern systems—artificial intelligence, advanced computation, semiconductor fabrication, autonomous platforms—require engineering capacities beyond the abilities of individuals or nations with limited STEM ecosystems.</p>
      <p>This monograph examines the deep anthropological roots of technological hierarchy, analyzes the modern imbalance of engineering talent among global blocs, explores the structural implications of platform ecosystems such as TikTok, Douyin, CapCut, and Jianying, and outlines an emerging world order shaped by engineering density rather than ideology or traditional geopolitics. The three-tier map is then qualified: institutions, the quality of training as well as its volume, and specialized small-state system-builders such as Taiwan, the Netherlands, South Korea, and Israel all matter, and they refine rather than repeal the central claim.</p>
    </section>
    {toc}
    {body}
  </article>
  <footer class="site-footer">
    <div class="inner">
      <p>© 2025–2026 Javed Alam. The text and figures of this monograph are licensed under <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
      <p><a href="index.html">Home</a> · <a href="The-Oldest-Law-of-Power-v0.2.pdf">Download the PDF</a> · <a href="https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy">Source on GitHub</a></p>
    </div>
  </footer>
</body>
</html>
"""


LANDING = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>The Oldest Law of Power — Javed Alam</title>
  <meta name="description" content="A monograph on how engineering capacity shapes human hierarchy and the emerging global order, by Javed Alam. Version 0.2." />
  <meta name="author" content="Javed Alam" />
  <meta property="og:title" content="The Oldest Law of Power: Technology, Human Hierarchy, and the Architecture of the Emerging Global Order" />
  <meta property="og:description" content="A monograph by Javed Alam on engineering capacity, technological sovereignty, and geopolitical hierarchy. Version 0.2." />
  <meta property="og:type" content="website" />
  <meta property="og:image" content="assets/social-preview.png" />
  <meta name="twitter:card" content="summary_large_image" />
  <link rel="stylesheet" href="css/style.css" />
</head>
<body class="home">
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header">
    <div class="inner">
      <a class="wordmark" href="index.html">The Oldest Law of Power</a>
      <nav>
        <a href="index.html" aria-current="page">Home</a>
        <a href="essay.html">Read</a>
        <a href="The-Oldest-Law-of-Power-v0.2.pdf">PDF</a>
        <a href="#cite">Cite</a>
      </nav>
    </div>
  </header>
  <main id="main">
    <section class="hero">
      <p class="eyebrow">A monograph · Version 0.2 · November 2026</p>
      <h1>The Oldest Law of Power</h1>
      <p class="subtitle">Technology, Human Hierarchy, and the Architecture of the Emerging Global Order</p>
      <p class="byline">Javed Alam</p>
      <p class="standfirst">From early tools to modern AI, engineering capacity—not ideology—has structured human hierarchy. This monograph traces that law of power, measures the global imbalance of STEM talent, and asks what it means for sovereignty in an age of platforms.</p>
      <div class="actions">
        <a class="btn primary" href="essay.html">Read online</a>
        <a class="btn" href="The-Oldest-Law-of-Power-v0.2.pdf">Download PDF</a>
        <a class="btn ghost" href="#cite">Cite this work</a>
      </div>
    </section>

    <section class="abstract-block" id="abstract">
      <h2>Abstract</h2>
      <p>Technology has always been the primary driver of hierarchy within human societies. From the earliest stone tools to modern artificial intelligence systems, the capacity to create and wield technical innovations has consistently determined which groups ascend and which decline. Although contemporary discourse often frames technological disruption as a novel phenomenon, the historical record shows that technological capacity has consistently structured civilizational hierarchy. The twenty-first century magnifies this pattern: modern systems—artificial intelligence, advanced computation, semiconductor fabrication, autonomous platforms—require engineering capacities beyond the abilities of individuals or nations with limited STEM ecosystems.</p>
      <p>This monograph examines the deep anthropological roots of technological hierarchy, analyzes the modern imbalance of engineering talent among global blocs, explores the structural implications of platform ecosystems such as TikTok, Douyin, CapCut, and Jianying, and outlines an emerging world order shaped by engineering density rather than ideology or traditional geopolitics. The three-tier map is then qualified: institutions, the quality of training as well as its volume, and specialized small-state system-builders such as Taiwan, the Netherlands, South Korea, and Israel all matter, and they refine rather than repeal the central claim.</p>
    </section>

    <section class="meta-grid">
      <div>
        <h2>This edition</h2>
        <p>Version 0.2 (November 2026) corrects citations, grounds the STEM comparison in Georgetown CSET’s 2020 data, updates the TikTok U.S. joint-venture account to verified 2026 reporting, draws the figures, adds a counterarguments section, and publishes an HTML reading edition.</p>
        <p><a href="https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/blob/main/CHANGELOG.md">See the changelog</a></p>
      </div>
      <div>
        <h2>Previous version</h2>
        <p>Version 0.1 is the original edition, preserved as first published in December 2025.</p>
        <p><a href="https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/releases/tag/v0.1">Release v0.1</a><br />
        <a href="https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/releases/download/v0.1/The-Oldest-Law-of-Power-v0.1-original.pdf">Download the original PDF</a></p>
      </div>
    </section>

    <section class="cite-block" id="cite">
      <h2>Cite</h2>
      <blockquote>
        <p>Alam, Javed. <em>The Oldest Law of Power: Technology, Human Hierarchy, and the Architecture of the Emerging Global Order</em>. Version 0.2. 2026. https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/</p>
      </blockquote>
      <p>A machine-readable <a href="https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/blob/main/CITATION.cff"><code>CITATION.cff</code></a> file is included in the repository. The text and figures are licensed under <a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0</a>. The author, Javed Alam, retains copyright.</p>
    </section>
  </main>
  <footer class="site-footer">
    <div class="inner">
      <p>© 2025–2026 Javed Alam. Text and figures: <a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>.</p>
      <p><a href="https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy">GitHub repository</a></p>
    </div>
  </footer>
</body>
</html>
"""


def main() -> None:
    DOCS.mkdir(exist_ok=True)
    (DOCS / "css").mkdir(exist_ok=True)
    (DOCS / "figures").mkdir(exist_ok=True)
    (DOCS / "assets").mkdir(exist_ok=True)

    raw = RAW.read_text()
    body = extract_body(raw)
    body = convert_tables(body)
    body = convert_figures(body)
    body = convert_citations(body)
    body = convert_internal_refs(body)
    body = add_ref_ids(body)
    # Drop accidental empty p / tabular leftovers
    body = re.sub(r"<p>\s*</p>", "", body)
    body = re.sub(r'<div class="center">.*?</div>', "", body, count=1, flags=re.S)
    toc = build_toc(body)

    essay = ESSAY_TEMPLATE.format(toc=toc, body=body)
    (DOCS / "essay.html").write_text(essay)
    (DOCS / "index.html").write_text(LANDING)

    # copy figures and pdf
    for svg in (PAPER / "figures").glob("fig*.svg"):
        dest = DOCS / "figures" / svg.name
        dest.write_bytes(svg.read_bytes())
    pdf_src = ROOT / "The-Oldest-Law-of-Power-v0.2.pdf"
    if pdf_src.exists():
        (DOCS / "The-Oldest-Law-of-Power-v0.2.pdf").write_bytes(pdf_src.read_bytes())

    print("wrote", DOCS / "index.html")
    print("wrote", DOCS / "essay.html", "bytes", (DOCS / "essay.html").stat().st_size)
    print("figures", list((DOCS / "figures").glob("*.svg")))


if __name__ == "__main__":
    main()
