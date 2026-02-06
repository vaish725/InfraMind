# 🧪 InfraMind - Complete Testing Guide

**Date:** February 5, 2026  
**Version:** 1.0  

---

## 📋 Table of Contents

1. [Quick Start - Test Everything Now](#quick-start---test-everything-now)
2. [Testing Each Phase](#testing-each-phase)
3. [Manual Testing Workflows](#manual-testing-workflows)
4. [Automated Test Scripts](#automated-test-scripts)
5. [Sample Data Testing](#sample-data-testing)
6. [API Testing](#api-testing)
7. [Frontend Testing](#frontend-testing)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start - Test Everything Now

### Option 1: Run All Tests (Recommended)

```bash
# From project root
cd /Users/vaishnavikamdi/Documents/InfraMind

# Activate virtual environment
source venv/bin/activate

# Run all phase tests in sequence
python scripts/test_phase2.py  # Data ingestion
python scripts/test_phase3.py  # Reasoning engine
python scripts/test_phase4.py  # API endpoints
python scripts/test_phase5.py  # Frontend validation
```

### Option 2: Full System Test (End-to-End)

```bash
# Terminal 1: Start API
source venv/bin/activate
python scripts/start_api.py

# Terminal 2: Start Frontend
source venv/bin/activate
python scripts/start_frontend.py

# Browser: Open http://localhost:8501
# Upload sample data and run analysis
```

### Option 3: One-Command Quick Test

```bash
# Run everything with single command
source venv/bin/activate && \
python scripts/test_phase2.py && \
python scripts/test_phase3.py && \
python scripts/test_phase4.py && \
python scripts/test_phase5.py && \
echo "✅ All tests passed!"
```

---

## 🧪 Testing Each Phase

### Phase 1: Foundation & Setup

**What to Test:**
- ✅ Gemini API client connection
- ✅ Configuration loading
- ✅ Data models validation

**Manual Test:**

```bash
source venv/bin/activate

# Test Gemini client
python -c "
from backend.reasoning.gemini_client import GeminiClient
from backend.core.config import get_settings

settings = get_settings()
client = GeminiClient()
result = client.generate_content('Say hello!')
print(f'✅ Gemini client working: {result[:50]}...')
"

# Test config loading
python -c "
from backend.core.config import get_settings

settings = get_settings()
print(f'✅ API Key loaded: {settings.GEMINI_API_KEY[:10]}...')
print(f'✅ Model: {settings.GEMINI_MODEL}')
"

# Test data models
python -c "
from backend.models.incident import LogEntry, UnifiedContext
from datetime import datetime

log = LogEntry(
    timestamp=datetime.now(),
    level='INFO',
    message='Test log',
    source='test',
    metadata={}
)
print(f'✅ Models working: {log.level}')
"
```

**Expected Output:**
```
✅ Gemini client working: Hello! How can I help you today?...
✅ API Key loaded: AIzaSyDklq...
✅ Model: gemini-2.0-flash
✅ Models working: INFO
```

---

### Phase 2: Data Ingestion

**What to Test:**
- ✅ Log parsing (JSON & text)
- ✅ Metrics parsing & anomaly detection
- ✅ Trace parsing & span hierarchy
- ✅ Config parsing & diff detection
- ✅ Data unification

**Automated Test:**

```bash
source venv/bin/activate
python scripts/test_phase2.py
```

**Expected Output:**
```
=== Phase 2: Data Ingestion Test ===

Testing Log Parser...
✅ Successfully parsed 77 logs
✅ Found 15 ERROR logs
✅ Found 2 CRITICAL logs
✅ Logs properly sorted by timestamp

Testing Metrics Parser...
✅ Successfully parsed 11 metric summaries
✅ Found 3 metrics with anomalies
✅ Metrics: cpu_usage_percent, memory_usage_bytes, disk_io_ops...

Testing Trace Parser...
✅ Successfully parsed 9 trace spans
✅ Found 3 error spans
✅ Max latency: 1523.5ms

Testing Config Parser...
✅ Successfully parsed config changes
✅ Found 1 configuration change
✅ Changed keys: connection_timeout

Testing Data Unifier...
✅ Successfully created unified context
✅ Total logs: 77
✅ Total metrics: 11
✅ Total traces: 9
✅ Total config changes: 1

=== All Phase 2 Tests Passed! ===
```

**Manual Test (Individual Parsers):**

```bash
# Test log parser only
python -c "
from backend.ingestion.log_parser import LogParser
from pathlib import Path

log_path = Path('data/samples/logs/api-gateway.log')
content = log_path.read_text()
logs = LogParser.parse_file(content, 'api-gateway')
print(f'✅ Parsed {len(logs)} logs')
for log in logs[:3]:
    print(f'  - {log.timestamp} [{log.level}] {log.message[:50]}...')
"

# Test metrics parser only
python -c "
from backend.ingestion.metrics_parser import MetricsParser
from pathlib import Path
import json

metrics_path = Path('data/samples/metrics/system-metrics.json')
content = metrics_path.read_text()
metrics = MetricsParser.parse_file(content)
summaries = MetricsParser.create_summaries(metrics)
print(f'✅ Created {len(summaries)} metric summaries')
for summary in summaries[:3]:
    print(f'  - {summary.metric_name}: avg={summary.avg_value:.2f}, anomaly={summary.anomaly_detected}')
"
```

---

### Phase 3: Reasoning Engine

**What to Test:**
- ✅ Prompt generation
- ✅ Gemini API integration
- ✅ RCA generation
- ✅ Fix suggestion creation
- ✅ Causal chain building

**Automated Test:**

```bash
source venv/bin/activate
python scripts/test_phase3.py
```

**Expected Output:**
```
=== Phase 3: Reasoning Engine Test ===

Testing Prompt Generation...
✅ Generated analysis prompt (8,234 tokens)
✅ Prompt includes all data sources
✅ Prompt has structured format

Testing Reasoning Engine...
✅ Successfully analyzed incident
✅ Root cause: Database Connection Pool Exhaustion
✅ Confidence: 92.0%
✅ Affected services: 3
✅ Causal chain: 4 links
✅ Fix suggestions: 5 fixes (2 critical, 2 high, 1 medium)

Testing AI Response Validation...
✅ Confidence score valid: 0.92
✅ All required fields present
✅ Fix suggestions properly prioritized
✅ Evidence provided for causal links

=== All Phase 3 Tests Passed! ===
```

**Manual Test (Quick RCA):**

```bash
# Quick RCA test with sample data
python -c "
import asyncio
from backend.reasoning.reasoning_engine import ReasoningEngine
from backend.ingestion.log_parser import LogParser
from backend.ingestion.data_unifier import DataUnifier
from pathlib import Path

async def test():
    # Parse sample logs
    log_path = Path('data/samples/logs/api-gateway.log')
    content = log_path.read_text()
    logs = LogParser.parse_file(content, 'api-gateway')
    
    # Create context
    context = DataUnifier.create_unified_context(
        logs=logs,
        metrics=[],
        traces=[],
        config_changes=[],
        deployments=[]
    )
    
    # Run RCA
    engine = ReasoningEngine()
    rca = await engine.analyze_incident(context)
    
    print(f'✅ RCA completed!')
    print(f'Root Cause: {rca.root_cause_title}')
    print(f'Confidence: {rca.confidence_score:.1%}')
    print(f'Fixes: {len(rca.fix_suggestions)}')

asyncio.run(test())
"
```

---

### Phase 4: FastAPI Backend

**What to Test:**
- ✅ API server startup
- ✅ Health check endpoints
- ✅ Incident analysis endpoint
- ✅ Incident retrieval endpoints
- ✅ Error handling
- ✅ CORS configuration

**Automated Test:**

```bash
source venv/bin/activate
python scripts/test_phase4.py
```

**Expected Output:**
```
=== Phase 4: API Backend Test ===

Testing API Server...
✅ API server is running on http://localhost:8000

Testing Health Endpoints...
✅ GET /api/v1/health - Status: 200
   Response: {"status": "healthy", "gemini_configured": true}
✅ GET /api/v1/ready - Status: 200
✅ GET /api/v1/live - Status: 200

Testing Incident Analysis Endpoint...
✅ POST /api/v1/incidents/analyze - Status: 200
   Incident ID: incident-20260205-150430
   Status: completed
   Root Cause: Database Connection Pool Exhaustion
   Confidence: 92.0%

Testing Incident Retrieval...
✅ GET /api/v1/incidents/{id} - Status: 200
✅ Incident data matches
✅ RCA data present

Testing Incident List...
✅ GET /api/v1/incidents - Status: 200
✅ Found 1 incidents

=== All Phase 4 Tests Passed! ===
```

**Manual Test (API Endpoints):**

```bash
# Start API first (in separate terminal)
source venv/bin/activate
python scripts/start_api.py

# Then test endpoints (in another terminal)

# Test health check
curl -X GET http://localhost:8000/api/v1/health | jq

# Test analysis endpoint
curl -X POST http://localhost:8000/api/v1/incidents/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "incident_id": "test-incident-001",
    "log_files": [
      {
        "content": "2026-02-05 10:00:00 ERROR Database connection timeout",
        "source": "test-service"
      }
    ],
    "metric_files": [],
    "trace_files": [],
    "time_window_minutes": 30
  }' | jq

# Test incident retrieval
curl -X GET http://localhost:8000/api/v1/incidents/test-incident-001 | jq

# Test API docs (open in browser)
open http://localhost:8000/docs
```

---

### Phase 5: Streamlit Frontend

**What to Test:**
- ✅ Frontend server startup
- ✅ API connectivity
- ✅ File upload functionality
- ✅ Sample data loading
- ✅ Results visualization
- ✅ Multi-page navigation

**Automated Test:**

```bash
source venv/bin/activate
python scripts/test_phase5.py
```

**Expected Output:**
```
=== Phase 5: Frontend Validation Test ===

Testing API Availability...
✅ API is running on http://localhost:8000
✅ API health check passed

Testing Frontend Files...
✅ Frontend app exists: frontend/app.py
✅ Streamlit config exists: .streamlit/config.toml
✅ Frontend launcher exists: scripts/start_frontend.py

Testing Sample Data...
✅ Sample logs directory exists (3 files)
✅ Sample metrics directory exists (2 files)
✅ Sample traces directory exists (1 file)
✅ Sample configs directory exists (1 file)

Testing API Endpoints...
✅ POST /api/v1/incidents/analyze works
✅ GET /api/v1/incidents/{id} works
✅ Analysis returns valid RCA

=== All Phase 5 Tests Passed! ===

🚀 To test the UI manually:
   1. Run: python scripts/start_all.py
   2. Open: http://localhost:8501
   3. Upload files or use sample data
   4. Click "Analyze Incident"
```

**Manual Test (Frontend UI):**

```bash
# Start both servers
source venv/bin/activate
python scripts/start_all.py

# This will open:
# - API: http://localhost:8000
# - Frontend: http://localhost:8501

# Then test in browser:
# 1. Navigate to http://localhost:8501
# 2. Go to "New Analysis" page
# 3. Click "Use Sample Data"
# 4. Click "Analyze Incident"
# 5. Wait for results
# 6. Check results display
# 7. Test "Incident History" page
# 8. Test "Settings" page
```

---

## 🔄 Manual Testing Workflows

### Workflow 1: Complete End-to-End Test

**Objective:** Test entire system from file upload to results display

**Steps:**

1. **Start Servers**
   ```bash
   source venv/bin/activate
   python scripts/start_all.py
   ```

2. **Open Frontend**
   - Browser: http://localhost:8501
   - Should see InfraMind header
   - Should see "API: Connected" in green

3. **Upload Custom Files**
   - Click "Logs" tab
   - Upload a log file (try `data/samples/logs/api-gateway.log`)
   - Click "Metrics" tab
   - Upload a metrics file
   - Click "Traces" tab
   - Upload a traces file

4. **Configure Analysis**
   - Set time window: 30 minutes
   - Set focus area: "auto"
   - Enable "Include executive summary"

5. **Run Analysis**
   - Click "Analyze Incident"
   - Should see "[PROCESSING] Analyzing incident..."
   - Wait 10-30 seconds

6. **Verify Results**
   - ✅ Executive summary displayed
   - ✅ Root cause title shown
   - ✅ Confidence score displayed (as percentage)
   - ✅ Affected services listed
   - ✅ Causal chain expandable
   - ✅ Fix suggestions grouped by priority
   - ✅ No emojis anywhere in UI

7. **Test History**
   - Navigate to "Incident History"
   - Should see your incident listed
   - Click to view details

8. **Download Report**
   - Click "Download Report (JSON)"
   - Should download JSON file
   - Verify contents

**Expected Time:** 2-3 minutes

---

### Workflow 2: Sample Data Quick Test

**Objective:** Fastest way to test complete system

**Steps:**

1. **Start Servers**
   ```bash
   source venv/bin/activate
   python scripts/start_all.py
   ```

2. **Use Sample Data**
   - Open http://localhost:8501
   - Click "Use Sample Data" button
   - All tabs should populate automatically
   - Should see file counts update

3. **Analyze**
   - Click "Analyze Incident"
   - Results should appear in ~15 seconds

4. **Verify Known Results**
   - Root cause: "Database Connection Pool Exhaustion"
   - Confidence: ~92%
   - Affected services: api-gateway, order-service, database
   - Critical fixes: 2
   - High priority fixes: 2

**Expected Time:** 30 seconds

---

### Workflow 3: API-Only Test (No Frontend)

**Objective:** Test backend API independently

**Steps:**

1. **Start API Only**
   ```bash
   source venv/bin/activate
   python scripts/start_api.py
   ```

2. **Test Health**
   ```bash
   curl http://localhost:8000/api/v1/health
   # Should return: {"status": "healthy", "gemini_configured": true}
   ```

3. **Test Analysis**
   ```bash
   # Prepare test data
   LOG_CONTENT=$(cat data/samples/logs/api-gateway.log)
   
   # Send analysis request
   curl -X POST http://localhost:8000/api/v1/incidents/analyze \
     -H "Content-Type: application/json" \
     -d "{
       \"incident_id\": \"curl-test-001\",
       \"log_files\": [{\"content\": \"$LOG_CONTENT\", \"source\": \"api-gateway\"}],
       \"metric_files\": [],
       \"trace_files\": [],
       \"time_window_minutes\": 30
     }" | jq
   ```

4. **Verify Response**
   - Status: 200
   - Has incident_id
   - Has rca object
   - RCA has root_cause_title, confidence_score, etc.

**Expected Time:** 1 minute

---

## 🎯 Sample Data Testing

### Available Sample Data

**Location:** `data/samples/`

**Files:**
- **Logs** (3 files, 77 total entries)
  - `api-gateway.log` - 25 logs
  - `order-service.log` - 30 logs
  - `payment-service.log` - 22 logs

- **Metrics** (2 files, 11 summaries)
  - `system-metrics.json` - CPU, memory, disk
  - `application-metrics.json` - Latency, error rate

- **Traces** (1 file, 9 spans)
  - `traces.json` - Distributed traces

- **Configs** (1 file, 1 change)
  - `database.yaml` - Database configuration

**Scenario:** Database connection pool exhaustion after config change

### Test with Sample Data

```bash
# Quick sample data test
python -c "
import asyncio
from backend.ingestion.log_parser import LogParser
from backend.ingestion.metrics_parser import MetricsParser
from backend.ingestion.trace_parser import TraceParser
from backend.ingestion.config_parser import ConfigParser
from backend.ingestion.data_unifier import DataUnifier
from backend.reasoning.reasoning_engine import ReasoningEngine
from pathlib import Path
import json

async def test_sample_data():
    # Parse all sample data
    log_files = list(Path('data/samples/logs').glob('*.log'))
    logs = []
    for log_file in log_files:
        content = log_file.read_text()
        logs.extend(LogParser.parse_file(content, log_file.stem))
    
    metrics_files = list(Path('data/samples/metrics').glob('*.json'))
    metrics = []
    for metrics_file in metrics_files:
        content = metrics_file.read_text()
        metrics.extend(MetricsParser.parse_file(content))
    
    trace_file = Path('data/samples/traces/traces.json')
    traces = TraceParser.parse_file(trace_file.read_text())
    
    config_file = Path('data/samples/configs/database.yaml')
    old_config = {'connection_timeout': '5s'}
    new_config = {'connection_timeout': '30s'}
    config_changes = ConfigParser.compare_configs(
        old_config, new_config, str(config_file)
    )
    
    # Create unified context
    context = DataUnifier.create_unified_context(
        logs=logs,
        metrics=MetricsParser.create_summaries(metrics),
        traces=traces,
        config_changes=config_changes,
        deployments=[]
    )
    
    print(f'✅ Loaded sample data:')
    print(f'   - Logs: {len(context.logs)}')
    print(f'   - Metrics: {len(context.metrics)}')
    print(f'   - Traces: {len(context.traces)}')
    print(f'   - Config changes: {len(context.config_changes)}')
    
    # Run analysis
    engine = ReasoningEngine()
    rca = await engine.analyze_incident(context)
    
    print(f'\\n✅ Analysis complete:')
    print(f'   - Root cause: {rca.root_cause_title}')
    print(f'   - Confidence: {rca.confidence_score:.1%}')
    print(f'   - Affected services: {len(rca.affected_services)}')
    print(f'   - Fix suggestions: {len(rca.fix_suggestions)}')

asyncio.run(test_sample_data())
"
```

---

## 📊 API Testing (Advanced)

### Using Postman/Insomnia

1. **Import Collection** (create these requests)

**GET Health Check**
```
GET http://localhost:8000/api/v1/health
```

**POST Analyze Incident**
```
POST http://localhost:8000/api/v1/incidents/analyze
Content-Type: application/json

{
  "incident_id": "postman-test-001",
  "log_files": [
    {
      "content": "2026-02-05 10:00:00 ERROR Database connection timeout",
      "source": "api-gateway"
    }
  ],
  "metric_files": [],
  "trace_files": [],
  "time_window_minutes": 30,
  "focus_area": null,
  "include_summary": true
}
```

**GET Incident Details**
```
GET http://localhost:8000/api/v1/incidents/postman-test-001
```

**GET List Incidents**
```
GET http://localhost:8000/api/v1/incidents?skip=0&limit=100
```

### Using Python Requests

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# Test health
response = requests.get(f"{BASE_URL}/health")
print(f"Health: {response.json()}")

# Test analysis
payload = {
    "incident_id": "python-test-001",
    "log_files": [
        {
            "content": "2026-02-05 10:00:00 ERROR Database timeout",
            "source": "test"
        }
    ],
    "metric_files": [],
    "trace_files": [],
    "time_window_minutes": 30
}

response = requests.post(f"{BASE_URL}/incidents/analyze", json=payload)
print(f"Analysis: {response.status_code}")
print(f"Result: {json.dumps(response.json(), indent=2)}")
```

---

## 🐛 Troubleshooting

### Issue: "API Not Running"

**Symptoms:**
```
❌ API health check failed
Connection refused on http://localhost:8000
```

**Solution:**
```bash
# Start API
source venv/bin/activate
python scripts/start_api.py

# Check if running
curl http://localhost:8000/api/v1/health
```

---

### Issue: "Gemini API Error"

**Symptoms:**
```
❌ GeminiAPIError: API key not configured
❌ 429 Resource Exhausted (quota exceeded)
```

**Solution:**
```bash
# Check API key
cat .env | grep GEMINI_API_KEY

# If missing, add it
echo "GEMINI_API_KEY=your-key-here" >> .env

# If quota exceeded, wait or upgrade
# Free tier: 1,500 requests/day
# Check usage: https://ai.google.dev/
```

---

### Issue: "Module Not Found"

**Symptoms:**
```
ModuleNotFoundError: No module named 'backend'
```

**Solution:**
```bash
# Make sure you're in project root
cd /Users/vaishnavikamdi/Documents/InfraMind

# Activate virtual environment
source venv/bin/activate

# Verify packages installed
pip list | grep -E "(streamlit|fastapi|google-genai)"
```

---

### Issue: "Frontend Won't Start"

**Symptoms:**
```
streamlit: command not found
Port 8501 already in use
```

**Solution:**
```bash
# Install Streamlit
pip install streamlit

# Kill existing process
lsof -ti:8501 | xargs kill -9

# Start again
python scripts/start_frontend.py
```

---

### Issue: "Sample Data Not Found"

**Symptoms:**
```
FileNotFoundError: data/samples/logs/api-gateway.log
```

**Solution:**
```bash
# Check if sample data exists
ls -la data/samples/logs/
ls -la data/samples/metrics/
ls -la data/samples/traces/
ls -la data/samples/configs/

# If missing, sample data should be there from Phase 2
# Verify with:
find data/samples -type f
```

---

## ✅ Test Checklist

Use this checklist to verify everything works:

### Phase 2: Data Ingestion
- [ ] `python scripts/test_phase2.py` passes
- [ ] All 77 logs parsed correctly
- [ ] All 11 metrics parsed with summaries
- [ ] All 9 traces parsed with hierarchy
- [ ] Config changes detected

### Phase 3: Reasoning Engine
- [ ] `python scripts/test_phase3.py` passes
- [ ] Prompts generated correctly
- [ ] Gemini API responds
- [ ] RCA object created with all fields
- [ ] Fix suggestions prioritized

### Phase 4: API Backend
- [ ] `python scripts/test_phase4.py` passes
- [ ] API starts on port 8000
- [ ] Health endpoints return 200
- [ ] Analysis endpoint works
- [ ] Incident retrieval works
- [ ] API docs accessible at /docs

### Phase 5: Frontend
- [ ] `python scripts/test_phase5.py` passes
- [ ] Frontend starts on port 8501
- [ ] Sample data loads correctly
- [ ] File upload works
- [ ] Analysis submits successfully
- [ ] Results display correctly
- [ ] No emojis in UI
- [ ] All 3 pages work (New Analysis, History, Settings)

### End-to-End
- [ ] Both servers start with `start_all.py`
- [ ] Sample data analysis completes in <30 seconds
- [ ] Results match expected output
- [ ] Can download JSON report
- [ ] Incident history shows past analyses

---

## 🎯 Summary

**Quick Test Commands:**
```bash
# Full automated test suite
source venv/bin/activate
python scripts/test_phase2.py && \
python scripts/test_phase3.py && \
python scripts/test_phase4.py && \
python scripts/test_phase5.py

# Manual UI test
python scripts/start_all.py
# Open http://localhost:8501
# Click "Use Sample Data" → "Analyze Incident"
```

**Expected Results:**
- ✅ All tests pass
- ✅ Sample data analysis: ~15 seconds
- ✅ Root cause identified with 92% confidence
- ✅ 5 fix suggestions generated
- ✅ Professional UI with no emojis

**Next Steps:**
- Run tests now to verify everything works
- Fix any issues discovered
- Proceed to Phase 6 (demo preparation)

---

*Last Updated: February 5, 2026*
