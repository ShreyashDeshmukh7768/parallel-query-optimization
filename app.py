import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

from data_generator import generate_dataset
from sequential import process_sequential
from parallel import process_parallel

st.set_page_config(page_title="Parallel DB Optimizer", layout="wide", page_icon="⚡")

def show_gauge(speedup):
    """Generates a gauge-style visualization using Plotly."""
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = speedup,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Performance Speedup Indicator"},
        number = {'suffix': "x"},
        gauge = {
            'axis': {'range': [0, max(5, speedup + 1)], 'tickwidth': 1},
            'bar': {'color': "rgba(0,0,0,0)"},  # Hide standard inner bar for a cleaner zone look
            'steps': [
                {'range': [0, 1], 'color': "salmon"},
                {'range': [1, 2], 'color': "khaki"},
                {'range': [2, max(5, speedup + 1)], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': speedup
            }
        }
    ))
    fig.update_layout(height=400, margin=dict(l=10, r=10, t=50, b=10))
    st.plotly_chart(fig, use_container_width=True)

def show_insight(speedup):
    """Automatically explains the performance result based on speedup."""
    if speedup < 1:
        st.error("📉 **Insight:** Parallel execution is slower due to overhead dominating computation. The overhead of spawning processes takes longer than just calculating sequentially.")
    elif 1 <= speedup <= 2:
        st.warning("⚖️ **Insight:** Parallel execution shows moderate improvement due to partial workload distribution.")
    else:
        st.success("🚀 **Insight:** Parallel execution significantly improves performance due to efficient CPU utilization.")

def display_metrics(seq_time, par_time, speedup):
    """Renders the execution time metrics side-by-side."""
    st.markdown("---")
    st.subheader("📊 Execution Benchmark")
    m1, m2, m3 = st.columns(3)
    m1.metric("⏱ Sequential Time", f"{seq_time:.4f} sec")
    m2.metric("⚡ Parallel Time", f"{par_time:.4f} sec", delta=f"{par_time - seq_time:.4f} sec", delta_color="inverse")
    m3.metric("🚀 Speedup multiplier", f"{speedup:.2f}x")
    st.markdown("---")

def run_experiment(dataset_size, num_cores):
    """Orchestrates data generation, computation, and rendering all visual metrics."""
    filename = "dataset.csv"
    
    # 1) Generate Dataset
    with st.spinner("Generating synthetic dataset..."):
        generate_dataset(num_rows=dataset_size, filename=filename)
        time.sleep(0.5) # Simulate slight UX delay
        
    st.markdown("---")
    
    # Execution layout Setup
    col1, col2 = st.columns(2)
    
    # 2) Sequential Execution Frame
    with col1:
        st.subheader("⏱ Sequential Tracker")
        seq_text = st.empty()
        seq_text.info("Running Sequential Execution...")
        seq_bar = st.progress(0, text="Sequential Execution Progress")
        
        # Simulate progress bar logic smoothly
        for i in range(100):
            time.sleep(0.005) # Simulated progress loop wrapper
            seq_bar.progress(i + 1, text="Sequential Execution Progress")
            
        # Execute actual backend logic
        seq_result, seq_time, seq_rows = process_sequential(filename)
        seq_text.success("Sequential Framework Completed!")
        
    # 3) Parallel Execution Frame
    with col2:
        st.subheader("⚡ Parallel Tracker")
        par_text = st.empty()
        par_text.info(f"Running Parallel Execution ({num_cores} cores)...")
        par_bar = st.progress(0, text="Parallel Execution Progress")
        
        # Simulate progress bar logic smoothly
        for i in range(100):
            time.sleep(0.005)
            par_bar.progress(i + 1, text="Parallel Execution Progress")
            
        # Execute actual backend logic
        par_result, par_time, par_rows = process_parallel(filename, num_cores=num_cores)
        par_text.success("Parallel Framework Completed!")
        
    # 4) Calculate Result Validation
    speedup = seq_time / par_time if par_time > 0 else 0
    display_metrics(seq_time, par_time, speedup)
    
    # 5) Complex Plotly Visualizations & Dynamic Auto-Explanations
    col_gauge, col_text = st.columns([1, 1.2])
    with col_gauge:
        show_gauge(speedup)
        
    with col_text:
        st.write("<br><br>", unsafe_allow_html=True)
        show_insight(speedup)
        
        st.subheader("📋 Results Summary")
        r_size, r_match = st.columns(2)
        r_size.info(f"📁 **Elements Processed:** {dataset_size:,}")
        
        if seq_result is not None and par_result is not None:
            results_match = seq_result.reset_index(drop=True).equals(par_result.reset_index(drop=True))
        else:
            results_match = False
            
        if results_match:
            r_match.success("✅ **Data Output Matching:** True")
        else:
            r_match.error("❌ **Data Output Matching:** False")


# ==========================================
# MAIN UI DRIVER
# ==========================================
st.sidebar.title("⚙️ Experiment Config")
st.sidebar.markdown("Use the sliders below to adjust dataset processing properties.")

dataset_size = st.sidebar.slider("Dataset Size (Rows)", 100000, 1000000, 500000, 100000)
num_cores = st.sidebar.slider("Number of Parallel Processes", 1, 8, 4, 1)

st.sidebar.markdown("---")
run_button = st.sidebar.button("Run Experiment", type="primary", use_container_width=True)

st.title("⚡ Parallel Database Query Optimization Dashboard")
st.markdown("Use this highly-available workspace to verify Python multiprocessing enhancements dynamically across CPU distributions!")

if run_button:
    run_experiment(dataset_size, num_cores)
else:
    st.info("👈 Please select your configuration in the sidebar and click **Run Experiment**.")
