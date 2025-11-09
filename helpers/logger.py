"""
Session-based logging system with structured output
One log file per session with detailed tracking
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional
from rich.console import Console
from rich.logging import RichHandler


class SessionLogger:
    """
    Session-based logger that writes to a single file per session
    Tracks all agent activity with timestamps and structured data
    """

    def __init__(self, session_id: Optional[str] = None, log_dir: str = "./logs"):
        """
        Initialize session logger

        Args:
            session_id: Unique session identifier (auto-generated if None)
            log_dir: Directory to store log files
        """
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)

        # Generate session ID if not provided
        if session_id is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.session_id = f"session_{timestamp}"
        else:
            self.session_id = session_id

        # Create session log file
        self.log_file = self.log_dir / f"{self.session_id}.log"
        self.json_log_file = self.log_dir / f"{self.session_id}.json"

        # Initialize session data
        self.session_data = {
            "session_id": self.session_id,
            "start_time": datetime.now().isoformat(),
            "events": [],
            "metrics": {
                "total_llm_calls": 0,
                "total_tool_calls": 0,
                "total_tokens": 0,
                "errors": 0,
            }
        }

        # Setup console
        self.console = Console()

        # Setup file logger
        self._setup_file_logger()

        # Log session start
        self.log_event("session_start", {"session_id": self.session_id})

    def _setup_file_logger(self):
        """Setup file-based logging"""
        self.file_logger = logging.getLogger(f"session_{self.session_id}")
        self.file_logger.setLevel(logging.DEBUG)

        # File handler
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setLevel(logging.DEBUG)

        # Format
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)

        self.file_logger.addHandler(file_handler)

    def log_event(self, event_type: str, data: Dict[str, Any]):
        """
        Log an event to the session

        Args:
            event_type: Type of event (e.g., 'llm_call', 'tool_execution')
            data: Event data dictionary
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "type": event_type,
            "data": data
        }

        self.session_data["events"].append(event)

        # Log to file
        self.file_logger.info(f"{event_type.upper()}: {json.dumps(data, indent=2)}")

        # Save JSON file
        self._save_json_log()

    def log_llm_call(self, request: Dict, response: Dict, duration: float):
        """
        Log LLM API call

        Args:
            request: Request payload
            response: Response data
            duration: Call duration in seconds
        """
        self.session_data["metrics"]["total_llm_calls"] += 1

        # Extract token usage if available
        usage = response.get("usage", {})
        if usage:
            self.session_data["metrics"]["total_tokens"] += usage.get("total_tokens", 0)

        self.log_event("llm_call", {
            "duration_seconds": duration,
            "model": request.get("model"),
            "prompt_tokens": usage.get("prompt_tokens"),
            "completion_tokens": usage.get("completion_tokens"),
            "total_tokens": usage.get("total_tokens"),
            "request_size": len(json.dumps(request)),
            "response_size": len(json.dumps(response)),
        })

    def log_tool_call(self, tool_name: str, arguments: Dict, result: Any, duration: float, success: bool = True):
        """
        Log tool execution

        Args:
            tool_name: Name of the tool
            arguments: Tool arguments
            result: Tool result
            duration: Execution duration in seconds
            success: Whether execution was successful
        """
        self.session_data["metrics"]["total_tool_calls"] += 1

        if not success:
            self.session_data["metrics"]["errors"] += 1

        self.log_event("tool_call", {
            "tool_name": tool_name,
            "arguments": arguments,
            "result": str(result)[:500],  # Truncate long results
            "duration_seconds": duration,
            "success": success,
        })

    def log_error(self, error_type: str, error_message: str, context: Optional[Dict] = None):
        """
        Log an error

        Args:
            error_type: Type of error
            error_message: Error message
            context: Additional context
        """
        self.session_data["metrics"]["errors"] += 1

        self.log_event("error", {
            "error_type": error_type,
            "message": error_message,
            "context": context or {},
        })

        # Also log to console
        self.console.print(f"[red]ERROR: {error_message}[/red]")

    def log_info(self, message: str, data: Optional[Dict] = None):
        """Log informational message"""
        self.file_logger.info(message)
        if data:
            self.log_event("info", {"message": message, **data})

    def log_debug(self, message: str):
        """Log debug message"""
        self.file_logger.debug(message)

    def print_info(self, message: str):
        """Print info to console"""
        self.console.print(f"[blue]ℹ[/blue] {message}")

    def print_success(self, message: str):
        """Print success message to console"""
        self.console.print(f"[green]✓[/green] {message}")

    def print_warning(self, message: str):
        """Print warning to console"""
        self.console.print(f"[yellow]⚠[/yellow] {message}")

    def print_error(self, message: str):
        """Print error to console"""
        self.console.print(f"[red]✗[/red] {message}")

    def print_section(self, title: str):
        """Print section header"""
        self.console.rule(f"[bold]{title}[/bold]")

    def _save_json_log(self):
        """Save current session data to JSON file"""
        with open(self.json_log_file, 'w') as f:
            json.dump(self.session_data, f, indent=2)

    def end_session(self):
        """End the session and save final logs"""
        self.session_data["end_time"] = datetime.now().isoformat()

        # Calculate total duration
        start = datetime.fromisoformat(self.session_data["start_time"])
        end = datetime.fromisoformat(self.session_data["end_time"])
        duration = (end - start).total_seconds()

        self.session_data["duration_seconds"] = duration

        self.log_event("session_end", {
            "duration_seconds": duration,
            "metrics": self.session_data["metrics"]
        })

        # Save final JSON
        self._save_json_log()

        # Print summary
        self.print_section("Session Summary")
        self.console.print(f"Session ID: {self.session_id}")
        self.console.print(f"Duration: {duration:.2f} seconds")
        self.console.print(f"LLM Calls: {self.session_data['metrics']['total_llm_calls']}")
        self.console.print(f"Tool Calls: {self.session_data['metrics']['total_tool_calls']}")
        self.console.print(f"Total Tokens: {self.session_data['metrics']['total_tokens']}")
        self.console.print(f"Errors: {self.session_data['metrics']['errors']}")
        self.console.print(f"\nLogs saved to: {self.log_file}")


def setup_logging(level: str = "INFO") -> logging.Logger:
    """
    Setup application-wide logging

    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR)

    Returns:
        Configured logger
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True)]
    )

    return logging.getLogger("crewai_coder")
