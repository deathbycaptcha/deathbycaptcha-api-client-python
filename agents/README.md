# AI Agent Integration Examples

This directory contains example implementations and patterns for integrating the DeathByCaptcha API client with AI agents and automated systems.

## Files

- **`agent_wrapper.py`** - Production-ready wrapper class for agents
- **`example_langchain.py`** - Integration with LangChain
- **`example_json_api.py`** - Fast API wrapper for HTTP-based agents
- **`example_tool_use.py`** - Example tool definition for Claude/GPT agents
- **`agent_config.example.json`** - Configuration template

## Quick Start

### 1. Simple Agent Tool (Recommended)
```python
from agent_wrapper import CaptchaSolver

# Use context manager for automatic cleanup
with CaptchaSolver(username="user", password="pass") as solver:
    result = solver.solve("captcha.png")
    if result.success:
        print(f"Solved: {result.text}")
    else:
        print(f"Error: {result.error}")
```

### 2. Batch Processing
```python
from agent_wrapper import CaptchaSolver

with CaptchaSolver(username="user", password="pass") as solver:
    results = solver.solve_batch(
        ["cap1.png", "cap2.png", "cap3.png"],
        timeout=60,
        max_per_batch=10
    )
    for r in results:
        if r.success:
            print(f"{r.captcha_id}: {r.text} (${r.cost_cents/100:.4f})")
```

### 3. Error Handling
```python
from agent_wrapper import CaptchaSolver

with CaptchaSolver(username="user", password="pass") as solver:
    result = solver.solve("captcha.png", timeout=30, max_retries=3)
    if result.success:
        print(f"Solved: {result.text}")
    else:
        print(f"Failed: {result.error}")
```

## Integration Patterns

### LangChain Integration
See `example_langchain.py` for how to use as a LangChain tool.

### FastAPI Wrapper
See `example_json_api.py` for HTTP-based API wrapper.

### Direct Tool Use
See `example_tool_use.py` for defining as a tool for LLM agents.

## Configuration

Copy `agent_config.example.json` to `agent_config.json` and fill in your credentials:
```json
{
  "dbc": {
    "username": "your_username",
    "password": "your_password",
    "client_type": "socket"
  }
}
```

## Performance Tips

1. **Reuse client instance** - Create once, use multiple times
2. **Batch operations** - Solve multiple CAPTCHAs with same client
3. **Async operations** - Use async wrapper for non-blocking calls
4. **Monitor balance** - Check before batch operations
5. **Set appropriate timeouts** - Longer for complex CAPTCHAs

## Quick Reference

For complete integration methods, see [../AGENT_USAGE.md](../AGENT_USAGE.md#L202) for patterns and examples.

## Environment Variables

Always use environment variables for credentials (recommended for security):
```bash
export DBC_USERNAME="your_username"
export DBC_PASSWORD="your_password"
```

Then in code:
```python
import os
username = os.getenv("DBC_USERNAME")
password = os.getenv("DBC_PASSWORD")
```

## See Also

- Agent Integration Guide: [../AGENT_USAGE.md](../AGENT_USAGE.md)
- API Schema: [../schema.json](../schema.json)
- Library docs: [../README.md](../README.md)
- Official API Metadata: https://github.com/deathbycaptcha/deathbycaptcha-agent-api-metadata
