# Adding Custom Tools Guide

Learn how to create and register custom tools for the CrewAI agent.

## What Are Tools?

Tools are functions that the agent can call to perform actions:
- File operations (create, read, delete)
- Code execution
- API calls
- Database operations
- Web scraping
- Anything the agent needs to do!

## Quick Example

```python
from crewai.tools import tool

@tool("Calculate Sum")
def sum_numbers(a: int, b: int) -> str:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum as a string
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}"
```

## Step-by-Step Guide

### Step 1: Create Tool File

Create a new file in `tools/` directory:

```bash
touch tools/my_tools.py
```

### Step 2: Define Tool Function

```python
# tools/my_tools.py
from crewai.tools import tool
from typing import Dict, Any

@tool("Tool Name")
def my_custom_tool(param1: str, param2: int) -> str:
    """
    Brief description of what the tool does.
    This docstring is crucial - the agent reads it to understand when to use the tool!

    Args:
        param1: Description of first parameter
        param2: Description of second parameter

    Returns:
        Description of return value

    Example:
        my_custom_tool('hello', 42)
    """
    try:
        # Tool logic here
        result = f"Processed {param1} with {param2}"
        return f"✓ Success: {result}"

    except Exception as e:
        return f"✗ Error: {str(e)}"
```

### Step 3: Export Tool

Add to `tools/__init__.py`:

```python
from .my_tools import my_custom_tool

__all__ = [
    # ... existing tools ...
    'my_custom_tool',
]
```

### Step 4: Register Tool

Add to agent in `core/agent_factory.py`:

```python
from tools.my_tools import my_custom_tool

def create_coder_agent(llm=None, verbose=True) -> Agent:
    # ... existing code ...

    agent = Agent(
        role=role,
        goal=goal,
        backstory=enhanced_backstory,
        llm=llm,
        tools=[
            # ... existing tools ...
            my_custom_tool,  # Add your tool here
        ],
        verbose=verbose,
    )

    return agent
```

### Step 5: Test Tool

Create a test script:

```python
# test_my_tool.py
from tools.my_tools import my_custom_tool

result = my_custom_tool('test', 123)
print(result)
```

Run: `python test_my_tool.py`

## Tool Best Practices

### 1. Clear Documentation
```python
@tool("Descriptive Name")
def tool_function(param: type) -> str:
    """
    DO: Write clear, detailed description
    DO: Explain when to use this tool
    DO: Provide examples
    DON'T: Leave docstring empty or vague
    """
```

### 2. Type Hints
```python
# ✅ Good: Clear types
def create_file(path: str, content: str) -> str:
    pass

# ❌ Bad: No type hints
def create_file(path, content):
    pass
```

### 3. Error Handling
```python
@tool("Safe Tool")
def safe_tool(param: str) -> str:
    try:
        # Tool logic
        result = do_something(param)
        return f"✓ Success: {result}"

    except FileNotFoundError as e:
        return f"✗ File not found: {str(e)}"

    except Exception as e:
        return f"✗ Error: {str(e)}"
```

### 4. Consistent Return Format
```python
# Always return strings with clear success/failure indication
return "✓ Success: operation completed"
return "✗ Error: something went wrong"
return "⚠ Warning: partial success"
```

### 5. Validation
```python
@tool("Validated Tool")
def validated_tool(file_path: str) -> str:
    # Validate input
    if not file_path.endswith('.txt'):
        return "✗ Error: Only .txt files allowed"

    if len(file_path) > 255:
        return "✗ Error: Path too long"

    # Proceed with logic
    # ...
```

## Tool Examples

### Example 1: API Call Tool

```python
import requests
from crewai_tools import tool

@tool("Fetch Data from API")
def fetch_api_data(url: str) -> str:
    """
    Fetch data from a REST API endpoint.

    Args:
        url: API endpoint URL

    Returns:
        JSON response as string
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return f"✓ Data fetched: {response.json()}"

    except requests.Timeout:
        return "✗ Error: Request timed out"

    except requests.HTTPError as e:
        return f"✗ HTTP Error: {e.response.status_code}"

    except Exception as e:
        return f"✗ Error: {str(e)}"
```

### Example 2: Database Tool

```python
import sqlite3
from crewai_tools import tool

@tool("Query Database")
def query_database(query: str) -> str:
    """
    Execute a SELECT query on the local database.

    Args:
        query: SQL SELECT query

    Returns:
        Query results as formatted string

    Security: Only SELECT queries are allowed.
    """
    # Security check
    if not query.strip().upper().startswith('SELECT'):
        return "✗ Error: Only SELECT queries allowed"

    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        conn.close()

        return f"✓ Found {len(results)} rows: {results}"

    except sqlite3.Error as e:
        return f"✗ Database error: {str(e)}"
```

### Example 3: Web Scraping Tool

```python
from crewai_tools import tool
import requests
from bs4 import BeautifulSoup

@tool("Scrape Website")
def scrape_website(url: str) -> str:
    """
    Scrape content from a website.

    Args:
        url: Website URL to scrape

    Returns:
        Extracted text content
    """
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Extract text
        text = soup.get_text(separator=' ', strip=True)

        # Limit length
        if len(text) > 1000:
            text = text[:1000] + '...'

        return f"✓ Scraped content: {text}"

    except Exception as e:
        return f"✗ Error scraping: {str(e)}"
```

### Example 4: Code Execution Tool

```python
from crewai_tools import tool
import subprocess

@tool("Run Python Code")
def run_python_code(code: str) -> str:
    """
    Execute Python code in a safe subprocess.

    Args:
        code: Python code to execute

    Returns:
        Output of the code execution

    Warning: Be careful with untrusted code!
    """
    try:
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True,
            timeout=5
        )

        if result.returncode == 0:
            return f"✓ Output: {result.stdout}"
        else:
            return f"✗ Error: {result.stderr}"

    except subprocess.TimeoutExpired:
        return "✗ Error: Execution timed out"

    except Exception as e:
        return f"✗ Error: {str(e)}"
```

## Tool Categories

### File Tools
- Create, read, update, delete files
- List directories
- Check file existence
- Get file metadata

### Code Tools
- Format code
- Validate syntax
- Run linters
- Execute code

### Data Tools
- Query databases
- Parse JSON/CSV/XML
- Transform data
- Validate data

### Network Tools
- API calls
- Web scraping
- File downloads
- Webhooks

### System Tools
- Run commands
- Check system status
- Manage processes
- Environment variables

## Advanced Topics

### Stateful Tools

```python
class DatabaseConnection:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = sqlite3.connect('db.sqlite')

# Tool with state
db = DatabaseConnection()

@tool("Connect Database")
def connect_db() -> str:
    db.connect()
    return "✓ Connected"
```

### Async Tools

```python
import asyncio
from crewai_tools import tool

@tool("Async API Call")
def async_api_call(url: str) -> str:
    async def fetch():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.text()

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(fetch())
    return f"✓ Data: {result}"
```

### Tool Chaining

```python
@tool("Download and Process")
def download_and_process(url: str) -> str:
    # Use other tools
    download_result = download_file_tool(url)
    if '✗' in download_result:
        return download_result

    process_result = process_file_tool('downloaded.txt')
    return process_result
```

## Testing Tools

### Unit Test Example

```python
# tests/test_my_tool.py
def test_my_custom_tool():
    result = my_custom_tool('test', 42)
    assert '✓' in result
    assert 'Success' in result

def test_my_custom_tool_error():
    result = my_custom_tool('', -1)
    assert '✗' in result
```

### Integration Test

```python
def test_tool_with_agent():
    agent = create_coder_agent()
    task = Task(
        description="Use my_custom_tool with param 'test' and 42",
        agent=agent
    )
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
    assert result is not None
```

## Debugging Tools

### Add Logging

```python
from helpers.logger import SessionLogger

logger = SessionLogger()

@tool("Logged Tool")
def logged_tool(param: str) -> str:
    logger.log_info(f"Tool called with: {param}")

    try:
        result = do_something(param)
        logger.log_info(f"Tool succeeded: {result}")
        return f"✓ {result}"

    except Exception as e:
        logger.log_error("tool_error", str(e))
        return f"✗ Error: {e}"
```

### Print Debugging

```python
@tool("Debug Tool")
def debug_tool(param: str) -> str:
    print(f"DEBUG: Tool called with {param}")
    result = process(param)
    print(f"DEBUG: Result is {result}")
    return result
```

## Common Pitfalls

### ❌ Don't: Forget Error Handling
```python
def bad_tool(path):
    file = open(path)  # Will crash if file doesn't exist!
    return file.read()
```

### ✅ Do: Handle Errors
```python
def good_tool(path: str) -> str:
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return "✗ File not found"
```

### ❌ Don't: Return Complex Objects
```python
def bad_tool() -> dict:
    return {"key": "value"}  # Agent can't handle dict!
```

### ✅ Do: Return Strings
```python
def good_tool() -> str:
    return "✓ key=value"  # Agent can understand this
```

### ❌ Don't: Side Effects Without Validation
```python
def bad_tool(path):
    os.system(f"rm -rf {path}")  # DANGEROUS!
```

### ✅ Do: Validate and Confirm
```python
def good_tool(path: str) -> str:
    if '..' in path or path.startswith('/'):
        return "✗ Invalid path"

    if not path.startswith('./output/'):
        return "✗ Must be in output directory"

    # Safe to proceed
```

## Next Steps

- [API Reference - Tools](../api/tools.md) - Complete API documentation
- [Creating Agents](creating-agents.md) - Use your tools with agents
- [Code Structure](../architecture/code-structure.md) - Understand the codebase
