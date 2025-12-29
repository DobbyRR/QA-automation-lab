"""Configuration helpers for the API client."""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    """Holds runtime configuration for Coupang HTTP requests."""

    base_url: str
    cdn_url: str
    timeout: float = 5.0
    user_agent: str = "QA-Automation-Lab/0.1 (+pytest requests)"

    def for_cdn(self) -> "Settings":
        """Return a copy configured to target the Coupang CDN."""
        return Settings(
            base_url=self.cdn_url,
            cdn_url=self.cdn_url,
            timeout=self.timeout,
            user_agent=self.user_agent,
        )


def get_settings() -> Settings:
    """Load settings from environment with safe defaults tailored for Coupang."""
    base_url = os.getenv("QA_LAB_BASE_URL", "https://www.coupang.com").rstrip("/")
    cdn_url = os.getenv("QA_LAB_CDN_URL", "https://static.coupangcdn.com").rstrip("/")
    timeout = float(os.getenv("QA_LAB_TIMEOUT", "5"))
    user_agent = os.getenv(
        "QA_LAB_USER_AGENT", "QA-Automation-Lab/0.1 (+pytest requests)"
    )
    return Settings(
        base_url=base_url,
        cdn_url=cdn_url,
        timeout=timeout,
        user_agent=user_agent,
    )
