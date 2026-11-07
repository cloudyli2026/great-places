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
root.SanMarcoReview={choices,key,load,save,annotate,summary};
})(typeof window!=='undefined'?window:globalThis);
