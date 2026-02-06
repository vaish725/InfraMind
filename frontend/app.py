"""
InfraMind Streamlit Frontend
AI-Powered Infrastructure Debugging Interface
"""
import streamlit as st
import requests
import json
from datetime import datetime
from pathlib import Path
import sys

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Page configuration
st.set_page_config(
    page_title="InfraMind - AI-Powered RCA",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API configuration
API_BASE_URL = "http://localhost:8000/api/v1"

# Professional Custom CSS - Enterprise-grade styling
st.markdown("""
<style>
    /* Import Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Roboto+Mono:wght@400;500&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    /* Professional Header */
    .hero-header {
        background: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%);
        padding: 2.5rem 2rem;
        border-radius: 0.5rem;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 600;
        margin: 0;
        letter-spacing: -0.02em;
    }
    
    .hero-subtitle {
        font-size: 1.125rem;
        font-weight: 400;
        margin: 0.5rem 0 0 0;
        opacity: 0.95;
    }
    
    /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 0.375rem;
        font-size: 0.875rem;
        font-weight: 500;
        margin-top: 1rem;
    }
    
    .status-connected {
        background-color: #10b981;
        color: white;
    }
    
    .status-disconnected {
        background-color: #ef4444;
        color: white;
    }
    
    /* Section Headers */
    .section-header {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 600;
        color: #1f2937;
        margin: 0;
    }
    
    .section-subtitle {
        font-size: 0.875rem;
        color: #6b7280;
        margin: 0.25rem 0 0 0;
    }
    
    /* Data Cards */
    .data-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
        margin-bottom: 1rem;
        transition: all 0.2s;
    }
    
    .data-card:hover {
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border-color: #3b82f6;
    }
    
    /* Fix Cards - Professional Priority System */
    .fix-card {
        background: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .fix-card-critical {
        border-left-color: #dc2626;
        background: linear-gradient(to right, #fef2f2 0%, white 100%);
    }
    
    .fix-card-high {
        border-left-color: #f59e0b;
        background: linear-gradient(to right, #fffbeb 0%, white 100%);
    }
    
    .fix-card-medium {
        border-left-color: #3b82f6;
        background: linear-gradient(to right, #eff6ff 0%, white 100%);
    }
    
    .fix-card-low {
        border-left-color: #10b981;
        background: linear-gradient(to right, #f0fdf4 0%, white 100%);
    }
    
    /* Priority Labels */
    .priority-label {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 0.25rem;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .priority-critical {
        background-color: #dc2626;
        color: white;
    }
    
    .priority-high {
        background-color: #f59e0b;
        color: white;
    }
    
    .priority-medium {
        background-color: #3b82f6;
        color: white;
    }
    
    .priority-low {
        background-color: #10b981;
        color: white;
    }
    
    /* Confidence Meter */
    .confidence-container {
        background: #f3f4f6;
        border-radius: 0.5rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .confidence-bar {
        background: linear-gradient(to right, #3b82f6 0%, #1e3a8a 100%);
        height: 0.5rem;
        border-radius: 0.25rem;
        transition: width 0.3s ease;
    }
    
    .confidence-label {
        font-size: 0.875rem;
        color: #374151;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* Service Tags */
    .service-tag {
        display: inline-block;
        padding: 0.375rem 0.75rem;
        background: #3b82f6;
        color: white;
        border-radius: 0.25rem;
        font-size: 0.875rem;
        font-weight: 500;
        margin: 0.25rem 0.25rem 0.25rem 0;
    }
    
    /* Evidence Block */
    .evidence-block {
        background: #1f2937;
        padding: 1rem;
        border-radius: 0.375rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3b82f6;
    }
    
    .evidence-text {
        font-family: 'Roboto Mono', monospace;
        font-size: 0.875rem;
        color: #f3f4f6;
        margin: 0;
        line-height: 1.6;
    }
    
    /* Implementation Steps */
    .implementation-step {
        display: flex;
        align-items: start;
        margin: 0.75rem 0;
        padding: 0.75rem;
        background: #f9fafb;
        border-radius: 0.375rem;
        border: 1px solid #e5e7eb;
    }
    
    .step-number {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 2rem;
        height: 2rem;
        background: #3b82f6;
        color: white;
        border-radius: 50%;
        font-weight: 600;
        font-size: 0.875rem;
        margin-right: 1rem;
        flex-shrink: 0;
    }
    
    .step-text {
        flex: 1;
        color: #374151;
        line-height: 1.5;
    }
    
    /* Buttons */
    .stButton button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-weight: 600;
        border-radius: 0.5rem;
        transition: all 0.2s;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .stButton button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    /* Quick Start Section */
    .quick-start {
        background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 1px solid #c7d2fe;
        margin-bottom: 2rem;
    }
    
    .quick-start-title {
        font-size: 1.25rem;
        font-weight: 600;
        color: #1e3a8a;
        margin: 0 0 0.5rem 0;
    }
    
    .quick-start-text {
        color: #475569;
        margin: 0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0.5rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #6b7280;
    }
    
    .stTabs [aria-selected="true"] {
        background: #3b82f6;
        color: white;
        border-color: #3b82f6;
    }
    
    /* File Uploader */
    .uploadedFile {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 0.375rem;
        padding: 0.75rem;
    }
    
    /* Metrics */
    .stMetric {
        background: white;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #e5e7eb;
    }
    
    /* Remove default Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }
    
    /* Input Fields */
    .stTextInput input, .stSelectbox select {
        border: 1px solid #d1d5db;
        border-radius: 0.375rem;
        padding: 0.625rem;
        font-size: 0.875rem;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }
    
    /* Checkboxes */
    .stCheckbox {
        font-size: 0.875rem;
    }
</style>
""", unsafe_allow_html=True)


def check_api_health():
    """Check if the API is healthy and accessible."""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            return True, response.json()
        return False, None
    except Exception as e:
        return False, str(e)


def initialize_session_state():
    """Initialize session state variables."""
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    if 'incident_id' not in st.session_state:
        st.session_state.incident_id = None
    if 'show_raw_data' not in st.session_state:
        st.session_state.show_raw_data = False


def render_header():
    """Render the application header with modern design."""
    # API health check
    healthy, health_data = check_api_health()
    
    # Hero header
    st.markdown(f"""
    <div class="hero-header">
        <div class="hero-title">InfraMind</div>
        <div class="hero-subtitle">AI-Powered Root Cause Analysis for Infrastructure Incidents</div>
        <div class="status-badge status-{'connected' if healthy else 'disconnected'}">
            {'●' if healthy else '○'} API {'Connected' if healthy else 'Disconnected'}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if not healthy:
        st.error("API server is offline. Start it with: `python scripts/start_api.py`")


def render_sidebar():
    """Render the sidebar with navigation and settings."""
    st.sidebar.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h2 style="color: #1e3a8a; margin: 0; font-weight: 600;">Navigation</h2>
    </div>
    """, unsafe_allow_html=True)
    
    page = st.sidebar.radio(
        "Select Page",
        ["New Analysis", "Incident History", "Settings"],
        label_visibility="collapsed"
    )
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("""
    <div class="data-card")
        <h3 style="color: #667eea; margin-top: 0;">About InfraMind</h3>
        <p style="line-height: 1.8;">
            <strong>InfraMind</strong> leverages <strong>Google Gemini AI</strong> to automatically 
            analyze infrastructure incidents and identify root causes by intelligently 
            correlating multiple data sources:
        </p>
        <ul style="line-height: 2;">
            <li><strong>Logs</strong> - Error patterns & anomalies</li>
            <li><strong>Metrics</strong> - Performance indicators</li>
            <li><strong>Traces</strong> - Distributed request flows</li>
            <li><strong>Configs</strong> - Configuration changes</li>
            <li><strong>Deployments</strong> - Release events</li>
        </ul>
        <div style="margin-top: 1rem; padding: 1rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 0.5rem; color: white; text-align: center;">
            <strong>Gemini 3 Hackathon 2026</strong>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    return page


def render_new_analysis_page():
    """Render the new analysis submission page."""
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">New Incident Analysis</h2>
        <p class="section-subtitle">Upload your infrastructure data or use our sample incident to get started</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Start Section
    st.markdown("""
    <div class="quick-start">
        <h3 class="quick-start-title">Quick Start</h3>
        <p class="quick-start-text">
            Try InfraMind with our pre-loaded sample incident scenario
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Load Sample Incident Data", use_container_width=True, type="primary"):
        st.session_state.use_sample_logs = True
        st.session_state.use_sample_metrics = True
        st.session_state.use_sample_traces = True
        st.success("Sample data loaded! Scroll down and click 'Analyze Incident' to continue.")
    
    st.markdown("---")
    
    # Incident Configuration
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">Incident Configuration</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Incident ID input
    incident_id = st.text_input(
        "Incident ID",
        value=f"incident-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
        help="Unique identifier for this incident"
    )
    
    # Time window
    col1, col2 = st.columns([2, 1])
    with col1:
        time_window = st.slider(
            "Time Window (minutes)",
            min_value=5,
            max_value=120,
            value=30,
            help="How far back to look for correlated events"
        )
    
    with col2:
        focus_area = st.selectbox(
            "Focus Area",
            ["auto", "configuration", "performance", "deployment", "dependencies"],
            help="Narrow the analysis focus"
        )
    
    # Create tabs for different data sources
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">Data Sources</h3>
        <p class="section-subtitle">Upload your infrastructure data files</p>
    </div>
    """, unsafe_allow_html=True)
    
    tabs = st.tabs(["Logs", "Metrics", "Traces", "Configuration", "Deployments"])
    
    # Tab 1: Logs
    with tabs[0]:
        st.markdown("#### Log Files")
        log_files = st.file_uploader(
            "Upload log files (TXT, JSON, LOG)",
            type=["log", "txt", "json"],
            accept_multiple_files=True,
            key="log_files",
            help="Upload application or infrastructure logs"
        )
        
        if log_files:
            st.success(f"{len(log_files)} log file(s) uploaded")
            for log_file in log_files:
                with st.expander(f"{log_file.name} ({log_file.size:,} bytes)"):
                    preview = log_file.read().decode('utf-8')[:500]
                    st.code(preview + "...", language="log")
                    log_file.seek(0)  # Reset file pointer
        else:
            # Option to use sample data
            if st.checkbox("Use sample log data", key="use_sample_logs"):
                st.info("Using 3 sample log files (api-gateway, order-service, payment-service)")
    
    # Tab 2: Metrics
    with tabs[1]:
        st.markdown("#### Metrics Data")
        metric_files = st.file_uploader(
            "Upload metrics files (JSON, CSV)",
            type=["json", "csv"],
            accept_multiple_files=True,
            key="metric_files",
            help="Upload system or application metrics"
        )
        
        if metric_files:
            st.success(f"{len(metric_files)} metric file(s) uploaded")
        else:
            if st.checkbox("Use sample metrics data", key="use_sample_metrics"):
                st.info("Using sample metrics (CPU, memory, latency, error rates)")
    
    # Tab 3: Traces
    with tabs[2]:
        st.markdown("#### Distributed Traces")
        trace_files = st.file_uploader(
            "Upload trace files (JSON)",
            type=["json"],
            accept_multiple_files=True,
            key="trace_files",
            help="Upload distributed tracing data (OpenTelemetry, Jaeger, etc.)"
        )
        
        if trace_files:
            st.success(f"{len(trace_files)} trace file(s) uploaded")
        else:
            if st.checkbox("Use sample trace data", key="use_sample_traces"):
                st.info("Using sample distributed traces (9 spans across 3 services)")
    
    # Tab 4: Configuration
    with tabs[3]:
        st.markdown("#### Configuration Files")
        config_files = st.file_uploader(
            "Upload configuration files (YAML, ENV, CONF)",
            type=["yaml", "yml", "env", "conf"],
            accept_multiple_files=True,
            key="config_files",
            help="Upload configuration files to detect recent changes"
        )
        
        if config_files:
            st.success(f"{len(config_files)} config file(s) uploaded")
        else:
            st.info("Tip: Upload before/after configs to detect changes")
    
    # Tab 5: Deployments
    with tabs[4]:
        st.markdown("#### Recent Deployments")
        st.info("Deployment tracking coming in future updates")
        deployment_info = st.text_area(
            "Deployment details (optional)",
            placeholder="e.g., Deployed payment-service v2.3.1 at 14:30 UTC on 2026-02-05",
            height=100,
            help="Manual deployment information"
        )
    
    # Analysis options
    st.markdown("---")
    st.markdown("""
    <div class="section-header">
        <h3 class="section-title">Analysis Options</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        include_summary = st.checkbox("Include executive summary", value=True)
    with col2:
        validate_analysis = st.checkbox("Validate analysis", value=True)
    
    # Submit button
    st.markdown("---")
    st.markdown("""
    <div class="section-header" style="text-align: center; border-left: none;">
        <h3 class="section-title">Ready to Analyze</h3>
        <p class="section-subtitle">Click below to start AI-powered root cause analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Analyze Incident with Gemini AI", type="primary", use_container_width=True):
        # Check if we have any data
        has_data = log_files or metric_files or trace_files or config_files
        use_samples = (
            st.session_state.get("use_sample_logs") or 
            st.session_state.get("use_sample_metrics") or 
            st.session_state.get("use_sample_traces")
        )
        
        if not has_data and not use_samples:
            st.error("Please upload at least one data source or click 'Load Sample Incident Data' above")
        else:
            with st.spinner("Analyzing incident with Google Gemini AI... This may take 10-30 seconds..."):
                result = submit_analysis(
                    incident_id=incident_id,
                    log_files=log_files,
                    metric_files=metric_files,
                    trace_files=trace_files,
                    config_files=config_files,
                    time_window=time_window,
                    focus_area=focus_area if focus_area != "auto" else None,
                    include_summary=include_summary,
                    use_samples=use_samples
                )
                
                if result:
                    st.session_state.analysis_results = result
                    st.session_state.incident_id = incident_id
                    st.success("Analysis complete! Scroll down to see results.")
                    st.rerun()


def submit_analysis(incident_id, log_files, metric_files, trace_files, config_files,
                   time_window, focus_area, include_summary, use_samples):
    """Submit analysis request to API."""
    try:
        # Prepare the request payload
        payload = {
            "incident_id": incident_id,
            "time_window_minutes": time_window,
            "focus_area": focus_area,
            "include_summary": include_summary,
            "log_files": [],
            "metric_files": [],
            "trace_files": [],
            "config_files": []
        }
        
        # Load sample data if requested
        if use_samples:
            sample_dir = Path(__file__).parent.parent / "data" / "samples"
            
            if st.session_state.get("use_sample_logs"):
                # Load all sample log files
                logs_dir = sample_dir / "logs"
                if logs_dir.exists():
                    for log_file in logs_dir.glob("*.log"):
                        payload["log_files"].append({
                            "content": log_file.read_text(),
                            "source": log_file.stem
                        })
            
            if st.session_state.get("use_sample_metrics"):
                # Load all metric files
                metrics_dir = sample_dir / "metrics"
                if metrics_dir.exists():
                    for metrics_file in metrics_dir.glob("*.json"):
                        payload["metric_files"].append({
                            "content": metrics_file.read_text()
                        })
            
            if st.session_state.get("use_sample_traces"):
                # Load trace files
                traces_dir = sample_dir / "traces"
                if traces_dir.exists():
                    for trace_file in traces_dir.glob("*.json"):
                        payload["trace_files"].append(trace_file.read_text())
        
        # Add uploaded files
        if log_files:
            for log_file in log_files:
                payload["log_files"].append({
                    "content": log_file.read().decode('utf-8'),
                    "source": log_file.name
                })
        
        if metric_files:
            for metric_file in metric_files:
                payload["metric_files"].append({
                    "content": metric_file.read().decode('utf-8')
                })
        
        if trace_files:
            for trace_file in trace_files:
                payload["trace_files"].append(trace_file.read().decode('utf-8'))
        
        if config_files:
            for config_file in config_files:
                payload["config_files"].append({
                    "content": config_file.read().decode('utf-8'),
                    "path": config_file.name,
                    "format": "auto"
                })
        
        # Send request to API
        response = requests.post(
            f"{API_BASE_URL}/incidents/analyze",
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503:
            st.error("Gemini API quota exceeded. Please try again later.")
            return None
        else:
            st.error(f"Analysis failed: {response.json().get('detail', 'Unknown error')}")
            return None
            
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def render_analysis_results():
    """Render the analysis results with modern, hackathon-level design."""
    if not st.session_state.analysis_results:
        return
    
    results = st.session_state.analysis_results
    rca = results.get("rca")
    
    if not rca:
        st.warning("Analysis is still processing or failed")
        return
    
    # Header
    st.markdown("---")
    st.markdown(f"""
    <div class="section-header">
        <h1 class="section-title">Analysis Complete</h1>
        <p class="section-subtitle">Incident ID: <code>{rca.get('incident_id', 'Unknown')}</code></p>
    </div>
    """, unsafe_allow_html=True)
    
    # Executive Summary
    if rca.get("summary"):
        st.markdown("""
        <div class="data-card" style="background: linear-gradient(to right, #eff6ff 0%, white 100%); border-left: 4px solid #3b82f6;">
            <h3 style="color: #1e3a8a; margin-top: 0; font-weight: 600;">Executive Summary</h3>
        """, unsafe_allow_html=True)
        st.markdown(f"<p style='font-size: 1rem; line-height: 1.6; color: #374151;'>{rca['summary']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Root Cause with confidence
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="data-card">
            <h2 style="color: #1e3a8a; margin-top: 0; font-weight: 600;">Root Cause</h2>
            <p style="font-size: 1rem; line-height: 1.6; color: #374151;">
                {rca.get('root_cause', 'Unknown')}
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Get confidence level
        confidence = rca.get('overall_confidence', 'MEDIUM')
        confidence_pct = {'HIGH': 90, 'MEDIUM': 70, 'LOW': 50}.get(confidence, 70)
        st.markdown(f"""
        <div class="confidence-container">
            <div class="confidence-label">Confidence</div>
            <div class="confidence-bar" style="width: {confidence_pct}%;"></div>
            <div style="margin-top: 0.5rem; font-size: 1.25rem; font-weight: 600; color: #1e3a8a;">{confidence}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Contributing Factors
    if rca.get('contributing_factors'):
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Contributing Factors</h3>
        </div>
        """, unsafe_allow_html=True)
        for factor in rca['contributing_factors']:
            st.markdown(f"- {factor}")
    
    # Symptoms
    if rca.get('symptoms'):
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Symptoms</h3>
        </div>
        """, unsafe_allow_html=True)
        for symptom in rca['symptoms']:
            st.markdown(f"- {symptom}")
    
    # Causal Chain
    if rca.get('causal_chain'):
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Causal Chain</h3>
            <p class="section-subtitle">Step-by-step breakdown of how the incident occurred</p>
        </div>
        """, unsafe_allow_html=True)
        
        for idx, link in enumerate(rca['causal_chain'], 1):
            event_text = link.get('event', 'Unknown event')
            confidence = link.get('confidence', 'MEDIUM')
            
            with st.expander(f"**Step {idx}:** {event_text}", expanded=idx==1):
                col_a, col_b = st.columns([1, 3])
                
                with col_a:
                    st.markdown(f"""
                    <div class="confidence-container">
                        <div class="confidence-label">Confidence</div>
                        <div style="font-size: 1.25rem; font-weight: 600; color: #1e3a8a;">{confidence}</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col_b:
                    if link.get('service'):
                        st.markdown(f"**Service:** {link['service']}")
                    if link.get('timestamp'):
                        st.markdown(f"**Time:** {link['timestamp']}")
                    if link.get('is_root_cause'):
                        st.markdown("**⚠️ This is the root cause**")
                    if link.get('is_symptom'):
                        st.markdown("**📋 This is a symptom**")
    
    # Fix Suggestions
    if rca.get('fix_suggestions'):
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">Recommended Fixes</h3>
            <p class="section-subtitle">Prioritized action items to resolve and prevent this incident</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Group by priority
        immediate_fixes = [f for f in rca['fix_suggestions'] if f.get('priority') == 'immediate']
        short_term_fixes = [f for f in rca['fix_suggestions'] if f.get('priority') == 'short-term']
        long_term_fixes = [f for f in rca['fix_suggestions'] if f.get('priority') == 'long-term']
        
        # Render each group
        for fixes, label in [(immediate_fixes, "Immediate"), (short_term_fixes, "Short-term"), (long_term_fixes, "Long-term")]:
            if fixes:
                st.markdown(f"### {label} Fixes")
                for fix in fixes:
                    render_fix_card(fix, fix.get('priority', 'short-term'))
    
    # Fix Suggestions with priority-based styling
    st.markdown("""
    <div class="glass-card">
        <h3 style="color: #667eea; margin-top: 0;">Recommended Fixes</h3>
        <p style="color: #666;">Prioritized action items to resolve this incident</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Group by priority
    critical_fixes = [f for f in rca['fix_suggestions'] if f['priority'] == 'critical']
    high_fixes = [f for f in rca['fix_suggestions'] if f['priority'] == 'high']
    medium_fixes = [f for f in rca['fix_suggestions'] if f['priority'] == 'medium']
    low_fixes = [f for f in rca['fix_suggestions'] if f['priority'] == 'low']
    
    if critical_fixes:
        st.markdown("#### Critical Priority")
        for fix in fixes:
            render_fix_card(fix, fix.get('priority', 'short-term'))
    
    # Reasoning Steps (collapsible)
    if rca.get('reasoning_steps'):
        st.markdown("""
        <div class="section-header">
            <h3 class="section-title">AI Reasoning Process</h3>
            <p class="section-subtitle">How Gemini analyzed this incident</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("Show Detailed Reasoning Steps", expanded=False):
            for step in rca['reasoning_steps']:
                st.markdown(f"**Step {step.get('step_number', '?')}:** {step.get('description', 'No description')}")
                if step.get('conclusion'):
                    st.markdown(f"*Conclusion:* {step['conclusion']}")
                if step.get('evidence'):
                    st.markdown("*Evidence:*")
                    for ev in step['evidence'][:3]:
                        if isinstance(ev, dict):
                            st.code(ev.get('description', str(ev)))
                        else:
                            st.code(str(ev))
                st.markdown("---")
    
    # Raw Data Toggle
    st.markdown("---")
    with st.expander("Advanced: View Raw JSON Data"):
        st.json(rca)
    
    # Action buttons
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        report_data = json.dumps(rca, indent=2, default=str)
        st.download_button(
            label="Download Report",
            data=report_data,
            file_name=f"{rca.get('incident_id', 'incident')}_analysis.json",
            mime="application/json",
            use_container_width=True,
            type="primary"
        )
    
    with col2:
        if st.button("New Analysis", use_container_width=True):
            st.session_state.analysis_results = None
            st.rerun()
    
    with col3:
        if st.button("View History", use_container_width=True):
            st.session_state.analysis_results = None
            st.info("History feature coming soon!")


def render_fix_card(fix, priority="medium"):
    """Render a fix suggestion card with priority-based styling."""
    priority_config = {
        "critical": {
            "class": "fix-card-critical",
            "badge_class": "priority-critical",
            "label": "CRITICAL"
        },
        "high": {
            "class": "fix-card-high",
            "badge_class": "priority-high",
            "label": "HIGH"
        },
        "medium": {
            "class": "fix-card-medium",
            "badge_class": "priority-medium",
            "label": "MEDIUM"
        },
        "low": {
            "class": "fix-card-low",
            "badge_class": "priority-low",
            "label": "LOW"
        }
    }
    
    config = priority_config.get(priority, priority_config["medium"])
    
    st.markdown(f"""
    <div class="fix-card {config['class']}">
        <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;">
            <h4 style="margin: 0; color: #1f2937; font-weight: 600;">{fix['title']}</h4>
            <span class="priority-label {config['badge_class']}">{config['label']}</span>
        </div>
        <p style="color: #4b5563; line-height: 1.6; margin: 1rem 0;">{fix['description']}</p>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1rem; margin-top: 1rem;">
            <div>
                <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase;">Type</div>
                <div style="font-size: 0.875rem; color: #1f2937; margin-top: 0.25rem;">{fix['fix_type'].replace('_', ' ').title()}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase;">Time Estimate</div>
                <div style="font-size: 0.875rem; color: #1f2937; margin-top: 0.25rem;">{fix['estimated_time']}</div>
            </div>
            <div>
                <div style="font-size: 0.75rem; color: #9ca3af; font-weight: 600; text-transform: uppercase;">Risk Level</div>
                <div style="font-size: 0.875rem; color: #1f2937; margin-top: 0.25rem;">{fix['risk_level'].title()}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    if fix.get('implementation_steps'):
        with st.expander("View Implementation Steps"):
            for idx, step in enumerate(fix['implementation_steps'], 1):
                st.markdown(f"""
                <div style="display: flex; gap: 1rem; margin: 0.8rem 0; padding: 0.8rem; background: #f8f9fa; border-radius: 0.5rem;">
                    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; width: 2rem; height: 2rem; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; flex-shrink: 0;">
                        {idx}
                    </div>
                    <div style="flex: 1; color: #333; line-height: 1.6;">
                        {step}
                    </div>
                </div>
                """, unsafe_allow_html=True)


def render_history_page():
    """Render the incident history page."""
    st.header("Incident History")
    
    try:
        response = requests.get(f"{API_BASE_URL}/incidents", timeout=10)
        if response.status_code == 200:
            data = response.json()
            incidents = data.get("incidents", [])
            
            if not incidents:
                st.info("No incidents found. Create your first analysis!")
                return
            
            st.markdown(f"**Total Incidents:** {data.get('total', 0)}")
            
            # Filters
            col1, col2 = st.columns(2)
            with col1:
                status_filter = st.multiselect(
                    "Filter by status",
                    ["completed", "failed", "processing"],
                    default=["completed", "failed"]
                )
            
            # Display incidents
            for incident in incidents:
                if incident['status'] not in status_filter:
                    continue
                
                status_emoji = {
                    "completed": "[COMPLETED]",
                    "failed": "[FAILED]",
                    "processing": "[PROCESSING]"
                }
                
                with st.expander(
                    f"{status_emoji.get(incident['status'], '[UNKNOWN]')} {incident['incident_id']} - "
                    f"{incident['status'].title()}"
                ):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Created:** {incident['created_at']}")
                    with col2:
                        if incident.get('completed_at'):
                            st.write(f"**Completed:** {incident['completed_at']}")
                    
                    if st.button(f"View Details", key=f"view_{incident['incident_id']}"):
                        # Fetch full details
                        detail_response = requests.get(
                            f"{API_BASE_URL}/incidents/{incident['incident_id']}",
                            timeout=10
                        )
                        if detail_response.status_code == 200:
                            st.session_state.analysis_results = detail_response.json()
                            st.session_state.incident_id = incident['incident_id']
                            st.rerun()
        else:
            st.error("Failed to fetch incident history")
    
    except Exception as e:
        st.error(f"Error: {str(e)}")


def render_settings_page():
    """Render the settings page."""
    st.header("Settings")
    
    st.subheader("API Configuration")
    api_url = st.text_input("API Base URL", value=API_BASE_URL)
    
    st.subheader("Analysis Settings")
    default_time_window = st.slider("Default Time Window (minutes)", 5, 120, 30)
    
    st.subheader("Display Settings")
    theme = st.selectbox("Theme", ["Light", "Dark", "Auto"])
    show_advanced = st.checkbox("Show advanced options", value=False)
    
    if st.button("Save Settings"):
        st.success("Settings saved!")


def main():
    """Main application entry point."""
    initialize_session_state()
    render_header()
    
    # Render sidebar and get selected page
    page = render_sidebar()
    
    # Render appropriate page
    if page == "New Analysis":
        # Check if we have results to show
        if st.session_state.analysis_results:
            render_analysis_results()
        else:
            render_new_analysis_page()
    
    elif page == "Incident History":
        render_history_page()
    
    elif page == "Settings":
        render_settings_page()


if __name__ == "__main__":
    main()
