-- The pre-launch waitlist: people asking to be notified when Scoo opens in their area. One row per
-- saved request; a person who signs up again for the same area keeps their original place.
CREATE TABLE IF NOT EXISTS requests (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  need          TEXT    NOT NULL,
  category      TEXT    NOT NULL,
  answer        TEXT,
  zip           TEXT    NOT NULL,
  city_key      TEXT    NOT NULL,          -- what the launch threshold counts against
  city_name     TEXT    NOT NULL,
  -- how to notify them at launch: a mobile number (digits, 1 + 10) or an email, at least one
  phone         TEXT,
  email         TEXT,
  -- consent is evidence: the exact wording shown, and when it was given
  consent_text  TEXT    NOT NULL,
  consent_at    TEXT    NOT NULL,
  code          TEXT    NOT NULL UNIQUE,   -- this person's invite code (/r/CODE, /pro/CODE)
  referred_by   TEXT,                      -- the code they arrived with, if any
  user_agent    TEXT,
  token         TEXT,                      -- private session token (cookie), never shown or shared
  CHECK (phone IS NOT NULL OR email IS NOT NULL)
);
CREATE INDEX IF NOT EXISTS requests_city ON requests (city_key);
CREATE UNIQUE INDEX IF NOT EXISTS requests_phone_city ON requests (phone, city_key) WHERE phone IS NOT NULL;
CREATE UNIQUE INDEX IF NOT EXISTS requests_email_city ON requests (email, city_key) WHERE email IS NOT NULL;
CREATE INDEX IF NOT EXISTS requests_referred_by ON requests (referred_by);
CREATE UNIQUE INDEX IF NOT EXISTS requests_token ON requests (token) WHERE token IS NOT NULL;

-- Pros who have signed up for their area. One row per phone, trade and area: a plumber who is also
-- an electrician joins twice, once per trade.
CREATE TABLE IF NOT EXISTS pros (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  business      TEXT    NOT NULL,
  trade         TEXT    NOT NULL,
  zip           TEXT    NOT NULL,
  city_key      TEXT    NOT NULL,
  city_name     TEXT    NOT NULL,
  phone         TEXT    NOT NULL,
  email         TEXT,
  consent_text  TEXT    NOT NULL,
  consent_at    TEXT    NOT NULL,
  code          TEXT    NOT NULL UNIQUE,   -- this pro's own invite code (/pro/CODE)
  referred_by   TEXT,                      -- a customer's or another pro's code
  user_agent    TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS pros_phone_trade_city ON pros (phone, trade, city_key);
CREATE INDEX IF NOT EXISTS pros_city_trade ON pros (city_key, trade);

-- Founding exchange operators: networks, brokers, trade groups. An application reserves the
-- exchange name (scoo.app/x/<slug>); `status` moves on as they are onboarded.
CREATE TABLE IF NOT EXISTS operators (
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  created_at    TEXT    NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now')),
  slug          TEXT    NOT NULL UNIQUE,
  name          TEXT    NOT NULL,
  org           TEXT    NOT NULL,
  trades        TEXT,                      -- comma-separated
  zip           TEXT    NOT NULL,
  city_key      TEXT    NOT NULL,
  city_name     TEXT    NOT NULL,
  size          TEXT,
  volume        TEXT,
  phone         TEXT,
  email         TEXT,
  consent_text  TEXT    NOT NULL,
  consent_at    TEXT    NOT NULL,
  referred_by   TEXT,
  user_agent    TEXT,
  status        TEXT    NOT NULL DEFAULT 'applied',
  CHECK (phone IS NOT NULL OR email IS NOT NULL)
);
