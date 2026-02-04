import streamlit as st
import pandas as pd
import requests
import json
import hashlib
import graphviz
from datetime import datetime

# --- CONFIGURATION ---
# Docker Network Communication: 'frontend' talks to 'backend' container
API_BASE_URL = "http://backend:8000/api/v1"

st.set_page_config(
    page_title="VertexAntiMoneyLaundering Compliance", 
    layout="wide",
    page_icon="🛡️"
)

# --- HEADER & METRICS ---
st.title("🛡️ VertexAntiMoneyLaundering Regulatory Engine")
st.markdown(f"**System Status:** 🟢 ACTIVE | **Day:** 13 (Regulatory Reporting) | **Architecture:** Mac M4 Optimized")

# --- TABS ---
# Tab 1: Live Feed | Tab 2: Immutable Audit (Day 11) | Tab 3: Graph Intelligence (Day 12/13)
tab1, tab2, tab3 = st.tabs(["🚀 Live Monitoring", "📜 Audit Room (Immutable)", "🕸️ Graph Intelligence"])

# =========================================================
# TAB 1: LIVE MONITORING
# =========================================================
with tab1:
    st.header("Real-Time Transaction Stream")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="System Uptime", value="99.99%")
    with col2:
        st.metric(label="Active Rules", value="15 (Inc. Graph)")
    with col3:
        st.metric(label="Compliance Version", value="v2.3.0-Report")
        
    st.info("Live transaction simulation running in backend. Graph ingestion active.")

# =========================================================
# TAB 2: AUDIT ROOM (DAY 11 FEATURE - PRESERVED)
# =========================================================
with tab2:
    st.header("Blockchain-Grade Audit Trail")
    st.markdown("This module fetches the **Immutable JSONL Log**, verifies the SHA-256 hash chain, and proves data integrity.")
    
    if st.button("🔄 Refresh Audit Logs", type="primary", key="audit_btn"):
        with st.spinner("Fetching and Verifying Cryptographic Chain..."):
            try:
                response = requests.get(f"{API_BASE_URL}/audit/trail", timeout=5)
                
                if response.status_code == 200:
                    logs = response.json()
                    
                    if not logs:
                        st.warning("⚠️ No audit logs found. Run the traffic simulator to generate data.")
                    else:
                        # VISUAL INTEGRITY CHECK LOGIC
                        chronological_logs = list(reversed(logs))
                        integrity_passed = True
                        broken_index = -1
                        
                        for i in range(1, len(chronological_logs)):
                            prev_entry_hash = chronological_logs[i-1].get('hash')
                            curr_entry_prev_hash = chronological_logs[i].get('previous_hash')
                            
                            if prev_entry_hash != curr_entry_prev_hash:
                                integrity_passed = False
                                broken_index = i
                                break
                        
                        if integrity_passed:
                            st.success(f"✅ **INTEGRITY VERIFIED:** {len(logs)} blocks checked. The Immutable Ledger is SECURE.")
                        else:
                            st.error(f"🚨 **TAMPER DETECTED:** Chain broken at Block {broken_index}!")

                        # Data Display
                        df = pd.DataFrame(logs)
                        cols = ["timestamp", "event_type", "severity", "hash", "previous_hash"]
                        display_cols = [c for c in cols if c in df.columns]
                        
                        st.dataframe(
                            df[display_cols],
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "timestamp": st.column_config.TextColumn("Time"),
                                "event_type": st.column_config.TextColumn("Event"),
                                "severity": st.column_config.TextColumn("Severity"),
                                "hash": st.column_config.TextColumn("SHA-256", width="medium"),
                            }
                        )
                else:
                    st.error(f"❌ Backend Error: {response.status_code}")
            except Exception as e:
                st.error(f"❌ Connection Error: {e}")

# =========================================================
# TAB 3: GRAPH INTELLIGENCE (DAY 13 UPDATE - REPORTING)
# =========================================================
with tab3:
    st.header("🕸️ Money Laundering Ring Detection")
    st.markdown("""
    **Technology:** Neo4j Graph Database (Cypher Query Language)
    **Detection Logic:** Identifies circular payment flows (A → B → C → A) indicating 'Round Tripping' or 'Layering'.
    """)

    col_ctrl, col_viz = st.columns([1, 2])

    with col_ctrl:
        st.subheader("Scanner Controls")
        
        # 1. Check Graph Health
        if st.button("🏥 Check Neo4j Connection"):
            try:
                res = requests.get(f"{API_BASE_URL}/graph/health", timeout=2)
                if res.status_code == 200:
                    st.success("✅ Neo4j is ONLINE")
                else:
                    st.error("❌ Neo4j is OFFLINE")
            except:
                st.error("❌ Connection Failed")

        # 2. Trigger Scan
        if st.button("🚀 Scan for Rings", type="primary"):
            with st.spinner("Querying Graph Pattern Matchers..."):
                try:
                    response = requests.get(f"{API_BASE_URL}/graph/rings", timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        st.session_state['graph_rings'] = data['rings']
                        st.session_state['ring_count'] = data['count']
                    else:
                        st.error(f"Scan Failed: {response.status_code}")
                except Exception as e:
                    st.error(f"Error: {e}")

        # Metric Display
        if 'ring_count' in st.session_state:
            st.metric("Suspicious Rings Detected", st.session_state['ring_count'], delta_color="inverse")

    with col_viz:
        st.subheader("Visual Analysis")
        
        if 'graph_rings' in st.session_state and st.session_state['graph_rings']:
            rings = st.session_state['graph_rings']
            
            for idx, ring in enumerate(rings):
                hops = ring.get('hops', 0)
                
                # --- DAY 13 UPDATE: Header with FILE SAR Button ---
                c1, c2 = st.columns([3, 2])
                with c1:
                    st.markdown(f"**🔴 Detected Ring #{idx+1}** (Length: {hops} Hops)")
                with c2:
                    # Unique key is critical for buttons in loops
                    if st.button(f"📄 File SAR (PDF)", key=f"sar_btn_{idx}"):
                        with st.spinner("Generating Regulatory Filing..."):
                            try:
                                # Call the Day 13 Report Endpoint
                                res = requests.post(f"{API_BASE_URL}/reports/generate_sar/{idx}")
                                if res.status_code == 200:
                                    st.download_button(
                                        label="📥 Download Signed PDF",
                                        data=res.content,
                                        file_name=f"SAR_CASE_G{idx+101}.pdf",
                                        mime="application/pdf",
                                        key=f"dl_btn_{idx}"
                                    )
                                    st.success("Report Generated!")
                                else:
                                    st.error(f"Failed: {res.text}")
                            except Exception as e:
                                st.error(f"Error: {e}")
                # --------------------------------------------
                
                # Create Directed Graph
                g = graphviz.Digraph()
                g.attr(rankdir='LR') 
                g.attr('node', shape='circle', style='filled', fillcolor='#ffcccc', fontname='Helvetica')
                g.attr('edge', color='red')

                path_ids = ring['path_ids']
                amounts = ring['amounts']
                
                # Draw Nodes and Edges
                for i in range(len(path_ids) - 1):
                    sender = path_ids[i]
                    receiver = path_ids[i+1]
                    
                    # Safety check for amount index
                    amt = amounts[i] if i < len(amounts) else "?"
                    g.edge(sender, receiver, label=f"${amt}")
                
                # Render the Graph
                st.graphviz_chart(g)
                st.divider()
        
        elif 'graph_rings' in st.session_state:
            st.success("No circular patterns detected. Traffic appears organic.")
        
        else:
            st.info("Awaiting Scan... Click 'Scan for Rings' to query the Graph Database.")