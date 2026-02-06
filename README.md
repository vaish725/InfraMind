# 🧠 InfraMind

**Tagline:** *Reasoning-first AI debugger for modern infrastructure*

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Gemini 3](https://img.shields.io/badge/Gemini-3-orange.svg)](https://deepmind.google/technologies/gemini/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What is InfraMind?

InfraMind is an AI-powered infrastructure debugger that uses **Gemini 3's advanced reasoning** to analyze logs, traces, metrics, and configuration files together to generate:

- 🔍 **Root Cause Analysis** - Identify the true source of failures
- 🔗 **Failure Propagation Chains** - Understand cascading effects
- 💡 **Actionable Fix Suggestions** - Get concrete remediation steps
- 📊 **Reasoning Traces** - See how conclusions were reached

> **The Problem:** Engineers can see *what* broke, but not *why* it broke or *what to fix first*.
> 
> **Our Solution:** Act as a senior SRE in the loop, not just a log search tool.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Gemini 3 API key ([Get one here](https://ai.google.dev/))

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/infra-mind.git
cd infra-mind

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Running the Application

**Option 1: Streamlit UI (Recommended)**
```bash
streamlit run frontend/app.py
```

**Option 2: Backend API**
```bash
uvicorn backend.api.main:app --reload --port 8000
```

---

## 🏗️ Architecture

```
┌─────────────┐
│   Frontend  │  Streamlit UI
│  (Streamlit)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  Backend    │  FastAPI + Python
│  (FastAPI)  │
└──────┬──────┘
       │
       ├──► Ingestion Layer    (Parse logs, metrics, configs)
       │
       ├──► Reasoning Engine   (Gemini 3 integration)
       │
       └──► Output Formatter   (Structured RCA)
```

---

## 📁 Project Structure

```
infra-mind/
├── backend/
│   ├── api/                    # FastAPI endpoints
│   │   ├── __init__.py
│   │   ├── main.py            # Main app entry
│   │   ├── routes/            # API routes
│   │   └── dependencies.py    # Dependency injection
│   │
│   ├── ingestion/             # Data parsers
│   │   ├── __init__.py
│   │   ├── log_parser.py
│   │   ├── metrics_parser.py
│   │   ├── config_parser.py
│   │   ├── trace_parser.py
│   │   └── unifier.py         # Unified context
│   │
│   ├── reasoning/             # Gemini integration
│   │   ├── __init__.py
│   │   ├── gemini_client.py   # API wrapper
│   │   ├── prompt_builder.py  # Prompt engineering
│   │   ├── analyzer.py        # Main reasoning logic
│   │   └── output_parser.py   # Response parsing
│   │
│   ├── models/                # Data models
│   │   ├── __init__.py
│   │   ├── incident.py
│   │   ├── rca.py
│   │   └── schemas.py
│   │
│   ├── core/                  # Core utilities
│   │   ├── __init__.py
│   │   ├── config.py          # Configuration
│   │   └── exceptions.py      # Custom exceptions
│   │
│   └── utils/                 # Helper functions
│       ├── __init__.py
│       └── helpers.py
│
├── frontend/
│   ├── app.py                 # Main Streamlit app
│   ├── components/            # UI components
│   │   ├── __init__.py
│   │   ├── upload.py
│   │   ├── analysis.py
│   │   └── results.py
│   └── styles/
│       └── custom.css
│
├── data/
│   ├── samples/               # Demo data
│   │   ├── logs/
│   │   ├── metrics/
│   │   ├── configs/
│   │   └── traces/
│   ├── temp/                  # Temporary files
│   └── cache/                 # Response cache
│
├── tests/
│   ├── __init__.py
│   ├── test_ingestion/
│   ├── test_reasoning/
│   └── test_api/
│
├── docs/
│   ├── architecture.md
│   ├── api.md
│   └── gemini_integration.md
│
├── scripts/
│   ├── generate_demo_data.py
│   └── test_gemini.py
│
├── .env.example
├── .gitignore
├── requirements.txt
├── README.md
└── prd.md
```

---

## 🧩 Core Features

### 1. Multi-Source Ingestion
- ✅ JSON & plain text logs
- ✅ Stack traces
- ✅ Metrics snapshots (CPU, memory, latency)
- ✅ Distributed traces (simplified spans)
- ✅ Configuration files (YAML/ENV)

### 2. Failure Correlation Engine
- ✅ Temporal correlation detection
- ✅ Cascading failure analysis
- ✅ Config change impact tracking
- ✅ Symptom vs root cause classification

### 3. Root Cause Analysis
- ✅ Primary root cause identification
- ✅ Contributing factors
- ✅ Non-root symptoms (labeled)
- ✅ Evidence-grounded conclusions

### 4. Actionable Fixes
- ✅ Immediate mitigation steps
- ✅ Long-term solutions
- ✅ Code/config suggestions
- ✅ Observability improvements

### 5. Reasoning Explainability
- ✅ Step-by-step causal reasoning
- ✅ Evidence references (log lines, metrics)
- ✅ Confidence scoring

---

## 🤖 Gemini 3 Integration

InfraMind leverages **Gemini 3's advanced capabilities**:

- **Long-Context Reasoning:** Analyze entire incident timelines (logs + metrics + configs)
- **Multimodal Understanding:** Process diverse data formats simultaneously
- **Structured Output:** Generate consistent, parseable RCA reports
- **Low-Latency Inference:** Deliver results in < 10 seconds

### Why Gemini 3?

Traditional tools surface signals but don't reason about them. Gemini 3's advanced reasoning capabilities enable InfraMind to:

1. **Understand causality** across distributed systems
2. **Correlate events** across multiple data sources
3. **Distinguish symptoms from root causes**
4. **Generate actionable insights** based on SRE best practices

See [docs/gemini_integration.md](docs/gemini_integration.md) for detailed implementation.

---

## 📊 Demo

Check out our 3-minute demo video showing InfraMind analyzing a real microservice outage:

🎥 [Watch Demo Video](#) *(Coming soon)*

**Demo Scenario:** Microservice timeout causing cascading failures
- Upload logs, metrics, and config files
- Click "Analyze Incident"
- See root cause identified in seconds
- Get actionable fix suggestions

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run specific test suite
pytest tests/test_ingestion/

# Run with coverage
pytest --cov=backend --cov-report=html
```

---

## 📝 API Documentation

Once the backend is running, visit:
- **Interactive Docs:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

---

## 🛣️ Roadmap

- [x] MVP with basic RCA
- [ ] Live log streaming
- [ ] GitHub PR auto-suggestions
- [ ] Slack/PagerDuty integration
- [ ] Learned failure patterns
- [ ] Graph-based failure visualization

---

## 🤝 Contributing

This is a hackathon project, but we welcome contributions! Please read our contributing guidelines.

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details

---

## 🏆 Hackathon Submission

Built for the **Gemini 3 Global Hackathon** (February 2026)

- **Team:** [Your Name]
- **Submission Date:** February 9, 2026
- **Category:** Infrastructure & DevOps

---

## 📧 Contact

Questions? Reach out:
- Email: your.email@example.com
- Twitter: [@yourhandle](https://twitter.com/yourhandle)
- GitHub: [@yourusername](https://github.com/yourusername)

---

**Built with ❤️ and powered by Gemini 3**
