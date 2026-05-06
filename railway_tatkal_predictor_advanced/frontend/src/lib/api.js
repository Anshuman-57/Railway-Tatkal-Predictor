export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';
export async function postPrediction(payload){
  const res = await fetch(`${API_BASE}/predictions`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
  if(!res.ok) throw new Error('Prediction failed');
  return res.json();
}
export async function getRouteDemand(){ const r=await fetch(`${API_BASE}/analytics/route-demand`); return r.json(); }
export async function getTrainPopularity(){ const r=await fetch(`${API_BASE}/analytics/train-popularity`); return r.json(); }
