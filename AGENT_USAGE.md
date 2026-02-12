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

### Pattern 1: Reliable CAPTCHA Solving with Retry
```python
def solve_captcha_with_retry(client, image_path, max_retries=3, timeout=60):
    """Solve CAPTCHA with automatic retry on failure"""
    for attempt in range(max_retries):
        try:
            captcha = client.decode(image_path, timeout=timeout)
            if captcha and captcha.get('text'):
                return captcha
        except deathbycaptcha.AccessDeniedException:
            raise  # Authentication error, don't retry
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            continue
    return None
```

### Pattern 2: Batch Processing with Cost Tracking
```python
def batch_solve_captchas(client, image_list, budget_cents=1000):
    """Solve multiple CAPTCHAs within budget constraint"""
    results = []
    spent = 0
    initial_balance = client.get_balance()
    
    for image_path in image_list:
        remaining_budget = budget_cents - spent
        if remaining_budget < 100:  # Min $1 safety margin
            break
            
        try:
            captcha = client.decode(image_path, timeout=60)
            if captcha:
                results.append(captcha)
                spent = initial_balance - client.get_balance()
        except Exception as e:
            print(f"Failed to solve {image_path}: {e}")
            
    return results, spent
```

### Pattern 3: Async-Compatible Wrapper
```python
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AsyncCaptchaSolver:
    def __init__(self, username, password, max_workers=5):
        self.client = deathbycaptcha.SocketClient(username, password)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    async def decode_async(self, image_path, timeout=60):
        """Async wrapper for decode function"""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            self.executor, 
            self.client.decode, 
            image_path, 
            timeout
        )
```

### Pattern 4: Conditional Solving Based on Type
```python
def solve_captcha_smart(client, image_path, captcha_type='normal', **kwargs):
    """
    Solve CAPTCHA with type-specific parameters.
    
    captcha_type: 'normal', 'recaptcha_v2', 'recaptcha_v3', 'hcaptcha', etc.
    """
    decode_params = kwargs.copy()
    
    # Add type-specific parameters
    if captcha_type == 'recaptcha_v2':
        decode_params['token_params'] = {
            'googlekey': kwargs.get('sitekey'),
            'pageurl': kwargs.get('pageurl')
        }
    elif captcha_type == 'recaptcha_v3':
        decode_params['type'] = 7
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
