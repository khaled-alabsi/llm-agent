# LLM Agent with Tool Calling

A learning-focused implementation of an AI agent that uses tool calling (function calling) with a local LLM via LLM Studio.

## What This Project Teaches You

This project demonstrates:

1. **How agents work** - See the full request/response cycle
2. **Tool calling** - How LLMs decide which tools to use and how to execute them
3. **Response handling** - How agent frameworks parse and process LLM responses
4. **Multi-step reasoning** - How agents chain multiple tool calls together
5. **Different frameworks** - Foundation to explore LangChain, AutoGen, CrewAI, etc.

## Features

- **Complete Request/Response Logging**: See EVERYTHING sent to and received from the LLM
  - Full request payload including all tool schemas
  - Raw LLM responses with tool calls
  - Saved to JSON files in `logs/` directory for inspection
- **Multiple Tools**: File operations, calculator, time, and easy to add more
- **Interactive UI**: Jupyter notebook for hands-on experimentation
- **Clean Code**: Well-documented and easy to understand implementation

## Prerequisites

1. **LLM Studio** running locally with `qwen/qwen3-coder-30b` model
   - Download from: https://lmstudio.ai/
   - Load the Qwen3-Coder-30B model
   - Start the local server (default: http://localhost:1234)

2. **Python 3.8+** with pip

## Setup

### 1. Install Dependencies

```bash
# Activate your virtual environment if you have one
source .venv/bin/activate  # On macOS/Linux
# or
.venv\Scripts\activate  # On Windows

# Install required packages
pip install -r requirements.txt
```

### 2. Verify LLM Studio Connection

Make sure LLM Studio is running and accessible:

```bash
curl http://localhost:1234/v1/models
```

You should see a response with your loaded model.

## Usage

### Option 1: Jupyter Notebook (Recommended for Learning)

```bash
jupyter notebook agent_ui.ipynb
```

The notebook includes:
- Step-by-step examples
- Detailed explanations
- Interactive cells to try your own prompts
- Visual breakdown of the request/response flow

### Option 2: Python Script

```bash
python agent.py
```

This runs the example scenarios defined in the script.

### Option 3: Import as Module

```python
from agent import Agent, create_file_tool, CREATE_FILE_SCHEMA

# Create agent
agent = Agent(
    base_url="http://localhost:1234/v1",
    model="qwen/qwen3-coder-30b",
    log_dir="logs"  # Save all requests/responses to JSON files
)

# Register tools
agent.register_tool("create_file", create_file_tool, CREATE_FILE_SCHEMA)

# Run agent
response = agent.run("Create a file called 'test.txt' with 'Hello World'")
print(response)
```

## Understanding Tool Calling

### Tool Schema Format

Tools are defined using the OpenAI function calling format:

```python
CREATE_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "create_file",
        "description": "Create a new file with specified content",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to create"
                },
                "content": {
                    "type": "string",
                    "description": "The content to write to the file"
                }
            },
            "required": ["filename", "content"]
        }
    }
}
```

### LLM Response Format

When the LLM wants to use a tool, it responds with:

```json
{
  "choices": [{
    "message": {
      "role": "assistant",
      "content": null,
      "tool_calls": [
        {
          "id": "call_abc123",
          "type": "function",
          "function": {
            "name": "create_file",
            "arguments": "{\"filename\": \"test.txt\", \"content\": \"Hello\"}"
          }
        }
      ]
    }
  }]
}
```

### Agent Processing Flow

1. **User Input** → Agent receives request
2. **LLM Call** → Agent sends message + available tools to LLM
3. **Response Parsing** → Agent extracts tool calls from LLM response
4. **Tool Execution** → Agent executes each tool and collects results
5. **Result Return** → Results sent back to LLM for final response
6. **Repeat** → Steps 2-5 repeat until no more tool calls needed

All of this is logged in detail when you run the agent!

## Available Tools

### 1. create_file
Creates a new file with specified content.

**Parameters:**
- `filename` (string): Name of file to create
- `content` (string): Content to write

### 2. read_file
Reads a file's content.

**Parameters:**
- `filename` (string): Name of file to read

### 3. calculator
Performs arithmetic operations.

**Parameters:**
- `operation` (string): One of 'add', 'subtract', 'multiply', 'divide'
- `a` (number): First number
- `b` (number): Second number

### 4. get_current_time
Gets current date and time.

**Parameters:** None

## Creating Custom Tools

Add your own tools in 3 steps:

### Step 1: Define the Function

```python
def my_custom_tool(param1: str, param2: int) -> dict:
    """Your tool logic here"""
    return {
        "status": "success",
        "result": f"Processed {param1} with {param2}"
    }
```

### Step 2: Define the Schema

```python
MY_TOOL_SCHEMA = {
    "type": "function",
    "function": {
        "name": "my_custom_tool",
        "description": "Description for the LLM",
        "parameters": {
            "type": "object",
            "properties": {
                "param1": {
                    "type": "string",
                    "description": "Description of param1"
                },
                "param2": {
                    "type": "integer",
                    "description": "Description of param2"
                }
            },
            "required": ["param1", "param2"]
        }
    }
}
```

### Step 3: Register the Tool

```python
agent.register_tool("my_custom_tool", my_custom_tool, MY_TOOL_SCHEMA)
```

## Logging and Transparency

The agent shows you EVERYTHING. No hidden information!

### Console Output

When you run the agent, you'll see complete logs including:

```
================================================================================
📤 SENDING TO LLM - COMPLETE REQUEST PAYLOAD
================================================================================
{
  "model": "qwen/qwen3-coder-30b",
  "messages": [
    {
      "role": "user",
      "content": "Create a file called 'test.txt' with 'Hello World'"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2000,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "create_file",
        "description": "Create a new file with the specified content",
        "parameters": {
          "type": "object",
          "properties": {
            "filename": {
              "type": "string",
              "description": "The name of the file to create"
            },
            "content": {
              "type": "string",
              "description": "The content to write to the file"
            }
          },
          "required": ["filename", "content"]
        }
      }
    },
    ... (all other tools)
  ],
  "tool_choice": "auto"
}

💾 Request saved to: logs/request_1_20251109_142030.json

================================================================================
📥 LLM RESPONSE - COMPLETE RAW RESPONSE
================================================================================
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "created": 1762694928,
  "model": "qwen/qwen3-coder-30b",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "",
        "tool_calls": [
          {
            "type": "function",
            "id": "call_1",
            "function": {
              "name": "create_file",
              "arguments": "{\"filename\": \"test.txt\", \"content\": \"Hello World\"}"
            }
          }
        ]
      },
      "finish_reason": "tool_calls"
    }
  ],
  "usage": {
    "prompt_tokens": 592,
    "completion_tokens": 37,
    "total_tokens": 629
  }
}

💾 Response saved to: logs/response_1_20251109_142030.json

================================================================================
🔧 EXECUTING TOOL: create_file
================================================================================
Arguments: {
  "filename": "test.txt",
  "content": "Hello World"
}

✓ Tool Result:
{
  "status": "success",
  "message": "File 'test.txt' created successfully",
  "filename": "test.txt",
  "size": 11
}
```

### Saved Log Files

Every request and response is saved to the `logs/` directory as JSON files:
- `request_1_20251109_142030.json` - Complete request payload with all tool schemas
- `response_1_20251109_142030.json` - Complete LLM response

You can open these files to examine exactly what was sent and received!

## Learning Path

1. **Start with the Jupyter Notebook** - Run through all examples
2. **Modify existing tools** - Change parameters, add features
3. **Create your own tools** - Try file operations, web APIs, data processing
4. **Experiment with prompts** - See how different requests affect tool usage
5. **Explore frameworks** - Try implementing with LangChain, AutoGen, etc.

## Next Steps

After understanding this implementation, explore:

- **LangChain** - High-level framework with many built-in tools
- **AutoGen** - Microsoft's multi-agent conversation framework
- **CrewAI** - Role-based agent collaboration
- **LlamaIndex** - Document indexing and retrieval
- **Semantic Kernel** - Microsoft's AI orchestration

## Troubleshooting

### LLM Studio Connection Issues

If the agent can't connect to LLM Studio:

1. Ensure LLM Studio is running
2. Check the port (default is 1234)
3. Verify the model is loaded
4. Update `base_url` in agent initialization if using different port

### Tool Not Being Called

If the LLM isn't using tools:

1. Check tool description is clear
2. Make sure your prompt clearly requests the tool's functionality
3. Try a more explicit prompt
4. Some models work better with tool calling than others

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

## Project Structure

```
llm-agent/
├── agent.py              # Main agent implementation
├── agent_ui.ipynb        # Interactive Jupyter notebook
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Contributing

This is a learning project! Feel free to:
- Add more tools
- Improve logging
- Add different agent frameworks
- Create examples for specific use cases

## License

MIT License - Feel free to use for learning and experimentation!

## Resources

- [OpenAI Function Calling](https://platform.openai.com/docs/guides/function-calling)
- [LLM Studio](https://lmstudio.ai/)
- [LangChain Documentation](https://python.langchain.com/)
- [AutoGen Documentation](https://microsoft.github.io/autogen/)
