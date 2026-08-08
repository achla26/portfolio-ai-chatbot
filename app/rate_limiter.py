"""
Simple in-memory rate limiter for FastAPI
Tracks requests per IP with time-based windows
"""
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Dict, List
from fastapi import Request, HTTPException


class RateLimiter:
    def __init__(
        self,
        per_minute: int = 5,
        per_day: int = 50,
        global_per_day: int = 500,
    ):
        self.per_minute = per_minute
        self.per_day = per_day
        self.global_per_day = global_per_day
        
        # Storage: {ip: [timestamp1, timestamp2, ...]}
        self.requests: Dict[str, List[datetime]] = defaultdict(list)
        
        # Global counter for the day
        self.global_requests: List[datetime] = []
        
        # Whitelisted IPs (no limits)
        self.whitelist: set = set()

    def add_to_whitelist(self, ip: str):
        """Add IP to whitelist (bypass limits)"""
        self.whitelist.add(ip)

    def _cleanup_old_requests(self, ip: str):
        """Remove requests older than 24 hours"""
        now = datetime.now()
        day_ago = now - timedelta(days=1)
        
        # Cleanup per-IP requests
        if ip in self.requests:
            self.requests[ip] = [
                ts for ts in self.requests[ip] if ts > day_ago
            ]
            
            # Cleanup empty entries
            if not self.requests[ip]:
                del self.requests[ip]
        
        # Cleanup global requests
        self.global_requests = [
            ts for ts in self.global_requests if ts > day_ago
        ]

    def check_rate_limit(self, request: Request):
        """
        Check if request should be rate limited
        Raises HTTPException 429 if limit exceeded
        """
        # Get client IP
        ip = self._get_client_ip(request)
        
        # Skip if whitelisted
        if ip in self.whitelist:
            return
        
        # Cleanup old entries
        self._cleanup_old_requests(ip)
        
        now = datetime.now()
        
        # Check global daily limit
        if len(self.global_requests) >= self.global_per_day:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "global_limit_exceeded",
                    "message": "The AI has reached its daily limit. Please try again tomorrow!",
                    "retry_after": "24 hours"
                }
            )
        
        # Get requests for this IP
        ip_requests = self.requests.get(ip, [])
        
        # Check per-minute limit
        minute_ago = now - timedelta(minutes=1)
        recent_requests = [ts for ts in ip_requests if ts > minute_ago]
        
        if len(recent_requests) >= self.per_minute:
            wait_seconds = int(
                (recent_requests[0] + timedelta(minutes=1) - now).total_seconds()
            )
            wait_seconds = max(1, wait_seconds)  # At least 1 second
            
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "rate_limit_exceeded",
                    "message": f"You're sending messages too quickly! Please wait {wait_seconds} seconds.",
                    "retry_after": f"{wait_seconds} seconds",
                    "limit_type": "per_minute"
                }
            )
        
        # Check per-day limit
        if len(ip_requests) >= self.per_day:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "daily_limit_exceeded",
                    "message": f"You've reached your daily limit of {self.per_day} messages. Please try again tomorrow!",
                    "retry_after": "24 hours",
                    "limit_type": "per_day"
                }
            )
        
        # Record this request
        self.requests[ip].append(now)
        self.global_requests.append(now)

    def _get_client_ip(self, request: Request) -> str:
        """Get client IP from request headers"""
        # Check for forwarded IP (behind proxy like Render/Vercel)
        forwarded = request.headers.get("X-Forwarded-For")
        if forwarded:
            return forwarded.split(",")[0].strip()
        
        # Check for real IP header
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # Fallback to client host
        return request.client.host if request.client else "unknown"

    def get_stats(self) -> dict:
        """Get current stats (for debugging/admin)"""
        return {
            "total_ips_tracked": len(self.requests),
            "global_requests_today": len(self.global_requests),
            "global_limit": self.global_per_day,
            "whitelist_count": len(self.whitelist),
            "limits": {
                "per_minute": self.per_minute,
                "per_day": self.per_day,
                "global_per_day": self.global_per_day,
            }
        }


# Create global instance with recommended limits
rate_limiter = RateLimiter(
    per_minute=5,        # 5 requests per minute per IP
    per_day=50,          # 50 requests per day per IP  
    global_per_day=500  # 500 total requests per day (Groq free tier safety)
)