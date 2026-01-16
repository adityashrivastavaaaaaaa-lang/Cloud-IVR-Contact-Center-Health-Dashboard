import streamlit as st
import pandas as pd
import requests
import time
from src.analytics import load_data, calculate_kpis, get_hourly_metrics

# Page Config
st.set_page_config(page_title="Contact Center Health", page_icon="📞", layout="wide")

# Styling
st.markdown("""
    <style>
    .big-font { font-size: 24px !important; }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📞 Cloud IVR & Contact Center Health Dashboard")

# Load Data
df = load_data()

# Tabs
tab1, tab2 = st.tabs(["📊 Health Dashboard", "🤖 IVR Simulator"])

with tab1:
    st.header("Real-Time KPI Overview")
    
    # Calculate KPIs
    kpis = calculate_kpis(df)
    
    # Top Metrics Row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Calls", kpis['total_calls'])
    with col2:
        st.metric("Dismal Abandon Rate", f"{kpis['abandon_rate']}%", delta_color="inverse")
    with col3:
        st.metric("Avg Handle Time (s)", f"{kpis['aht']}s")
    with col4:
        st.metric("SLA % (<20s)", f"{kpis['sla_percent']}%", delta=f"{kpis['sla_percent'] - 80}%")

    st.markdown("---")
    
    # Charts
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("Calls & Abandons per Hour")
        hourly_data = get_hourly_metrics(df)
        if not hourly_data.empty:
            st.bar_chart(hourly_data.set_index('hour')[['calls', 'abandons']])
        else:
            st.info("No data available for hourly chart.")
            
    with col_chart2:
        st.subheader("Call Distribution by Queue")
        if not df.empty:
            queue_counts = df['queue'].value_counts()
            st.bar_chart(queue_counts)
        else:
            st.info("No data available.")

    st.subheader("Recent Call Logs")
    st.dataframe(df.tail(10))

with tab2:
    st.header("Interactive IVR Simulator")
    st.write("Simulate a call flow by entering DTMF digits.")
    
    col_sim_left, col_sim_right = st.columns([1, 2])
    
    with col_sim_left:
        st.markdown("### User Input")
        user_input = st.text_input("Enter DTMF (1 for Sales, 2 for Support):", max_chars=1)
        
        if st.button("📞 Call / Send DTMF"):
            if user_input:
                try:
                    # Assuming API is running locally on port 5000
                    response = requests.post("http://127.0.0.1:5000/ivr", json={"input": user_input})
                    if response.status_code == 200:
                        res_data = response.json()
                        st.success(f"IVR Response: {res_data['message']}")
                        st.info(f"Action: {res_data['action']} -> {res_data['queue']}")
                    else:
                        st.error("Failed to connect to IVR Backend.")
                except requests.exceptions.ConnectionError:
                    st.error("🚨 Backend is not running! Run `python src/api.py` first.")
            else:
                st.warning("Please enter a digit (1 or 2).")
                
    with col_sim_right:
        st.markdown("### Live Queue Status")
        if st.button("🔄 Refresh Queues"):
            try:
                q_response = requests.get("http://127.0.0.1:5000/queues")
                if q_response.status_code == 200:
                    queues = q_response.json()
                    for q in queues:
                        st.markdown(f"""
                        **{q['queue_name']} Queue**
                        - Agents Available: `{q['agents_available']}`
                        - Waiting: `{q['calls_waiting']}`
                        """)
                        st.progress(q['agents_busy'] / (q['agents_available'] + q['agents_busy'] + 0.1))
                else:
                    st.error("Failed to fetch queue status.")
            except requests.exceptions.ConnectionError:
                 st.error("🚨 Backend is not running.")
