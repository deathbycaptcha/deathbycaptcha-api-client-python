#!/usr/bin/env python3
"""
Example: Using DeathByCaptcha as a tool for LLM agents (Claude, GPT, etc.)

This shows how to define the CAPTCHA solving capability as a "tool"
that an LLM agent can call.
"""

import json
from agent_wrapper import CaptchaSolver, CaptchaResult


# Tool definition compatible with Claude, GPT, and other LLM APIs
CAPTCHA_TOOL_DEFINITION = {
    "name": "solve_captcha",
    "description": "Solve a CAPTCHA image using DeathByCaptcha API. Returns the solved text.",
    "input_schema": {
        "type": "object",
        "properties": {
            "captcha_path": {
                "type": "string",
                "description": "Path to the CAPTCHA image file or base64-encoded image data"
            },
            "timeout": {
                "type": "integer",
                "description": "Maximum time to wait for solution in seconds (default: 60)",
                "default": 60,
                "minimum": 10,
                "maximum": 300
            }
        },
        "required": ["captcha_path"]
    }
}


class CaptchaToolHandler:
    """
    Handler for LLM agents calling the CAPTCHA solving tool.
    
    Usage with Anthropic's SDK:
    ```python
    handler = CaptchaToolHandler(username, password)
    result = handler.process_tool_call("solve_captcha", {
        "captcha_path": "image.png", 
        "timeout": 60
    })
    ```
    """
    
    def __init__(self, username: str, password: str):
        """Initialize tool handler with DBC credentials"""
        self.solver = CaptchaSolver(username, password)
    
    def process_tool_call(
        self,
        tool_name: str,
        tool_input: dict
    ) -> dict:
        """
        Process a tool call from an LLM agent.
        
        Args:
            tool_name: Name of the tool (should be 'solve_captcha')
            tool_input: Input parameters from agent
        
        Returns:
            Result dict that can be sent back to agent
        """
        if tool_name != "solve_captcha":
            return {
                "error": f"Unknown tool: {tool_name}",
                "success": False
            }
        
        captcha_path = tool_input.get("captcha_path")
        timeout = tool_input.get("timeout", 60)
        
        if not captcha_path:
            return {
                "error": "Missing required parameter: captcha_path",
                "success": False
            }
        
        # Solve the CAPTCHA
        result: CaptchaResult = self.solver.solve(captcha_path, timeout=timeout)
        
        # Convert to format suitable for agent
        return {
            "success": result.success,
            "text": result.text,
            "captcha_id": result.captcha_id,
            "error": result.error,
            "cost_cents": result.cost_cents,
            "time_seconds": result.time_seconds
        }
    
    def get_tool_definition(self) -> dict:
        """Get the tool definition for agent"""
        return CAPTCHA_TOOL_DEFINITION
    
    def close(self):
        """Clean up resources"""
        self.solver.close()


# Example implementations with different LLM frameworks
class AnthropicAgentExample:
    """Example using Anthropic's Claude API"""
    
    @staticmethod
    def example():
        """
        This would work with anthropic SDK:
        pip install anthropic
        """
        try:
            import anthropic
        except ImportError:
            print("anthropic SDK not installed. Install with: pip install anthropic")
            return
        
        # Initialize
        client = anthropic.Anthropic()
        tool_handler = CaptchaToolHandler("username", "password")
        tools = [tool_handler.get_tool_definition()]
        
        # Example conversation
        messages = [
            {
                "role": "user",
                "content": "I need you to solve this CAPTCHA for me: /path/to/captcha.png"
            }
        ]
        
        # Call Claude with tools
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )
        
        # Process tool calls
        for content_block in response.content:
            if content_block.type == "tool_use":
                tool_result = tool_handler.process_tool_call(
                    content_block.name,
                    content_block.input
                )
                print(f"Tool result: {tool_result}")
        
        tool_handler.close()


class OpenAIAgentExample:
    """Example using OpenAI's GPT API"""
    
    @staticmethod
    def example():
        """
        This would work with openai SDK:
        pip install openai
        """
        try:
            from openai import OpenAI
        except ImportError:
            print("openai SDK not installed. Install with: pip install openai")
            return
        
        client = OpenAI()
        tool_handler = CaptchaToolHandler("username", "password")
        
        # OpenAI format
        tools = [
            {
                "type": "function",
                "function": tool_handler.get_tool_definition()
            }
        ]
        
        messages = [
            {
                "role": "user",
                "content": "Please solve this CAPTCHA: /path/to/captcha.png"
            }
        ]
        
        # Call GPT
        response = client.chat.completions.create(
            model="gpt-4o",
            tools=tools,
            messages=messages
        )
        
        # Process tool calls
        for tool_call in response.choices[0].message.tool_calls:
            result = tool_handler.process_tool_call(
                tool_call.function.name,
                json.loads(tool_call.function.arguments)
            )
            print(f"Tool result: {result}")
        
        tool_handler.close()


class LangChainToolExample:
    """Example using LangChain"""
    
    @staticmethod
    def create_tool():
        """
        Create a LangChain tool for CAPTCHA solving.
        
        Usage:
        ```python
        from langchain.tools import tool
        
        @tool
        def solve_captcha(captcha_path: str) -> str:
            \"\"\"Solve a CAPTCHA image and return the text\"\"\"
            solver = CaptchaSolver("username", "password")
            try:
                result = solver.solve(captcha_path)
                return result.text if result.success else f"Error: {result.error}"
            finally:
                solver.close()
        ```
        """
        pass


# Simple sync example
def simple_agent_workflow():
    """
    Example of a simple agent solving CAPTCHAs in a loop.
    """
    tool_handler = CaptchaToolHandler(
        username="your_username",
        password="your_password"
    )
    
    # Simulate agent making multiple CAPTCHA solve requests
    captcha_paths = [
        "/path/to/captcha1.png",
        "/path/to/captcha2.png",
        "/path/to/captcha3.png"
    ]
    
    for captcha_path in captcha_paths:
        result = tool_handler.process_tool_call(
            "solve_captcha",
            {"captcha_path": captcha_path, "timeout": 60}
        )
        
        if result["success"]:
            print(f"✓ Solved: {result['text']}")
        else:
            print(f"✗ Failed: {result['error']}")
    
    tool_handler.close()


if __name__ == "__main__":
    print("DeathByCaptcha Tool Examples for LLM Agents")
    print("=" * 50)
    print()
    print("Tool Definition:")
    print(json.dumps(CAPTCHA_TOOL_DEFINITION, indent=2))
    print()
    print("See docstrings for usage with Claude, GPT, LangChain, etc.")
