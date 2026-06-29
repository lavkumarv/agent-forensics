-- Append-only ledger schema.
--
-- Append-only is enforced both at the application layer (LedgerStore exposes no
-- update/delete code path) and here with BEFORE UPDATE/DELETE triggers as a
-- defense-in-depth backstop. An attacker with raw file access can still drop the
-- triggers and mutate rows -- that is exactly the tampering verify() detects via
-- the hash chain and Merkle root.

CREATE TABLE IF NOT EXISTS ledger (
  seq           INTEGER PRIMARY KEY AUTOINCREMENT,  -- monotonic ordering
  record_id     TEXT NOT NULL UNIQUE,
  kind          TEXT NOT NULL,        -- 'write' | 'retrieval' | 'action' | 'rollback'
  namespace     TEXT NOT NULL,
  payload_json  TEXT NOT NULL,        -- canonical record JSON (signable fields only)
  entry_hash    TEXT NOT NULL,        -- blake3 of (payload || prev_hash)
  prev_hash     TEXT,                 -- prior row's entry_hash; NULL for genesis
  signature     TEXT NOT NULL,        -- ed25519 over blake3_raw(payload || prev_hash)
  signer_kid    TEXT NOT NULL,
  created_at    TEXT NOT NULL         -- RFC-3339 UTC append time
);

CREATE INDEX IF NOT EXISTS idx_ledger_ns ON ledger(namespace);
CREATE INDEX IF NOT EXISTS idx_ledger_kind ON ledger(kind);

CREATE TRIGGER IF NOT EXISTS ledger_no_update
BEFORE UPDATE ON ledger
BEGIN
  SELECT RAISE(ABORT, 'ledger is append-only: UPDATE is forbidden');
END;

CREATE TRIGGER IF NOT EXISTS ledger_no_delete
BEFORE DELETE ON ledger
BEGIN
  SELECT RAISE(ABORT, 'ledger is append-only: DELETE is forbidden');
END;
