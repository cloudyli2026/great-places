/* Preliminary OSM pedestrian network analysis, not an axial/segment/VGA syntax result. */
(function(root){
'use strict';
function distance(a,b){const r=Math.PI/180,dy=(b[1]-a[1])*r,dx=(b[0]-a[0])*r*Math.cos((a[1]+b[1])*.5*r);return 6371000*Math.hypot(dx,dy)}
function graph(features){
 const nodes=[],index=new Map(),edges=[],seen=new Set();
 function node(p){const k=p[0].toFixed(7)+','+p[1].toFixed(7);if(!index.has(k)){index.set(k,nodes.length);nodes.push({point:p,links:[]})}return index.get(k)}
 for(const f of features){if(f.geometry?.type!=='LineString')continue;const c=f.geometry.coordinates;for(let i=1;i<c.length;i++){const a=node(c[i-1]),b=node(c[i]);if(a===b)continue;const k=Math.min(a,b)+'|'+Math.max(a,b);if(seen.has(k))continue;seen.add(k);const length=distance(nodes[a].point,nodes[b].point);if(length<.01)continue;const e=edges.length;edges.push({a,b,length});nodes[a].links.push({to:b,length,edge:e});nodes[b].links.push({to:a,length,edge:e})}}
 const components=new Int32Array(nodes.length).fill(-1),sizes=[];for(let i=0;i<nodes.length;i++){if(components[i]!==-1)continue;const id=sizes.length,stack=[i];components[i]=id;let count=0;while(stack.length){const u=stack.pop();count++;for(const v of nodes[u].links){if(components[v.to]===-1){components[v.to]=id;stack.push(v.to)}}}sizes.push(count)}
 return {nodes,edges,components,sizes}
}
function reach(g,start,radius){
 const n=g.nodes.length,dist=new Float64Array(n).fill(Infinity);dist[start]=0;
 const heap=[];function push(d,u){heap.push([d,u]);let i=heap.length-1;while(i){const p=(i-1)>>1;if(heap[p][0]<=d)break;heap[i]=heap[p];i=p}heap[i]=[d,u]}
 function pop(){const top=heap[0],last=heap.pop();if(heap.length){let i=0;while(true){let l=i*2+1;if(l>=heap.length)break;let r=l+1,c=r<heap.length&&heap[r][0]<heap[l][0]?r:l;if(heap[c][0]>=last[0])break;heap[i]=heap[c];i=c}heap[i]=last}return top}
 push(0,start);while(heap.length){const [d,u]=pop();if(d!==dist[u]||d>radius)continue;for(const e of g.nodes[u].links){const nd=d+e.length;if(nd<dist[e.to]&&nd<=radius){dist[e.to]=nd;push(nd,e.to)}}}
 let meters=0;for(const e of g.edges){const da=dist[e.a],db=dist[e.b];if(da===Infinity&&db===Infinity)continue;const fromA=Math.max(0,Math.min(e.length,radius-da)),fromB=Math.max(0,Math.min(e.length,radius-db));meters+=Math.min(e.length,fromA+fromB)}return meters
}
function analyze(features,radius,maxSamples){
 const g=graph(features),n=g.nodes.length;
 const samples=[],stride=Math.max(1,Math.ceil(n/(maxSamples||350)));
 for(let i=0;i<n;i+=stride){if(g.nodes[i].links.length) samples.push({node:i,point:g.nodes[i].point,reachMeters:reach(g,i,radius||300),degree:g.nodes[i].links.length,component:g.components[i]})}
 const vals=samples.map(x=>x.reachMeters).sort((a,b)=>a-b);
 return {graph:g,samples,radius:radius||300,min:vals[0]||0,max:vals[vals.length-1]||0,median:vals[Math.floor(vals.length/2)]||0,totalLength:g.edges.reduce((sum,e)=>sum+e.length,0)}
}
root.SanMarcoGraph={distance,graph,reach,analyze};
})(typeof window!=='undefined'?window:globalThis);
