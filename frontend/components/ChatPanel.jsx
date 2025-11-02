import { useState } from 'react';
import { api } from '../lib/api';

export default function ChatPanel({ applicationId }) {
  const [messages, setMessages] = useState([]);
  const [text, setText] = useState('');
  const [loading, setLoading] = useState(false);

  const send = async () => {
    if (!text.trim()) return;
    const userMsg = { role:'user', content:text };
    setMessages(m => [...m, userMsg]);
    setLoading(true);
    try {
      const res = await api.chat(applicationId, text);
      const botMsg = { role:'assistant', content: res.reply };
      setMessages(m => [...m, botMsg]);
    } catch (e) {
      setMessages(m => [...m, { role:'assistant', content:`(error) ${e.message}` }]);
    } finally {
      setLoading(false);
      setText('');
    }
  };

  return (
    <div style={{border:'1px solid #e5e7eb', borderRadius:10, padding:16}}>
      <h3 style={{marginTop:0}}>Chatbot</h3>
      <div style={{maxHeight:260, overflowY:'auto', padding:8, background:'#f9fafb', border:'1px solid #eef2f7', borderRadius:8}}>
        {messages.length === 0 && <div style={{color:'#6b7280'}}>Ask about your application status, documents, or next steps.</div>}
        {messages.map((m, idx) => (
          <div key={idx} style={{marginBottom:10}}>
            <strong>{m.role === 'user' ? 'You' : 'Assistant'}: </strong>{m.content}
          </div>
        ))}
        {loading && <div style={{color:'#6b7280'}}>Assistant is typing…</div>}
      </div>
      <div style={{display:'flex', gap:8, marginTop:12}}>
        <input style={{flex:1}} placeholder="Type a question…" value={text} onChange={e=>setText(e.target.value)} />
        <button onClick={send} disabled={loading}>Send</button>
      </div>
    </div>
  );
}
