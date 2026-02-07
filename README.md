# VertexAntiMoneyLaundering 🛡️
### High-Frequency Financial Intelligence & Graph-AI Compliance Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen) ![Python](https://img.shields.io/badge/Python-3.10%2B-blue) ![Architecture](https://img.shields.io/badge/Arch-Hybrid%20SQL%2FGraph-orange) ![M4 Optimized](https://img.shields.io/badge/Silicon-M4_ARM64-purple) ![License](https://img.shields.io/badge/License-MIT-gray)

**VertexAntiMoneyLaundering** is a production-grade Regulatory Technology (RegTech) platform architected to detect complex financial crime patterns—specifically **Cyclic Money Laundering Loops ("Red Rings")**—in real-time.

Unlike traditional rule-based AML systems, VertexUtilizes a **Hybrid Database Architecture** (PostgreSQL + Neo4j) to perform deep-link analysis on transaction networks.

---

## 🏗️ System Architecture

The system follows a microservices event-driven pattern optimized for Apple Silicon (ARM64) infrastructure.

```mermaid
graph TD
    %% Universal High-Contrast Palette (Works in Light & Dark Mode)
    classDef client fill:#0984e3,stroke:#74b9ff,stroke-width:2px,color:white,rx:10,ry:10;
    classDef api fill:#00b894,stroke:#55efc4,stroke-width:2px,color:white,rx:10,ry:10;
    classDef security fill:#6c5ce7,stroke:#a29bfe,stroke-width:2px,color:white,rx:10,ry:10;
    classDef db fill:#2d3436,stroke:#b2bec3,stroke-width:2px,color:white,stroke-dasharray: 5 5;
    classDef ai fill:#d63031,stroke:#ff7675,stroke-width:2px,color:white,rx:10,ry:10;

    %% Nodes
    Client["Client Dashboard<br>(Streamlit)"]:::client -->|HTTPS/JSON| Gateway["API Gateway<br>(FastAPI)"]:::api
    
    subgraph "Core Services Layer"
        Gateway -->|Auth HS256| Auth{"Security<br>Engine"}:::security
        Auth -->|Token Valid| TxService["Transaction<br>Service"]:::api
    end
    
    subgraph "Hybrid Persistence Layer"
        TxService -->|ACID Write| Postgres[("PostgreSQL<br>Transaction Log")]:::db
        TxService -->|Async Sync| Neo4j[("Neo4j<br>Graph Network")]:::db
    end
    
    subgraph "Intelligence Engine"
        Neo4j -->|DFS Algorithm| Loop["Loop Detection<br>(Red Rings)"]:::ai
        Postgres -->|SQL Rules| Velocity["Velocity<br>Checks"]:::ai
    end
    
    Loop -->|High Risk Alert| Audit["Immutable<br>Audit Trail"]:::security
    Velocity -->|Alert| Audit