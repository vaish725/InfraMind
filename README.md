# InfraMind

**Reasoning-first AI debugger for modern infrastructure**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gemini 2.0 Flash](https://img.shields.io/badge/Gemini-2.0%20Flash-orange.svg)](https://deepmind.google/technologies/gemini/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-16.1-black.- **Postgr## Roadmap

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is InfraMind?

InfraMind is an intelligent incident analysis platform that uses **Google's Gemini 2.0 Flash AI** to perform comprehensive root cause analysis on production incidents. By analyzing logs, metrics, traces, and configuration files together, InfraMind acts as a senior SRE, identifying not just *what* broke, but *why* it broke and *how to fix it*.

### Key Capabilities

- **Automated Root Cause Analysis** - Identify the true source of failures across distributed systems
- **Causal Chain Visualization** - Understand how issues propagate through your infrastructure  
- **Multi-Source Correlation** - Analyze logs, metrics, traces, and configs simultaneously
- **Actionable Fix Suggestions** - Get prioritized remediation steps with validation criteria
- **AI Reasoning Transparency** - See step-by-step how conclusions were reached

### The Problem We Solve

Modern infrastructure generates overwhelming amounts of telemetry data. Engineers can see *what* broke through dashboards and alerts, but determining *why* requires manually correlating information across multiple systems—a time-consuming and error-prone process during critical incidents.

### Our Solution

InfraMind acts as an AI-powered SRE that:
1. **Ingests** multi-format incident data (logs, metrics, traces, configs)
2. **Correlates** events across time and services
3. **Reasons** about causality using advanced AI
4. **Delivers** structured RCA reports with actionable fixes

---
### Completed (MVP)
- [x] Multi-source data ingestion (logs, metrics, traces, configs)
- [x] Gemini 2.0 Flash integration with retry logic
- [x] Root cause analysis with causal chains
- [x] Next.js dashboard with file upload
- [x] Actionable fix suggestions with validation steps
- [x] Demo mode fallback for rate limits
- [x] JSON repair for malformed AI responses
- [x] PostgreSQL config file support
### Future Enhancementsabase configuration files
---

## Quick Start

### Prerequisites

- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Gemini API Key** - [Get one here](https://aistudio.google.com/apikey) (Free tier available)
- **Available Ports** - Ensure ports 8000 (API) and 3001 (UI) are not in use

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/vaish725/InfraMind.git
cd InfraMind

# 2. Set up Python backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Set up Next.js frontend
cd infra-mind-dashboard-ui
npm install
cd ..
```

### Running the Application

**Terminal 1 - Start Backend:**
```bash
source venv/bin/activate
uvicorn backend.api.main:app --host 0.0.0.0 --port 8000 --reload
```

**Terminal 2 - Start Frontend:**
```bash
cd infra-mind-dashboard-ui
npm run dev
```

### Access the Application

- **Frontend Dashboard:** http://localhost:3001
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### Try a Demo Analysis

1. Navigate to http://localhost:3001
2. Click **"New Analysis"**
3. Upload sample files from `sample-demo-files-3/`:
   - `INCIDENT_DESCRIPTION.txt`
   - `payment-api.log`
   - `payment-metrics.csv`
   - `payment-traces.json`
   - `application-config.json`
4. Click **"Analyze Incident"**
5. View comprehensive RCA in 30-60 seconds!

---

---

## Architecture

```
┌─────────────────────────────────────┐
│     Next.js Dashboard (Port 3001)   │
│  - File Upload Interface            │
│  - Real-time Analysis Display       │
│  - Causal Chain Visualization       │
└──────────────┬──────────────────────┘
               │ REST API
               ▼
┌─────────────────────────────────────┐
│    FastAPI Backend (Port 8000)      │
│  ┌─────────────────────────────┐   │
│  │   Ingestion Layer           │   │
│  │  - Log Parser               │   │
│  │  - Metrics Parser           │   │
│  │  - Trace Parser             │   │
│  │  - Config Parser            │   │
│  │  - Data Unifier             │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │   Reasoning Engine          │   │
│  │  - Gemini 2.0 Flash Client  │   │
│  │  - Prompt Engineering       │   │
│  │  - Response Parsing         │   │
│  │  - JSON Repair Logic        │   │
│  └──────────┬──────────────────┘   │
│             │                       │
│  ┌──────────▼──────────────────┐   │
│  │   Output Formatter          │   │
│  │  - RCA Model                │   │
│  │  - Validation               │   │
│  │  - Demo Mode Fallback       │   │
│  └─────────────────────────────┘   │
└─────────────────────────────────────┘
               │
               ▼
     ┌─────────────────┐
     │  Gemini 2.0 API │
     │  (Google Cloud) │
     └─────────────────┘
```

### Tech Stack

**Backend:**
- FastAPI - Modern Python web framework
- Pydantic - Data validation and settings
- Google Generative AI SDK - Gemini integration
- Tenacity - Retry logic with exponential backoff

**Frontend:**
- Next.js 16.1 - React framework with Turbopack
- TypeScript - Type-safe development
- Tailwind CSS - Utility-first styling
- shadcn/ui - High-quality UI components

**AI Model:**
- Gemini 2.0 Flash - Fast, cost-effective reasoning
- Temperature: 0.3 - Focused, deterministic analysis
- Max tokens: 4096 - Comprehensive responses

---

---

## Project Structure

```
InfraMind/
├── backend/                          # Python Backend
│   ├── api/                         # FastAPI Application
│   │   ├── main.py                  # App entry point & CORS config
│   │   └── routes/
│   │       ├── incident.py          # Analysis endpoints
│   │       └── health.py            # Health check
│   │
│   ├── ingestion/                   # Data Parsers
│   │   ├── log_parser.py           # JSON/text log parsing
│   │   ├── metrics_parser.py       # CSV/JSON metrics
│   │   ├── trace_parser.py         # Distributed traces
│   │   ├── config_parser.py        # Multi-format configs (JSON/YAML/ENV/INI)
│   │   └── data_unifier.py         # Create unified context
│   │
│   ├── reasoning/                   # AI Reasoning
│   │   ├── gemini_client.py        # Gemini API wrapper with retry
│   │   ├── prompts.py              # Prompt templates
│   │   └── reasoning_engine.py     # RCA orchestration & JSON repair
│   │
│   ├── models/                      # Data Models
│   │   ├── incident.py             # Incident data structures
│   │   ├── rca.py                  # RCA output models
│   │   └── schemas.py              # API request/response schemas
│   │
│   └── core/                        # Core Utilities
│       ├── config.py               # Settings management
│       └── exceptions.py           # Custom exceptions
│
├── infra-mind-dashboard-ui/         # Next.js Frontend
│   ├── app/
│   │   ├── page.tsx                # Main dashboard page
│   │   └── layout.tsx              # Root layout
│   │
│   ├── components/inframind/       # Custom Components
│   │   ├── dashboard.tsx           # Main dashboard
│   │   ├── analysis-form.tsx       # File upload form
│   │   ├── executive-summary.tsx   # Results display
│   │   ├── causal-chain.tsx        # Visual causal chain
│   │   ├── recommended-fixes.tsx   # Fix suggestions
│   │   └── reasoning-process.tsx   # AI reasoning steps
│   │
│   ├── lib/
│   │   ├── api-client.ts           # Backend API client
│   │   └── transform.ts            # Response transformation
│   │
│   └── package.json                # Dependencies
│
├── sample-demo-files-3/             # Demo Incident Files
│   ├── INCIDENT_DESCRIPTION.txt    # P0 payment system outage
│   ├── payment-api.log             # Application logs
│   ├── payment-metrics.csv         # System metrics
│   ├── payment-traces.json         # Distributed traces
│   └── application-config.json     # Config with bug details
│
├── tests/                           # Test Suites
│   ├── test_api/                   # API endpoint tests
│   ├── test_ingestion/             # Parser tests
│   └── test_reasoning/             # AI reasoning tests
│
├── .env.example                     # Environment template
├── requirements.txt                 # Python dependencies
└── README.md                        # This file
```

---

---

## Core Features

### 1. Multi-Source Ingestion
Supports diverse data formats and automatically detects file types:

| Data Type | Supported Formats | Auto-Detection |
|-----------|------------------|----------------|
| **Logs** | JSON, plain text, structured logs | Yes |
| **Metrics** | CSV, JSON time-series | Yes |
| **Traces** | JSON distributed traces | Yes |
| **Configs** | JSON, YAML, ENV, INI, PostgreSQL conf | Yes |

**Intelligent Parsing:**
- Handles malformed files gracefully
- Extracts timestamps, severity, service names
- Correlates events across data sources

### 2. AI-Powered Root Cause Analysis

Uses Gemini 2.0 Flash to:
- **Identify Root Cause** - Distinguishes symptoms from actual causes
- **Build Causal Chains** - Shows how failures propagate
- **Assess Confidence** - Provides confidence scores (LOW/MEDIUM/HIGH)
- **Cite Evidence** - References specific log lines and metrics

### 3. Actionable Fix Suggestions

Each incident analysis includes:
- **Prioritized Fixes** - Ordered by impact and urgency
- **Time Estimates** - Expected effort for each fix
- **Validation Steps** - How to verify the fix worked
- **Business Impact** - Expected outcomes (e.g., "Reduce error rate to <1%")

### 4. Transparent Reasoning

View AI's step-by-step analysis:
- **Reasoning Steps** - How conclusions were reached
- **Evidence Links** - Which data led to each conclusion
- **Confidence Scores** - How certain the AI is about each finding

### 5. Demo Mode Fallback

When Gemini API hits rate limits:
- Automatically switches to demo mode
- Returns realistic hardcoded analysis
- Analyzes uploaded files for contextual responses
- Clearly labeled as demo mode

---

## Gemini Integration

InfraMind leverages **Gemini 2.0 Flash's** capabilities:

### Why Gemini 2.0 Flash?

| Capability | How We Use It |
|-----------|---------------|
| **Long Context Window** | Analyze entire incident timelines with full logs |
| **Fast Inference** | Deliver RCA in 30-60 seconds |
| **Structured Output** | Generate consistent JSON responses |
| **Advanced Reasoning** | Understand causality across distributed systems |
| **Cost Effective** | Free tier suitable for demos and testing |

### Prompt Engineering

Our prompts are designed to:
1. **Provide Context** - Full incident data in structured format
2. **Set Role** - "Act as senior SRE performing root cause analysis"
3. **Specify Output** - Exact JSON schema with required fields
4. **Guide Reasoning** - Focus on causality, not just correlation

### Error Handling

- **Retry Logic** - Exponential backoff for transient failures
- **JSON Repair** - Fixes truncated/malformed Gemini responses
- **Rate Limit** - Graceful degradation to demo mode
- **Validation** - Pydantic models ensure output consistency

---

## Demo Scenario

### Sample Incident: Payment System Outage

Included in `sample-demo-files-3/`:

**Incident Details:**
- **Severity:** P0 (Critical)
- **Impact:** 100% payment failure rate, $2.5M/hour revenue loss
- **Duration:** 8 minutes before rollback
- **Affected Users:** 50,000+

**Files Provided:**
1. **INCIDENT_DESCRIPTION.txt** - Business context and impact
2. **payment-api.log** - OOM errors, connection pool exhaustion
3. **payment-metrics.csv** - Error rate progression (0.2% → 100%)
4. **payment-traces.json** - Distributed traces showing connection leaks
5. **application-config.json** - Recent v3.5.0 deployment details

**Expected RCA Output:**
- **Root Cause:** FraudDetectionService v3.5.0 not closing database connections
- **Contributing Factors:** New driver v2.5.0, missing finally blocks, disabled monitoring
- **Immediate Fix:** Rollback to v3.4.9 (3 minutes)
- **Long-term Fix:** Add proper resource cleanup in finally blocks
- **Confidence:** 95% (HIGH)

---

## Testing

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests
pytest

# Run specific test suite
pytest tests/test_ingestion/
pytest tests/test_reasoning/
pytest tests/test_api/

# Run with coverage report
pytest --cov=backend --cov-report=html
open htmlcov/index.html

# Test specific file
pytest tests/test_ingestion/test_config_parser.py -v
```

---

---

## API Documentation

### Backend API

Once running, access interactive documentation:

- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Key Endpoints

#### `POST /api/v1/incidents/analyze`
Analyze an incident with uploaded files.

**Request:**
```json
{
  "incident_id": "incident-20260209T143000",
  "log_files": [...],
  "metric_files": [...],
  "trace_files": [...],
  "config_files": [...],
  "time_window_minutes": 30
}
```

**Response:**
```json
{
  "incident_id": "incident-20260209T143000",
  "status": "COMPLETED",
  "rca": {
    "root_cause_description": "...",
    "overall_confidence": 0.95,
    "reasoning_steps": [...],
    "causal_chain": [...],
    "fix_suggestions": [...]
  }
}
```

#### `GET /api/v1/health`
Health check endpoint.

---

## Configuration

### Environment Variables

Create `.env` file with:

```bash
# Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.0-flash

# Application Settings
APP_ENV=development
DEBUG=True
LOG_LEVEL=INFO

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
API_WORKERS=1

# Processing Limits
MAX_FILE_SIZE_MB=10
MAX_CONTEXT_LENGTH=100000
REQUEST_TIMEOUT_SECONDS=30
```

### Supported Config Formats

The config parser automatically detects and handles:
- **JSON** - Standard configuration files
- **YAML** - Kubernetes configs, docker-compose
- **ENV** - Environment variable files
- **INI/CFG** - Legacy application configs
- **PostgreSQL .conf** - Database configuration files

---

---

## �️ Roadmap

### ✅ Hackathon Deliverables (Completed)
- [x] Multi-source data ingestion (logs, metrics, traces, configs)
- [x] Gemini 2.0 Flash integration with retry logic
- [x] Root cause analysis with causal chains
- [x] Next.js dashboard with file upload
- [x] Actionable fix suggestions with validation steps
- [x] Demo mode fallback for rate limits
- [x] JSON repair for malformed AI responses
- [x] PostgreSQL config file support

### 🚧 In Progress
- [ ] Comprehensive test coverage
- [ ] Performance optimization for large files
- [ ] Enhanced error messages

### 🔮 Future Enhancements
- [ ] **Live Log Streaming** - Real-time incident detection
- [ ] **Historical Analysis** - Learn from past incidents
- [ ] **GitHub Integration** - Auto-generate fix PRs
- [ ] **Slack/PagerDuty** - Incident management integration
- [ ] **Graph Visualization** - Interactive causal chain explorer
- [ ] **Custom Models** - Fine-tuned industry-specific RCA
- [ ] **Multi-Language** - Support for non-English logs
- [ ] **Anomaly Detection** - Proactive incident prediction

---

## Contributing

This project was built for the Gemini 3 Global Hackathon, but contributions are welcome!

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use TypeScript for frontend code
- Add tests for new features
- Update documentation as needed

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Hackathon Submission

Built for the **Gemini 3 Global Hackathon** (February 2026)

**Category:** Infrastructure & DevOps Tools  
**Submission Date:** February 9, 2026  
**Team:** Vaishnavi Kamdi

### Why This Matters

Production incidents cost businesses millions in lost revenue and engineering time. InfraMind accelerates incident resolution by automating the most time-consuming part of debugging: root cause analysis. By leveraging Gemini's advanced reasoning, we're making AI-powered SRE capabilities accessible to teams of all sizes.

---

## 📞 Contact

**Vaishnavi Kamdi**
- Email: vaishnaviskamdi@gmail.com
- GitHub: [@vaish725](https://github.com/vaish725)
- LinkedIn: [Connect with me](https://linkedin.com/in/vaishnavikamdi)

---

## Acknowledgments

- **Google Gemini Team** - For the powerful Gemini 2.0 Flash API
- **FastAPI** - For the excellent Python web framework
- **Next.js** - For the amazing React framework
- **shadcn/ui** - For beautiful, accessible UI components

---

<div align="center">

**Built with ❤️ and powered by Gemini 2.0 Flash**

[⭐ Star this repo](https://github.com/vaish725/InfraMind) | [🐛 Report Bug](https://github.com/vaish725/InfraMind/issues) | [💡 Request Feature](https://github.com/vaish725/InfraMind/issues)

</div>
