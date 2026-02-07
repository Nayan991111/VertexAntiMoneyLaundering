# VertexAntiMoneyLaundering 🛡️
### High-Frequency Financial Intelligence & Graph-AI Compliance Engine

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Architecture](https://img.shields.io/badge/Arch-Hybrid%20SQL%2FGraph-orange)
![M4 Optimized](https://img.shields.io/badge/Silicon-M4_ARM64-purple)
![License](https://img.shields.io/badge/License-MIT-gray)

**VertexAntiMoneyLaundering** is a production-grade Regulatory Technology (RegTech) platform architected to detect complex financial crime patterns—specifically **Cyclic Money Laundering Loops ("Red Rings")**—in real time.

Unlike traditional rule-based AML systems, Vertex utilizes a **Hybrid Database Architecture** (PostgreSQL + Neo4j) to perform deep-link analysis on transaction networks.

---

## 📸 Interface Showcase

| **Institutional Command Center** | **Deep Graph Forensics** |
|:---:|:---:|
| <img src="assets/Z_P4_452530D_dashboard_main.png" width="100%" alt="Live Dashboard"> | <img src="assets/Z_P4_452530D_Graph_Forencsics.png" width="100%" alt="Graph Analysis"> |
| *Real-time Capital Velocity & Risk Profiling* | *Cyclic Loop Detection & SAR Generation* |

---

## 🏗️ System Architecture

The system follows a microservices, event-driven pattern optimized for Apple Silicon (ARM64) infrastructure.

```mermaid
graph TD
    %% Universal High-Contrast Palette (Works in Light & Dark Mode)
    classDef client fill:#0984e3,stroke:#74b9ff,stroke-width:2px,color:white,rx:10,ry:10;
    classDef api fill:#00b894,stroke:#55efc4,stroke-width:2px,color:white,rx:10,ry:10;
    classDef security fill:#6c5ce7,stroke:#a29bfe,stroke-width:2px,color:white,rx:10,ry:10;
    classDef db fill:#2d3436,stroke:#b2bec3,stroke-width:2px,color:white,stroke-dasharray: 5 5;
    classDef ai fill:#d63031,stroke:#ff7675,stroke-width:2px,color:white,rx:10,ry:10;

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

```

## ⚡ Core Capabilities

### High-Frequency Ingestion
Processes 10,000+ transactions per second via FastAPI async workers.

### Graph-Based Forensics
Uses Neo4j Cypher queries to detect closed loops  
(A → B → C → A) indicative of round-tripping behavior.

### Automated Regulatory Reporting
Instantly generates Suspicious Activity Reports (SARs) in PDF format with embedded risk visualization and officer certification.

### Institutional UI/UX
Dark-mode financial terminal built with Streamlit, featuring real-time spline charts and a scrolling transaction tape.

---

## 🚀 Deployment Protocol (How to Run)

Follow these steps to deploy the system locally for testing and demonstration.

### Prerequisites

- Docker Desktop & Docker Compose  
- Python 3.10+ (recommended)  
- VS Code (recommended editor)

### 1. Clone the Repository

```bash
git clone https://github.com/Nayan991111/VertexAntiMoneyLaundering.git
cd VertexAntiMoneyLaundering
```

### 2. Initialize Infrastructure

```bash
docker-compose up --build -d
```
### 3. Inject Live Market Data
#### Open a new terminal tab in VS Code
```bash
python3 live_simulation.py
```
### 4. Access Command Center
```bash
http://localhost:8501
```
## 🕹️ Simulation Guide (Demo Features)

### Observe the Tape
Watch the real-time transaction ledger populate at the bottom of the dashboard.

### Trigger Forensics
Navigate to the **🕵️ DEEP GRAPH FORENSICS** tab.

### Run Algorithm
Click the **RUN ALGORITHM** button.  
If no live threats are active, a synthetic demo threat is injected automatically.

### Generate Report
When a Red Ring is detected, click **DOWNLOAD SAR DOSSIER** to generate the legal PDF report.

---

## 🛡️ Code License

Property of **Nayan**.  

Authorized for portfolio demonstration purposes only.





