#!/usr/bin/env python3
"""Fetch reproducible, validated and versioned OSM snapshots for the La Rambla case study.
Source: OpenStreetMap contributors (ODbL), API 0.6. No inferred geometry.
"""
import json, pathlib, urllib.request, xml.etree.ElementTree as ET
from datetime import datetime, timezone

BASE = pathlib.Path(__file__).resolve().parents[1] / "docs" / "data"
BASE.mkdir(parents=True, exist_ok=True)
BBOX = "2.1642,41.3755,2.1745,41.3879"
req = urllib.request.Request(
    "https://api.openstreetmap.org/api/0.6/map?bbox=" + BBOX,
    headers={"User-Agent": "GreatPlacesAtlas/1.0 (educational research; GitHub cloudyli2026/great-places)"},
)
with urllib.request.urlopen(req, timeout=55) as response:
    root = ET.fromstring(response.read())
nodes = {n.attrib["id"]: {"lat": float(n.attrib["lat"]), "lon": float(n.attrib["lon"])}
         for n in root.findall("node")}
walk, buildings = [], []
for way in root.findall("way"):
    tags = {t.attrib["k"]: t.attrib["v"] for t in way.findall("tag")}
    highway = tags.get("highway", "")
    permitted = highway in {"pedestrian", "footway", "path", "steps", "living_street", "residential", "service"} and tags.get("access") not in {"private", "no"} and tags.get("foot") != "no"
    plaza = (tags.get("area") == "yes" and highway == "pedestrian") or tags.get("place") == "square"
    building = "building" in tags
    if not (permitted or plaza or building):
        continue
    geometry = [nodes[n.attrib["ref"]] for n in way.findall("nd") if n.attrib["ref"] in nodes]
    if len(geometry) < 2:
        continue
    item = {"type": "way", "id": int(way.attrib["id"]), "tags": tags, "geometry": geometry}
    if permitted or plaza:
        walk.append(item)
    if building:
        buildings.append(item)
if len(walk) < 10 or len(buildings) < 10:
    raise RuntimeError("Insufficient geometry; refusing to replace snapshot")
stamp = datetime.now(timezone.utc).isoformat()
for name, items in (("la-rambla-walkways.json", walk), ("la-rambla-buildings.json", buildings)):
    payload = {"source": "OpenStreetMap contributors / ODbL", "retrieved_at": stamp,
               "bbox": BBOX, "elements": items}
    (BASE / name).write_text(json.dumps(payload, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(name, len(items))
