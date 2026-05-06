
import React, {useEffect, useState} from 'react';
import { createRoot } from 'react-dom/client';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { Train, ShieldAlert, TrendingUp, Brain, Route } from 'lucide-react';
import { postPrediction, getRouteDemand, getTrainPopularity } from './lib/api';
import './style.css';

function StatCard({icon:Icon,title,value,sub}){return <div className="card stat"><Icon/><div><p>{title}</p><h2>{value}</h2><span>{sub}</span></div></div>}

function App(){
 const [form,setForm]=useState({train_no:'19483',source:'ADI',destination:'MFP',travel_class:'3A',quota:'GN',waitlist_type:'PQWL',waitlist_position:18,days_before_journey:8,distance_km:1167,journey_month:5,day_of_week:5,is_festival_season:false});
 const [result,setResult]=useState(null); const [demand,setDemand]=useState([]); const [pop,setPop]=useState([]); const [loading,setLoading]=useState(false);
 useEffect(()=>{getRouteDemand().then(setDemand); getTrainPopularity().then(setPop)},[])
 async function submit(e){e.preventDefault(); setLoading(true); try{setResult(await postPrediction({...form, waitlist_position:+form.waitlist_position, days_before_journey:+form.days_before_journey, distance_km:+form.distance_km, journey_month:+form.journey_month, day_of_week:+form.day_of_week}));} finally{setLoading(false)}}
 const probData = result ? [{name:'Confirmed',value:result.probabilities.confirmed},{name:'RAC',value:result.probabilities.rac},{name:'Waiting',value:result.probabilities.waiting}] : [];
 return <div className="app"><header><div><h1>Railway Tatkal Intelligence Platform</h1><p>Advanced WL/RAC/Confirmed probability prediction, route demand analytics and decision support.</p></div><Train size={54}/></header>
 <section className="grid stats"><StatCard icon={Brain} title="Prediction Engine" value="ML + Rules" sub="Random forest-ready pipeline"/><StatCard icon={Route} title="Route Analytics" value="Demand Score" sub="Route-wise risk patterns"/><StatCard icon={TrendingUp} title="Movement" value="WL Forecast" sub="Expected waitlist movement"/><StatCard icon={ShieldAlert} title="Risk" value={result?.risk_level||'--'} sub="Low / Medium / High"/></section>
 <main className="layout"><form className="card form" onSubmit={submit}><h2>Predict Ticket Status</h2>{Object.entries(form).map(([k,v])=> k==='is_festival_season'? <label key={k} className="check"><input type="checkbox" checked={v} onChange={e=>setForm({...form,[k]:e.target.checked})}/> Festival season</label> : <label key={k}>{k.replaceAll('_',' ')}<input value={v} onChange={e=>setForm({...form,[k]:e.target.value})}/></label>)}<button>{loading?'Predicting...':'Predict Status'}</button></form>
 <section className="card result"><h2>Prediction Result</h2>{!result && <p className="muted">Submit details to see probability, explanation and recommendations.</p>}{result && <><div className="prob"><div><h3>{result.probabilities.confirmed}%</h3><p>Confirmed</p></div><div><h3>{result.probabilities.rac}%</h3><p>RAC</p></div><div><h3>{result.probabilities.waiting}%</h3><p>Waiting</p></div></div><p><b>Confidence:</b> {result.confidence_score}% | <b>Popularity:</b> {result.popularity_score}/100 | <b>Expected movement:</b> {result.expected_movement}</p><ResponsiveContainer width="100%" height={230}><PieChart><Pie data={probData} dataKey="value" nameKey="name" outerRadius={80} label /></PieChart></ResponsiveContainer><h3>Explanation</h3><ul>{result.explanation.map((x,i)=><li key={i}>{x}</li>)}</ul><h3>Recommendations</h3>{result.recommendations.map((r,i)=><div className="rec" key={i}><b>{r.title}</b><p>{r.reason}</p><small>{r.action}</small></div>)}</>}</section></main>
 <section className="grid"><div className="card"><h2>Route Demand Analytics</h2><ResponsiveContainer width="100%" height={280}><BarChart data={demand}><XAxis dataKey="route"/><YAxis/><Tooltip/><Bar dataKey="demand"/></BarChart></ResponsiveContainer></div><div className="card"><h2>Train Popularity</h2>{pop.map(t=><div className="row" key={t.train_no}><span>{t.train_no} - {t.name}</span><b>{t.score}</b></div>)}</div></section>
 </div>
}
createRoot(document.getElementById('root')).render(<App/>);
