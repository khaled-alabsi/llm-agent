
# Microsoft Agent Framework (Python) — Offline Guide (with LM Studio & Qwen3-Coder-30B)

_Last updated: 2025-11-09 (Europe/Berlin)_

This document is designed for environments **without internet access**. It provides everything you need to get productive with **Microsoft Agent Framework (Python)** while connecting to a **local OpenAI‑compatible server** such as **LM Studio** (for example, using `qwen/qwen3-coder-30b`).

> Tip: All code in this doc uses standard Python and the public Agent Framework APIs, so you can copy‑paste into your offline project once you’ve installed the packages.

---

## 1) Install

You typically want the full meta‑package (all integrations). If pre‑release builds are required in your environment, keep `--pre`:

```bash
pip install --pre agent-framework
```

If you prefer a minimal footprint:

```bash
pip install --pre agent-framework-core
```

To verify installation:

```bash
python -c "import agent_framework, sys; print('OK', sys.version)"
```

> Requires Python 3.10+.

---

## 2) Pointing to a Local Server (LM Studio)

LM Studio exposes an **OpenAI‑compatible API** on `http://127.0.0.1:1234/v1` by default. You can route Agent Framework’s OpenAI client to this base URL in two ways.

### Option A — Environment variables (recommended)

```bash
export OPENAI_BASE_URL="http://127.0.0.1:1234/v1"
export OPENAI_API_KEY="lm-studio"                    # any non-empty string
export OPENAI_CHAT_MODEL_ID="qwen/qwen3-coder-30b"   # or your chosen model
```

Your Python code can stay clean and read from env automatically.

### Option B — Explicit client (fallback/fine‑grained)

If you need total control (e.g., advanced proxies), pass an explicit AsyncOpenAI client into Agent Framework:

```python
import os, asyncio
from agent_framework.openai import OpenAIChatClient
from openai import AsyncOpenAI

async def main():
    async_client = AsyncOpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1"),
        api_key=os.getenv("OPENAI_API_KEY", "lm-studio"),
    )
    client = OpenAIChatClient(async_client=async_client, model_id=os.getenv("OPENAI_CHAT_MODEL_ID", "qwen/qwen3-coder-30b"))
    print(await client.get_response(messages=[{"role":"user","content":"Hello!"}]))

asyncio.run(main())
```

---

## 3) Minimal Agent

```python
import asyncio
from agent_framework.openai import OpenAIChatClient

async def main():
    client = OpenAIChatClient()  # uses OPENAI_* env vars
    agent = client.create_agent(
        name="CoderBot",
        instructions="You are a precise coding assistant. Prefer short, correct code with comments.",
        temperature=0.2,
        max_tokens=1024,
    )
    result = await agent.run("Write a Python function that merges two sorted lists.")
    print(result)

asyncio.run(main())
```

---

## 4) Tool Calling (Function Tools)

```python
from typing import List
from agent_framework.core.tools import tool

@tool
def sum_integers(values: List[int]) -> int:
    """Return the sum of integers."""
    return sum(values)

agent = OpenAIChatClient().create_agent(
    name="Tooly",
    instructions="Use tools when helpful; show only final results.",
    tools=[sum_integers],
)

# The model can decide to call the tool:
print(await agent.run("Use your tool to add [3, 10, 27]."))
```

**Tips**

- Keep tool docstrings short and clear.
- Return simple, serializable types (or Pydantic models if you need structure).

---

## 5) Structured Output (Validated JSON via Pydantic)

```python
from pydantic import BaseModel
from agent_framework.openai import OpenAIChatClient

class Plan(BaseModel):
    filename: str
    steps: list[str]

client = OpenAIChatClient()
agent = client.create_agent(
    name="Planner",
    instructions="Return only valid JSON for the schema.",
    response_format=Plan,   # validated output
)

result = await agent.run("Plan a small CLI in Python that prints Fibonacci numbers.")
print(result)              # -> Plan(filename='...', steps=[...])
```

---

## 6) Streaming Tokens

```python
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient()

async for token in client.get_streaming_response(
    messages=[{"role":"user","content":"Write a docstring for a Dijkstra implementation."}],
):
    print(token, end="", flush=True)
```

---

## 7) Direct Chat Calls (without creating an Agent)

```python
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient()
reply = await client.get_response(
    messages=[
        {"role": "system", "content": "You are a careful reviewer."},
        {"role": "user", "content": "Review this function for edge cases:\n\n" + open("impl.py").read()},
    ]
)
print(reply)
```

---

## 8) Responses API Path (Alternative)

LM Studio also implements `/v1/responses`. You can use the Agent Framework **OpenAIResponsesClient** with the same env vars:

```python
from agent_framework.openai import OpenAIResponsesClient

rc = OpenAIResponsesClient()  # honors OPENAI_* env vars
agent = rc.create_agent(name="Responder", instructions="Be concise.")
print(await agent.run("Create a TypeScript debounce utility."))
```

---

## 9) Workflows (Basics)

You can orchestrate multi‑step flows with `WorkflowBuilder` and attach an existing agent as an executor. A tiny sketch:

```python
from agent_framework import WorkflowBuilder
from agent_framework.openai import OpenAIChatClient

client = OpenAIChatClient()
agent = client.create_agent(name="Worker", instructions="Be concise.")

wf = WorkflowBuilder("demo").add_agent("start", agent).set_start_executor("start").build()
result = await wf.run("Summarize: Why do generators help with memory usage?")
print(result)
```

(Expand with edges, branches, conditions, or multiple agents as needed.)

---

## 10) End‑to‑End Template (Single File)

```python
# app.py
import os, asyncio
from agent_framework.openai import OpenAIChatClient
from agent_framework.core.tools import tool
from pydantic import BaseModel

# Defaults for LM Studio (override with env in production)
os.environ.setdefault("OPENAI_BASE_URL", "http://127.0.0.1:1234/v1")
os.environ.setdefault("OPENAI_API_KEY", "lm-studio")
os.environ.setdefault("OPENAI_CHAT_MODEL_ID", "qwen/qwen3-coder-30b")

@tool
def grep_py_functions(code: str) -> list[str]:
    """Return function names defined in the given Python source."""
    import re
    return re.findall(r"def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", code)

class Patch(BaseModel):
    filename: str
    summary: str
    diff: str

async def main():
    client = OpenAIChatClient()
    agent = client.create_agent(
        name="RepoHelper",
        instructions=(
            "You are a code assistant. When asked to modify code, return a Patch JSON."
        ),
        tools=[grep_py_functions],
        temperature=0.2,
        response_format=Patch,
    )

    sample = "def add(a,b):\n    return a+b\n"
    task = (
        "Suggest a small refactor and output a unified diff for the file 'example.py'.\n"
        f"""Code:\n```python\n{sample}\n```"""
    )
    result = await agent.run(task)
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 11) Troubleshooting

- **`ModuleNotFoundError: No module named 'agent_framework'`**  
  Install or upgrade the package in the **same interpreter** you use to run code:  
  `pip install --pre agent-framework` (or `agent-framework-core`).  
  Check with `pip show agent-framework` and `python -c "import agent_framework"`.

- **Connection refused**  
  Ensure LM Studio’s Local Server is running on port 1234. Test: `curl http://127.0.0.1:1234/v1/models`.

- **`model_not_found`**  
  Make sure the model is downloaded in LM Studio and the id matches (e.g., `qwen/qwen3-coder-30b`).

- **Tool calls not triggered**  
  Strengthen instructions and ensure the tool’s docstring clearly explains when to use it.

- **Structured output fails validation**  
  Tighten the prompt (“Return only valid JSON, no extra text.”) or loosen the schema.

---

## 12) Offline Packaging Tips

- Cache wheels (via a local PyPI mirror or `pip download`) for `agent-framework`, `agent-framework-core`, and `openai` before going offline.
- Vendor small helper scripts alongside this document.
- Keep a local copy of LM Studio installer and your model files to allow re‑provisioning.

---

## References (for when you’re back online)

- **Docs hub**: Agent Framework documentation (overview, quickstarts, user guides).  
  https://learn.microsoft.com/en-us/agent-framework/

- **Python API reference** (packages, classes, settings):  
  - `agent_framework.openai.OpenAIChatClient`  
    https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework.openai.openaichatclient  
  - `agent_framework.openai` package (incl. `OpenAIResponsesClient`, env settings)  
    https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework.openai  
  - `agent_framework.ChatAgent`  
    https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework.chatagent  
  - `WorkflowBuilder`  
    https://learn.microsoft.com/en-us/python/api/agent-framework-core/agent_framework.workflowbuilder

- **Quickstart & agent types**: OpenAI ChatCompletion Agents guide  
  https://learn.microsoft.com/en-us/agent-framework/user-guide/agents/agent-types/openai-chat-completion-agent

- **GitHub** (source, samples, releases):  
  https://github.com/microsoft/agent-framework  
  https://github.com/microsoft/Agent-Framework-Samples  
  https://github.com/microsoft/agent-framework/releases

- **PyPI** (package index):  
  https://pypi.org/project/agent-framework/

---

**License note**: Microsoft Agent Framework is MIT‑licensed; review the LICENSE in the repository for details.
