"""Read File Tool - Reads files from source code or context directory"""

import os
from typing import Dict, Any


def read_file_tool(file_path: str, source_code_path: str, context_dir: str) -> Dict[str, Any]:
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
            for root, _, files in os.walk(context_dir):
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


# Tool schema
SCHEMA = {
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
}
