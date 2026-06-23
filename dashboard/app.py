"""
Streamlit Dashboard: Real-time BMS visualization.
Run with: streamlit run dashboard/app.py
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import sys
sys.path.append("..")

st.set_page_config(page_title="🔋 AI Battery Monitor", layout="wide")
st.title("🔋 AI-Powered Battery Management System")

# --- Sidebar ---
st.sidebar.header("Simulation Controls")
num_cycles = st.sidebar.slider("Simulated Cycles", 50, 500, 200)
degradation_rate = st.sidebar.slider("Degradation Rate (%/100 cycles)", 1.0, 10.0, 3.5)
noise = st.sidebar.slider("Sensor Noise", 0.0, 0.5, 0.1)

# --- Simulate data ---
np.random.seed(42)
cycles = np.arange(1, num_cycles + 1)
soh = 100 - (degradation_rate / 100) * cycles + np.random.normal(0, noise, num_cycles)
soh = np.clip(soh, 0, 100)
voltage = 3.7 + 0.5 * (soh / 100) + np.random.normal(0, noise * 0.1, num_cycles)
temperature = 25 + 5 * np.sin(cycles / 20) + np.random.normal(0, noise, num_cycles)
df = pd.DataFrame({"cycle": cycles, "soh": soh, "voltage": voltage, "temperature": temperature})

# --- KPIs ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Current SoH", f"{soh[-1]:.1f}%", f"{soh[-1]-soh[-10]:.1f}% (10 cycles)")
col2.metric("Voltage", f"{voltage[-1]:.3f} V")
col3.metric("Temperature", f"{temperature[-1]:.1f} °C")
eol_cycle = int((100 - 70) / (degradation_rate / 100))
col4.metric("Est. End-of-Life", f"Cycle ~{eol_cycle}")

st.divider()

col_left, col_right = st.columns(2)

with col_left:
    st.subheader("State of Health Over Cycles")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["cycle"], y=df["soh"], mode="lines", name="SoH",
        line=dict(color="#00b4d8", width=2)
    ))
    fig.add_hline(y=70, line_dash="dash", line_color="red", annotation_text="End-of-Life (70%)")
    fig.update_layout(xaxis_title="Cycle", yaxis_title="SoH (%)", height=350)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("Voltage & Temperature Trends")
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=df["cycle"], y=df["voltage"], name="Voltage (V)", line=dict(color="#f77f00")))
    fig2.add_trace(go.Scatter(
        x=df["cycle"], y=df["temperature"], name="Temp (°C)",
        yaxis="y2", line=dict(color="#e63946", dash="dot")
    ))
    fig2.update_layout(
        yaxis=dict(title="Voltage (V)"),
        yaxis2=dict(title="Temperature (°C)", overlaying="y", side="right"),
        height=350,
    )
    st.plotly_chart(fig2, use_container_width=True)

# --- Charging recommendation ---
st.subheader("⚡ Charging Recommendation")
urgency = st.radio("Charging Urgency", ["normal", "fast"], horizontal=True)
tier = "high" if soh[-1] >= 80 else "low"
profiles = {
    ("high", "fast"):   (1.0, 4.2,  60),
    ("high", "normal"): (0.7, 4.15, 80),
    ("low",  "fast"):   (0.5, 4.1,  100),
    ("low",  "normal"): (0.3, 4.05, 120),
}
cc, cv, est = profiles[(tier, urgency)]
c1, c2, c3 = st.columns(3)
c1.metric("Constant Current", f"{cc} A")
c2.metric("Cutoff Voltage", f"{cv} V")
c3.metric("Est. Charge Time", f"{est} min")

st.caption("Built with ❤️ | NASA/CALCE battery data | AI-powered degradation model")
