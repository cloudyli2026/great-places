/* Geometry-only QA for candidate OSM plaza polygons and street endpoints.
 * Not a pedestrian permeability, visibility or space syntax model. */
(function(root){
'use strict';
const RAD=Math.PI/180,lat0=45.4342*RAD;
function xy(p){return [p[0]*111320*Math.cos(lat0),p[1]*111320]}
function inside(point,ring){let c=false;const p=xy(point);for(let i=0,j=ring.length-1;i<ring.length;j=i++){const a=xy(ring[i]),b=xy(ring[j]);if((a[1]>p[1])!==(b[1]>p[1])&&p[0]<(b[0]-a[0])*(p[1]-a[1])/(b[1]-a[1])+a[0])c=!c}return c}
function segmentDistance(point,a,b){const p=xy(point),u=xy(a),v=xy(b),dx=v[0]-u[0],dy=v[1]-u[1],len=dx*dx+dy*dy;const t=len?Math.max(0,Math.min(1,((p[0]-u[0])*dx+(p[1]-u[1])*dy)/len)):0;return Math.hypot(p[0]-u[0]-t*dx,p[1]-u[1]-t*dy)}
function boundaryDistance(point,ring){let best=Infinity;for(let i=1;i<ring.length;i++)best=Math.min(best,segmentDistance(point,ring[i-1],ring[i]));return best}
function audit(lines,polygons,threshold){
 const t=Number(threshold)||8,entries=[],seen=new Set(),endpointCounts=new Map(),vertexWays=new Map(),valid=polygons.filter(p=>p.geometry?.type==='Polygon'&&p.geometry.coordinates?.[0]?.length>=4);
 for(const f of lines){if(f.geometry?.type!=='LineString')continue;const c=f.geometry.coordinates;if(c.length<2)continue;const unique=new Set(c.map(p=>p[0].toFixed(7)+','+p[1].toFixed(7)));for(const k of unique)vertexWays.set(k,(vertexWays.get(k)||0)+1);for(const p of [c[0],c[c.length-1]]){const k=p[0].toFixed(7)+','+p[1].toFixed(7);endpointCounts.set(k,(endpointCounts.get(k)||0)+1)}}
 for(const f of lines){if(f.geometry?.type!=='LineString')continue;const c=f.geometry.coordinates;if(c.length<2)continue;for(const p of [c[0],c[c.length-1]]){const key=p[0].toFixed(7)+','+p[1].toFixed(7);if(seen.has(key))continue;seen.add(key);let best=null;for(const poly of valid){const ring=poly.geometry.coordinates[0];const inArea=inside(p,ring),dist=boundaryDistance(p,ring);if(inArea||dist<=t){if(!best||dist<best.distanceMeters)best={point:p,polygonId:poly.properties?.osm_id||null,polygonName:poly.properties?.name||null,distanceMeters:dist,inside:inArea}}}if(best){best.sharedWayCount=vertexWays.get(key)||1;best.dangling=(best.sharedWayCount===1);entries.push(best)}}}
 return {entries,polygonCount:valid.length,thresholdMeters:t,endpointCandidates:seen.size,insideCount:entries.filter(e=>e.inside).length,nearCount:entries.filter(e=>!e.inside).length,danglingCount:entries.filter(e=>e.dangling).length,sharedCount:entries.filter(e=>!e.dangling).length}
}
root.SanMarcoPlazaAudit={inside,boundaryDistance,audit};
})(typeof window!=='undefined'?window:globalThis);
