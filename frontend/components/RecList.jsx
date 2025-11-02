export default function RecList({ recs }) {
  if (!recs) return null;
  return (
    <div style={{display:'grid', gap:16}}>
      {recs.upskilling && (
        <section style={{border:'1px solid #e5e7eb', borderRadius:10, padding:16}}>
          <h3 style={{marginTop:0}}>Upskilling</h3>
          <ul style={{margin:0}}>
            {recs.upskilling.map((u, i) => (
              <li key={i} style={{marginBottom:6}}>
                <strong>{u.title}</strong> — {u.provider} {u.link && <a href={u.link} target="_blank" rel="noreferrer">[link]</a>}
              </li>
            ))}
          </ul>
        </section>
      )}

      {recs.jobs && (
        <section style={{border:'1px solid #e5e7eb', borderRadius:10, padding:16}}>
          <h3 style={{marginTop:0}}>Job Matches</h3>
          <ul style={{margin:0}}>
            {recs.jobs.map((j, i) => (
              <li key={i} style={{marginBottom:6}}>
                <strong>{j.title}</strong> — {j.industry} <em style={{color:'#6b7280'}}>({j.why_match})</em>
              </li>
            ))}
          </ul>
        </section>
      )}

      {recs.counseling && (
        <section style={{border:'1px solid #e5e7eb', borderRadius:10, padding:16}}>
          <h3 style={{marginTop:0}}>Counseling</h3>
          <ul style={{margin:0}}>
            {recs.counseling.map((c, i) => (
              <li key={i} style={{marginBottom:6}}>
                <strong>{c.type}</strong> — {c.note}
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
