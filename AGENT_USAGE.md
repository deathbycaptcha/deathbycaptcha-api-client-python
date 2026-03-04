# DeathByCaptcha API Client - Agent Integration Guide

This guide is designed for AI agents and automated systems that need to integrate DeathByCaptcha CAPTCHA solving capabilities into their workflows.

## Quick Start for Agents

### Installation
```bash
pip install deathbycaptcha-official
```

### Basic Setup
```python
import deathbycaptcha

# Initialize client (choose one method)
client = deathbycaptcha.SocketClient(username="your_username", password="your_password")
# OR
client = deathbycaptcha.HttpClient(username="your_username", password="your_password")
```

### Minimal Working Example
```python
try:
    # Check balance before attempting to solve
    balance = client.get_balance()
    if balance <= 0:
        print(f"Insufficient balance: {balance}")
        exit(1)
    
    # Solve a CAPTCHA
    captcha = client.decode("path/to/captcha.png", timeout=60)
    
    if captcha:
        print(f"CAPTCHA solved: {captcha['text']}")
    else:
        print("Failed to solve CAPTCHA")
        
except deathbycaptcha.AccessDeniedException as e:
    print(f"Authentication failed: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    if hasattr(client, 'close'):
        client.close()
```

## Client Selection

### SocketClient (Recommended for Agents)
- **Persistent connection** - Reuse same client instance across multiple requests
- **Faster responses** - Lower latency
- **Thread-safe** - Can be shared across threads
- **Better for long-running processes**

```python
client = deathbycaptcha.SocketClient(username, password)
# Keep client alive for multiple decode operations
for captcha_file in captcha_files:
    result = client.decode(captcha_file)
```

### HttpClient
- **Stateless** - Each request is independent
- **Better for serverless environments** (AWS Lambda, etc.)
- **Lower memory footprint**
- **No persistent connection overhead**

```python
client = deathbycaptcha.HttpClient(username, password)
# Create new client per request if needed
```

## Key Methods for Agents

### 1. Check Balance
```python
balance = client.get_balance()  # Returns balance in US cents
if balance < 100:  # Less than $1.00
    print("Balance low, consider refunding account")
```

### 2. Solve CAPTCHA
```python
# From file path
captcha = client.decode("image.png", timeout=60)

# From file-like object (BytesIO, requests stream, etc.)
import io
image_bytes = b"..."  # Your image bytes
file_obj = io.BytesIO(image_bytes)
captcha = client.decode(file_obj, timeout=60)
```

### 3. Get CAPTCHA Details
```python
captcha = client.get_captcha(captcha_id)
print(captcha['text'])      # The solved text
print(captcha['is_correct']) # Whether solution is correct
```

### 4. Report Incorrect Solution
```python
# Use if CAPTCHA was solved incorrectly
success = client.report(captcha_id)
if success:
    print("CAPTCHA reported and refunded")
```

### 5. Get User Info
```python
user = client.get_user()
print(f"User ID: {user['user']}")
print(f"Balance: {user['balance']} cents")
print(f"Banned: {user['is_banned']}")
```

## Advanced Agent Patterns

### Pattern 1: Using CaptchaSolver Wrapper (Recommended for Agents)
```python
from agents.agent_wrapper import CaptchaSolver

# Using context manager for automatic cleanup
with CaptchaSolver(username="your_username", password="your_password") as solver:
    # Single CAPTCHA
    result = solver.solve("captcha.png", timeout=60)
    if result.success:
        print(f"Solved: {result.text}")
    else:
        print(f"Error: {result.error}")
```

### Pattern 2: Batch Processing with Cost Tracking
```python
from agents.agent_wrapper import CaptchaSolver

with CaptchaSolver(username="your_username", password="your_password") as solver:
    # Solve multiple CAPTCHAs efficiently
    image_list = ["cap1.png", "cap2.png", "cap3.png"]
    results = solver.solve_batch(
        image_list,
        timeout=60,
        max_per_batch=10,
        min_balance_cents=100  # Stop if balance too low
    )
    
    for result in results:
        if result.success:
            print(f"ID {result.captcha_id}: {result.text} (${result.cost_cents/100:.4f})")
        else:
            print(f"Failed: {result.error}")
```

### Pattern 3: Quick Convenience Function
```python
from agents.agent_wrapper import solve_captcha_quick

# Fastest way to solve a single CAPTCHA
result_text = solve_captcha_quick(
    username="your_username",
    password="your_password",
    captcha="captcha.png",
    timeout=60
)

if result_text:
    print(f"Solved: {result_text}")
else:
    print("Failed to solve")
```

### Pattern 4: Retry Logic with Exponential Backoff
```python
from agents.agent_wrapper import CaptchaSolver
import time

with CaptchaSolver(username="your_username", password="your_password") as solver:
    # The solve() method has built-in retry support
    result = solver.solve(
        "captcha.png",
        timeout=60,
        max_retries=3  # Will retry up to 3 times with exponential backoff
    )
    
    if not result.success:
        print(f"Failed after retries: {result.error}")
        decode_params['token_params'] = {
            'googlekey': kwargs.get('sitekey'),
            'pageurl': kwargs.get('pageurl'),
            'action': kwargs.get('action', 'verify')
        }
    
    return client.decode(image_path, timeout=60, **decode_params)
```

## Error Handling Guide

### Exception Types
```python
import deathbycaptcha

try:
    result = client.decode(image)
except deathbycaptcha.AccessDeniedException:
    # Handle auth errors (bad credentials, insufficient balance)
    # Action: Check credentials, refund account
    pass
except ValueError as e:
    # Handle invalid CAPTCHA image
    # Action: Validate image before sending
    pass
except OverflowError:
    # Handle service overload (HTTP 503)
    # Action: Retry with backoff
    pass
except Exception as e:
    # Generic errors (network, timeout, etc.)
    # Action: Log and retry
    pass
```

## Configuration Best Practices for Agents

### Environment Variables
```python
import os

username = os.getenv('DBC_USERNAME')
password = os.getenv('DBC_PASSWORD')
client = deathbycaptcha.SocketClient(username, password)
```

### Config File
```python
import json

with open('config.json') as f:
    config = json.load(f)

client = deathbycaptcha.SocketClient(
    config['dbc']['username'],
    config['dbc']['password']
)
```

### Token-Based Auth (Alternative)
```python
# Some agents may prefer token authentication
client = deathbycaptcha.SocketClient(authtoken="your_auth_token")
```

## Performance Tips

1. **Reuse client instances**: Create once, use multiple times
2. **Set appropriate timeouts**: 
   - Normal CAPTCHAs: 30-60 seconds
   - Complex CAPTCHAs: 120+ seconds
   - Tokens: 120 seconds (default)
3. **Monitor balance**: Check before batch operations
4. **Use exponential backoff**: For retries (1s, 2s, 4s, 8s...)
5. **Thread pool sizing**: 5-10 workers for good concurrency
6. **Clean up**: Always close client when done

```python
try:
    client = deathbycaptcha.SocketClient(username, password)
    # ... work with client ...
finally:
    client.close()  # Important!
```

## Integration Examples

### With Selenium
```python
def solve_captcha_selenium(driver, image_locator):
    """Solve CAPTCHA from Selenium WebDriver"""
    # Get image element
    img = driver.find_element(*image_locator)
    img.screenshot('captcha.png')
    
    # Solve it
    client = deathbycaptcha.SocketClient(username, password)
    captcha = client.decode('captcha.png', timeout=60)
    
    return captcha['text'] if captcha else None
```

### With Requests
```python
def solve_captcha_from_url(url, session=None):
    """Download and solve CAPTCHA from URL"""
    s = session or requests.Session()
    
    # Download image
    response = s.get(url)
    image_bytes = io.BytesIO(response.content)
    
    # Solve
    client = deathbycaptcha.SocketClient(username, password)
    captcha = client.decode(image_bytes, timeout=60)
    
    return captcha['text'] if captcha else None
```

### With FastAPI
```python
from fastapi import FastAPI, UploadFile
import deathbycaptcha

app = FastAPI()
client = deathbycaptcha.SocketClient(username, password)

@app.post("/solve-captcha")
async def solve_captcha(file: UploadFile):
    """HTTP endpoint for CAPTCHA solving"""
    image_bytes = await file.read()
    image_io = io.BytesIO(image_bytes)
    
    captcha = client.decode(image_io, timeout=60)
    
    return {
        "solved": captcha is not None,
        "text": captcha['text'] if captcha else None,
        "captcha_id": captcha.get('captcha') if captcha else None
    }

@app.on_event("shutdown")
def shutdown():
    client.close()
```

## Troubleshooting for Agents

| Issue | Cause | Solution |
|-------|-------|----------|
| AccessDeniedException | Bad credentials or no balance | Verify username/password, check balance |
| ValueError (invalid image) | Corrupted or unsupported image | Validate image format before submission |
| OverflowError (503) | Service overload | Implement exponential backoff retry |
| Timeout | Network slow or CAPTCHA too complex | Increase timeout, check network |
| Connection refused | Socket API ports blocked | Use HttpClient instead, check firewall |

## Rate Limits

- **No rate limits** on API calls (pay per CAPTCHA)
- **Typical cost**: $0.0050 - $0.15 per CAPTCHA
- **Balance check**: Free (use to monitor)
- **User info**: Free (use to get rates and status)

## References

- Main Docs: https://deathbycaptcha.com/user/api
- GitHub: https://github.com/deathbycaptcha/deathbycaptcha-api-client-python
- PyPI: https://pypi.org/project/deathbycaptcha-official/
