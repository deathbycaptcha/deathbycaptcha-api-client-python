# AI Agents Integration - Complete Guide

This repository has been enhanced with comprehensive support for AI agents to integrate CAPTCHA solving capabilities.

## 📋 What's New

### In Root Directory

- **[AGENT_USAGE.md](AGENT_USAGE.md)** - Complete agent integration guide
  - Quick start
  - Client selection guide
  - Key methods reference
  - Advanced patterns
  - Error handling
  - Integration examples
  - Performance tips

- **[schema.json](schema.json)** - Machine-readable API specification
  - Full API structure (classes, methods, exceptions)
  - Parameter types and descriptions
  - Return value specifications
  - Common workflows
  - Performance metrics

### In `agents/` Directory

1. **[agents/agent_wrapper.py](agents/agent_wrapper.py)** - Production-ready wrapper
   - Simplified, agent-friendly API
   - Better error handling
   - Standardized result format (`CaptchaResult`)
   - Balance tracking
   - Batch processing
   - Retry logic
   - Context manager support

2. **[agents/README.md](agents/README.md)** - Agents directory guide

3. **[agents/example_tool_use.py](agents/example_tool_use.py)** - LLM tool integration
   - Tool definition (Claude/GPT compatible)
   - `CaptchaToolHandler` for processing tool calls
   - Examples for Anthropic, OpenAI, LangChain

4. **[agents/example_langchain.py](agents/example_langchain.py)** - LangChain integration
   - Create LangChain tools
   - Build agents with CAPTCHA capability
   - Complete workflow example

5. **[agents/example_json_api.py](agents/example_json_api.py)** - FastAPI HTTP wrapper
   - REST API for CAPTCHA solving
   - Multiple endpoints (file upload, base64, batch)
   - Health checks and balance endpoints
   - Perfect for serverless/distributed agents

6. **[agents/agent_config.example.json](agents/agent_config.example.json)** - Configuration template

## 🚀 Quick Integration Paths

### Path 1: Direct Python Integration (Simplest)
```python
from agents.agent_wrapper import CaptchaSolver

solver = CaptchaSolver("username", "password")
result = solver.solve("captcha.png")
print(result.text)
```

### Path 2: LLM Tool Integration (Claude/GPT)
```python
from agents.example_tool_use import CaptchaToolHandler

handler = CaptchaToolHandler("username", "password")
tool_def = handler.get_tool_definition()
# Add to your LLM's tools, process calls with handler.process_tool_call()
```

### Path 3: LangChain Integration
```python
# Import and use tools from agents/example_langchain.py
from agents.example_langchain import create_captcha_agent

agent = create_captcha_agent()
response = agent.run("Solve the CAPTCHA at /path/to/image.png")
```

### Path 4: HTTP API (Distributed/Serverless)
```bash
# Start server
python agents/example_json_api.py

# Call via curl or any HTTP client
curl -X POST http://localhost:8000/solve-base64 \
  -H "Content-Type: application/json" \
  -d '{"image_base64": "iVBORw0KGgo...", "timeout": 60}'
```

## 📚 Documentation Structure

```
├── README.md                          (Original library README)
├── AGENT_USAGE.md                     ← NEW Agent guide (START HERE)
├── schema.json                        ← NEW API schema (machine-readable)
└── agents/
    ├── README.md                      ← Agents overview
    ├── agent_wrapper.py               ← Core wrapper class
    ├── example_tool_use.py            ← LLM tool examples
    ├── example_langchain.py           ← LangChain example
    ├── example_json_api.py            ← HTTP API wrapper
    └── agent_config.example.json      ← Config template
```

## 🤖 AI Agent Friendly Features

✅ **Clear API surface** - Documented with types and descriptions  
✅ **Machine-readable schema** - `schema.json` for parsing  
✅ **Simplified wrapper** - `CaptchaSolver` class reduces complexity  
✅ **Standardized results** - `CaptchaResult` dataclass  
✅ **Error handling** - Clear exceptions for different failure modes  
✅ **Multiple integration patterns** - Tool, HTTP, async, batch  
✅ **Production-ready** - Retry logic, balance tracking, logging  
✅ **Examples for popular frameworks** - Claude, GPT, LangChain  

## 🔧 Implementation Recommendations

### For Simple Agents
Use `agents/agent_wrapper.py` with direct Python calls.

### For LLM-Powered Agents
Use `agents/example_tool_use.py` to define CAPTCHA solving as a tool.

### For Distributed Agents
Deploy `agents/example_json_api.py` and call via HTTP endpoints.

### For Workflow Integration
Use `agents/example_langchain.py` for agent frameworks.

## 📖 Reading Guide for Agents

1. **First time?** → Read [AGENT_USAGE.md](AGENT_USAGE.md)
2. **Need API details?** → Check [schema.json](schema.json)
3. **Want to integrate?** → See appropriate example in [agents/](agents/)
4. **Have questions?** → Check error handling in AGENT_USAGE.md

## 🔐 Security Notes

- Never hardcode credentials
- Use environment variables: `DBC_USERNAME`, `DBC_PASSWORD`
- For HTTP API, use secrets management (AWS Secrets, Vault, etc.)
- Protect credentials in configuration files
- Consider token-based auth for sensitive deployments

## 💡 Tips for Agents

1. **Reuse client instances** - Create once, use multiple times
2. **Check balance first** - Avoid failed requests
3. **Set appropriate timeouts** - 30s for simple, 120s for complex
4. **Implement backoff** - For retries (exponential backoff recommended)
5. **Monitor costs** - Track spend across multiple solves
6. **Handle errors gracefully** - Different exception types need different handling

## 📊 What Agents Get

| Feature | Details |
|---------|---------|
| **API Schema** | Structured JSON with full API details |
| **Type Hints** | Clear parameter/return types |
| **Examples** | 5+ integration patterns |
| **Documentation** | Comprehensive guides + docstrings |
| **Error Handling** | Documented exception types |
| **Batch Processing** | Solve multiple CAPTCHAs efficiently |
| **Balance Tracking** | Know when to stop |
| **Logging** | Debug integration issues |

## 🚀 Next Steps

1. Read [AGENT_USAGE.md](AGENT_USAGE.md) for your use case
2. Choose integration pattern from [agents/](agents/)
3. Copy configuration template: `agents/agent_config.example.json`
4. Run an example to verify setup
5. Integrate into your agent framework

---

**Questions?** Check AGENT_USAGE.md or examine the example files.

Made for AI agents integration. Happy solving! 🎯
