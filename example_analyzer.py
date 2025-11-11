"""
Example: How to use the Code Analyzer Agent

This script demonstrates how to set up and use the CodeAnalyzerAgent
to analyze source code following the context-driven discovery process.
"""

from code_analyzer_agent import CodeAnalyzerAgent, create_code_analysis_tools


def main():
    # Configuration
    CONTEXT_START = "/Users/Khaled.Alabsi/projects/llm-agent/context/v1/start-here.md"
    APP_NAME = "cbv"
    PATTERN = "ucc"
    SOURCE_CODE = "/Users/Khaled.Alabsi/projects/llm-agent/source-code"

    # Create the agent
    print("Creating Code Analyzer Agent...")
    agent = CodeAnalyzerAgent(
        context_start_path=CONTEXT_START,
        app_name=APP_NAME,
        pattern=PATTERN,
        source_code_path=SOURCE_CODE,
        base_url="http://localhost:1234/v1",
        model="qwen/qwen3-coder-30b",
        log_dir="analyzer_logs"
    )

    # Register code analysis tools
    print("\nRegistering code analysis tools...")
    tools, schemas = create_code_analysis_tools(
        source_code_path=SOURCE_CODE,
        context_dir=agent.context_dir
    )

    for tool_name, (tool_func, schema) in zip(tools.keys(), zip(tools.values(), schemas)):
        agent.register_tool(tool_name, tool_func, schema)

    # Example 1: Ask agent to read the start-here.md and understand the task
    print("\n" + "="*80)
    print("EXAMPLE 1: Understanding the Discovery Process")
    print("="*80)

    task = f"""
Read the context file at '{CONTEXT_START}' and understand the discovery process for a {PATTERN.upper()} pattern application.

Then explain:
1. What are the main phases of the discovery process?
2. What tools do you have available to analyze the code?
3. What outputs should be generated?

Application: {APP_NAME}
Pattern: {PATTERN}
"""

    response = agent.run(task, max_iterations=5)
    print("\n" + "="*80)
    print("AGENT RESPONSE:")
    print("="*80)
    print(response)

    # Example 2: Discover entrypoints (Phase 1, Step 1)
    print("\n\n" + "="*80)
    print("EXAMPLE 2: Discover Entrypoints (Phase 1, Step 1)")
    print("="*80)

    agent.reset_conversation()

    task = f"""
Following the UCC pattern discovery process for the '{APP_NAME}' application:

1. Read the context document at '{CONTEXT_START}' to understand Phase 1, Step 1 (Discover Entrypoints)
2. Search for REST controllers in the source code at '{SOURCE_CODE}'
3. Search for LSG pages
4. Document your findings

Use your tools to search the code and create an initial analysis.
"""

    response = agent.run(task, max_iterations=10)
    print("\n" + "="*80)
    print("AGENT RESPONSE:")
    print("="*80)
    print(response)


if __name__ == "__main__":
    main()
