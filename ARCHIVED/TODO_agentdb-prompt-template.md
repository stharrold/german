# AgentDB Integration Prompt

## Database Configuration
You have access to AgentDB for persistent storage during this session.

**Database ID:** `{session_id}`  
**Lifecycle:** Data persists for session duration, auto-deleted after 24h  
**Engine:** DuckDB (optimized for append-only analytical workloads)

### Workflow Integration
**State conventions:** See `workflow-states.json` for canonical state definitions  
**State format:** `<prefix>_<description>` (e.g., `20_in-progress`, `99_done`, `E01_failed`)  
**Objects:** feature, story, epic, task, spec_md, plan_md, git_branch, pull_request, test_suite  
**Frameworks:** SpecKit (specification-driven), BMAD (agent-based), Unified (combined)

## Unique Identifier Generation

### Session ID (Database Identifier)
If not provided in your prompt, generate on first database access:

**Method 1: Use conversation context (recommended)**
```python
# If available via recent_chats tool
chat_data = recent_chats(n=1, sort_order='desc')
session_id = hash(chat_data.uri)[:16]  # Extract from conversation URI

# Example: "conv_abc123def456" â†’ "a3f9c8d2e1b4f7a2"
```

**Method 2: Timestamp-based (fallback)**
```python
# Use user_time_v0 tool to get current ISO timestamp
current_time = user_time_v0()  # Returns ISO 8601
session_id = hash(current_time + user_context)[:16]

# Example: "2025-10-31T14:30:00Z" â†’ "f8e7d6c5b4a39281"
```

**Method 3: Pure random (stateless)**
```python
# Generate cryptographically random ID
import secrets
session_id = secrets.token_hex(8)  # 16-char hex

# Example: "7f3e9a2c1d5b8e4f"
```

**Choose based on requirements:**
- Reproducible across agent invocations: Method 1 or 2
- Unique per invocation: Method 3

### Record IDs (DuckDB-native)
**UUID (recommended):**
```sql
-- Native UUID generation
INSERT INTO workflow_objects (id, object_type, state, created_at) 
VALUES (uuid(), 'task', '00_pending', current_timestamp);
```

**Timestamp + Random (sortable):**
```sql
INSERT INTO workflow_objects (id, object_type, state) 
VALUES (
    strftime(current_timestamp, '%s') || '-' || md5(random()::VARCHAR)[:8],
    'task', '00_pending'
);
```

## Available Operations

### Initialize Database
```sql
-- Immutable append-only schema
CREATE TABLE IF NOT EXISTS {table_name} (
    record_id UUID PRIMARY KEY DEFAULT uuid(),
    record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
    object_id VARCHAR NOT NULL,
    object_type VARCHAR NOT NULL,
    object_state VARCHAR NOT NULL,
    object_metadata JSON
);

CREATE INDEX IF NOT EXISTS idx_{table_name}_object 
ON {table_name}(object_id, record_datetimestamp DESC);
```

### Standard Queries
Use standard SQL syntax:
- `INSERT`, `UPDATE`, `DELETE`, `SELECT`
- Transactions: `BEGIN; ... COMMIT;`
- JSON operations: `json_extract_string(data, '$.field')` or `data->>'field'`
- Sequences: `CREATE SEQUENCE seq_name;` then `nextval('seq_name')`

## Common Patterns

### Workflow State Tracking
Immutable append-only records from `workflow-states.json`:

```sql
-- All workflow state changes are new records (never UPDATE)
CREATE TABLE IF NOT EXISTS workflow_records (
    record_id UUID PRIMARY KEY DEFAULT uuid(),
    record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
    object_id VARCHAR NOT NULL,     -- Stable ID for the workflow object
    object_type VARCHAR NOT NULL,   -- 'feature', 'story', 'task', 'spec_md', etc.
    object_state VARCHAR NOT NULL,  -- '20_in-progress', '99_done', 'E01_failed'
    object_metadata JSON            -- framework, branch, dependencies, etc.
);

CREATE INDEX idx_records_object ON workflow_records(object_id, record_datetimestamp DESC);
CREATE INDEX idx_records_type_state ON workflow_records(object_type, object_state);

-- Example: Track feature progression (3 state changes = 3 records)
INSERT INTO workflow_records (object_id, object_type, object_state, object_metadata)
VALUES 
    ('feat-001', 'feature', '00_pending', {'framework': 'speckit'}),
    ('feat-001', 'feature', '10_open', {'framework': 'speckit', 'branch': '001-auth'}),
    ('feat-001', 'feature', '20_in-progress', {'framework': 'speckit', 'branch': '001-auth'});

-- Get current state (latest record per object)
SELECT DISTINCT ON (object_id) *
FROM workflow_records
WHERE object_type = 'feature'
ORDER BY object_id, record_datetimestamp DESC;
```

### Atomic Operations (from workflow-states.json)
Append-only pattern - never UPDATE, always INSERT:
```sql
-- Pattern: work → commit → archive → document
BEGIN;
INSERT INTO workflow_records (object_id, object_type, object_state, object_metadata)
VALUES (?, ?, '60_implementing', {'branch': ?, 'commit': ?});
INSERT INTO commits (branch, message, timestamp) VALUES (?, ?, current_timestamp);
INSERT INTO archived_work (id, snapshot, archived_at) VALUES (?, ?, current_timestamp);
COMMIT;
```

### State Validation Queries
```sql
-- Get current state for all objects
WITH current_states AS (
    SELECT DISTINCT ON (object_id) 
        object_id, object_type, object_state, object_metadata
    FROM workflow_records
    ORDER BY object_id, record_datetimestamp DESC
)
-- Check completion requirements (from workflow-states.json)
SELECT cs.object_id, cs.object_state,
       COUNT(CASE WHEN dep.object_state != '99_done' THEN 1 END) as blocking_deps
FROM current_states cs
LEFT JOIN current_states dep ON dep.object_id = ANY(
    SELECT unnest(json_extract_string(cs.object_metadata, '$.depends_on')::VARCHAR[])
)
WHERE cs.object_type = 'feature'
GROUP BY cs.object_id, cs.object_state
HAVING blocking_deps = 0;  -- Ready to close
```

## Best Practices

1. **Append-only (immutable):** NEVER UPDATE or DELETE records - always INSERT new records
2. **Idempotent initialization:** Always use `CREATE TABLE IF NOT EXISTS`
3. **Index strategically:** Index (object_id, record_datetimestamp DESC) for current state queries
4. **Use transactions:** Wrap multi-statement operations in `BEGIN/COMMIT`
5. **Current state pattern:** Use `DISTINCT ON (object_id) ... ORDER BY record_datetimestamp DESC`

## Schema Templates

### Workflow State Store (references workflow-states.json)
```sql
-- Immutable append-only records
CREATE TABLE IF NOT EXISTS workflow_records (
    record_id UUID PRIMARY KEY DEFAULT uuid(),
    record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
    object_id VARCHAR NOT NULL,
    object_type VARCHAR NOT NULL,  -- 'feature', 'story', 'task', 'spec_md', etc.
    object_state VARCHAR NOT NULL, -- '20_in-progress', '99_done', 'E01_failed'
    object_metadata JSON            -- branch, dependencies, risk_score, etc.
);

CREATE INDEX idx_records_object ON workflow_records(object_id, record_datetimestamp DESC);
CREATE INDEX idx_records_type_state ON workflow_records(object_type, object_state);
CREATE INDEX idx_records_timestamp ON workflow_records(record_datetimestamp);

-- State transition analysis
CREATE VIEW state_transitions AS
SELECT 
    record_id,
    object_id,
    object_type,
    LAG(object_state) OVER (PARTITION BY object_id ORDER BY record_datetimestamp) as from_state,
    object_state as to_state,
    record_datetimestamp
FROM workflow_records;
```

### Task Dependencies (BMAD/SpecKit)
```sql
CREATE TABLE IF NOT EXISTS task_dependencies (
    record_id UUID PRIMARY KEY DEFAULT uuid(),
    record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
    object_id VARCHAR NOT NULL,     -- Task ID
    object_type VARCHAR DEFAULT 'task',
    object_state VARCHAR NOT NULL,
    object_metadata JSON            -- depends_on: [task_ids], parallel_ok: bool
);
```

## Error Handling

When database operations fail:
1. Check schema: `SELECT table_name FROM information_schema.tables;`
2. Verify data types match schema
3. Ensure foreign key constraints are satisfied
4. Check JSON structure validity for JSON columns

## Limitations

- Single database per agent session
- DuckDB optimized for OLAP/analytics, not OLTP (append-only workflows ideal)
- No built-in vector search extensions (unlike PostgreSQL pgvector)
- HTTP latency for each query

## Initialization Template

```sql
-- Session metadata
CREATE TABLE IF NOT EXISTS session_metadata (
    key VARCHAR PRIMARY KEY,
    value VARCHAR
);

INSERT INTO session_metadata (key, value) 
VALUES 
    ('session_id', '{session_id}'),
    ('framework', '{speckit|bmad|unified}'),
    ('started_at', current_timestamp)
ON CONFLICT (key) DO UPDATE SET value = EXCLUDED.value;

-- Immutable workflow records (references workflow-states.json)
CREATE TABLE IF NOT EXISTS workflow_records (
    record_id UUID PRIMARY KEY DEFAULT uuid(),
    record_datetimestamp TIMESTAMP DEFAULT current_timestamp,
    object_id VARCHAR NOT NULL,
    object_type VARCHAR NOT NULL,
    object_state VARCHAR NOT NULL,
    object_metadata JSON
);

CREATE INDEX idx_records_object ON workflow_records(object_id, record_datetimestamp DESC);
CREATE INDEX idx_records_type_state ON workflow_records(object_type, object_state);
```

---

**Usage:** Replace `{session_id}`, `{table_name}` placeholders with actual values. Initialize schema on first database interaction. DuckDB syntax with native UUID support, JSON columns, and optimized for append-only workflow operations.
