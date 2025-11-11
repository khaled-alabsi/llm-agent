"""Grep Code Tool - Search for code patterns in files"""

import os
import glob
from typing import Dict, Any


def grep_code_tool(
    search_term: str,
    file_pattern: str = "*.java",
    base_path: str = "",
    max_results: int = 50,
    search_in: str = "source",
    source_code_path: str = "",
    context_dir: str = ""
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


# Tool schema
SCHEMA = {
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
}
