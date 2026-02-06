# System Architecture: VertexAntiMoneyLaundering RCE

## High-Level Design
The system follows a **Service-Oriented Architecture (SOA)** with strict separation of concerns between data ingestion, logic processing, and persistence.

### 1. Backend Service (`/backend`)
* **Framework:** FastAPI (Async/Await).
* **Role:** Central orchestrator for all compliance checks.
* **Security:**
    * OAuth2 with Password Flow (JWT).
    * `Slowapi` Rate Limiting (Memory-based).
* **ORM:** SQLAlchemy (Async) for Postgres; Bolt Driver for Neo4j.

### 2. Frontend Service (`/frontend`)
* **Framework:** Streamlit.
* **Role:** Stateless UI for Compliance Officers.
* **Communication:** Consumes Backend REST APIs via `httpx`.

### 3. Data Persistence Layer
* **PostgreSQL (Primary):** Stores structured data (Customers, Transactions, Audit Logs).
* **Neo4j (Graph):** Stores relationship data (Entity --TRANSFERRED--> Entity) for loop detection.

## Critical Data Flows

### A. The "Red Ring" Detection
1.  Transaction POSTed to `/api/v1/transactions`.
2.  Data committed to PostgreSQL (ACID safety).
3.  Async task syncs node/edge to Neo4j.
4.  Graph algorithm scans for `(n)-[*1..5]->(n)` cycles.
5.  If detected -> Flag Transaction -> Alert Compliance Officer.

### B. Immutable Audit Trail
1.  Any state change triggers `AuditService`.
2.  Event data is serialized.
3.  `SHA-256` hash generated of (Previous_Hash + Current_Data).
4.  Log entry written to `audit_logs` table.

## Deployment Strategy
* **Containerization:** Docker multi-stage builds.
* **Orchestration:** Docker Compose network bridge.