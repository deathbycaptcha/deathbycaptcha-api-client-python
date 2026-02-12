# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

#### AI Agent Integration Features
- **AGENT_USAGE.md** - Comprehensive guide for AI agents integrating with the library
  - Quick start guide
  - Client selection recommendations (SocketClient vs HttpClient)
  - Complete method reference
  - Advanced usage patterns (retry logic, batch processing, async)
  - Error handling guide
  - Integration examples (Selenium, Requests, FastAPI)
  - Performance optimization tips

- **schema.json** - Machine-readable API specification
  - Full API structure in JSON format
  - Class definitions with methods and parameters
  - Exception specifications
  - Constants and default values
  - Common workflows
  - Performance metrics

- **AI_AGENTS_INTEGRATION.md** - Overview of agent integration features
  - Summary of new documentation
  - Quick integration paths
  - Security recommendations
  - Tips for AI agents

- **agents/** - Directory with integration examples and tools

  - **agent_wrapper.py** - Production-ready wrapper class
    - `CaptchaSolver` class with simplified API
    - `CaptchaResult` dataclass for standardized responses
    - Balance tracking and cost calculation
    - Batch processing capabilities
    - Retry logic with exponential backoff
    - Context manager support for safe resource cleanup
    - `solve_captcha_quick()` convenience function

  - **example_tool_use.py** - LLM tool integration
    - Tool definition compatible with Claude/GPT APIs
    - `CaptchaToolHandler` class for processing tool calls
    - Examples for Anthropic, OpenAI, and LangChain
    - Simple agent workflow example

  - **example_langchain.py** - LangChain integration
    - `@tool` decorated functions for LangChain
    - `create_captcha_agent()` for agent initialization
    - Complete workflow example

  - **example_json_api.py** - FastAPI HTTP wrapper
    - RESTful API endpoints for CAPTCHA solving
    - Support for file upload, base64, and batch solving
    - Health check and balance endpoints
    - Perfect for serverless and distributed agents
    - CORS and error handling included

  - **agent_config.example.json** - Configuration template
    - Credential management structure
    - Agent-specific settings
    - Logging configuration

  - **README.md** - Agents directory guide
    - Overview of available examples
    - Quick start instructions
    - Integration pattern descriptions

### Design Principles

- **Non-invasive** - All additions are outside the core library code
- **Agent-friendly** - Designed specifically for AI agent integration
- **Examples-driven** - Multiple real-world integration patterns
- **Well-documented** - Comprehensive guides and docstrings
- **Production-ready** - Includes error handling, logging, and best practices

### Backward Compatibility

- ✅ No changes to existing API
- ✅ No changes to library code
- ✅ Fully backward compatible
- ✅ All new features are additive

## [4.7.0] - Previous Release

(See original CHANGELOG.md for previous versions)
