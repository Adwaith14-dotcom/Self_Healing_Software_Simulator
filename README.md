# Self Healing Software Simulator

Lightweight Streamlit-based simulator for demonstrating self-healing behaviors in services and processes.

## Features
- Monitor simulated processes and resource spikes
- Trigger recovery actions and visualize state
- Extensible modules under `dashboard/`, `tools/`, and `upgrades/`

## Quick Start
1. Create a virtual environment and install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Run the app with Streamlit:

```powershell
streamlit run app.py
```

Open the local URL printed by Streamlit (usually http://localhost:8501).

## Configuration
- See `settings.py` for configurable options and environment variables.

## Directory Layout (important files)
- `app.py` — Streamlit entry point
- `dashboard/` — visualization components
- `tools/` — utility scripts and viewers
- `upgrades/` — self-healing rules and handlers
- `requirements.txt` — Python dependencies

## Development
- Run linters and tests (if added). Use the existing scripts as examples.

## Contributing
Open issues or PRs on GitHub. Follow standard GitHub flow: feature branch → PR → review → merge.

