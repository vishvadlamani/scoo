// The waitlist's storage, behind two calls so the database can change without touching the API:
//
//   first(sql, params) -> the first row as a plain object, or null
//   all(sql, params)    -> every row, as plain objects
//   run(sql, params)    -> { lastRowId, changes }
//
// Production is Turso. It is used whenever TURSO_URL is set (with TURSO_AUTH_TOKEN as a secret);
// otherwise the D1 binding `DB` is used, which is what the pre-launch site runs on today. Both are
// SQLite, so `schema.sql` and every query here run unchanged on either.

export function openStore(env) {
  if (env.TURSO_URL) return tursoStore(env.TURSO_URL, env.TURSO_AUTH_TOKEN);
  if (env.DB) return d1Store(env.DB);
  throw new Error('No database configured: set TURSO_URL or bind DB');
}

function d1Store(db) {
  return {
    kind: 'd1',
    async first(sql, params = []) {
      return (await db.prepare(sql).bind(...params).first()) ?? null;
    },
    async all(sql, params = []) {
      return (await db.prepare(sql).bind(...params).all()).results;
    },
    async run(sql, params = []) {
      const r = await db.prepare(sql).bind(...params).run();
      return { lastRowId: r.meta.last_row_id, changes: r.meta.changes };
    },
  };
}

// Turso over its HTTP API (the Hrana "pipeline" endpoint), with plain fetch: no client library, so
// nothing to bundle and nothing that assumes Node. One statement per request, closed immediately;
// the waitlist never needs an interactive transaction.
function tursoStore(url, token) {
  const endpoint = url.replace(/^libsql:\/\//, 'https://').replace(/\/+$/, '') + '/v2/pipeline';

  const arg = v => {
    if (v === null || v === undefined) return { type: 'null' };
    if (typeof v === 'number') return Number.isInteger(v) ? { type: 'integer', value: String(v) } : { type: 'float', value: v };
    if (typeof v === 'bigint') return { type: 'integer', value: v.toString() };
    return { type: 'text', value: String(v) };
  };
  const value = c => {
    switch (c.type) {
      case 'null': return null;
      // Counts and ids here are far below 2^53, so a Number is exact.
      case 'integer': return Number(c.value);
      case 'float': return c.value;
      case 'blob': return c.base64;
      default: return c.value;
    }
  };

  async function execute(sql, params) {
    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
      body: JSON.stringify({ requests: [{ type: 'execute', stmt: { sql, args: params.map(arg) } }, { type: 'close' }] }),
    });
    if (!res.ok) throw new Error(`Turso HTTP ${res.status}: ${(await res.text()).slice(0, 200)}`);
    const out = (await res.json()).results[0];
    // Errors carry SQLite's message (e.g. "UNIQUE constraint failed: ..."), which callers match on.
    if (out.type === 'error') throw new Error(out.error.message);
    return out.response.result;
  }

  return {
    kind: 'turso',
    async first(sql, params = []) {
      const r = await execute(sql, params);
      if (!r.rows.length) return null;
      return Object.fromEntries(r.cols.map((c, i) => [c.name, value(r.rows[0][i])]));
    },
    async all(sql, params = []) {
      const r = await execute(sql, params);
      return r.rows.map(row => Object.fromEntries(r.cols.map((c, i) => [c.name, value(row[i])])));
    },
    async run(sql, params = []) {
      const r = await execute(sql, params);
      return { lastRowId: r.last_insert_rowid == null ? null : Number(r.last_insert_rowid), changes: r.affected_row_count };
    },
  };
}
