"""
LLM Agent with Tool Calling
Demonstrates how agents process LLM responses and execute tools
"""

import json
import requests
from typing import List, Dict, Callable, Any, Optional
from datetime import datetime
import os


class Agent:
    """
    A simple agent that uses a local LLM with tool calling capabilities.
    This implementation helps you understand:
    1. How to structure tool definitions
    2. How to send tool definitions to the LLM
    3. How to parse LLM responses for tool calls
    4. How to execute tools and return results
    """

    def __init__(self, base_url: str = "http://localhost:1234/v1", model: str = "qwen/qwen3-coder-30b",
                 log_dir: Optional[str] = "logs"):
        """
        Initialize the agent with LLM connection details

        Args:
            base_url: LLM Studio API endpoint
            model: Model identifier
            log_dir: Directory to save request/response logs (None to disable file logging)
        """
        self.base_url = base_url
        self.model = model
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict] = []
        self.conversation_history: List[Dict] = []
        self.log_dir = log_dir
        self.request_count = 0

        # Create log directory if logging is enabled
        if self.log_dir:
            os.makedirs(self.log_dir, exist_ok=True)
            print(f"📁 Logging enabled: {os.path.abspath(self.log_dir)}")

    def register_tool(self, name: str, func: Callable, schema: Dict):
        """
        Register a tool that the agent can use

        Args:
            name: Tool name
            func: Python function to execute
            schema: OpenAI-style function schema
        """
        self.tools[name] = func
        self.tool_schemas.append(schema)
        print(f"✓ Registered tool: {name}")

    def call_llm(self, messages: List[Dict]) -> Dict:
        """
        Call the local LLM with messages and tool definitions

        Args:
            messages: Conversation history

        Returns:
            LLM response dictionary
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
        }

        # Include tools if any are registered
        if self.tool_schemas:
            payload["tools"] = self.tool_schemas
            payload["tool_choice"] = "auto"

        print("\n" + "="*80)
        print("📤 SENDING TO LLM - COMPLETE REQUEST PAYLOAD")
        print("="*80)
        print(json.dumps(payload, indent=2))

        # Save request to file
        if self.log_dir:
            self.request_count += 1
            request_file = os.path.join(
                self.log_dir,
                f"request_{self.request_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            )
            with open(request_file, 'w') as f:
                json.dump(payload, f, indent=2)
            print(f"\n💾 Request saved to: {request_file}")

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()

            print("\n" + "="*80)
            print("📥 LLM RESPONSE - COMPLETE RAW RESPONSE")
            print("="*80)
            print(json.dumps(result, indent=2))

            # Save response to file
            if self.log_dir:
                response_file = os.path.join(
                    self.log_dir,
                    f"response_{self.request_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                )
                with open(response_file, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"\n💾 Response saved to: {response_file}")

            return result

        except Exception as e:
            print(f"\n❌ Error calling LLM: {e}")
            if hasattr(e, 'response') and hasattr(e.response, 'text'):
                print(f"Response text: {e.response.text}")
            raise

    def parse_response(self, response: Dict) -> tuple:
        """
        Parse LLM response to extract message content and tool calls

        Args:
            response: Raw LLM response

        Returns:
            Tuple of (text_response, tool_calls)
        """
        print("\n" + "="*80)
        print("🔍 PARSING RESPONSE")
        print("="*80)

        choice = response.get("choices", [{}])[0]
        message = choice.get("message", {})

        text_content = message.get("content", "")
        tool_calls = message.get("tool_calls", [])

        print(f"Text content: {text_content}")
        print(f"Tool calls found: {len(tool_calls)}")

        if tool_calls:
            print("\n📋 Tool Calls:")
            for i, tc in enumerate(tool_calls):
                print(f"\n  Tool Call #{i+1}:")
                print(f"    ID: {tc.get('id')}")
                print(f"    Function: {tc.get('function', {}).get('name')}")
                print(f"    Arguments: {tc.get('function', {}).get('arguments')}")

        return text_content, tool_calls

    def execute_tool(self, tool_name: str, arguments: str) -> Any:
        """
        Execute a registered tool with given arguments

        Args:
            tool_name: Name of the tool to execute
            arguments: JSON string of arguments

        Returns:
            Tool execution result
        """
        print("\n" + "="*80)
        print(f"🔧 EXECUTING TOOL: {tool_name}")
        print("="*80)

        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found"
            print(f"❌ {error_msg}")
            return {"error": error_msg}

        try:
            # Parse arguments
            args = json.loads(arguments)
            print(f"Arguments: {json.dumps(args, indent=2)}")

            # Execute tool
            result = self.tools[tool_name](**args)

            print(f"\n✓ Tool Result:")
            print(json.dumps(result, indent=2) if isinstance(result, dict) else result)

            return result

        except Exception as e:
            error_msg = f"Error executing tool: {str(e)}"
            print(f"❌ {error_msg}")
            return {"error": error_msg}

    def run(self, user_message: str, max_iterations: int = 5) -> str:
        """
        Run the agent with a user message, handling tool calls in a loop

        Args:
            user_message: User's input message
            max_iterations: Maximum number of tool call iterations

        Returns:
            Final agent response
        """
        print("\n" + "🤖 "*40)
        print(f"AGENT RUN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🤖 "*40)

        # Add user message to conversation
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })

        iteration = 0
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'─'*80}")
            print(f"ITERATION {iteration}/{max_iterations}")
            print(f"{'─'*80}")

            # Call LLM
            response = self.call_llm(self.conversation_history)

            # Parse response
            text_content, tool_calls = self.parse_response(response)

            # Add assistant message to history
            assistant_message = {
                "role": "assistant",
                "content": text_content
            }

            if tool_calls:
                assistant_message["tool_calls"] = tool_calls

            self.conversation_history.append(assistant_message)

            # If no tool calls, we're done
            if not tool_calls:
                print("\n" + "✅ "*40)
                print("AGENT RUN COMPLETED - No tool calls")
                print("✅ "*40 + "\n")
                return text_content or ""

            # Execute each tool call
            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_args = tool_call["function"]["arguments"]
                tool_id = tool_call.get("id", "unknown")

                # Execute tool
                result = self.execute_tool(tool_name, tool_args)

                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })

        # If we hit max iterations
        print("\n" + "⚠️  "*40)
        print("AGENT RUN COMPLETED - Max iterations reached")
        print("⚠️  "*40 + "\n")
        return text_content or "Max iterations reached"

    def reset_conversation(self):
        """Reset the conversation history"""
        self.conversation_history = []
        print("🔄 Conversation history reset")


# ============================================================================
# EXAMPLE TOOLS
# ============================================================================

def create_file_tool(filename: str, content: str) -> Dict[str, Any]:
    """
    Tool: Create a file with given content

    Args:
        filename: Name of file to create
        content: Content to write

    Returns:
        Result dictionary
    """
    try:
        with open(filename, 'w') as f:
            f.write(content)
        return {
            "status": "success",
            "message": f"File '{filename}' created successfully",
            "filename": filename,
            "size": len(content)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def read_file_tool(filename: str) -> Dict[str, Any]:
    """
    Tool: Read a file's content

    Args:
        filename: Name of file to read

    Returns:
        Result dictionary
    """
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return {
            "status": "success",
            "content": content,
            "filename": filename,
            "size": len(content)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }


def calculator_tool(operation: str, a: float, b: float) -> Dict[str, Any]:
    """
    Tool: Perform basic calculations

    Args:
        operation: One of 'add', 'subtract', 'multiply', 'divide'
        a: First number
        b: Second number

    Returns:
        Result dictionary
    """
    operations = {
        'add': lambda x, y: x + y,
        'subtract': lambda x, y: x - y,
        'multiply': lambda x, y: x * y,
        'divide': lambda x, y: x / y if y != 0 else None
    }

    if operation not in operations:
        return {
            "status": "error",
            "message": f"Unknown operation: {operation}"
        }

    result = operations[operation](a, b)

    if result is None:
        return {
            "status": "error",
            "message": "Division by zero"
        }

    return {
        "status": "success",
        "operation": operation,
        "a": a,
        "b": b,
        "result": result
    }


def get_current_time_tool() -> Dict[str, Any]:
    """
    Tool: Get current time

    Returns:
        Current time information
    """
    now = datetime.now()
    return {
        "status": "success",
        "datetime": now.strftime("%Y-%m-%d %H:%M:%S"),
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "timestamp": now.timestamp()
    }


# ============================================================================
# TOOL SCHEMAS (OpenAI Function Calling Format)
# ============================================================================

CREATE_FILE_SCHEMA = {
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
}

READ_FILE_SCHEMA = {
    "type": "function",
    "function": {
        "name": "read_file",
        "description": "Read the content of a file",
        "parameters": {
            "type": "object",
            "properties": {
                "filename": {
                    "type": "string",
                    "description": "The name of the file to read"
                }
            },
            "required": ["filename"]
        }
    }
}

CALCULATOR_SCHEMA = {
    "type": "function",
    "function": {
        "name": "calculator",
        "description": "Perform basic arithmetic operations",
        "parameters": {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The arithmetic operation to perform"
                },
                "a": {
                    "type": "number",
                    "description": "The first number"
                },
                "b": {
                    "type": "number",
                    "description": "The second number"
                }
            },
            "required": ["operation", "a", "b"]
        }
    }
}

GET_TIME_SCHEMA = {
    "type": "function",
    "function": {
        "name": "get_current_time",
        "description": "Get the current date and time",
        "parameters": {
            "type": "object",
            "properties": {}
        }
    }
}


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

def create_agent_example():
    """Create an example agent with tools"""
    # Initialize agent
    agent = Agent(
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3-coder-30b"
    )

    # Register tools
    agent.register_tool("create_file", create_file_tool, CREATE_FILE_SCHEMA)
    agent.register_tool("read_file", read_file_tool, READ_FILE_SCHEMA)
    agent.register_tool("calculator", calculator_tool, CALCULATOR_SCHEMA)
    agent.register_tool("get_current_time", get_current_time_tool, GET_TIME_SCHEMA)

    return agent


if __name__ == "__main__":
    # Create agent
    agent = create_agent_example()

    # Example 1: Ask agent to create a file
    print("\n" + "="*80)
    print("EXAMPLE 1: Create a file")
    print("="*80)
    response = agent.run("Create a file called 'test.txt' with the content 'Hello from the agent!'")
    print(f"\n📝 Final Response: {response}")

    # Reset for next example
    agent.reset_conversation()

    # Example 2: Use calculator
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Use calculator")
    print("="*80)
    response = agent.run("What is 15 multiplied by 7?")
    print(f"\n📝 Final Response: {response}")
