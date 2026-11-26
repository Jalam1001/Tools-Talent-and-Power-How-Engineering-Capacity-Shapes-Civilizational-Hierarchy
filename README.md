# The Oldest Law of Power

**Technology, Human Hierarchy, and the Architecture of the Emerging Global Order**

A monograph by **Javed Alam**. Version 0.2, revised November 2026 (first published December 2025).

This essay argues that technology has always structured human hierarchy, and that in the twenty-first century engineering capacity—not ideology—is a central constraint on national power. It examines global STEM talent, platform ecosystems such as TikTok and Douyin, and a revised map of system-builders, specialized chokepoint builders, system-consumers, and system-dependents.

## Read and download

- **[Read online](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/)** — full HTML article (GitHub Pages entry page)
- **[Download the v0.2 PDF](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/The-Oldest-Law-of-Power-v0.2.pdf)** ([release asset](https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/releases/download/v0.2/The-Oldest-Law-of-Power-v0.2.pdf))

## Table of contents

- [Introduction](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#introduction)
- [Technology as an Evolutionary and Anthropological Foundation](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:anthro)
  - From Tools to Techniques to Institutions
  - Technology and the Elimination of Ecological Constraints
- [Why Technology Rarely Receives Historical Credit](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:credit)
- [Complexity in the Modern Era: The End of the Lone Genius](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:complexity)
  - Division of Cognitive Labor in High-Complexity Systems
- [The Global STEM Imbalance: Demographic and Educational Realities](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:stem)
  - China: Engineering as National Strategy
  - India: Rising Talent in a Constrained Infrastructure
  - The United States: High Talent Density, Low Talent Volume
  - Europe and the Rest of the World
- [Platforms as Ecosystems: The ByteDance Model](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:platforms)
  - Douyin: An Integrated Digital Economy
  - TikTok and the 2026 U.S. Joint Venture
  - Editing Pipelines: CapCut and Jianying
- [The Coming Three-Tier World Order](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:tiers)
- [Qualifications and Counterarguments](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:counter)
  - Institutions, not tools, as the first cause
  - Quality versus headcount
  - Small states and specialized chokepoints
- [Policy and Research Implications](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#sec:policy)
  - Education Policy and the Design of STEM Pipelines
  - Immigration Policy and the Global Market for Engineers
  - Industrial Policy and Technological Sovereignty
  - Platform Governance and Cross-Border Dependence
  - Research Agenda: The Political Economy of Technological Systems
- [Conclusion](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#conclusion)
- [References](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#references)
- [Revision notes](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#revisions)
- [How to cite](https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/#cite)

## Versions

| Version | Date | Description |
| --- | --- | --- |
| [v0.2](https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/releases/tag/v0.2) | November 2026 | Revised edition, HTML site, corrected citations and figures |
| [v0.1](https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/releases/tag/v0.1) | December 2025 | Original edition, preserved as first published |

The original v0.1 PDF is kept in [`original/The-Oldest-Law-of-Power-v0.1-original.pdf`](original/The-Oldest-Law-of-Power-v0.1-original.pdf) and as a [release asset](https://github.com/Jalam1001/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/releases/download/v0.1/The-Oldest-Law-of-Power-v0.1-original.pdf). A detailed list of changes is in [CHANGELOG.md](CHANGELOG.md).

## Citation

Alam, Javed. *The Oldest Law of Power: Technology, Human Hierarchy, and the Architecture of the Emerging Global Order*. Version 0.2. 2026. https://jalam1001.github.io/Tools-Talent-and-Power-How-Engineering-Capacity-Shapes-Civilizational-Hierarchy/

A machine-readable citation is in [`CITATION.cff`](CITATION.cff).

## License

Copyright © 2025–2026 Javed Alam. The author retains copyright.

The text and figures of the monograph are licensed under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Build scripts are licensed under the MIT License. See [LICENSE.md](LICENSE.md).

## Building from source

The paper is written in LaTeX (`paper/main.tex`, `paper/references.bib`). On a system with TeX Live, pandoc, and pdf2svg:

```bash
make          # PDF and HTML site
make pdf      # PDF only
make site     # PDF plus docs/ for GitHub Pages
```

The official PDF is written to `The-Oldest-Law-of-Power-v0.2.pdf` and copied into `docs/` for the website. Intermediate LaTeX files remain under `paper/`.

`scripts/build_site.py` converts the LaTeX source into the HTML article and writes it to `docs/index.html` (the GitHub Pages entry page) and identically to `docs/essay.html`, so older links continue to work. The page opens with the title, author, version, date, and a link to the v0.2 PDF; revision notes, the v0.1 PDF, and the citation appear after the references.

The GitHub repository name is unchanged from the original posting. The document title used throughout is *The Oldest Law of Power: Technology, Human Hierarchy, and the Architecture of the Emerging Global Order*.
