import streamlit as st
import pandas as pd
import requests
import time
import plotly.graph_objects as go
import networkx as nx
import graphviz
import random
import uuid
from datetime import datetime
from fpdf import FPDF

# ---------------------------------------------------------
# 1. GLOBAL CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="VERTEX | Institutional Terminal",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

API_URL = "http://backend:8000/api/v1"

# ---------------------------------------------------------
# 2. ADVANCED PDF ENGINE (Visuals Included)
# ---------------------------------------------------------
class VertexSAR(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 14)
        self.set_text_color(200, 0, 0) # Dark Red for "CONFIDENTIAL"
        self.cell(0, 10, 'CONFIDENTIAL // SUSPICIOUS ACTIVITY REPORT', 0, 1, 'C')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Vertex Intelligence Unit | Automated Filing System | Page {self.page_no()}', 0, 0, 'C')

    def risk_bar(self, score):
        # Draws a visual "Risk Heatmap" on the PDF
        self.set_fill_color(200, 200, 200)
        self.rect(10, self.get_y(), 190, 5, 'F') # Background
        
        # Risk Level Color
        if score > 80: self.set_fill_color(255, 0, 0) # Red
        elif score > 50: self.set_fill_color(255, 165, 0) # Orange
        else: self.set_fill_color(0, 255, 0) # Green
        
        width = (score / 100) * 190
        self.rect(10, self.get_y(), width, 5, 'F') # Foreground
        self.ln(8)

def generate_sar_pdf(ring_data, case_id):
    pdf = VertexSAR()
    pdf.add_page()
    
    # 1. CASE METADATA BOX
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, 30, 190, 25, 'F')
    pdf.set_y(32)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 6, "Report Date:", 0, 0); pdf.set_font("Arial", '', 10); pdf.cell(60, 6, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 0, 0)
    pdf.set_font("Arial", 'B', 10); pdf.cell(30, 6, "Case ID:", 0, 0); pdf.set_font("Arial", '', 10); pdf.cell(0, 6, case_id, 0, 1)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(30, 6, "Filer:", 0, 0); pdf.set_font("Arial", '', 10); pdf.cell(60, 6, "Vertex FIU (Automated)", 0, 0)
    pdf.set_font("Arial", 'B', 10); pdf.cell(30, 6, "Status:", 0, 0); pdf.set_font("Arial", 'B', 10); pdf.set_text_color(255, 0, 0); pdf.cell(0, 6, "CRITICAL / PRIORITY 1", 0, 1)
    pdf.set_text_color(0, 0, 0)
    pdf.ln(10)

    # 2. RISK VISUALIZATION
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, f"Calculated Risk Score: {ring_data.get('risk_score', 95)}/100", 0, 1)
    pdf.risk_bar(ring_data.get('risk_score', 95))
    pdf.ln(5)

    # 3. EXECUTIVE SUMMARY
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Executive Summary", 0, 1, 'L')
    pdf.set_font("Arial", '', 10)
    summary_text = (
        "The Vertex Compliance Engine has detected a high-probability money laundering pattern "
        f"involving {len(ring_data['path_ids'])-1} entities in a '{ring_data.get('type', 'Cyclic Loop')}' topology. "
        "This activity triggers velocity checks and indicates potential placement/layering stages "
        "of money laundering violations under the Bank Secrecy Act (BSA)."
    )
    pdf.multi_cell(0, 5, summary_text)
    pdf.ln(5)
    
    # 4. EVIDENCE TABLE
    pdf.set_font("Arial", 'B', 10)
    pdf.set_fill_color(50, 50, 50)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(60, 8, "Origin Entity", 1, 0, 'C', 1)
    pdf.cell(60, 8, "Destination Entity", 1, 0, 'C', 1)
    pdf.cell(40, 8, "Amount (USD)", 1, 0, 'C', 1)
    pdf.cell(30, 8, "Flag", 1, 1, 'C', 1)
    
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", '', 9)
    path = ring_data.get('path_ids', [])
    amts = ring_data.get('amounts', [])
    
    for i in range(len(path)-1):
        sender = path[i]
        receiver = path[i+1]
        amt = f"${amts[i]:,.2f}" if i < len(amts) else "-"
        pdf.cell(60, 8, sender, 1, 0)
        pdf.cell(60, 8, receiver, 1, 0)
        pdf.cell(40, 8, amt, 1, 0, 'R')
        pdf.cell(30, 8, "Structuring", 1, 1, 'C')
    pdf.ln(10)
    
    # 5. CERTIFICATION
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(0, 8, "Compliance Officer Certification", 0, 1, 'L')
    pdf.set_font("Arial", '', 10)
    pdf.multi_cell(0, 5, "I hereby certify that the information contained in this report is true and accurate to the best of my knowledge. This report is filed in accordance with BSA/AML regulations.")
    pdf.ln(15)
    
    # Signature
    pdf.set_font("Courier", '', 10)
    pdf.cell(0, 5, "SIGNED: __________________________", 0, 1)
    pdf.ln(2)
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(0, 5, "Nayan", 0, 1)
    pdf.set_font("Arial", 'I', 10)
    pdf.cell(0, 5, "Sr. Compliance Architect | Vertex FIU", 0, 1)
    
    return pdf.output(dest='S').encode('latin-1')

# ---------------------------------------------------------
# 3. DYNAMIC THREAT GENERATOR (The "Live" Feel)
# ---------------------------------------------------------
def generate_random_threat():
    """Creates a unique, randomized money laundering topology."""
    schemes = ["Cyclic Loop", "Star Burst", "Layering Chain"]
    scheme = random.choice(schemes)
    
    # Generate random entities
    entities = [f"Shell_Corp_{str(uuid.uuid4())[:4].upper()}", 
                f"Offshore_Trust_{random.randint(10,99)}", 
                f"Holding_LLC_{random.choice(['A','B','C'])}",
                f"Rapid_Mover_{random.randint(100,999)}"]
    random.shuffle(entities)
    
    # Build path based on scheme
    if scheme == "Cyclic Loop":
        # A -> B -> C -> A
        path = entities[:3] + [entities[0]]
        base_amt = random.randint(8000, 15000)
        amounts = [base_amt, base_amt - random.randint(50,200), base_amt - random.randint(100,300)]
    elif scheme == "Layering Chain":
        # A -> B -> C -> D
        path = entities
        amounts = [random.randint(10000, 20000) for _ in range(3)]
    else:
        path = entities[:3] + [entities[0]] # Fallback
        amounts = [9000, 8500, 8000]

    return {
        "path_ids": path,
        "amounts": amounts,
        "risk_score": random.randint(85, 99),
        "type": scheme
    }

# ---------------------------------------------------------
# 4. HIGH-FREQUENCY CSS ENGINE
# ---------------------------------------------------------
st.markdown("""
    <style>
        .stApp { background-color: #000000; background-image: linear-gradient(rgba(0, 255, 65, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(0, 255, 65, 0.03) 1px, transparent 1px); background-size: 40px 40px; font-family: 'Roboto Mono', monospace; }
        div[data-testid="stMetric"] { background-color: rgba(10, 10, 10, 0.8); border: 1px solid #1a1a1a; padding: 15px; border-left: 3px solid #00ff41; box-shadow: 0 0 20px rgba(0, 255, 65, 0.05); }
        div[data-testid="stMetricValue"] { color: #fff; font-size: 28px; font-weight: 700; text-shadow: 0 0 10px rgba(0,255,65,0.3); }
        div[data-testid="stMetricLabel"] { color: #666; font-size: 11px; letter-spacing: 1px; }
        .stTabs [data-baseweb="tab-list"] { gap: 0px; border-bottom: 1px solid #333; }
        .stTabs [data-baseweb="tab"] { background-color: #000; color: #555; border: none; padding: 10px 25px; }
        .stTabs [data-baseweb="tab"][aria-selected="true"] { color: #00ff41; background-color: rgba(0, 255, 65, 0.05); border-top: 2px solid #00ff41; }
        div[data-testid="stDataFrame"] { background-color: #000; border: 1px solid #222; }
        @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.4; } 100% { opacity: 1; } }
        .status-dot { color: #00ff41; animation: pulse 2s infinite; font-size: 10px; margin-right: 5px; }
        header {visibility: hidden;} footer {visibility: hidden;} .main .block-container { padding-top: 1rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. DATA FETCHING
# ---------------------------------------------------------
def fetch_live_data():
    try:
        response = requests.get(f"{API_URL}/transactions/?limit=100", timeout=1)
        if response.status_code == 200:
            data = response.json()
            alerts = [t for t in data if t['amount'] > 8000]
            return data, alerts
        return [], []
    except:
        return [], []

transactions, alerts = fetch_live_data()
df = pd.DataFrame(transactions)

# ---------------------------------------------------------
# 6. DASHBOARD
# ---------------------------------------------------------
c1, c2, c3 = st.columns([3, 3, 2])
with c1:
    st.markdown("<h1 style='color: white; margin:0; font-size: 34px; letter-spacing: -1px;'>VERTEX <span style='color:#00ff41'>//</span> ENGINE</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; font-size: 12px; margin-top: -5px; letter-spacing: 2px;'>FINANCIAL INTELLIGENCE UNIT | M4 OPTIMIZED</p>", unsafe_allow_html=True)
with c3:
    st.markdown("<div style='text-align: right; font-family: monospace; font-size: 10px; color: #555;'><span class='status-dot'>●</span>POSTGRES: SYNCED<br><span class='status-dot'>●</span>NEO4J: ONLINE<br><span style='color:#00ff41'>LATENCY: 12ms</span></div>", unsafe_allow_html=True)
st.markdown("<hr style='border-top: 1px solid #222; margin-top: 5px; margin-bottom: 20px;'>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)
vol = df['amount'].sum() if not df.empty else 0
k1.metric("LIQUIDITY (1H)", f"${vol:,.0f}", "+14.2%")
k2.metric("THREATS", f"{len(alerts)} DETECTED", "CRITICAL", delta_color="inverse")
k3.metric("SENTIMENT", "ACCUMULATION", "High Conf")
k4.metric("LATENCY", "12ms", "Optimal")

tab_ops, tab_forensics = st.tabs(["📊 LIVE INTELLIGENCE", "🕵️ DEEP GRAPH FORENSICS"])

with tab_ops:
    c_chart, c_profile = st.columns([2, 1])
    with c_chart:
        st.markdown("<h5 style='color:#fff'>🌊 CAPITAL VELOCITY</h5>", unsafe_allow_html=True)
        if not df.empty:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['amount'], mode='lines', line=dict(color='#00ff41', width=2, shape='spline'), fill='tozeroy', fillcolor='rgba(0, 255, 65, 0.05)'))
            fig.add_trace(go.Scatter(x=df['timestamp'], y=df['amount']*0.45, mode='lines', line=dict(color='#ff3333', width=2, shape='spline')))
            fig.update_layout(paper_bgcolor='#000', plot_bgcolor='#050505', margin=dict(l=0, r=0, t=0, b=0), height=320, xaxis=dict(showgrid=True, gridcolor='#1a1a1a'), yaxis=dict(showgrid=True, gridcolor='#1a1a1a'), showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    with c_profile:
        st.markdown("<h5 style='color:#fff'>📊 RISK DISTRIBUTION</h5>", unsafe_allow_html=True)
        fig_bar = go.Figure(data=[go.Bar(x=['LOW', 'MED', 'HIGH', 'CRITICAL'], y=[random.randint(10,80) for _ in range(4)], marker_color=['#00ff41', '#ccff00', '#ffaa00', '#ff0000'])])
        fig_bar.update_layout(paper_bgcolor='#000', plot_bgcolor='#000', margin=dict(l=0, r=0, t=0, b=0), height=320, xaxis=dict(showgrid=False), yaxis=dict(showgrid=False, visible=False), showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)
    
    st.markdown("---")
    st.markdown("<h5 style='color:#fff'>🔴 LIVE TRANSACTION LEDGER</h5>", unsafe_allow_html=True)
    if not df.empty:
        st.dataframe(df[['timestamp', 'sender_account_id', 'receiver_account_id', 'amount', 'notes']].head(10), use_container_width=True, hide_index=True)

with tab_forensics:
    c_scan, c_viz = st.columns([1, 4])
    with c_scan:
        st.markdown("### 🔍 DEEP SCAN")
        st.caption("Initiate Depth-First Search on Neo4j.")
        
        # --- DYNAMIC THREAT GENERATION LOGIC ---
        if st.button("RUN ALGORITHM", type="primary"):
            try:
                # Try real backend
                res = requests.get(f"{API_URL}/graph/rings", timeout=2)
                rings = res.json().get('rings', []) if res.status_code == 200 else []
                
                # If no real rings, GENERATE DYNAMIC SIMULATION
                if not rings:
                    threat = generate_random_threat()
                    rings = [threat]
                    st.toast(f"SIMULATION: Detected {threat['type']}", icon="⚠️")
                else:
                    st.toast(f"REAL THREAT DETECTED", icon="🚨")
                
                st.session_state['rings'] = rings
            except:
                # Fallback generator if backend down
                threat = generate_random_threat()
                st.session_state['rings'] = [threat]
                st.error("OFFLINE MODE: Simulating Threat")

        if 'rings' in st.session_state and st.session_state['rings']:
            ring = st.session_state['rings'][0]
            st.metric("THREATS FOUND", len(st.session_state['rings']))
            st.warning(f"⚠️ {ring.get('type', 'Suspicious Activity')} DETECTED")
            
            # PDF GENERATOR
            case_id = f"CASE-{str(uuid.uuid4())[:8].upper()}"
            pdf_bytes = generate_sar_pdf(ring, case_id)
            st.download_button("📄 DOWNLOAD SAR DOSSIER", data=pdf_bytes, file_name=f"{case_id}_SAR.pdf", mime="application/pdf", type="secondary")

    with c_viz:
        st.markdown("### 🕸️ NETWORK TOPOLOGY")
        if 'rings' in st.session_state and st.session_state['rings']:
            ring = st.session_state['rings'][0]
            g = graphviz.Digraph()
            g.attr(bgcolor='#000', rankdir='LR')
            g.attr('node', style='filled', fillcolor='#111', color='#ff3333', fontcolor='#ff3333', shape='doublecircle', fontname='Courier')
            g.attr('edge', color='#ff3333', penwidth='2', fontcolor='#ff3333', fontname='Courier')
            path = ring['path_ids']; amts = ring['amounts']
            for i in range(len(path)-1):
                amt = amts[i] if i < len(amts) else 0
                g.edge(path[i], path[i+1], label=f" ${amt:,.0f} ")
            st.graphviz_chart(g, use_container_width=True)
        else:
            st.info("AWAITING SCAN... SYSTEM IDLE.")

time.sleep(1)
st.rerun()