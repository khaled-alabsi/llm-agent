"""
Code manipulation and validation tools
"""

import json
from crewai.tools import tool


@tool("Format Code")
def format_code_tool(code: str, language: str = "javascript") -> str:
    """
    Format code for better readability.
    This is a basic formatter - just returns the code with validation.

    Args:
        code: Code to format
        language: Programming language (javascript, python, html, css)

    Returns:
        Formatted code or error message
    """
    try:
        # Basic validation
        if not code.strip():
            return "✗ Error: Code is empty"

        # For now, just return the code
        # In production, you might use prettier, black, etc.
        return code

    except Exception as e:
        return f"✗ Error formatting code: {str(e)}"


@tool("Validate JSON")
def validate_json_tool(json_string: str) -> str:
    """
    Validate JSON syntax.
    Use this to verify package.json, config files, etc. are valid.

    Args:
        json_string: JSON string to validate

    Returns:
        Validation result message

    Example:
        validate_json_tool('{"name": "my-app", "version": "1.0.0"}')
    """
    try:
        json.loads(json_string)
        return "✓ JSON is valid"

    except json.JSONDecodeError as e:
        return f"✗ Invalid JSON: {str(e)}"

    except Exception as e:
        return f"✗ Error validating JSON: {str(e)}"
