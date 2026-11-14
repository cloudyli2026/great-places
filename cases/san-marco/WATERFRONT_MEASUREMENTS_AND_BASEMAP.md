# San Marco — measured waterfront typologies from published research

## Verified published dataset (not a Piazza cross-section)

A peer-reviewed coastal engineering study provides an orthophoto with a **0–50 m scale bar** and a table of **three waterfront cross-section typologies** along Riva S. Marco. This is the first source in this research series with explicit cross-section numerical parameters.

**Primary source:** *Water* **12** (2020), article 427, p.4, Figure 2 and Table 1: https://www.research.unipd.it/retrieve/e14fb26c-c85c-3de1-e053-1705fe0ac030/water-12-00427-v2.pdf

| Type | Paper's description | Reach length | z1 | z2 | z3 | L1 | L2 |
|---|---|---:|---:|---:|---:|---:|---:|
| A | Vertical wall (Fig. 3a) | 25 m | 1.00 m | 1.10 m | 1.10 m | 5 m | 0 m |
| B | Vertical wall (Fig. 3a) | 15 m | 1.00 m | 1.10 m | 1.17 m | 5 m | 15 m |
| C | With steps (Fig. 3b) | 85 m | 1.00 m | 1.10 m | 1.17 m | 5 m | 15 m |

**Critical interpretation:** the reach lengths (25/15/85 m) are *lengths of shoreline segments*, not the width of the section. The z1/z2/z3 and L1/L2 variables must be interpreted with the original Figure 3 legend and the paper's vertical datum; do **not** draw a supposedly accurate 1:200 section by guessing how these numbers connect. The study uses a sea-level reference **ZMPS** in its water-level data, which is not interchangeable with a generic building datum.

## Figure-ground data acquisition

For present-day footprints, obtain OSM building polygons through an Overpass export and archive an attributed GeoJSON snapshot with timestamp, query bounds and ODbL notice. OSM is volunteered geographic data, not certified building survey. A public tool describes the buildings export and license: https://www.quickmaptools.com/download-osm ; https://docs.nextgis.com/docs_toolbox/source/osm_download.html

An alternative Venice-specific OSM-derived ArcGIS service exposes a **buildings (7)** layer: https://services6.arcgis.com/wNUCgbZ3TmLukLnT/ArcGIS/rest/services/Venice_OSMdata/FeatureServer . **The layer may be stale**; inspect its metadata before using it as contemporary geometry.

The environment used for this iteration could not resolve the Overpass host, so **no building polygons were downloaded** and no footprint dataset is claimed as delivered.

## Historic scale references

Penn State University Libraries catalogues a **1921** San Marco plan with an explicit measurement scale, public domain, but the online image is only **385×467 px**: https://www.flickr.com/photos/psulibscollections/5835862325 . It is suitable for source comparison, not automatically for 1:1000 output.

INHA AGORHA catalogues **Charles Percier, 1786–1791**, *Plans et vues de la place et de la piazzetta Saint-Marc*, as **dimensioned and annotated drawings** depicting the square before Napoleonic demolition of San Geminiano. Bibliothèque de l'Institut de France, MS 1010 fol 166 num 237: https://agorha.inha.fr/ark:/54721/39019bc9-2f0a-4ad0-9941-09eab8e6b761 . The catalog establishes the presence of dimensions, not their values; obtain a readable scan before transcription.

## Next drawing priorities

1. **Waterfront section:** read Figure 3 and datum notes from the Water paper; then produce a true source-reconstructed section for Type C (steps), labelled as a hydraulic cross-section, **not** an urban architectural section through Piazza.
2. **Historic plan:** obtain Percier's annotated original and verify units; compare with 1921 plan.
3. **Current Figure–Ground:** obtain and archive OSM polygon snapshot; mark accuracy and licensing.
4. **Urban section:** secure measured Procuratie heights and paving datums from architectural drawings; do not fill gaps with conjectural silhouettes.
