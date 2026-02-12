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
    solver = CaptchaSolver(
        username="your_username",  # Set via environment variables in production
        password="your_password"
    )
    
    try:
        result = solver.solve(image_path, timeout=timeout)
        if result.success:
            return f"CAPTCHA solved: {result.text}"
        else:
            return f"Failed to solve CAPTCHA: {result.error}"
    finally:
        solver.close()


@tool
def check_captcha_balance() -> str:
    """
    Check the current DeathByCaptcha account balance.
    
    Returns:
        Current balance in USD format
    """
    solver = CaptchaSolver(
        username="your_username",
        password="your_password"
    )
    
    try:
        balance = solver.get_balance()
        return f"Current balance: ${balance/100:.2f}"
    finally:
        solver.close()


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
        "First check my DBC balance. If I have enough balance, "
        "solve the CAPTCHA at /tmp/captcha.png"
    )
    
    print(response)


if __name__ == "__main__":
    print("LangChain CAPTCHA Agent Example")
    print("=" * 50)
    print()
    print("To use this example:")
    print("1. Install dependencies: pip install langchain langchain-community anthropic")
    print("2. Set environment variables:")
    print("   - ANTHROPIC_API_KEY (your Anthropic API key)")
    print("   - DBC_USERNAME (your DeathByCaptcha username)")
    print("   - DBC_PASSWORD (your DeathByCaptcha password)")
    print("3. Run: python example_langchain.py")
    print()
    print("The agent will have access to:")
    print("  - solve_captcha(image_path, timeout) - Solve CAPTCHA")
    print("  - check_captcha_balance() - Check balance")
