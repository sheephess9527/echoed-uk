// echoed.uk 的 Worker：静态页面交给 ASSETS，只处理 /api/*。
// 订阅邮箱存进 D1（binding: DB），表在首次写入时自动建好。

const SCHEMA = `CREATE TABLE IF NOT EXISTS subscribers (
  email TEXT PRIMARY KEY,
  created_at TEXT NOT NULL,
  source TEXT
)`;
const INSERT = `INSERT INTO subscribers (email, created_at, source) VALUES (?1, ?2, ?3)
  ON CONFLICT(email) DO NOTHING`;
const EMAIL_RE = /^[^@\s]+@[^@\s]+\.[^@\s]+$/;

function json(status, body, headers = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...headers },
  });
}

async function readBody(request) {
  const type = request.headers.get('Content-Type') || '';
  const text = await request.text();
  if (text.length > 2048) return null;
  if (type.includes('application/json')) {
    try { return JSON.parse(text); } catch { return null; }
  }
  return Object.fromEntries(new URLSearchParams(text));
}

async function insert(db, email, source) {
  const stmt = db.prepare(INSERT).bind(email, new Date().toISOString(), source);
  try {
    return await stmt.run();
  } catch (err) {
    if (!/no such table/i.test(String(err && err.message))) throw err;
    await db.prepare(SCHEMA).run();
    return await stmt.run();
  }
}

async function subscribe(request, env, url) {
  if (request.method !== 'POST') return json(405, { ok: false, error: 'method_not_allowed' }, { Allow: 'POST' });

  const origin = request.headers.get('Origin');
  if (origin) {
    try {
      if (new URL(origin).host !== url.host) return json(403, { ok: false, error: 'forbidden' });
    } catch {
      return json(403, { ok: false, error: 'forbidden' });
    }
  }

  const body = await readBody(request);
  if (!body || typeof body !== 'object') return json(400, { ok: false, error: 'bad_request' });

  const email = String(body.email || '').trim().toLowerCase();
  if (email.length > 254 || !EMAIL_RE.test(email)) return json(400, { ok: false, error: 'invalid_email' });
  const source = String(body.source || '').slice(0, 100) || null;

  if (!env.DB) return json(503, { ok: false, error: 'storage_unavailable' });
  try {
    const result = await insert(env.DB, email, source);
    return json(200, { ok: true });
  } catch (err) {
    console.error('subscribe insert failed', err);
    return json(500, { ok: false, error: 'storage_error' });
  }
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname === '/api/subscribe') return subscribe(request, env, url);
    if (url.pathname.startsWith('/api/')) return json(404, { ok: false, error: 'not_found' });
    return env.ASSETS.fetch(request);
  },
};
