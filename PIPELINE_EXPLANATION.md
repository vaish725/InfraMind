# 🏗️ InfraMind - Complete Codebase Pipeline Explanation

**Date:** February 5, 2026  
**Version:** 1.0  

---

## 📚 Table of Contents

1. [High-Level Overview](#high-level-overview)
2. [Architecture Diagram](#architecture-diagram)
3. [Complete Data Flow](#complete-data-flow)
4. [Component Deep Dive](#component-deep-dive)
5. [Code Organization](#code-organization)
6. [Request Lifecycle](#request-lifecycle)
7. [Key Classes & Functions](#key-classes--functions)

---

## 🎯 High-Level Overview

**InfraMind** is an AI-powered infrastructure debugging tool that analyzes logs, metrics, traces, and configuration files to identify root causes of incidents and generate actionable fix suggestions.

### Core Technology Stack
- **Frontend:** Streamlit (Python web framework)
- **Backend:** FastAPI (REST API)
- **AI Engine:** Google Gemini 2.0 Flash
- **Data Processing:** Pandas, custom parsers
- **Storage:** In-memory (demo), designed for database

### System Architecture (3-Layer)
```
┌────────────────────────────────────────────────────────┐
│                  PRESENTATION LAYER                     │
│              (Streamlit Web Interface)                  │
│  - File upload UI                                       │
│  - Results visualization                                │
│  - Incident history                                     │
└────────────────┬───────────────────────────────────────┘
                 │ HTTP REST API Calls
                 ↓
┌────────────────────────────────────────────────────────┐
│                   APPLICATION LAYER                     │
│                   (FastAPI Backend)                     │
│  - API endpoints                                        │
│  - Request validation                                   │
│  - Business logic orchestration                         │
└────────────────┬───────────────────────────────────────┘
                 │ Function Calls
                 ↓
┌────────────────────────────────────────────────────────┐
│                    PROCESSING LAYER                     │
│              (Parsers + Reasoning Engine)               │
│  - Data ingestion & parsing                             │
│  - Gemini AI integration                                │
│  - Root cause analysis                                  │
└────────────────────────────────────────────────────────┘
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                            USER INTERFACE                            │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              Streamlit Frontend (Port 8501)                 │   │
│  │                                                             │   │
│  │  Pages:                                                     │   │
│  │  • New Analysis      (file upload, configuration)          │   │
│  │  • Incident History  (past analyses)                       │   │
│  │  • Settings          (preferences)                         │   │
│  │                                                             │   │
│  │  Components:                                                │   │
│  │  • Multi-file uploader                                     │   │
│  │  • Sample data selector                                    │   │
│  │  • Results visualizer                                      │   │
│  │  • Causal chain display                                    │   │
│  │  • Fix suggestions cards                                   │   │
│  └────────────────────┬───────────────────────────────────────┘   │
│                       │                                             │
└───────────────────────┼─────────────────────────────────────────────┘
                        │
                        │ HTTP Requests (REST API)
                        │ POST /api/v1/incidents/analyze
                        │ GET  /api/v1/incidents/{id}
                        │ GET  /api/v1/health
                        ↓
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                          API LAYER (FastAPI)                         │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐   │
│  │              FastAPI Backend (Port 8000)                    │   │
│  │                                                             │   │
│  │  Routes:                                                    │   │
│  │  • /api/v1/health      → Health check                      │   │
│  │  • /api/v1/ready       → Readiness probe                   │   │
│  │  • /api/v1/live        → Liveness probe                    │   │
│  │  • /api/v1/incidents/analyze → Main analysis endpoint      │   │
│  │  • /api/v1/incidents/{id}    → Get incident details        │   │
│  │  • /api/v1/incidents   → List all incidents                │   │
│  │                                                             │   │
│  │  Middleware:                                                │   │
│  │  • CORS (cross-origin requests)                            │   │
│  │  • Request validation (Pydantic)                           │   │
│  │  • Error handling                                          │   │
│  └────────────────────┬───────────────────────────────────────┘   │
│                       │                                             │
└───────────────────────┼─────────────────────────────────────────────┘
                        │
                        │ Direct Function Calls
                        ↓
┌─────────────────────────────────────────────────────────────────────┐
│                                                                      │
│                       PROCESSING LAYER                               │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                    DATA INGESTION                            │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │ │
│  │  │  LogParser   │  │MetricsParser │  │ConfigParser  │     │ │
│  │  ├──────────────┤  ├──────────────┤  ├──────────────┤     │ │
│  │  │ • Parse JSON │  │• Parse JSON  │  │• Parse YAML  │     │ │
│  │  │ • Parse text │  │• Detect      │  │• Parse ENV   │     │ │
│  │  │ • Extract    │  │  anomalies   │  │• Compare     │     │ │
│  │  │   fields     │  │• Calculate   │  │  configs     │     │ │
│  │  │ • Filter by  │  │  stats       │  │• Find diffs  │     │ │
│  │  │   timestamp  │  │• Summarize   │  │              │     │ │
│  │  └──────────────┘  └──────────────┘  └──────────────┘     │ │
│  │                                                              │ │
│  │  ┌──────────────┐  ┌──────────────────────────────────┐   │ │
│  │  │TraceParser   │  │       DataUnifier                │   │ │
│  │  ├──────────────┤  ├──────────────────────────────────┤   │ │
│  │  │• Parse spans │  │• Combine all data sources        │   │ │
│  │  │• Build tree  │  │• Create UnifiedContext           │   │ │
│  │  │• Calculate   │  │• Apply time window filtering     │   │ │
│  │  │  latencies   │  │• Deduplicate events              │   │ │
│  │  │• Find errors │  │• Sort chronologically            │   │ │
│  │  └──────────────┘  └──────────────────────────────────┘   │ │
│  │                                                              │ │
│  └────────────────────────┬─────────────────────────────────────┘ │
│                           │                                        │
│                           │ Creates UnifiedContext                 │
│                           ↓                                        │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │                  REASONING ENGINE                            │ │
│  │                                                              │ │
│  │  ┌────────────────────────────────────────────────────┐    │ │
│  │  │           ReasoningEngine                          │    │ │
│  │  ├────────────────────────────────────────────────────┤    │ │
│  │  │ analyze_incident()                                 │    │ │
│  │  │   ↓                                                │    │ │
│  │  │   1. Generate prompts from context                │    │ │
│  │  │   2. Call Gemini API                              │    │ │
│  │  │   3. Parse AI response                            │    │ │
│  │  │   4. Validate results                             │    │ │
│  │  │   5. Build causal chain                           │    │ │
│  │  │   6. Generate fix suggestions                     │    │ │
│  │  │   7. Calculate confidence scores                  │    │ │
│  │  └────────────────────────────────────────────────────┘    │ │
│  │                           │                                  │ │
│  │                           │ Uses                             │ │
│  │                           ↓                                  │ │
│  │  ┌────────────────────────────────────────────────────┐    │ │
│  │  │             GeminiClient                           │    │ │
│  │  ├────────────────────────────────────────────────────┤    │ │
│  │  │ • API key management                               │    │ │
│  │  │ • Retry logic (3 attempts)                        │    │ │
│  │  │ • Rate limiting handling                          │    │ │
│  │  │ • Response formatting                             │    │ │
│  │  │ • Error handling                                  │    │ │
│  │  └────────────────────────────────────────────────────┘    │ │
│  │                           │                                  │ │
│  └───────────────────────────┼──────────────────────────────────┘ │
│                              │                                     │
└──────────────────────────────┼─────────────────────────────────────┘
                               │
                               │ API Calls
                               ↓
                     ┌──────────────────────┐
                     │   Google Gemini API  │
                     │   (Gemini 2.0 Flash) │
                     │                      │
                     │ • Reasoning          │
                     │ • Analysis           │
                     │ • Fix generation     │
                     └──────────────────────┘
```

---

## 🔄 Complete Data Flow

### Step-by-Step Journey of an Incident Analysis

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: User Interaction                                        │
└─────────────────────────────────────────────────────────────────┘

User opens Streamlit UI (http://localhost:8501)
   ↓
Uploads files OR selects sample data:
   • Logs:    3 files (api-gateway.log, order-service.log, payment-service.log)
   • Metrics: 2 files (system-metrics.json, application-metrics.json)
   • Traces:  1 file (traces.json)
   • Configs: 0 files (optional)
   ↓
Configures analysis:
   • Time window: 30 minutes
   • Focus area: "auto"
   • Include summary: Yes
   ↓
Clicks "Analyze Incident" button

┌─────────────────────────────────────────────────────────────────┐
│ STEP 2: Frontend Processing                                     │
└─────────────────────────────────────────────────────────────────┘

frontend/app.py → submit_analysis() function
   ↓
Reads file contents:
   • log_file.read().decode('utf-8')
   • OR loads from data/samples/ directory
   ↓
Constructs payload:
{
    "incident_id": "incident-20260205-143000",
    "log_files": [
        {"content": "...", "source": "api-gateway"},
        {"content": "...", "source": "order-service"},
        {"content": "...", "source": "payment-service"}
    ],
    "metric_files": [
        {"content": "{...}"},
        {"content": "{...}"}
    ],
    "trace_files": ["[{...}]"],
    "time_window_minutes": 30,
    "focus_area": null,
    "include_summary": true
}
   ↓
Makes HTTP POST request:
   URL: http://localhost:8000/api/v1/incidents/analyze
   Headers: {"Content-Type": "application/json"}
   Body: payload
   Timeout: 60 seconds

┌─────────────────────────────────────────────────────────────────┐
│ STEP 3: API Layer - Request Reception                          │
└─────────────────────────────────────────────────────────────────┘

FastAPI receives request at backend/api/routes/incident.py
   ↓
Middleware processes request:
   • CORS check (allow all origins in development)
   • Content-Type validation
   ↓
Pydantic validation:
   • Validates AnalyzeIncidentRequest schema
   • Checks required fields
   • Converts types
   ↓
Creates incident record in memory:
incidents_db[incident_id] = {
    "incident_id": incident_id,
    "status": "processing",
    "created_at": datetime.now(),
    "rca": None
}

┌─────────────────────────────────────────────────────────────────┐
│ STEP 4: Data Parsing - Logs                                    │
└─────────────────────────────────────────────────────────────────┘

backend/ingestion/log_parser.py → LogParser.parse_file()
   ↓
For each log file content:
   ↓
   Detect format (JSON or plain text)
   ↓
   IF JSON:
      • json.loads(content)
      • Extract fields: timestamp, level, message, service
   IF Text:
      • Parse with regex patterns
      • Extract timestamp, level, message
   ↓
   Create LogEntry objects:
   LogEntry(
       timestamp=datetime(...),
       level="ERROR",
       message="Database connection timeout",
       source="api-gateway",
       service="api-gateway",
       trace_id="abc123",
       metadata={...}
   )
   ↓
   Filter by time window (if specified)
   ↓
   Collect all LogEntry objects into list

Result: List[LogEntry] (77 logs from sample data)

┌─────────────────────────────────────────────────────────────────┐
│ STEP 5: Data Parsing - Metrics                                 │
└─────────────────────────────────────────────────────────────────┘

backend/ingestion/metrics_parser.py → MetricsParser.parse_file()
   ↓
For each metric file:
   ↓
   Parse JSON: json.loads(content)
   ↓
   Create Metric objects for each time series:
   Metric(
       timestamp=datetime(...),
       name="cpu_usage_percent",
       value=85.3,
       labels={"host": "web-1", "service": "api"},
       unit="percent"
   )
   ↓
   Calculate statistics:
      • Mean, median, std_dev
      • Min, max values
      • Anomaly detection (> mean + 2*std_dev)
   ↓
   Create MetricSummary objects:
   MetricSummary(
       metric_name="cpu_usage_percent",
       time_range=(start, end),
       avg_value=75.2,
       max_value=95.8,
       anomaly_detected=True,
       anomaly_threshold=85.0,
       data_points=[...]
   )

Result: List[MetricSummary] (11 metric summaries from sample data)

┌─────────────────────────────────────────────────────────────────┐
│ STEP 6: Data Parsing - Traces                                  │
└─────────────────────────────────────────────────────────────────┘

backend/ingestion/trace_parser.py → TraceParser.parse_file()
   ↓
Parse JSON trace data
   ↓
For each span in traces:
   ↓
   Create TraceSpan objects:
   TraceSpan(
       trace_id="abc123",
       span_id="span001",
       parent_span_id=None,
       service="api-gateway",
       operation="GET /orders",
       start_time=datetime(...),
       end_time=datetime(...),
       duration_ms=1523.5,
       status="error",
       error_message="Timeout connecting to database",
       tags={"http.method": "GET", ...}
   )
   ↓
   Build span hierarchy (parent-child relationships)
   ↓
   Calculate latencies
   ↓
   Identify error spans

Result: List[TraceSpan] (9 traces from sample data)

┌─────────────────────────────────────────────────────────────────┐
│ STEP 7: Data Parsing - Configs (if provided)                   │
└─────────────────────────────────────────────────────────────────┘

backend/ingestion/config_parser.py → ConfigParser.parse_file()
   ↓
If config files provided:
   ↓
   Detect format (YAML, ENV, auto)
   ↓
   Parse configuration:
      • YAML: yaml.safe_load()
      • ENV: Custom parser for KEY=VALUE
   ↓
   Compare with previous config (if provided):
      • Find added keys
      • Find removed keys
      • Find changed values
   ↓
   Create ConfigChange objects:
   ConfigChange(
       timestamp=datetime(...),
       file_path="database.yaml",
       key="connection_timeout",
       old_value="5s",
       new_value="30s",
       change_type="modified"
   )

Result: List[ConfigChange] (1 config change from sample data)

┌─────────────────────────────────────────────────────────────────┐
│ STEP 8: Data Unification                                       │
└─────────────────────────────────────────────────────────────────┘

backend/ingestion/data_unifier.py → DataUnifier.create_unified_context()
   ↓
Receives all parsed data:
   • logs: List[LogEntry]
   • metrics: List[MetricSummary]
   • traces: List[TraceSpan]
   • configs: List[ConfigChange]
   • deployments: List[DeploymentEvent]
   ↓
Apply time window filtering:
   • Calculate time_start = latest_timestamp - time_window_minutes
   • Filter all data to this window
   ↓
Deduplicate events (same timestamp, same content)
   ↓
Sort chronologically by timestamp
   ↓
Create UnifiedContext object:
UnifiedContext(
    incident_id="incident-20260205-143000",
    logs=[...],              # 77 logs
    metrics=[...],           # 11 metric summaries
    traces=[...],            # 9 traces
    config_changes=[...],    # 1 config change
    deployments=[...],       # 0 deployments
    time_window_start=datetime(...),
    time_window_end=datetime(...)
)

Result: UnifiedContext object with all correlated data

┌─────────────────────────────────────────────────────────────────┐
│ STEP 9: Reasoning Engine - Prompt Generation                   │
└─────────────────────────────────────────────────────────────────┘

backend/reasoning/reasoning_engine.py → ReasoningEngine.analyze_incident()
   ↓
Receives UnifiedContext
   ↓
backend/reasoning/prompts.py → PromptTemplates.get_analysis_prompt()
   ↓
Converts UnifiedContext to dictionary:
{
    "incident_id": "...",
    "logs": [{"timestamp": "...", "level": "ERROR", ...}, ...],
    "metrics": [{"metric_name": "cpu_usage", ...}, ...],
    "traces": [{"trace_id": "...", "duration_ms": 1523, ...}, ...],
    ...
}
   ↓
Generates structured prompt:

"""
You are an expert Site Reliability Engineer (SRE) analyzing an infrastructure incident.

## Incident Data

### Logs (77 entries):
2026-02-05 14:28:32 ERROR [api-gateway] Database connection timeout after 5000ms
2026-02-05 14:28:35 ERROR [order-service] Failed to fetch order #12345
...

### Metrics:
- cpu_usage_percent: avg=75.2%, max=95.8%, anomaly detected at 14:28
- memory_usage_bytes: avg=8.2GB, max=11.5GB
...

### Traces:
- Trace abc123: GET /orders -> 1523ms (TIMEOUT)
  - api-gateway -> order-service: 45ms
  - order-service -> database: TIMEOUT (5000ms)
...

### Configuration Changes:
- 14:25 - database.yaml: connection_timeout changed from 5s to 30s
...

## Your Task

Analyze this incident and provide:
1. Root cause identification
2. Affected services
3. Causal chain of events
4. Fix suggestions (prioritized)
5. Confidence score

Format your response as JSON...
"""

Result: Structured prompt string (~5,000-10,000 tokens)

┌─────────────────────────────────────────────────────────────────┐
│ STEP 10: Gemini API Call                                       │
└─────────────────────────────────────────────────────────────────┘

backend/reasoning/gemini_client.py → GeminiClient.generate_content()
   ↓
Prepares API request:
   • API key from settings
   • Model: "gemini-2.0-flash"
   • Temperature: 0.3 (low for consistency)
   • Max output tokens: 8192
   ↓
Makes API call with retry logic:
   @retry(stop_after_attempt=3, wait_exponential)
   ↓
   Attempt 1:
      client.models.generate_content(
          model="gemini-2.0-flash",
          contents=prompt,
          config={
              "temperature": 0.3,
              "max_output_tokens": 8192
          }
      )
   ↓
   IF API Error (quota, network, etc.):
      Wait 2 seconds
      Attempt 2 (same process)
   ↓
   IF Still failing:
      Wait 4 seconds
      Attempt 3 (final)
   ↓
   IF All attempts fail:
      Raise GeminiAPIError("Failed after 3 attempts")
   ↓
Receives response from Gemini:
{
    "text": "{...JSON response...}",
    "candidates": [...],
    "usage_metadata": {...}
}
   ↓
Extracts response.text
   ↓
Returns AI-generated JSON string

Result: JSON string with root cause analysis (~2,000-5,000 tokens)

┌─────────────────────────────────────────────────────────────────┐
│ STEP 11: Response Parsing & Validation                         │
└─────────────────────────────────────────────────────────────────┘

ReasoningEngine.analyze_incident() continues...
   ↓
Receives AI response (JSON string)
   ↓
Parse JSON:
   rca_dict = json.loads(response)
   ↓
Validate structure:
   • Has required fields? (root_cause_title, description, etc.)
   • Are confidence scores valid? (0-1 range)
   • Are fix suggestions present?
   • Is causal chain logical?
   ↓
Create RootCauseAnalysis object:
RootCauseAnalysis(
    incident_id="incident-20260205-143000",
    root_cause_title="Database Connection Pool Exhaustion",
    root_cause_description="The connection timeout configuration...",
    confidence_score=0.92,
    affected_services=["api-gateway", "order-service", "database"],
    causal_chain=[
        CausalLink(
            from_event="Config change: connection_timeout 5s->30s",
            to_event="Database connection timeout",
            relationship_type="caused_by",
            confidence=0.95,
            explanation="...",
            evidence=[...]
        ),
        ...
    ],
    fix_suggestions=[
        FixSuggestion(
            title="Revert connection timeout to 5 seconds",
            description="...",
            priority="critical",
            fix_type="configuration",
            estimated_time="5 minutes",
            risk_level="low",
            implementation_steps=[...]
        ),
        ...
    ],
    reasoning_steps=[...],
    severity="high",
    category="configuration",
    user_impact="high",
    business_impact="high"
)
   ↓
IF validate=True:
   • Validate confidence scores
   • Check logical consistency
   • Verify evidence exists
   ↓
Generate summary (if requested):
   summary = await engine.generate_summary(rca)

Result: Complete RootCauseAnalysis object + optional summary

┌─────────────────────────────────────────────────────────────────┐
│ STEP 12: API Response Construction                             │
└─────────────────────────────────────────────────────────────────┘

Back in backend/api/routes/incident.py
   ↓
Update incident record:
incidents_db[incident_id] = {
    "incident_id": incident_id,
    "status": "completed",
    "created_at": datetime(...),
    "completed_at": datetime.now(),
    "rca": rca.model_dump(),
    "error": None
}
   ↓
Create response:
AnalyzeIncidentResponse(
    incident_id=incident_id,
    status="completed",
    rca=rca,
    summary=summary
)
   ↓
Serialize to JSON:
{
    "incident_id": "incident-20260205-143000",
    "status": "completed",
    "rca": {
        "root_cause_title": "Database Connection Pool Exhaustion",
        "confidence_score": 0.92,
        ...
    },
    "summary": "The incident was caused by..."
}
   ↓
Return HTTP 200 with JSON body

┌─────────────────────────────────────────────────────────────────┐
│ STEP 13: Frontend - Results Display                            │
└─────────────────────────────────────────────────────────────────┘

frontend/app.py → submit_analysis() receives response
   ↓
IF response.status_code == 200:
   result = response.json()
   st.session_state.analysis_results = result
   st.session_state.incident_id = incident_id
   st.rerun()
   ↓
Page reloads, detects analysis_results in session_state
   ↓
render_analysis_results() function called
   ↓
Displays results in sections:

1. Executive Summary (if present)
   st.info(results["summary"])

2. Root Cause Title
   st.markdown(f"## {rca['root_cause_title']}")
   st.markdown(f"**Confidence:** {rca['confidence_score']:.1%}")

3. Root Cause Description
   st.write(rca['root_cause_description'])

4. Affected Services (grid)
   for service in rca['affected_services']:
       st.markdown(f'<div class="metric-card">{service}</div>')

5. Impact Assessment (4 metrics)
   st.metric("Severity", rca['severity'])
   st.metric("Category", rca['category'])
   st.metric("User Impact", rca['user_impact'])
   st.metric("Business Impact", rca['business_impact'])

6. Causal Chain (expandable)
   for link in rca['causal_chain']:
       with st.expander(f"{link['from_event']} → {link['to_event']}"):
           st.markdown(link['explanation'])
           for evidence in link['evidence']:
               st.markdown(f'<div class="evidence-item">{evidence}</div>')

7. Fix Suggestions (grouped by priority)
   if critical_fixes:
       st.markdown("#### Critical Priority")
       for fix in critical_fixes:
           render_fix_card(fix)  # Shows title, description, steps

8. Reasoning Steps (collapsible)
   with st.expander("Show Reasoning Steps"):
       for step in rca['reasoning_steps']:
           st.markdown(step['description'])

9. Action Buttons
   - Download Report (JSON)
   - New Analysis
   - View All Incidents

User sees complete analysis results with:
✅ Clear root cause explanation
✅ Visual confidence indicators
✅ Step-by-step causal chain
✅ Prioritized, actionable fixes
✅ AI reasoning transparency

┌─────────────────────────────────────────────────────────────────┐
│ COMPLETE! Total Time: 10-30 seconds                            │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🗂️ Code Organization

```
InfraMind/
│
├── frontend/                          # Presentation Layer
│   └── app.py                        # Streamlit UI (659 lines)
│       ├── render_header()           # App header with API status
│       ├── render_sidebar()          # Navigation menu
│       ├── render_new_analysis_page()# File upload & configuration
│       ├── submit_analysis()         # API call handler
│       ├── render_analysis_results() # Results visualization
│       ├── render_fix_card()         # Fix suggestion display
│       ├── render_history_page()     # Incident history
│       └── render_settings_page()    # Settings interface
│
├── backend/                           # Application Layer
│   │
│   ├── api/                          # REST API Layer
│   │   ├── main.py                   # FastAPI app initialization
│   │   │   ├── lifespan()           # Startup/shutdown logic
│   │   │   ├── app (FastAPI)        # Main app instance
│   │   │   └── CORS middleware      # Cross-origin support
│   │   │
│   │   └── routes/                   # API Endpoints
│   │       ├── health.py            # Health check endpoints
│   │       │   ├── /health          # Full health check
│   │       │   ├── /ready           # Readiness probe
│   │       │   └── /live            # Liveness probe
│   │       │
│   │       └── incident.py          # Incident analysis endpoints
│   │           ├── POST /analyze    # Main analysis endpoint
│   │           ├── GET /{id}        # Get incident by ID
│   │           ├── GET /            # List all incidents
│   │           ├── POST /analyze-files # File upload endpoint
│   │           └── DELETE /{id}     # Delete incident
│   │
│   ├── ingestion/                    # Data Processing Layer
│   │   ├── log_parser.py            # Log file parsing (300 lines)
│   │   │   ├── parse_file()        # Main parsing function
│   │   │   ├── _parse_json_log()   # JSON log handler
│   │   │   ├── _parse_text_log()   # Plain text handler
│   │   │   └── _parse_timestamp()  # Timestamp extraction
│   │   │
│   │   ├── metrics_parser.py        # Metrics parsing (250 lines)
│   │   │   ├── parse_file()        # Parse metrics JSON
│   │   │   ├── create_summaries()  # Generate statistics
│   │   │   ├── _detect_anomalies() # Anomaly detection
│   │   │   └── _calculate_stats()  # Statistical analysis
│   │   │
│   │   ├── config_parser.py         # Config parsing (200 lines)
│   │   │   ├── parse_file()        # Parse config files
│   │   │   ├── compare_configs()   # Diff two configs
│   │   │   ├── _parse_yaml()       # YAML handler
│   │   │   └── _parse_env()        # ENV handler
│   │   │
│   │   ├── trace_parser.py          # Trace parsing (300 lines)
│   │   │   ├── parse_file()        # Parse trace JSON
│   │   │   ├── _build_span_tree()  # Build hierarchy
│   │   │   ├── _calculate_latency()# Latency calculation
│   │   │   └── _find_errors()      # Error detection
│   │   │
│   │   └── data_unifier.py          # Data combination (230 lines)
│   │       ├── create_unified_context() # Combine all sources
│   │       ├── _filter_by_time()   # Time window filtering
│   │       ├── _deduplicate()      # Remove duplicates
│   │       └── _sort_chronologically() # Sort by time
│   │
│   ├── reasoning/                    # AI Reasoning Layer
│   │   ├── gemini_client.py         # Gemini API wrapper (153 lines)
│   │   │   ├── __init__()          # Client initialization
│   │   │   ├── generate_content()  # Main API call (with retry)
│   │   │   └── _handle_error()     # Error handling
│   │   │
│   │   ├── prompts.py               # Prompt templates (300+ lines)
│   │   │   ├── get_analysis_prompt() # Main analysis prompt
│   │   │   ├── get_summary_prompt()  # Summary generation
│   │   │   ├── get_validation_prompt() # Validation prompt
│   │   │   └── _format_context()   # Context formatting
│   │   │
│   │   └── reasoning_engine.py      # RCA engine (320+ lines)
│   │       ├── analyze_incident()  # Main analysis function
│   │       ├── generate_summary()  # Summary generation
│   │       ├── explain_reasoning() # Explain AI logic
│   │       ├── validate_analysis() # Validate results
│   │       └── _parse_response()   # Parse Gemini response
│   │
│   ├── models/                       # Data Models
│   │   ├── incident.py              # Incident data models
│   │   │   ├── LogEntry            # Single log entry
│   │   │   ├── MetricSummary       # Metric statistics
│   │   │   ├── TraceSpan           # Distributed trace span
│   │   │   ├── ConfigChange        # Configuration change
│   │   │   ├── DeploymentEvent     # Deployment event
│   │   │   └── UnifiedContext      # Combined context
│   │   │
│   │   ├── rca.py                   # RCA data models
│   │   │   ├── RootCauseAnalysis   # Main RCA result
│   │   │   ├── CausalLink          # Chain link
│   │   │   ├── Evidence            # Supporting evidence
│   │   │   ├── FixSuggestion       # Fix recommendation
│   │   │   └── ReasoningStep       # AI reasoning step
│   │   │
│   │   └── schemas.py               # API schemas
│   │       ├── AnalyzeIncidentRequest  # Request model
│   │       ├── AnalyzeIncidentResponse # Response model
│   │       ├── HealthCheckResponse     # Health check model
│   │       ├── LogFileData            # Log file input
│   │       ├── MetricFileData         # Metric file input
│   │       └── ConfigFileData         # Config file input
│   │
│   ├── core/                         # Core Utilities
│   │   ├── config.py                # Settings management
│   │   │   ├── Settings            # Pydantic settings class
│   │   │   └── get_settings()      # Settings singleton
│   │   │
│   │   └── exceptions.py            # Custom exceptions
│   │       ├── InfraMindError      # Base exception
│   │       ├── GeminiAPIError      # Gemini-specific
│   │       ├── ParsingError        # Data parsing
│   │       ├── ValidationError     # Data validation
│   │       └── ConfigurationError  # Config issues
│   │
│   └── utils/                        # Utility Functions
│       └── (future utilities)
│
├── data/                             # Sample Data
│   └── samples/                     # Demo scenario data
│       ├── logs/                    # Log files
│       │   ├── api-gateway.log     # 25 logs
│       │   ├── order-service.log   # 30 logs
│       │   └── payment-service.log # 22 logs
│       ├── metrics/                 # Metrics files
│       │   ├── system-metrics.json # CPU, memory, disk
│       │   └── application-metrics.json # Latency, errors
│       ├── traces/                  # Trace files
│       │   └── traces.json         # 9 distributed traces
│       ├── configs/                 # Config files
│       │   └── database.yaml       # Database config
│       └── deployments/             # Deployment events
│           └── deployments.json    # Deployment history
│
├── scripts/                          # Utility Scripts
│   ├── start_api.py                 # Start FastAPI server
│   ├── start_frontend.py            # Start Streamlit UI
│   ├── start_all.py                 # Start both servers
│   ├── test_phase2.py               # Test data ingestion
│   ├── test_phase3.py               # Test reasoning engine
│   ├── test_phase4.py               # Test API endpoints
│   └── test_phase5.py               # Test frontend
│
├── .streamlit/                       # Streamlit Config
│   └── config.toml                  # UI settings
│
├── .env                              # Environment Variables
│   ├── GEMINI_API_KEY              # API key
│   ├── GEMINI_MODEL                # Model name
│   └── (other settings)
│
├── requirements.txt                  # Python Dependencies
├── .gitignore                       # Git ignore rules
├── README.md                        # Project documentation
├── prd.md                           # Product requirements
├── hackathon_details.md             # Hackathon info
├── TODO.md                          # Task list
├── PIPELINE_EXPLANATION.md          # This file
│
└── PHASE*_STATUS.md                 # Phase documentation
    ├── PHASE1_STATUS.md
    ├── PHASE2_STATUS.md
    ├── PHASE3_STATUS.md
    ├── PHASE4_STATUS.md
    └── PHASE5_STATUS.md
```

---

## 🔑 Key Classes & Functions

### Frontend (Streamlit)

**File:** `frontend/app.py`

```python
# Main application entry
def main():
    """Initialize and run Streamlit app"""
    
# Page rendering
def render_new_analysis_page():
    """Render incident submission form"""
    
def render_analysis_results():
    """Display RCA results with visualizations"""
    
def render_history_page():
    """Show past incident analyses"""

# API interaction
def submit_analysis(...) -> dict:
    """Send analysis request to API"""
    # Makes POST to /api/v1/incidents/analyze
    # Returns: {"incident_id": "...", "rca": {...}, "summary": "..."}

# Session state
st.session_state.analysis_results  # Stores current results
st.session_state.incident_id       # Current incident ID
```

### Backend API (FastAPI)

**File:** `backend/api/main.py`

```python
# Application instance
app = FastAPI(
    title="InfraMind API",
    lifespan=lifespan,
    docs_url="/docs"
)

# Lifespan manager
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic"""
```

**File:** `backend/api/routes/incident.py`

```python
@router.post("/incidents/analyze")
async def analyze_incident(request: AnalyzeIncidentRequest):
    """Main RCA endpoint"""
    # 1. Parse all data sources
    # 2. Create unified context
    # 3. Call reasoning engine
    # 4. Return RCA results
    
@router.get("/incidents/{incident_id}")
async def get_incident(incident_id: str):
    """Retrieve incident by ID"""
    
@router.get("/incidents")
async def list_incidents(skip: int = 0, limit: int = 100):
    """List all incidents with pagination"""
```

### Data Ingestion

**File:** `backend/ingestion/log_parser.py`

```python
class LogParser:
    def parse_file(content: str, source: str) -> List[LogEntry]:
        """Parse log file content"""
        # Detects JSON or text format
        # Returns list of LogEntry objects
        
    def _parse_json_log(content: str) -> List[LogEntry]:
        """Parse JSON-formatted logs"""
        
    def _parse_text_log(content: str) -> List[LogEntry]:
        """Parse plain text logs with regex"""
```

**File:** `backend/ingestion/metrics_parser.py`

```python
class MetricsParser:
    def parse_file(content: str) -> List[Metric]:
        """Parse metrics JSON"""
        
    def create_summaries(metrics: List[Metric]) -> List[MetricSummary]:
        """Generate statistical summaries"""
        # Calculates mean, median, std_dev
        # Detects anomalies
        # Returns metric summaries
```

**File:** `backend/ingestion/data_unifier.py`

```python
class DataUnifier:
    def create_unified_context(
        logs: List[LogEntry],
        metrics: List[MetricSummary],
        traces: List[TraceSpan],
        configs: List[ConfigChange],
        deployments: List[DeploymentEvent],
        time_window_minutes: Optional[int]
    ) -> UnifiedContext:
        """Combine all data sources into single context"""
        # Filters by time window
        # Deduplicates events
        # Sorts chronologically
        # Returns unified view
```

### Reasoning Engine

**File:** `backend/reasoning/gemini_client.py`

```python
class GeminiClient:
    def __init__(api_key: str):
        """Initialize Gemini API client"""
        self.client = genai.Client(api_key=api_key)
        
    @retry(stop_after_attempt=3, wait_exponential)
    async def generate_content(
        prompt: str,
        temperature: float = 0.7,
        max_output_tokens: int = None
    ) -> str:
        """Call Gemini API with retry logic"""
        # Makes API call
        # Handles rate limiting
        # Returns generated text
```

**File:** `backend/reasoning/prompts.py`

```python
class PromptTemplates:
    @staticmethod
    def get_analysis_prompt(context: dict, focus_area: str) -> str:
        """Generate root cause analysis prompt"""
        # Formats context data
        # Adds SRE instructions
        # Returns structured prompt
        
    @staticmethod
    def get_summary_prompt(rca: dict) -> str:
        """Generate executive summary prompt"""
```

**File:** `backend/reasoning/reasoning_engine.py`

```python
class ReasoningEngine:
    async def analyze_incident(
        context: UnifiedContext,
        focus_area: Optional[str] = None,
        validate: bool = True
    ) -> RootCauseAnalysis:
        """Perform complete root cause analysis"""
        # 1. Generate prompts
        # 2. Call Gemini API
        # 3. Parse AI response
        # 4. Validate results
        # 5. Build causal chain
        # 6. Generate fix suggestions
        # Returns: RootCauseAnalysis object
        
    async def generate_summary(rca: RootCauseAnalysis) -> str:
        """Generate executive summary of RCA"""
```

### Data Models

**File:** `backend/models/incident.py`

```python
class LogEntry(BaseModel):
    """Single log entry"""
    timestamp: datetime
    level: str
    message: str
    source: str
    service: Optional[str]
    trace_id: Optional[str]
    metadata: Dict[str, Any]

class MetricSummary(BaseModel):
    """Aggregated metric statistics"""
    metric_name: str
    time_range: Tuple[datetime, datetime]
    avg_value: float
    max_value: float
    anomaly_detected: bool
    data_points: List[Metric]

class UnifiedContext(BaseModel):
    """Combined view of all incident data"""
    incident_id: str
    logs: List[LogEntry]
    metrics: List[MetricSummary]
    traces: List[TraceSpan]
    config_changes: List[ConfigChange]
    deployments: List[DeploymentEvent]
    time_window_start: Optional[datetime]
    time_window_end: Optional[datetime]
```

**File:** `backend/models/rca.py`

```python
class RootCauseAnalysis(BaseModel):
    """Complete root cause analysis result"""
    incident_id: str
    root_cause_title: str
    root_cause_description: str
    confidence_score: float
    affected_services: List[str]
    causal_chain: List[CausalLink]
    fix_suggestions: List[FixSuggestion]
    reasoning_steps: List[ReasoningStep]
    severity: str
    category: str
    user_impact: str
    business_impact: str

class CausalLink(BaseModel):
    """Link in the causal chain"""
    from_event: str
    to_event: str
    relationship_type: str
    confidence: float
    explanation: str
    evidence: List[str]

class FixSuggestion(BaseModel):
    """Actionable fix recommendation"""
    title: str
    description: str
    priority: str  # critical, high, medium, low
    fix_type: str
    estimated_time: str
    risk_level: str
    implementation_steps: List[str]
```

---

## 🎯 Summary

InfraMind follows a clean **3-layer architecture**:

1. **Presentation Layer** (Streamlit) - User interface
2. **Application Layer** (FastAPI) - Business logic & API
3. **Processing Layer** (Parsers + Reasoning Engine) - Data processing & AI

**Data flows** through the system in this sequence:
```
User Upload → Frontend → API → Parsers → DataUnifier → 
ReasoningEngine → Gemini AI → RCA Results → API → Frontend → User
```

**Key strengths:**
- ✅ Clean separation of concerns
- ✅ Modular, testable components
- ✅ Type-safe with Pydantic models
- ✅ Comprehensive error handling
- ✅ Well-documented code
- ✅ Production-ready architecture

This architecture makes InfraMind:
- **Scalable**: Easy to add new data sources
- **Maintainable**: Clear component boundaries
- **Testable**: Each layer can be tested independently
- **Extensible**: New features slot in cleanly

---

*This pipeline explanation is current as of February 5, 2026*
