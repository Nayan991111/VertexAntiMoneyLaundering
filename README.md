# VertexAntiMoneyLaundering 🛡️
### High-Frequency Financial Intelligence & Graph-AI Compliance Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Architecture](https://img.shields.io/badge/Arch-Hybrid%20SQL%2FGraph-orange) ![M4 Optimized](https://img.shields.io/badge/Silicon-M4_ARM64-purple) ![License](https://img.shields.io/badge/License-MIT-gray)

**VertexAntiMoneyLaundering** is a production-grade Regulatory Technology (RegTech) platform architected to detect complex financial crime patterns—specifically **Cyclic Money Laundering Loops ("Red Rings")**—in real-time.

Unlike traditional rule-based AML systems, VertexAntiMoneyLaundering utilizes a **Hybrid Database Architecture** (PostgreSQL + Neo4j) to perform deep-link analysis on transaction networks.

---

## 🏗️ System Architecture

The system follows a microservices event-driven pattern optimized for Apple Silicon (ARM64) infrastructure.

```mermaid
graph TD
    A[Client Dashboard\n(Streamlit)] -->|HTTPS/JSON| B[API Gateway\n(FastAPI)]
    B -->|Auth HS256| C{Security Layer}
    C -->|Valid| D[Transaction Service]
    
    subgraph "Hybrid Persistence Layer"
    D -->|ACID Write| E[(PostgreSQL\nTransaction Log)]
    D -->|Async Sync| F[(Neo4j\nGraph Network)]
    end
    
    subgraph "Intelligence Engine"
    F -->|Graph Algo| G[Loop Detection\n(Red Rings)]
    E -->|Rules| H[Velocity Checks]
    end
    
    G -->|Alert| I[Compliance\nAudit Log]
    H -->|Alert| I