// The waitlist's storage, behind three calls so the database can change without touching the API.
//
// Production will be Turso: it is used whenever TURSO_URL is set (with TURSO_AUTH_TOKEN as a
// secret). Otherwise the D1 binding `DB` is used, which is what the pre-launch site runs on today.
// Both are SQLite, so schema.sql and every query run unchanged on either.

export type Value = string | number | null;
export type Row = Record<string, Value>;

export interface Store {
	kind: 'd1' | 'turso';
	/** The first row, or null. */
	first<T = Row>(sql: string, params?: Value[]): Promise<T | null>;
	/** Every row. */
	all<T = Row>(sql: string, params?: Value[]): Promise<T[]>;
	run(sql: string, params?: Value[]): Promise<{ lastRowId: number | null; changes: number }>;
}

export function openStore(env: Env): Store {
	if (env.TURSO_URL) return tursoStore(env.TURSO_URL, env.TURSO_AUTH_TOKEN);
	if (env.DB) return d1Store(env.DB);
	throw new Error('No database configured: set TURSO_URL or bind DB');
}

function d1Store(db: D1Database): Store {
	return {
		kind: 'd1',
		async first<T>(sql: string, params: Value[] = []) {
			return (await db.prepare(sql).bind(...params).first<T>()) ?? null;
		},
		async all<T>(sql: string, params: Value[] = []) {
			return (await db.prepare(sql).bind(...params).all<T>()).results;
		},
		async run(sql: string, params: Value[] = []) {
			const r = await db.prepare(sql).bind(...params).run();
			return { lastRowId: r.meta.last_row_id, changes: r.meta.changes };
		}
	};
}

type HranaValue =
	| { type: 'null' }
	| { type: 'integer'; value: string }
	| { type: 'float'; value: number }
	| { type: 'text'; value: string }
	| { type: 'blob'; base64: string };
type HranaResult = {
	cols: { name: string }[];
	rows: HranaValue[][];
	affected_row_count: number;
	last_insert_rowid: string | null;
};

// Turso over its HTTP API (the Hrana "pipeline" endpoint) with plain fetch: no client library, so
// nothing that assumes Node. One statement per request, closed at once; the waitlist never needs
// an interactive transaction.
function tursoStore(url: string, token: string | undefined): Store {
	const endpoint = url.replace(/^libsql:\/\//, 'https://').replace(/\/+$/, '') + '/v2/pipeline';

	const arg = (v: Value): HranaValue => {
		if (v === null) return { type: 'null' };
		if (typeof v === 'number') return Number.isInteger(v) ? { type: 'integer', value: String(v) } : { type: 'float', value: v };
		return { type: 'text', value: v };
	};
	const value = (c: HranaValue): Value => {
		switch (c.type) {
			case 'null':
				return null;
			// Counts and ids here are far below 2^53, so a Number is exact.
			case 'integer':
				return Number(c.value);
			case 'float':
				return c.value;
			case 'blob':
				return c.base64;
			default:
				return c.value;
		}
	};
	const toRow = (r: HranaResult, row: HranaValue[]) => Object.fromEntries(r.cols.map((c, i) => [c.name, value(row[i])]));

	async function execute(sql: string, params: Value[]): Promise<HranaResult> {
		const res = await fetch(endpoint, {
			method: 'POST',
			headers: { 'content-type': 'application/json', ...(token ? { authorization: `Bearer ${token}` } : {}) },
			body: JSON.stringify({ requests: [{ type: 'execute', stmt: { sql, args: params.map(arg) } }, { type: 'close' }] })
		});
		if (!res.ok) throw new Error(`Turso HTTP ${res.status}: ${(await res.text()).slice(0, 200)}`);
		const out = ((await res.json()) as { results: { type: string; error?: { message: string }; response?: { result: HranaResult } }[] }).results[0];
		// Errors carry SQLite's message (e.g. "UNIQUE constraint failed: ..."), which callers match on.
		if (out.type === 'error') throw new Error(out.error!.message);
		return out.response!.result;
	}

	return {
		kind: 'turso',
		async first<T>(sql: string, params: Value[] = []) {
			const r = await execute(sql, params);
			return r.rows.length ? (toRow(r, r.rows[0]) as T) : null;
		},
		async all<T>(sql: string, params: Value[] = []) {
			const r = await execute(sql, params);
			return r.rows.map((row) => toRow(r, row) as T);
		},
		async run(sql: string, params: Value[] = []) {
			const r = await execute(sql, params);
			return { lastRowId: r.last_insert_rowid == null ? null : Number(r.last_insert_rowid), changes: r.affected_row_count };
		}
	};
}
