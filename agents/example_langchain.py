#!/usr/bin/env python3
"""
Example: Using DeathByCaptcha with LangChain

This example shows how to integrate CAPTCHA solving into a LangChain agent.
"""

try:
    from langchain.tools import tool
    from langchain_community.llms import Anthropic
    from langchain.agents import initialize_agent, AgentType
except ImportError:
    print("LangChain not installed. Install with:")
    print("  pip install langchain langchain-community anthropic")
    exit(1)

import os
from agent_wrapper import CaptchaSolver


# Create a LangChain tool for CAPTCHA solving
@tool
def solve_captcha(image_path: str, timeout: int = 60) -> str:
    """
    Solve a CAPTCHA image and return the recognized text.
    
    Args:
        image_path: Path to the CAPTCHA image file
        timeout: Maximum time to wait for solution in seconds (default 60)
    
    Returns:
        The solved CAPTCHA text, or error message if failed
    """
    # Get credentials from environment variables
    username = os.getenv("DBC_USERNAME")
    password = os.getenv("DBC_PASSWORD")
    
    if not username or not password:
        return "Error: DBC_USERNAME and DBC_PASSWORD environment variables not set"
    
    # Use context manager for automatic cleanup
    with CaptchaSolver(username=username, password=password) as solver:
        result = solver.solve(image_path, timeout=timeout)
        if result.success:
            return f"CAPTCHA solved: {result.text}"
        else:
            return f"Failed to solve CAPTCHA: {result.error}"


@tool
def check_captcha_balance() -> str:
    """
    Check the current DeathByCaptcha account balance.
    
    Returns:
        Current balance in USD format
    """
    # Get credentials from environment variables
    username = os.getenv("DBC_USERNAME")
    password = os.getenv("DBC_PASSWORD")
    
    if not username or not password:
        return "Error: DBC_USERNAME and DBC_PASSWORD environment variables not set"
    
    # Use context manager for automatic cleanup
    with CaptchaSolver(username=username, password=password) as solver:
        balance = solver.get_balance()
        return f"Current balance: ${balance/100:.2f}"


def create_captcha_agent():
    """
    Create a LangChain agent with CAPTCHA solving capabilities.
    
    Returns:
        An agent that can solve CAPTCHAs and check balance
    """
    # Define all available tools
    tools = [solve_captcha, check_captcha_balance]
    
    # Initialize LLM
    llm = Anthropic()
    
    # Create agent
    agent = initialize_agent(
        tools,
        llm,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        handle_parsing_errors=True
    )
    
    return agent


def run_agent_example():
    """
    Run an example agent workflow with CAPTCHA solving.
    """
    agent = create_captcha_agent()
    
    # Example: Agent decides to check balance, then solve a CAPTCHA
    response = agent.run(
        "First check my DeathByCaptcha account balance. "
        "If I have enough credits (at least $1), solve the CAPTCHA at /tmp/test_captcha.png. "
        "Return both the balance and the solved CAPTCHA text."
    )
    
    print("\n=== Agent Response ===")
    print(response)


if __name__ == "__main__":
    print("DeathByCaptcha LangChain Agent Example")
    print("=" * 50)
    print("\nMake sure to set environment variables:")
    print("  export ANTHROPIC_API_KEY='your_api_key'")
    print("  export DBC_USERNAME='your_username'")
    print("  export DBC_PASSWORD='your_password'")
    print("\nInstall dependencies with:")
    print("  pip install langchain langchain-community anthropic")
    print("\nRunning agent example...\n")
    
    try:
        run_agent_example()
    except ImportError as e:
        print(f"Error: {e}")
        print("Install dependencies with: pip install langchain langchain-community anthropic")
