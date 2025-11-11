"""
Code Analyzer Agent
Analyzes monolith source code following context-driven discovery process
"""

import json
import requests
import os
import glob
from typing import List, Dict, Callable, Any, Optional
from datetime import datetime


class CodeAnalyzerAgent:
    """
    Agent that analyzes source code based on context documents.

    This agent:
    1. Reads context documents (start-here.md, architecture docs, skills)
    2. Uses tools to analyze source code
    3. Follows discovery process to generate migration documentation
    """

    def __init__(
        self,
        context_start_path: str,
        app_name: str,
        pattern: str,
        source_code_path: str,
        base_url: str = "http://localhost:1234/v1",
        model: str = "qwen/qwen3-coder-30b",
        log_dir: Optional[str] = "logs"
    ):
        """
        Initialize the code analyzer agent

        Args:
            context_start_path: Path to start-here.md (entry point for context)
            app_name: Name of the application to analyze (e.g., "cbv")
            pattern: Pattern type - "ucc" or "legacy"
            source_code_path: Path to source code directory to analyze
            base_url: LLM API endpoint
            model: Model identifier
            log_dir: Directory to save logs (None to disable)
        """
        self.context_start_path = context_start_path
        self.app_name = app_name
        self.pattern = pattern.lower()
        self.source_code_path = source_code_path
        self.base_url = base_url
        self.model = model
        self.log_dir = log_dir
        self.request_count = 0

        # Validate inputs
        if self.pattern not in ["ucc", "legacy"]:
            raise ValueError(f"Pattern must be 'ucc' or 'legacy', got: {pattern}")

        if not os.path.exists(self.context_start_path):
            raise ValueError(f"Context start path not found: {context_start_path}")

        if not os.path.exists(self.source_code_path):
            raise ValueError(f"Source code path not found: {source_code_path}")

        # Setup
        self.tools: Dict[str, Callable] = {}
        self.tool_schemas: List[Dict] = []
        self.conversation_history: List[Dict] = []

        # Create session-based log directory
        self.session_dir = None
        self.tool_log_dir = None
        self.llm_log_dir = None
        self.log_counter = 0  # Shared counter for all logs

        if self.log_dir:
            # Create session folder with timestamp
            session_name = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            self.session_dir = os.path.join(self.log_dir, session_name)
            self.tool_log_dir = os.path.join(self.session_dir, "tool")
            self.llm_log_dir = os.path.join(self.session_dir, "llm")

            os.makedirs(self.tool_log_dir, exist_ok=True)
            os.makedirs(self.llm_log_dir, exist_ok=True)

            print(f"📁 Session logging enabled: {os.path.abspath(self.session_dir)}")
            print(f"   Tool logs: {self.tool_log_dir}")
            print(f"   LLM logs: {self.llm_log_dir}")

        # Context directory (where architecture docs, skills, templates are)
        self.context_dir = os.path.dirname(self.context_start_path)

        print(f"\n🔍 Code Analyzer Agent Initialized")
        print(f"   App Name: {self.app_name}")
        print(f"   Pattern: {self.pattern}")
        print(f"   Source Code: {self.source_code_path}")
        print(f"   Context: {self.context_start_path}")

    def register_tool(self, name: str, func: Callable, schema: Dict):
        """Register a tool for the agent"""
        self.tools[name] = func
        self.tool_schemas.append(schema)
        print(f"✓ Registered tool: {name}")

    def call_llm(self, messages: List[Dict]) -> Dict:
        """Call the LLM with messages and tools"""
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 4000,
        }

        if self.tool_schemas:
            payload["tools"] = self.tool_schemas
            payload["tool_choice"] = "auto"

        print("\n" + "="*80)
        print("📤 SENDING TO LLM")
        print("="*80)
        print(f"Messages: {len(messages)}")
        print(f"Tools available: {len(self.tool_schemas)}")

        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            result = response.json()

            print("📥 LLM Response received")

            # Save request and response in one file
            if self.llm_log_dir:
                self.log_counter += 1
                log_file = os.path.join(
                    self.llm_log_dir,
                    f"{self.log_counter:03d}_request_response.json"
                )

                log_data = {
                    "log_number": self.log_counter,
                    "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    "request": payload,
                    "response": result
                }

                with open(log_file, 'w') as f:
                    json.dump(log_data, f, indent=2)

                print(f"💾 Logged to: {log_file}")

            return result

        except Exception as e:
            print(f"\n❌ Error calling LLM: {e}")
            raise

    def parse_response(self, response: Dict) -> tuple:
        """Parse LLM response to extract content and tool calls"""
        choice = response.get("choices", [{}])[0]
        message = choice.get("message", {})

        text_content = message.get("content", "")
        tool_calls = message.get("tool_calls", [])

        if tool_calls:
            print(f"\n🔧 Tool calls requested: {len(tool_calls)}")
            for tc in tool_calls:
                print(f"   - {tc.get('function', {}).get('name')}")

        return text_content, tool_calls

    def execute_tool(self, tool_name: str, arguments: str) -> Any:
        """Execute a registered tool"""
        print(f"\n🔧 Executing: {tool_name}")

        if tool_name not in self.tools:
            error_msg = f"Tool '{tool_name}' not found"
            print(f"❌ {error_msg}")
            return {"error": error_msg}

        try:
            args = json.loads(arguments)
            print(f"   Args: {json.dumps(args, indent=2)[:100]}...")

            # Execute tool
            result = self.tools[tool_name](**args)

            print(f"   ✓ Executed successfully")

            # Log tool usage
            if self.tool_log_dir:
                self.log_counter += 1
                log_file = os.path.join(
                    self.tool_log_dir,
                    f"{self.log_counter:03d}_{tool_name}.log"
                )

                log_content = f"""Tool Execution Log
{'='*80}
Log Number: {self.log_counter}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Tool Name: {tool_name}

INPUT FROM AGENT:
{'='*80}
{json.dumps(args, indent=2)}

OUTPUT FROM TOOL:
{'='*80}
{json.dumps(result, indent=2) if isinstance(result, (dict, list)) else str(result)}
"""

                with open(log_file, 'w') as f:
                    f.write(log_content)

                print(f"💾 Tool logged to: {log_file}")

            return result

        except Exception as e:
            error_msg = f"Error executing tool: {str(e)}"
            print(f"❌ {error_msg}")

            error_result = {"status": "error", "message": error_msg}

            # Log error
            if self.tool_log_dir:
                self.log_counter += 1
                log_file = os.path.join(
                    self.tool_log_dir,
                    f"{self.log_counter:03d}_{tool_name}_ERROR.log"
                )

                log_content = f"""Tool Execution Log (ERROR)
{'='*80}
Log Number: {self.log_counter}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Tool Name: {tool_name}

INPUT FROM AGENT:
{'='*80}
{arguments}

ERROR:
{'='*80}
{error_msg}
"""

                with open(log_file, 'w') as f:
                    f.write(log_content)

            return error_result

    def run(self, task: str, max_iterations: int = 10) -> str:
        """
        Run the analyzer with a task

        Args:
            task: Task description (e.g., "Analyze cbv app following UCC pattern")
            max_iterations: Max tool call iterations

        Returns:
            Final response
        """
        print("\n" + "🤖 "*40)
        print(f"CODE ANALYZER RUN STARTED: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🤖 "*40)

        # Add user message
        self.conversation_history.append({
            "role": "user",
            "content": task
        })

        iteration = 0
        text_content = ""  # Initialize to avoid unbound variable warning
        while iteration < max_iterations:
            iteration += 1
            print(f"\n{'─'*80}")
            print(f"ITERATION {iteration}/{max_iterations}")
            print(f"{'─'*80}")

            # Call LLM
            response = self.call_llm(self.conversation_history)

            # Parse response
            text_content, tool_calls = self.parse_response(response)

            # Add assistant message
            assistant_message = {
                "role": "assistant",
                "content": text_content
            }

            if tool_calls:
                assistant_message["tool_calls"] = tool_calls

            self.conversation_history.append(assistant_message)

            # If no tool calls, done
            if not tool_calls:
                print("\n" + "✅ "*40)
                print("ANALYZER RUN COMPLETED")
                print("✅ "*40 + "\n")
                return text_content or ""

            # Execute tools
            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                tool_args = tool_call["function"]["arguments"]
                tool_id = tool_call.get("id", "unknown")

                result = self.execute_tool(tool_name, tool_args)

                # Add tool result to conversation
                self.conversation_history.append({
                    "role": "tool",
                    "tool_call_id": tool_id,
                    "name": tool_name,
                    "content": json.dumps(result)
                })

        print("\n" + "⚠️  "*40)
        print("ANALYZER RUN COMPLETED - Max iterations reached")
        print("⚠️  "*40 + "\n")
        return text_content or "Max iterations reached"

    def reset_conversation(self):
        """Reset conversation history"""
        self.conversation_history = []
        print("🔄 Conversation reset")


# ============================================================================
# CODE ANALYSIS TOOLS
# ============================================================================

def create_code_analysis_tools(source_code_path: str, context_dir: str):
    """
    Create tools for code analysis

    Args:
        source_code_path: Path to source code to analyze
        context_dir: Path to context directory (for reading docs)

    Returns:
        Tuple of (tools_dict, schemas_list)
    """

    # Tool 1: Read File
    def read_file_tool(file_path: str) -> Dict[str, Any]:
        """Read a file from source code or context directory with smart path resolution"""
        try:
            paths_to_try = []

            # If absolute path, try it directly
            if os.path.isabs(file_path):
                paths_to_try.append(file_path)
            else:
                # Strategy 1: Try as-is relative to source code
                paths_to_try.append(os.path.join(source_code_path, file_path))

                # Strategy 2: Try as-is relative to context dir
                paths_to_try.append(os.path.join(context_dir, file_path))

                # Strategy 3: Auto-correct common path issues
                # If path starts with "context/v1/", strip it and try with context_dir
                if file_path.startswith("context/v1/"):
                    stripped = file_path.replace("context/v1/", "", 1)
                    paths_to_try.append(os.path.join(context_dir, stripped))

                # If path starts with "context/", strip it and try with context_dir parent
                if file_path.startswith("context/"):
                    stripped = file_path.replace("context/", "", 1)
                    context_parent = os.path.dirname(context_dir)
                    paths_to_try.append(os.path.join(context_parent, stripped))

                # Strategy 4: Try just the basename in context dir
                basename = os.path.basename(file_path)
                paths_to_try.append(os.path.join(context_dir, basename))

                # Strategy 5: Search recursively in context dir for the basename
                for root, dirs, files in os.walk(context_dir):
                    if basename in files:
                        paths_to_try.append(os.path.join(root, basename))
                        break

            # Try each path until one works
            for attempt_path in paths_to_try:
                if os.path.exists(attempt_path):
                    with open(attempt_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    return {
                        "status": "success",
                        "file_path": attempt_path,
                        "resolved_from": file_path,
                        "content": content,
                        "size": len(content)
                    }

            # If no path worked, return error with all attempts
            return {
                "status": "error",
                "message": f"File not found. Tried paths: {paths_to_try[:3]}... ({len(paths_to_try)} total)",
                "file_path": file_path,
                "paths_tried": len(paths_to_try)
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e),
                "file_path": file_path
            }

    # Tool 2: Search Files (glob pattern)
    def search_files_tool(pattern: str, base_path: str = "", search_in: str = "source") -> Dict[str, Any]:
        """Search for files matching a pattern in source code or context"""
        try:
            # Choose root directory based on search_in parameter
            root_path = context_dir if search_in == "context" else source_code_path
            search_path = os.path.join(root_path, base_path) if base_path else root_path
            full_pattern = os.path.join(search_path, pattern)

            matches = glob.glob(full_pattern, recursive=True)

            # Make paths relative to root_path for cleaner output
            relative_matches = [
                os.path.relpath(m, root_path) for m in matches
            ]

            return {
                "status": "success",
                "pattern": pattern,
                "search_in": search_in,
                "root_path": root_path,
                "matches": relative_matches[:100],  # Limit to 100 results
                "count": len(matches),
                "truncated": len(matches) > 100
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    # Tool 3: Grep Code
    def grep_code_tool(
        search_term: str,
        file_pattern: str = "*.java",
        base_path: str = "",
        max_results: int = 50,
        search_in: str = "source"
    ) -> Dict[str, Any]:
        """Search for code patterns in files in source code or context"""
        try:
            # Choose root directory based on search_in parameter
            root_path = context_dir if search_in == "context" else source_code_path
            search_path = os.path.join(root_path, base_path) if base_path else root_path
            pattern_path = os.path.join(search_path, "**", file_pattern)

            results = []
            files_searched = 0

            for file_path in glob.glob(pattern_path, recursive=True):
                if len(results) >= max_results:
                    break

                try:
                    files_searched += 1
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        for line_num, line in enumerate(f, 1):
                            if search_term in line:
                                results.append({
                                    "file": os.path.relpath(file_path, root_path),
                                    "line": line_num,
                                    "content": line.strip()
                                })

                                if len(results) >= max_results:
                                    break
                except:
                    continue

            return {
                "status": "success",
                "search_term": search_term,
                "search_in": search_in,
                "root_path": root_path,
                "results": results,
                "files_searched": files_searched,
                "matches_found": len(results),
                "truncated": len(results) >= max_results
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    # Tool 4: Write Analysis Output
    def write_analysis_tool(filename: str, content: str, output_dir: str = "output") -> Dict[str, Any]:
        """Write analysis results to file"""
        try:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, filename)

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)

            return {
                "status": "success",
                "file_path": output_path,
                "size": len(content)
            }
        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }

    # Tool schemas
    tools = {
        "read_file": read_file_tool,
        "search_files": search_files_tool,
        "grep_code": grep_code_tool,
        "write_analysis": write_analysis_tool
    }

    schemas = [
        {
            "type": "function",
            "function": {
                "name": "read_file",
                "description": "Read a file from source code or context directory. Auto-corrects common path issues. You can use relative paths, absolute paths, or partial paths - the tool will find the file.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "file_path": {
                            "type": "string",
                            "description": "Path to file. Can be: absolute path, relative to source, relative to context, or just filename. Examples: 'start-here.md', 'context/v1/start-here.md', 'architecture/architecture-overview.md'"
                        }
                    },
                    "required": ["file_path"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "search_files",
                "description": "Search for files matching a glob pattern. Can search in source code or context directories.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "pattern": {
                            "type": "string",
                            "description": "Glob pattern to match files (e.g., '**/*Controller.java', '**/*.md')"
                        },
                        "base_path": {
                            "type": "string",
                            "description": "Optional base path within the search directory (e.g., 'ucc/cbv', 'architecture')"
                        },
                        "search_in": {
                            "type": "string",
                            "enum": ["source", "context"],
                            "description": "Where to search: 'source' for source code directory, 'context' for context/documentation directory (default: 'source')"
                        }
                    },
                    "required": ["pattern"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "grep_code",
                "description": "Search for text/code patterns in files. Can search in source code or context directories. Returns matching lines with file path and line number.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "search_term": {
                            "type": "string",
                            "description": "Text or code to search for"
                        },
                        "file_pattern": {
                            "type": "string",
                            "description": "File pattern to search in (default: '*.java', use '*.md' for markdown, etc.)"
                        },
                        "base_path": {
                            "type": "string",
                            "description": "Optional base path to search within"
                        },
                        "max_results": {
                            "type": "number",
                            "description": "Maximum results to return (default: 50)"
                        },
                        "search_in": {
                            "type": "string",
                            "enum": ["source", "context"],
                            "description": "Where to search: 'source' for source code directory, 'context' for context/documentation directory (default: 'source')"
                        }
                    },
                    "required": ["search_term"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "write_analysis",
                "description": "Write analysis results to an output file (markdown, json, etc.)",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "filename": {
                            "type": "string",
                            "description": "Output filename (e.g., 'entrypoints.md')"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write"
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Output directory (default: 'output')"
                        }
                    },
                    "required": ["filename", "content"]
                }
            }
        }
    ]

    return tools, schemas
