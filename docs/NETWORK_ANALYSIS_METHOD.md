# San Marco pedestrian network: preliminary graph analysis

## Status

This is a **computed exploratory network metric**, not formal Space Syntax axial integration, segment angular choice, or visibility graph analysis (VGA). Do not relabel it as any of those.

## Data

- Source: OpenStreetMap (© OSM contributors, ODbL), queried through Overpass at page load.
- Bounding box: south 45.4325, west 12.3350, north 45.4360, east 12.3420.
- Candidate highways: pedestrian, footway, path, steps, living_street; optional residential and service ways.
- Exclusions: access=private/no, foot=no.
- Mapped pedestrian areas and place=square polygons are displayed and exportable, **but are not connected to the graph**.
- Live data and the graph can change as OSM changes. No frozen snapshot is committed.

## Algorithm (`docs/syntax-graph.js`)

1. Each consecutive pair of OSM way vertices is an undirected edge; identical vertices are matched at 7 decimal places.
2. Weight edges by approximate geodesic length using an equirectangular approximation around the segment latitude.
3. Deduplicate identical undirected vertex-pair edges.
4. Compute connected components using depth-first search.
5. Partition the region into approximately 22m metric grid cells and select the OSM vertex nearest each cell center. Limit to approximately 350 samples by deterministic stride over occupied cells. This reduces bias from uneven OSM vertex density, but does not constitute a full grid-based visibility analysis.
6. For each sampled vertex, run Dijkstra shortest paths limited to the selected 150m, 300m or 500m radius.
7. Sum the portion of each edge within network distance R, counting each edge once. For an edge with endpoint distances dA and dB and length L, included length = min(L, max(0,min(L,R-dA)) + max(0,min(L,R-dB))).
8. Color sample markers by relative min/max within that specific run. These colors are not comparable between runs with different OSM filters.
9. Export sample-point GeoJSON with `network_reach_m`, `degree`, `component`, and radius metadata.

## Important limitations

- Exact shared-vertex topology misses crossing lines without shared OSM vertices, and may misrepresent multi-level connections.
- Streets inside pedestrian plaza polygons are not represented as continuous traversable space; a proper polygon-based visibility model remains pending.
- OSM access tags and physical barriers have not been independently verified.
- Boundary effects depress reach near the bounding-box edges, particularly at the 500m radius. Cross-radius color scales are independently normalized and cannot be compared visually without numerical values.
- Sampling is based on a 22m geographic grid; selection remains sensitive to cell alignment and the available OSM vertices.
- Do not interpret this metric as pedestrian counts, accessibility compliance, pedestrian flow, or safety.
- A genuine VGA requires a surveyed pedestrian boundary and obstruction dataset; a genuine angular segment analysis requires audited topology, turn angles and model calibration.

## Smoke test

The 3-edge T-shaped synthetic graph with four vertices at [0,0], [0.0001,0], [0.0002,0], [0.0001,0.0001] has one connected component, 4 vertices and 3 edges. At 150m, 300m and 500m radii, the test returns 33.36m of reachable network at its sample point. An independent 10m radius test from the first vertex returns exactly 10m of reachable network. These checks were executed against the current module.

## Next technical priorities

1. Audit OSM way topology and plaza entrance points against reliable architectural base plans.
2. Acquire and document actual walkable polygon boundaries, building walls, obstructions, barriers and portico permeability.
3. Generate a validated visibility grid and angular segment graph using a dedicated syntax engine; publish parameters and results separately.

## Plaza-edge geometric QA (added)

Implementation: `docs/syntax-plaza-audit.js`.

- Input: OSM road line endpoints and mapped OSM pedestrian-area / square polygons.
- For each unique road endpoint, check whether it lies inside any polygon (planar ray casting), or within **8m** of a polygon boundary (nearest point on line segment).
- Display blue markers for endpoints inside polygons, orange markers for endpoints near polygon boundaries; export GeoJSON with polygon OSM ID, approximate distance and review-required flag.
- This **does not create graph edges**, infer pedestrian entrances, validate access permissions, or infer visibility.
- Polygons from OSM may be incomplete or inaccurate, may not represent the entire Piazza, and may contain unmodeled obstacles.
- This check is a triage aid for a later manually verified base map, not a replacement for a surveyed pedestrian-space boundary.

### Plaza geometry smoke test

A synthetic square with corners [0,0], [0.0001,0], [0.0001,0.0001], [0,0.0001] and a line with endpoints [0.00005,0.00005] and [0.0002,0.00005] yields: one endpoint inside the polygon; the second approximately 7.81m from its boundary, therefore flagged as a near-boundary candidate at 8m threshold. Both outcomes were checked against the JavaScript module.

### Critical next step

Review the OSM base data against verified building plans and a georeferenced architectural plan, including arcades, entrances, steps, temporary barriers and raised walkways during flooding. Only after validating the pedestrian-space geometry should the project run a formal VGA or angular segment analysis.
