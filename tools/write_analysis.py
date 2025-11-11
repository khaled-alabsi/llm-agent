"""Write Analysis Tool - Write analysis results to files"""

import os
from typing import Dict, Any


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


# Tool schema
SCHEMA = {
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
