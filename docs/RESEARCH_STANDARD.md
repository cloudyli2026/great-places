# Research and visual evidence protocol

## Case template
1. Thesis and three keywords
2. City context and maps
3. Figure-ground and spatial morphology
4. Experience route and viewpoint register
5. Sections, elevations and human scale
6. Historical transformation
7. Seven evidence-led dimensions
8. Transferable design principles
9. Sources, limitations and confidence

## Dimensions
Boundary, Richness, Connectivity, Nature, Public Vitality, Cultural Value, Operations. Each 1–5 rating requires cited observations and editorial approval. No aggregate ranking.

## Scale
Urban approximately 1:5000, district 1:1000, sections 1:200, details 1:50, but only if source geometry and display scale permit. A nominal screen scale is not a verified drawing scale.

## Asset requirements
For each drawing/photo record: id, title, author, date, institution, source_url, source_class, rights_status, scope, notes, confidence. For measured values: unit, source, method, uncertainty. Do not reproduce third-party scans without reuse permission.

## Editorial checks
- Separate original historic conditions from present-day survey.
- Label GIS as approximate where relevant.
- Photos must have attributable source and viewpoint when claimed.
- No invented sections, building heights, or AI-generated evidence.
- Unverified claims remain hypotheses, not scored conclusions.

## Published quantitative data policy (all future cases)
- For area, height, length, width, capacity, and other headline figures, use an explicitly published value from an attributable source. Do not derive or estimate a headline value from dimensions, drawings, satellite imagery, or photographs.
- Prefer official authorities, heritage registers, survey documents, building owners/operators, and primary architectural documentation. When these are unavailable, use a clearly attributed reputable secondary source; Wikipedia figures must be labeled as such, not presented as official measurements.
- Record the source URL, publisher, access date, units, measurement boundary, and whether the value is exact or approximate. For public squares, distinguish the main square from adjoining piazzette, streets, and waterfronts.
- If credible sources disagree, present the range or differing figures with their respective scope and provenance; do not average or silently choose one. If no reliable published figure exists, mark 'not confirmed' rather than calculate one.
- Case overview standard fields: Location, Period, Published Area, Primary Uses, Spatial Typology, Defining Character. Apply consistently across all cases.
- Piazza San Marco current editorial value: 12,600 m² for Piazza proper (Italian Wikipedia, https://it.wikipedia.org/wiki/Piazza_San_Marco), excluding Piazzetta. This is an attributed secondary-source value, not an official cadastral survey.


## Publication layout and navigation (2026-11)

The San Marco case is presented as seven independently navigable chapter views in `docs/index.html`, rather than one continuous scroll. Canonical chapter hash routes are `#intro`, `#scale`, `#syntax`, `#boundary`, `#life`, `#climate`, and `#conclusion`. The historical subchapter remains under Overview, figure-ground under Scale, and the source appendix under Evaluation. Each chapter has an editorial masthead and previous/next controls. The original anchor IDs remain for direct links and source references.

Images inside research figures open in a large inspection overlay with captions; their original files are not altered. Verify source provenance, image licensing and actual file availability separately from the viewer. The live OSM map must call Leaflet `invalidateSize` after the Space Syntax chapter becomes visible.

This is client-side chapter pagination, not separate HTML documents. Test hash navigation, bilingual switching, mobile layout, image overlays, keyboard access and Leaflet map rendering in a real browser before treating the site as production-validated.
