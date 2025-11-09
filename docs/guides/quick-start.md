# Quick Start Guide

Get the CrewAI Coder Agent running in 5 minutes!

## Prerequisites Check

Before starting, ensure you have:
- [ ] Python 3.10+ installed
- [ ] LM Studio downloaded and running
- [ ] Qwen3-Coder-30B model loaded in LM Studio
- [ ] LM Studio server started (default: http://localhost:1234)

## Step 1: Install Dependencies (2 minutes)

```bash
# Navigate to project directory
cd /path/to/llm-agent

# Create virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# or .venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt
```

## Step 2: Verify LM Studio (1 minute)

```bash
# Test if LM Studio is accessible
curl http://localhost:1234/v1/models
```

You should see a JSON response with your loaded model.

## Step 3: Run the Agent (2 minutes)

### Option A: Command Line
```bash
python main.py
```

### Option B: Jupyter Notebook
```bash
jupyter notebook agent_control.ipynb
```

## What Happens Next?

The agent will:
1. Load configuration from `config.yaml`
2. Initialize with context (skills, guidelines, safety rules)
3. Execute the task defined in `prompts/build-website.md`
4. Create files in `./output/` directory
5. Save logs to `./logs/` directory

Expected duration: 3-10 minutes depending on task complexity.

## Check the Output

```bash
# View generated files
ls -R output/

# View session logs
ls logs/
```

## Next Steps

- **Customize the prompt**: Edit `prompts/build-website.md`
- **Change configuration**: Edit `config.yaml`
- **View logs**: Check `logs/session_*.log` and `logs/session_*.json`
- **Try notebook**: Run `jupyter notebook agent_control.ipynb` for interactive control

## Troubleshooting

**Problem**: Can't connect to LM Studio
- Solution: Ensure LM Studio server is running and port matches config.yaml

**Problem**: Import errors
- Solution: `pip install -r requirements.txt --upgrade`

**Problem**: Agent creates nothing
- Solution: Check logs in `logs/` directory for errors

## What to Read Next

- [Configuration Guide](configuration.md) - Customize settings
- [Prompt Engineering](prompt-engineering.md) - Write better prompts
- [Architecture Overview](../architecture/overview.md) - Understand the system
