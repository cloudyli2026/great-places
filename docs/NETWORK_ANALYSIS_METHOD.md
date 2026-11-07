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
5. Sample at most approximately 350 vertices using a deterministic index stride. This is **not spatially uniform** sampling.
6. For each sampled vertex, run Dijkstra shortest paths limited to 300m.
7. Sum the portion of each edge within network distance 300m, counting each edge once. For an edge with endpoint distances dA and dB and length L, included length = min(L, max(0,min(L,300-dA)) + max(0,min(L,300-dB))).
8. Color sample markers by relative min/max within that specific run. These colors are not comparable between runs with different OSM filters.
9. Export sample-point GeoJSON with `reach_300m_m`, `degree`, `component`.

## Important limitations

- Exact shared-vertex topology misses crossing lines without shared OSM vertices, and may misrepresent multi-level connections.
- Streets inside pedestrian plaza polygons are not represented as continuous traversable space; a proper polygon-based visibility model remains pending.
- OSM access tags and physical barriers have not been independently verified.
- Boundary effects depress reach near the bounding-box edges.
- OSM vertex density affects the **sample locations** (though the reach metric sums physical edge lengths rather than vertex counts).
- Do not interpret this metric as pedestrian counts, accessibility compliance, pedestrian flow, or safety.
- A genuine VGA requires a surveyed pedestrian boundary and obstruction dataset; a genuine angular segment analysis requires audited topology, turn angles and model calibration.

## Smoke test

The 3-edge T-shaped synthetic graph with four vertices at [0,0], [0.0001,0], [0.0002,0], [0.0001,0.0001] has one connected component and, at a 100m radius, all four vertices can reach the full approximately 33m network. This was evaluated against the module.

## Next technical priorities

1. Audit OSM way topology and plaza entrance points against reliable architectural base plans.
2. Acquire and document actual walkable polygon boundaries, building walls, obstructions, barriers and portico permeability.
3. Generate a validated visibility grid and angular segment graph using a dedicated syntax engine; publish parameters and results separately.
