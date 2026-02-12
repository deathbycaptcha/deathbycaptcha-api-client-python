#!/usr/bin/env python3
"""
Example: FastAPI wrapper for DeathByCaptcha CAPTCHA solving.

Agents can interact with CAPTCHA solving via HTTP JSON API.

Usage:
    pip install fastapi uvicorn
    python example_json_api.py
    # Server runs at http://localhost:8000
"""

import base64
import json
import logging
from io import BytesIO
from typing import Optional

try:
    from fastapi import FastAPI, HTTPException, UploadFile, File
    from fastapi.responses import JSONResponse
    import uvicorn
except ImportError:
    print("FastAPI not installed. Install with: pip install fastapi uvicorn")
    exit(1)

from agent_wrapper import CaptchaSolver, CaptchaResult


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DeathByCaptcha Agent API",
    description="HTTP API wrapper for CAPTCHA solving",
    version="1.0.0"
)

# Global solver instance
solver: Optional[CaptchaSolver] = None


@app.on_event("startup")
async def startup():
    """Initialize CAPTCHA solver on app startup"""
    global solver
    
    # Read credentials from environment or config
    # For production, use environment variables or secrets management
    import os
    username = os.getenv("DBC_USERNAME", "your_username")
    password = os.getenv("DBC_PASSWORD", "your_password")
    
    if username == "your_username":
        logger.warning(
            "Using default credentials. Set DBC_USERNAME and DBC_PASSWORD "
            "environment variables."
        )
    
    solver = CaptchaSolver(username, password, verbose=True)
    logger.info("CAPTCHA Solver initialized")


@app.on_event("shutdown")
async def shutdown():
    """Close solver connection on app shutdown"""
    global solver
    if solver:
        solver.close()
        logger.info("CAPTCHA Solver closed")


# Routes


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    if solver:
        balance = solver.get_balance()
        return {
            "status": "healthy",
            "solver": "ready",
            "balance_cents": balance
        }
    else:
        return {"status": "unhealthy", "solver": "not initialized"}


@app.get("/balance")
async def get_balance():
    """Get current account balance"""
    if not solver:
        raise HTTPException(status_code=503, detail="Solver not initialized")
    
    try:
        balance = solver.get_balance()
        return {
            "balance_cents": balance,
            "balance_usd": balance / 100
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/user-info")
async def get_user_info():
    """Get detailed user information"""
    if not solver:
        raise HTTPException(status_code=503, detail="Solver not initialized")
    
    try:
        info = solver.get_user_info()
        return info
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/solve")
async def solve_captcha(
    file: UploadFile = File(...),
    timeout: int = 60
):
    """
    Solve CAPTCHA from uploaded file.
    
    Request:
        POST /solve
        Content-Type: multipart/form-data
        
        file: binary CAPTCHA image file
        timeout: max seconds to wait (optional, default 60)
    
    Response:
        {
            "success": true/false,
            "text": "captcha text",
            "captcha_id": 12345,
            "cost_cents": 5,
            "time_seconds": 15.3
        }
    """
    if not solver:
        raise HTTPException(status_code=503, detail="Solver not initialized")
    
    try:
        # Read file contents
        contents = await file.read()
        
        # Solve
        result = solver.solve(contents, timeout=timeout)
        
        return result.to_dict()
    
    except Exception as e:
        logger.error(f"Error solving CAPTCHA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/solve-base64")
async def solve_captcha_base64(data: dict):
    """
    Solve CAPTCHA from base64-encoded image.
    
    Request:
        POST /solve-base64
        Content-Type: application/json
        
        {
            "image_base64": "iVBORw0KGgo...",
            "timeout": 60
        }
    
    Response:
        (same as /solve)
    """
    if not solver:
        raise HTTPException(status_code=503, detail="Solver not initialized")
    
    try:
        image_base64 = data.get("image_base64")
        timeout = data.get("timeout", 60)
        
        if not image_base64:
            raise HTTPException(status_code=400, detail="Missing image_base64")
        
        # Decode base64
        image_bytes = base64.b64decode(image_base64)
        
        # Solve
        result = solver.solve(image_bytes, timeout=timeout)
        
        return result.to_dict()
    
    except Exception as e:
        logger.error(f"Error solving CAPTCHA: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/solve-batch")
async def solve_batch(data: dict):
    """
    Solve multiple CAPTCHAs from base64 data.
    
    Request:
        POST /solve-batch
        Content-Type: application/json
        
        {
            "images": [
                "iVBORw0KGgo...",
                "iVBORw0KGgo..."
            ],
            "timeout": 60,
            "max_per_batch": 10
        }
    
    Response:
        {
            "total": 2,
            "successful": 1,
            "results": [
                {"success": true, "text": "abc123", ...},
                {"success": false, "error": "...", ...}
            ]
        }
    """
    if not solver:
        raise HTTPException(status_code=503, detail="Solver not initialized")
    
    try:
        images_base64 = data.get("images", [])
        timeout = data.get("timeout", 60)
        max_per_batch = data.get("max_per_batch")
        
        if not images_base64:
            raise HTTPException(status_code=400, detail="No images provided")
        
        # Decode images
        images = [
            base64.b64decode(img) for img in images_base64
        ]
        
        # Solve batch
        results = solver.solve_batch(
            images,
            timeout=timeout,
            max_per_batch=max_per_batch
        )
        
        successful = sum(1 for r in results if r.success)
        
        return {
            "total": len(results),
            "successful": successful,
            "results": [r.to_dict() for r in results]
        }
    
    except Exception as e:
        logger.error(f"Error solving batch: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/report/{captcha_id}")
async def report_incorrect(captcha_id: int):
    """Report a CAPTCHA as incorrectly solved (for refund)"""
    if not solver:
        raise HTTPException(status_code=503, detail="Solver not initialized")
    
    try:
        success = solver.report_incorrect(captcha_id)
        return {"reported": success}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/docs")
def api_schema():
    """Get OpenAPI schema"""
    return app.openapi()


if __name__ == "__main__":
    print("Starting DeathByCaptcha Agent API Server...")
    print("Endpoints:")
    print("  GET    /health     - Health check")
    print("  GET    /balance    - Check balance")
    print("  GET    /user-info  - User information")
    print("  POST   /solve      - Solve from uploaded file")
    print("  POST   /solve-base64 - Solve from base64 image")
    print("  POST   /solve-batch  - Solve multiple CAPTCHAs")
    print("  POST   /report/{id}  - Report incorrect CAPTCHA")
    print()
    print("Server will be at http://localhost:8000")
    print("OpenAPI docs at http://localhost:8000/docs")
    print()
    
    # Set credentials via environment variables
    import os
    if "DBC_USERNAME" not in os.environ:
        print("WARNING: DBC_USERNAME environment variable not set")
    if "DBC_PASSWORD" not in os.environ:
        print("WARNING: DBC_PASSWORD environment variable not set")
    
    # Start server
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
