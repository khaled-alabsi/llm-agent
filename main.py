"""
Main entry point for CrewAI Coder Agent
Run this script to execute the agent
"""

import sys
import time
from datetime import datetime

from helpers.logger import SessionLogger
from helpers.config_loader import load_config
from core.agent_factory import create_coder_crew


def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("CrewAI Coder Agent - Personal Website Builder")
    print("=" * 80 + "\n")

    # Load configuration
    print("Loading configuration...")
    config = load_config()
    print(f"✓ Configuration loaded from config.yaml\n")

    # Setup session logging
    session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    logger = SessionLogger(session_id=session_id)

    logger.print_section("Initializing Agent")
    logger.print_info(f"Session ID: {session_id}")
    logger.print_info(f"LLM: {config.get('llm.model')}")
    logger.print_info(f"Base URL: {config.get('llm.base_url')}")

    try:
        # Create crew
        logger.print_section("Creating CrewAI Crew")
        start_time = time.time()

        crew = create_coder_crew(verbose=True)

        logger.print_success("Crew created successfully")
        logger.log_info("Crew created", {
            "agents": len(crew.agents),
            "tasks": len(crew.tasks),
        })

        # Execute crew
        logger.print_section("Executing Task")
        logger.print_info("The agent will now build a personal website...")
        logger.print_info("This may take several minutes. Please wait...\n")

        execution_start = time.time()

        # Run the crew
        result = crew.kickoff()

        execution_time = time.time() - execution_start

        # Log execution
        logger.log_event("crew_execution", {
            "duration_seconds": execution_time,
            "result_length": len(str(result)),
        })

        # Display results
        logger.print_section("Execution Complete")
        logger.print_success(f"Task completed in {execution_time:.2f} seconds")
        logger.print_info(f"\nResult:\n{result}\n")

        # Check output directory
        logger.print_section("Output Files")
        logger.print_info("Check the ./output directory for generated files")

        total_time = time.time() - start_time
        logger.print_success(f"\nTotal execution time: {total_time:.2f} seconds")

    except KeyboardInterrupt:
        logger.print_warning("\n\nExecution interrupted by user")
        logger.log_error("keyboard_interrupt", "User interrupted execution")
        sys.exit(1)

    except Exception as e:
        logger.print_error(f"\n\nError during execution: {str(e)}")
        logger.log_error("execution_error", str(e))
        import traceback
        logger.log_debug(traceback.format_exc())
        sys.exit(1)

    finally:
        # End session and save logs
        logger.end_session()


if __name__ == "__main__":
    main()
