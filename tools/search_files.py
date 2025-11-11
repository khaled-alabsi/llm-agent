"""Search Files Tool - Search for files matching glob patterns"""

import os
import glob
from typing import Dict, Any


def search_files_tool(
    pattern: str,
    base_path: str = "",
    search_in: str = "source",
    source_code_path: str = "",
    context_dir: str = ""
) -> Dict[str, Any]:
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


# Tool schema
SCHEMA = {
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
}
