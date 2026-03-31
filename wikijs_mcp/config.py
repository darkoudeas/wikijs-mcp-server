"""Configuration management for WikiJS MCP Server."""

import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv


class WikiJSConfig(BaseModel):
    """Configuration for Wiki.js connection."""

    url: str = Field(default="")
    api_key: str = Field(default="")
    graphql_endpoint: str = Field(default="/graphql")
    debug: bool = Field(default=False)

    # HTTP Server configuration
    http_host: str = Field(default="0.0.0.0")
    http_port: int = Field(default=8000)
    cors_origins: list[str] = Field(default=["*"])

    # MCP Streamable HTTP transport security configuration
    # Use these for reverse-proxy/cloud deployments where Host/Origin differ
    # from localhost defaults.
    mcp_public_host: Optional[str] = Field(default=None)
    mcp_enable_dns_rebinding_protection: bool = Field(default=False)
    mcp_allowed_hosts: list[str] = Field(default_factory=list)
    mcp_allowed_origins: list[str] = Field(default_factory=list)

    @classmethod
    def load_config(cls, env_file: str = ".env") -> "WikiJSConfig":
        """Load configuration from .env file."""
        if os.path.exists(env_file):
            load_dotenv(env_file)
        else:
            print(
                f"No configuration found at {env_file}. Please create a .env file with your WikiJS settings."
            )

        return cls(
            url=os.getenv("WIKIJS_URL", ""),
            api_key=os.getenv("WIKIJS_API_KEY", ""),
            graphql_endpoint=os.getenv("WIKIJS_GRAPHQL_ENDPOINT", "/graphql"),
            debug=os.getenv("DEBUG", "false").lower() == "true",
            http_host=os.getenv("HTTP_HOST", "0.0.0.0"),
            http_port=int(os.getenv("HTTP_PORT", "8000")),
            cors_origins=(
                os.getenv("CORS_ORIGINS", "*").split(",")
                if os.getenv("CORS_ORIGINS")
                else ["*"]
            ),
            mcp_public_host=os.getenv("MCP_PUBLIC_HOST") or None,
            mcp_enable_dns_rebinding_protection=(
                os.getenv("MCP_ENABLE_DNS_REBINDING_PROTECTION", "false").lower()
                == "true"
            ),
            mcp_allowed_hosts=(
                [item.strip() for item in os.getenv("MCP_ALLOWED_HOSTS", "").split(",")]
                if os.getenv("MCP_ALLOWED_HOSTS")
                else []
            ),
            mcp_allowed_origins=(
                [
                    item.strip()
                    for item in os.getenv("MCP_ALLOWED_ORIGINS", "").split(",")
                ]
                if os.getenv("MCP_ALLOWED_ORIGINS")
                else []
            ),
        )

    @property
    def graphql_url(self) -> str:
        """Get the full GraphQL endpoint URL."""
        return f"{self.url.rstrip('/')}{self.graphql_endpoint}"

    @property
    def headers(self) -> dict[str, str]:
        """Get authentication headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

    def validate_config(self) -> None:
        """Validate that required configuration is present."""
        if not self.url:
            raise ValueError("WIKIJS_URL must be set in your .env file.")
        if not self.api_key:
            raise ValueError("WIKIJS_API_KEY must be set in your .env file.")
