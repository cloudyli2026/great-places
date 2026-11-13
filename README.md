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

## Aligned readers: 01 / 03 / 04

San Marco, Piazza del Campo and Federation Square share one bilingual, paginated reader, ten assessment dimensions, scoped numerical indicators and three defining qualities per case. Start at [the three-case comparison](docs/comparison.html), or [01](docs/index.html), [03](docs/cases/piazza-del-campo.html), [04](docs/cases/federation-square.html).

The current content source is `cases/reader/`, with shared CSS/JS under `docs/assets/`. Run `python scripts/build_case_readers.py`; do not hand-edit generated HTML. See [the content and evidence contract](cases/reader/README.md) for scope, reproducible build and browser/GIS/source test commands, and [actual review evidence](docs/research/aligned-cases/README.md).

All three figure-grounds use 600 × 600 m metric frames, north up, and 100 m graphic bars. The native 300 mm SVG is 1:2500; responsive screen rendering uses the graphic bar. Melbourne retains official 2020 footprints; 01 and 03 use frozen Overture extracts with source/license metadata. Original data epochs differ and white space includes water.

The earlier 04 source register and [first-stage audit](cases/federation-square/RESEARCH_AUDIT.md) remain available. Earlier 04-only browser screenshots refer to that previous reader, not the current three-case implementation.
