-- Public pages (migration 0002). A pro's profile at scoo.app/p/<slug> and an exchange's page at
-- scoo.app/x/<slug> are public, and indexed, only once `published_at` is set. For a pro that needs
-- their opt-in (`profile_ok`, ticked on the sign-up form) and a check by Scoo, so nobody can put an
-- unverified business on Google through the form. Track-record numbers are not columns: they will
-- be counted from real calls, never typed in.
ALTER TABLE pros ADD COLUMN profile_ok INTEGER NOT NULL DEFAULT 0;
ALTER TABLE pros ADD COLUMN slug TEXT;
ALTER TABLE pros ADD COLUMN about TEXT;
ALTER TABLE pros ADD COLUMN premium INTEGER NOT NULL DEFAULT 0;
ALTER TABLE pros ADD COLUMN published_at TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS pros_slug ON pros (slug) WHERE slug IS NOT NULL;

ALTER TABLE operators ADD COLUMN tagline TEXT;
ALTER TABLE operators ADD COLUMN about TEXT;
ALTER TABLE operators ADD COLUMN rules TEXT;              -- one house rule per line
ALTER TABLE operators ADD COLUMN published_at TEXT;

-- Which pros belong to which exchange. A pro can be in several.
CREATE TABLE IF NOT EXISTS exchange_members (
  operator_id   INTEGER NOT NULL REFERENCES operators (id),
  pro_id        INTEGER NOT NULL REFERENCES pros (id),
  joined_at     TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  PRIMARY KEY (operator_id, pro_id)
);
CREATE INDEX IF NOT EXISTS exchange_members_pro ON exchange_members (pro_id);
