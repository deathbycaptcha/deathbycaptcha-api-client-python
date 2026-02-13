#!/usr/bin/env python3
"""
Production-ready wrapper for DeathByCaptcha API for AI agents.

This module provides a simplified, agent-friendly interface to the
DeathByCaptcha library with better error handling, logging, and
result standardization.
"""

import sys
from pathlib import Path

# Add parent directory to path to find deathbycaptcha module
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from deathbycaptcha import (
    SocketClient,
    HttpClient,
    AccessDeniedException
)

import io
import logging
import time
from dataclasses import dataclass
from typing import Optional, List, Dict, Union
from enum import Enum


logger = logging.getLogger(__name__)


class ClientType(str, Enum):
    """Supported client types"""
    SOCKET = "socket"
    HTTP = "http"


@dataclass
class CaptchaResult:
    """Standardized CAPTCHA solving result"""
    success: bool
    text: Optional[str] = None
    captcha_id: Optional[int] = None
    is_correct: Optional[bool] = None
    error: Optional[str] = None
    cost_cents: Optional[int] = None
    time_seconds: Optional[float] = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'success': self.success,
            'text': self.text,
            'captcha_id': self.captcha_id,
            'is_correct': self.is_correct,
            'error': self.error,
            'cost_cents': self.cost_cents,
            'time_seconds': self.time_seconds
        }


class CaptchaSolver:
    """
    AI Agent-friendly wrapper for DeathByCaptcha CAPTCHA solving.
    
    Features:
    - Simplified interface for agents
    - Better error handling and logging
    - Standardized result format
    - Balance tracking
    - Retry logic
    - Batch processing support
    """
    
    def __init__(
        self,
        username: str,
        password: str,
        client_type: ClientType = ClientType.SOCKET,
        verbose: bool = False,
        auto_close: bool = False
    ):
        """
        Initialize the CAPTCHA solver.
        
        Args:
            username: DBC account username
            password: DBC account password
            client_type: 'socket' (recommended) or 'http'
            verbose: Enable detailed logging
            auto_close: Automatically close client after each solve
        """
        self.username = username
        self.password = password
        self.client_type = client_type
        self.verbose = verbose
        self.auto_close = auto_close
        self._client = None
        self._initial_balance = None
        
        if verbose:
            logging.basicConfig(level=logging.DEBUG)
        
        self._connect()
    
    def _connect(self):
        """Establish connection to DBC API"""
        try:
            if self.client_type == ClientType.SOCKET:
                self._client = SocketClient(
                    self.username,
                    self.password
                )
            else:
                self._client = HttpClient(
                    self.username,
                    self.password
                )
            self._client.is_verbose = self.verbose
            
            # Get initial balance
            self._initial_balance = self.get_balance()
            logger.info(f"Connected to DBC API. Balance: ${self._initial_balance/100:.2f}")
        except Exception as e:
            logger.error(f"Failed to connect to DBC API: {e}")
            raise
    
    def get_balance(self) -> int:
        """
        Get account balance in US cents.
        
        Returns:
            Balance in cents (or 0 if unavailable)
        """
        try:
            balance = self._client.get_balance()
            logger.debug(f"Current balance: ${balance/100:.2f}")
            return balance
        except Exception as e:
            logger.error(f"Failed to get balance: {e}")
            return 0
    
    def get_user_info(self) -> Dict:
        """
        Get full user information.
        
        Returns:
            Dict with user_id, balance, rate, is_banned
        """
        try:
            info = self._client.get_user()
            logger.debug(f"User info: {info}")
            return info
        except Exception as e:
            logger.error(f"Failed to get user info: {e}")
            return {}
    
    def solve(
        self,
        captcha: Union[str, bytes, io.IOBase],
        timeout: int = 60,
        max_retries: int = 1
    ) -> CaptchaResult:
        """
        Solve a single CAPTCHA.
        
        Args:
            captcha: File path, bytes, or file-like object
            timeout: Max time to wait for solution (seconds)
            max_retries: Number of retry attempts
        
        Returns:
            CaptchaResult with solved text or error details
        """
        start_time = time.time()
        initial_balance = self.get_balance()
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Solving CAPTCHA (attempt {attempt + 1}/{max_retries})")
                
                # Convert bytes to file-like object if needed
                if isinstance(captcha, bytes):
                    captcha_input = io.BytesIO(captcha)
                else:
                    captcha_input = captcha
                
                # Solve CAPTCHA
                result = self._client.decode(captcha_input, timeout=timeout)
                
                if result and result.get('text'):
                    elapsed = time.time() - start_time
                    cost = initial_balance - self.get_balance()
                    
                    logger.info(
                        f"✓ CAPTCHA solved: {result['text']} "
                        f"(ID: {result['captcha']}, Cost: ${cost/100:.4f}, "
                        f"Time: {elapsed:.1f}s)"
                    )
                    
                    return CaptchaResult(
                        success=True,
                        text=result.get('text'),
                        captcha_id=result.get('captcha'),
                        is_correct=result.get('is_correct'),
                        cost_cents=cost,
                        time_seconds=elapsed
                    )
                else:
                    logger.warning("CAPTCHA was not solved (timeout or failed)")
                    
            except AccessDeniedException as e:
                logger.error(f"Authentication failed: {e}")
                return CaptchaResult(
                    success=False,
                    error=f"Authentication failed: {str(e)}"
                )
            except ValueError as e:
                logger.error(f"Invalid CAPTCHA image: {e}")
                return CaptchaResult(
                    success=False,
                    error=f"Invalid image: {str(e)}"
                )
            except OverflowError as e:
                logger.warning(f"Service overload, retrying: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                continue
            except Exception as e:
                logger.error(f"Error solving CAPTCHA: {e}")
                if attempt < max_retries - 1:
                    time.sleep(2 ** attempt)
                    continue
        
        elapsed = time.time() - start_time
        return CaptchaResult(
            success=False,
            error="Failed to solve CAPTCHA after retries",
            time_seconds=elapsed
        )
    
    def solve_batch(
        self,
        captchas: List[Union[str, bytes]],
        timeout: int = 60,
        max_per_batch: Optional[int] = None,
        min_balance_cents: int = 100
    ) -> List[CaptchaResult]:
        """
        Solve multiple CAPTCHAs efficiently.
        
        Args:
            captchas: List of file paths or bytes
            timeout: Max time per CAPTCHA
            max_per_batch: Max CAPTCHAs to solve (budget limit)
            min_balance_cents: Stop if balance falls below this
        
        Returns:
            List of CaptchaResult objects
        """
        results = []
        initial_balance = self.get_balance()
        
        logger.info(f"Starting batch solve of {len(captchas)} CAPTCHAs")
        
        for i, captcha in enumerate(captchas):
            # Check budget
            if max_per_batch and i >= max_per_batch:
                logger.info(f"Reached batch limit ({max_per_batch})")
                break
            
            current_balance = self.get_balance()
            if current_balance < min_balance_cents:
                logger.warning(
                    f"Balance too low (${current_balance/100:.2f}), stopping"
                )
                break
            
            # Solve
            result = self.solve(captcha, timeout=timeout)
            results.append(result)
            
            # Log progress
            successful = sum(1 for r in results if r.success)
            spent = initial_balance - self.get_balance()
            logger.info(
                f"Progress: {i+1}/{len(captchas)} "
                f"({successful} solved, ${spent/100:.2f} spent)"
            )
        
        return results
    
    def report_incorrect(self, captcha_id: int) -> bool:
        """
        Report a CAPTCHA as incorrectly solved (for refund).
        
        Args:
            captcha_id: ID of the CAPTCHA to report
        
        Returns:
            True if reported successfully
        """
        try:
            result = self._client.report(captcha_id)
            if result:
                logger.info(f"✓ Reported CAPTCHA {captcha_id} for refund")
                return True
            else:
                logger.warning(f"Failed to report CAPTCHA {captcha_id}")
                return False
        except Exception as e:
            logger.error(f"Error reporting CAPTCHA: {e}")
            return False
    
    def close(self):
        """Close client connection"""
        if self._client and hasattr(self._client, 'close'):
            try:
                self._client.close()
                logger.info("Client connection closed")
            except Exception as e:
                logger.error(f"Error closing client: {e}")
    
    def __enter__(self):
        """Context manager entry"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
    
    def __del__(self):
        """Cleanup on garbage collection"""
        if self.auto_close:
            self.close()


# Convenience function for quick solving
def solve_captcha_quick(
    username: str,
    password: str,
    captcha: Union[str, bytes],
    timeout: int = 60
) -> Optional[str]:
    """
    Quick convenience function to solve a CAPTCHA.
    
    Args:
        username: DBC username
        password: DBC password
        captcha: File path or bytes
        timeout: Solving timeout
    
    Returns:
        Solved text or None
    """
    with CaptchaSolver(username, password) as solver:
        result = solver.solve(captcha, timeout=timeout)
        return result.text if result.success else None


if __name__ == '__main__':
    # Example usage
    import sys
    
    if len(sys.argv) < 4:
        print("Usage: python agent_wrapper.py <username> <password> <captcha_path>")
        sys.exit(1)
    
    username, password, captcha_path = sys.argv[1:4]
    
    # Simple solve
    text = solve_captcha_quick(username, password, captcha_path)
    if text:
        print(f"Solved: {text}")
    else:
        print("Failed to solve")
