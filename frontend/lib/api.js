const BASE = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://127.0.0.1:8000';

async function jfetch(path, opts = {}) {
  const res = await fetch(`${BASE}${path}`, opts);
  const ct = res.headers.get('content-type') || '';
  const body = ct.includes('application/json') ? await res.json() : await res.text();
  if (!res.ok) {
    const msg = typeof body === 'string' ? body : JSON.stringify(body);
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return body;
}

export const api = {
  createApplication(formData) {
    return fetch(`${BASE}/api/applications/create`, { method: 'POST', body: formData })
      .then(async r => (r.ok ? r.json() : Promise.reject(await r.text())));
  },
  assess(application_id) {
    return jfetch(`/api/assess`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ application_id })
    });
  },
  recommend(application_id) {
    return jfetch(`/api/recommend`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ application_id })
    });
  },
  chat(application_id, message) {
    return jfetch(`/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ application_id, message })
    });
  }
};
