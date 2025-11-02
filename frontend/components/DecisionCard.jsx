export default function DecisionCard({ decision }) {
  if (!decision) return null;
  const badge = (d) => {
    const m = {
      approve: { bg:'#e6ffed', color:'#05603a' },
      soft_decline:{ bg:'#fff1f2', color:'#b42318' },
      needs_more_info:{ bg:'#fff7e6', color:'#93370d' }
    }[d] || { bg:'#eef2ff', color:'#3730a3' };
    return <span style={{padding:'4px 10px', borderRadius:999, background:m.bg, color:m.color, fontWeight:600, fontSize:14}}>{d}</span>;
  };

  const criteria = decision.criteria || {};
  return (
    <div style={{border:'1px solid #e5e7eb', borderRadius:10, padding:16}}>
      <div style={{display:'flex', alignItems:'center', gap:12}}>
        <h3 style={{margin:0}}>Eligibility Decision</h3>
        {badge(decision.decision)}
        {'confidence' in decision && <span style={{marginLeft:'auto', color:'#6b7280'}}>Confidence: {(decision.confidence*100).toFixed(0)}%</span>}
      </div>

      {decision.reasons?.length > 0 && (
        <>
          <h4 style={{margin:'12px 0 6px'}}>Top reasons</h4>
          <ul>
            {decision.reasons.map((r, idx) => <li key={idx}>{r}</li>)}
          </ul>
        </>
      )}

      <h4 style={{margin:'12px 0 6px'}}>Criteria</h4>
      <table style={{width:'100%', borderCollapse:'collapse'}}>
        <tbody>
          {Object.entries(criteria).map(([k,v]) => (
            <tr key={k}>
              <td style={{borderTop:'1px solid #e5e7eb', padding:'8px 6px', color:'#6b7280', width:240}}>{k.replaceAll('_',' ')}</td>
              <td style={{borderTop:'1px solid #e5e7eb', padding:'8px 6px'}}>{String(v)}</td>
            </tr>
          ))}
        </tbody>
      </table>

      {decision.evidence_citations?.length > 0 && (
        <>
          <h4 style={{margin:'12px 0 6px'}}>Evidence citations</h4>
          <ul>
            {decision.evidence_citations.map((c, i) => <li key={i} style={{color:'#475569'}}>{c}</li>)}
          </ul>
        </>
      )}
    </div>
  );
}
