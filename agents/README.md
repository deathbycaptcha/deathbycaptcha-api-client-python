# AI Agent Integration Examples

This directory contains example implementations and patterns for integrating the DeathByCaptcha API client with AI agents and automated systems.

## Files

- **`agent_wrapper.py`** - Production-ready wrapper class for agents
- **`example_langchain.py`** - Integration with LangChain
- **`example_json_api.py`** - Fast API wrapper for HTTP-based agents
- **`example_tool_use.py`** - Example tool definition for Claude/GPT agents
- **`agent_config.example.json`** - Configuration template

## Quick Start

### 1. Simple Agent Tool
```python
from agent_wrapper import CaptchaSolver

solver = CaptchaSolver(username="user", password="pass")
result = solver.solve("captcha.png")
print(result.text)
```

### 2. Batch Processing
```python
results = solver.solve_batch(["cap1.png", "cap2.png", "cap3.png"])
for r in results:
    print(f"{r.captcha_id}: {r.text}")
```

### 3. Error Handling
```python
result = solver.solve("captcha.png", timeout=30)
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

## See Also

- Main documentation: [../AGENT_USAGE.md](../AGENT_USAGE.md)
- API Schema: [../schema.json](../schema.json)
- Library docs: [../README.md](../README.md)
