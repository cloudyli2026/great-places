# 01 / 03 / 04 — shared reader and research vocabulary

The current publication source is `01.json`, `03.json`, `04.json` and `vocabulary.json` in this directory. `cases/federation-square/` preserves the earlier, more detailed asset/source register; its former independent layout is superseded.

Run `python scripts/build_case_readers.py` to regenerate all three case pages, the four-page comparison and JSON/CSV exports. Edit `docs/assets/case-reader.css` and `.js` once for all readers. The builder embeds identical copies to support GitHub's third-party HTML preview without raw-JavaScript MIME failures. Generated pages carry a shared reader-version hash.

All cases use the same eight chapters and 17 smaller pages. The active page alone appears; hash URLs, browser history, chapter tabs, previous/next, language persistence, image inspection and printable factsheets share one implementation. Long citations and methodological discussion belong in collapsed Sources disclosures. Climate belongs in environmental assessment, not a separate chapter.

## Shared dimensions

Spatial form; public transport; landscape integration; commercial edges; climate response; use programme; ordinary/holiday use; capacity and annual visitation; technology; community/tourism. These are evidence-based judgments, not numerical quality scores. Each conclusion has exactly three defining qualities.

## Numerical scope

- Population: municipality/LGA and reference date; registry versus estimated resident population disclosed. Melbourne metropolitan population is separate from the LGA.
- Capacity: a published event/layout-specific number, not area divided by a speculative crowd density. San Marco's 20,000 relates to the **2018 Flight of the Angel**; Siena's approximately 15,000 is the **central standing area at the July 2026 Palio**, reported by the safety provider; Federation Square's 10,000 is the **current Main Square venue listing**. These are not interchangeable legal limits for all occasions.
- Annual visitation: Federation Square's 11.9M+ is reported visitation for FY2025–26, not a deduplicated population. No square-level annual total was established for 01 or 03. Their values remain JSON null / CSV empty, not zero or city tourism totals.
- Calendar: compare ordinary weekdays, normal weekends/holidays, and major event days separately. No matched continuous pedestrian series was established for all three; do not calculate holiday growth factors or annual-to-daily averages.
- Climate: city-level climatology with station/period, not measured plaza comfort. Melbourne's former Regional Office historical series and Siena's 1961–90 baseline are not a claim of contemporary site monitoring.
- Building coverage: union of actual polygons clipped to an identical 600 × 600 m metric frame, including water in the denominator. Official Melbourne 2020 and Overture 2026 have different epochs/definitions; coverage is morphology, not a public-space quality rank.

## Drawings and evidence

04 uses the original design-team plan/section images, displayed directly. The slope detail is a viewport crop of the original city section; inspection opens the complete original. The approximately 6 m west–east rise is stated in the Heritage Council determination, physical PDF page 6. No universal slope percentage or access-compliance conclusion is inferred.

03's directly displayed plan/sections are limited excerpts of Lisa Hollmann's 2025 TU Wien thesis: Abb.4 on physical PDF spread 26 and Abb.7/8 on spread 29. Original graphics/scales retained; not relabeled as a municipal survey. Attribution and exact crop metadata: `docs/drawings/sources.json`.

01 retains existing local project images; where original creator/date was absent, the reader identifies that limitation. No invented attribution or survey status is added.

Connectivity is a qualitative reading of maps and published drawings. There is no authenticated segment/axial model, radius definition or formal integration/choice run for these pages. The reader does not claim Space Syntax numerical results.

## Tests

```sh
python -m pip install -r scripts/requirements-gis.txt
python scripts/build_comparison_figures.py
python tests/case-reader-integrity.py
python tests/federation-gis.py
python tests/case-reader-links.py
python -m http.server 8017 --directory docs
# separate terminal, Node.js + Playwright + Chromium installed:
node tests/case-reader-browser.cjs
```

Browser defaults to `http://127.0.0.1:8017/`; set `TEST_BASE` to an alternate root and `TEST_OUTPUT` for artifacts. Link audit uses GET, actual image MIME, PDF magic bytes and reports access-challenge HTML separately from HTTP status. Browser validation decodes real images (including original SVG image references), checks rendered Google Maps, three viewport widths, both languages, pagination, history, inspection, and PDF printing. GIS integrity independently verifies metric scale against geodesic 100 m offsets and deterministic rebuilds. No live remote dataset is needed for offline GIS rebuilding.
