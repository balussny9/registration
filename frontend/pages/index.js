import { useState } from 'react';
import { api } from '../lib/api';
import DecisionCard from '../components/DecisionCard';
import RecList from '../components/RecList';
import ChatPanel from '../components/ChatPanel';

export default function Home() {
  const [name,setName]=useState(''); const [email,setEmail]=useState(''); const [phone,setPhone]=useState('');
  const [income,setIncome]=useState(''); const [employment,setEmployment]=useState(''); const [familySize,setFamilySize]=useState('');
  const [wealth,setWealth]=useState(''); const [demographics,setDemographics]=useState('');
  const [files,setFiles]=useState([]); const [appId,setAppId]=useState(null);
  const [decision,setDecision]=useState(null); const [recs,setRecs]=useState(null);
  const [busy,setBusy]=useState(false); const [error,setError]=useState('');

  const submitApplication = async (e) => {
    e.preventDefault(); setError('');
    try {
      const fd = new FormData();
      fd.append('name', name); fd.append('email', email); fd.append('phone', phone);
      fd.append('form_json', JSON.stringify({
        income_level: income, employment_history: employment, family_size: familySize,
        wealth: wealth, demographic_profile: demographics
      }));
      for (const f of files) fd.append('files', f);
      const r = await api.createApplication(fd);
      setAppId(r.application_id);
      setDecision(null); setRecs(null);
      alert(`Application created: ${r.application_id}`);
    } catch (e) { setError(e.message); }
  };

  const runAssessment = async () => {
    if (!appId) return;
    setBusy(true); setError('');
    try { const r = await api.assess(appId); setDecision(r.decision); }
    catch (e) { setError(e.message); }
    finally { setBusy(false); }
  };

  const runRecommendations = async () => {
    if (!appId) return;
    setBusy(true); setError('');
    try { const r = await api.recommend(appId); setRecs(r.recommendations); }
    catch (e) { setError(e.message); }
    finally { setBusy(false); }
  };

  return (
    <div style={{ fontFamily:'system-ui, sans-serif', padding:24, maxWidth:1100, margin:'0 auto' }}>
      <h1>Social Support Platform</h1>

      <form onSubmit={submitApplication} style={{ border:'1px solid #e5e7eb', borderRadius:10, padding:16, marginBottom:24 }}>
        <h2 style={{marginTop:0}}>Ingest Application & Documents</h2>
        <div style={{ display:'grid', gridTemplateColumns:'1fr 1fr', gap:12 }}>
          <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} required />
          <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} required />
          <input placeholder="Phone" value={phone} onChange={e=>setPhone(e.target.value)} />
          <input placeholder="Income Level (low/medium/high)" value={income} onChange={e=>setIncome(e.target.value)} />
          <input placeholder="Employment History (stable/unstable/unknown)" value={employment} onChange={e=>setEmployment(e.target.value)} />
          <input placeholder="Family Size" value={familySize} onChange={e=>setFamilySize(e.target.value)} />
          <input placeholder="Wealth (low/medium/high)" value={wealth} onChange={e=>setWealth(e.target.value)} />
          <input placeholder="Demographic (at_risk/standard)" value={demographics} onChange={e=>setDemographics(e.target.value)} />
        </div>
        <div style={{ marginTop:12 }}>
          <label>Upload PDFs/DOCX/XLSX/Images: </label>
          <input type="file" multiple onChange={e=>setFiles([...e.target.files])}/>
        </div>
        <button type="submit" style={{ marginTop:16 }}>Create Application</button>
        {error && <div style={{ color:'#b91c1c', marginTop:8 }}>{error}</div>}
      </form>

      {appId && (
        <div style={{ display:'grid', gap:16 }}>
          <div style={{ display:'flex', gap:12, alignItems:'center' }}>
            <button onClick={runAssessment} disabled={busy}>Run Eligibility Assessment</button>
            <button onClick={runRecommendations} disabled={busy || !decision}>Get Enablement Recommendations</button>
            <span style={{ color:'#6b7280' }}>Application ID: <strong>{appId}</strong></span>
          </div>

          <DecisionCard decision={decision} />
          <RecList recs={recs} />
          <ChatPanel applicationId={appId} />
        </div>
      )}
    </div>
  );
}
