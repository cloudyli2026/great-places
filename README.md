# THE GREAT PLACES

A bilingual, evidence-led atlas of great public spaces, urban streets and architecture.

## Pilot: Piazza San Marco, Venice

The research separates historical drawings from contemporary measured data. No inferred geometry, AI image or unsourced measurement may be labeled as surveyed evidence.

## Evidence standard

- S1: original measured drawings, authoritative archives, official surveys
- S2: peer-reviewed research and published professional drawings
- S3: GIS / OpenStreetMap geometry, checked against imagery and metadata
- S4: interpretation or unverified inference; never presented as measured fact

Every visual asset must record creator, date, institution/source URL, license/reuse status, geographic scope, and confidence. Unknown rights mean link to the original rather than copy it into the repository.

## Research workflow

Source discovery → provenance review → spatial analysis → visual cross-check → editorial review → publication.

## Pilot milestones

1. Verify historical Piazza/Piazzetta plan and Campanile section.
2. Acquire and validate current building footprints and scale.
3. Geolocate photograph viewpoints and section lines.
4. Produce seven-dimension evidence matrix; score only where supported.
5. Build the bilingual interactive case page.

The repository starts with research infrastructure; it does **not** claim a finished survey or published site.

## 04 Federation Square

The bilingual case in `docs/cases/federation-square.html` now has reviewed content in `cases/federation-square/case.json`, an individual asset register, frozen official Melbourne 2020 footprints and a reproducible SVG figure-ground. See [the comparison audit](cases/federation-square/RESEARCH_AUDIT.md) and [actual browser/source test results](docs/research/federation-square/README.md). Formal Space Syntax results, independent behavioural observations and a complete calibrated orthographic elevation set remain unavailable and are explicitly identified.

Regenerate the page with `python scripts/build_federation_page.py`, and the figure-ground with `python scripts/update_federation_gis.py --offline`. Run `python tests/federation-gis.py`, `python tests/federation-links.py`, and the Chromium/Playwright regression in `tests/federation-browser.cjs` while serving `docs/` on port 8000.
