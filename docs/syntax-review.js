/* Local-only review decisions for geometric plaza endpoint candidates.
 * Decisions are annotations, not surveyed or validated entrances. */
(function(root){
'use strict';
const choices=['unreviewed','inspect','likely-open','blocked','not-entrance'];
function key(e){return e.point.map(x=>Number(x).toFixed(7)).join(',')+'|'+String(e.polygonId??'')}
function load(storageKey){try{const value=JSON.parse(root.localStorage.getItem(storageKey)||'{}');return value&&typeof value==='object'&&!Array.isArray(value)?value:{}}catch(e){return {}}}
function save(storageKey,decisions){try{root.localStorage.setItem(storageKey,JSON.stringify(decisions));return true}catch(e){return false}}
function annotate(entries,decisions){return entries.map(e=>({...e,reviewStatus:choices.includes(decisions[key(e)]?.status)?decisions[key(e)].status:'unreviewed',reviewNote:String(decisions[key(e)]?.note||'').slice(0,400)}))}
function summary(entries,decisions){const totals=Object.fromEntries(choices.map(x=>[x,0]));for(const e of annotate(entries,decisions))totals[e.reviewStatus]++;return totals}
function importGeoJSON(data,entries){
 if(!data||data.type!=='FeatureCollection'||!Array.isArray(data.features))throw Error('Expected a GeoJSON FeatureCollection');
 if(data.features.length>2000)throw Error('Too many features');
 const valid=new Set(entries.map(key)),result={};let accepted=0,ignored=0;
 for(const f of data.features){
  if(f?.geometry?.type!=='Point'||!Array.isArray(f.geometry.coordinates)||f.geometry.coordinates.length<2){ignored++;continue}
  const p=f.geometry.coordinates,props=f.properties||{};
  if(!Number.isFinite(p[0])||!Number.isFinite(p[1])){ignored++;continue}
  const k=key({point:p,polygonId:props.osm_polygon_id??props.polygon_osm_id??null});
  if(!valid.has(k)||!choices.includes(props.review_status)){ignored++;continue}
  result[k]={status:props.review_status,note:String(props.review_note||'').slice(0,400)};accepted++;
 }
 return {decisions:result,accepted,ignored};
}
root.SanMarcoReview={choices,key,load,save,annotate,summary,importGeoJSON};
})(typeof window!=='undefined'?window:globalThis);
