"""
Configuration management for Selenium MCP Server.

This module provides centralized configuration management with environment variable
support, validation, and production-ready defaults.
"""

import os
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from pathlib import Path


@dataclass
class BrowserConfig:
    """Configuration for browser-specific settings."""
    name: str
    enabled: bool = True
    default_options: Dict[str, Any] = field(default_factory=dict)
    executable_path: Optional[str] = None
    driver_path: Optional[str] = None


@dataclass
class SecurityConfig:
    """Security-related configuration."""
    allow_file_uploads: bool = True
    allowed_file_extensions: List[str] = field(default_factory=lambda: [
        '.txt', '.csv', '.json', '.xml', '.pdf', '.png', '.jpg', '.jpeg', '.gif'
    ])
    max_file_size_mb: int = 10
    restrict_local_files: bool = True
    allowed_domains: List[str] = field(default_factory=list)
    blocked_domains: List[str] = field(default_factory=list)


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    file_path: str = "selenium_mcp_server.log"
    max_file_size_mb: int = 10
    backup_count: int = 5
    console_output: bool = False
    format_string: str = "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"


@dataclass
class PerformanceConfig:
    """Performance and resource management configuration."""
    default_timeout_ms: int = 10000
    max_sessions: int = 5
    session_cleanup_interval_seconds: int = 300
    max_page_load_timeout_ms: int = 30000
    implicit_wait_seconds: int = 0
    enable_session_pooling: bool = False


@dataclass
class ScreenshotConfig:
    """Screenshot configuration."""
    directory: str = "screenshots"
    format: str = "png"
    quality: int = 95
    max_width: int = 1920
    max_height: int = 1080
    auto_cleanup_days: int = 7


@dataclass
class ServerConfig:
    """Main server configuration with all subsystem configurations."""
    
    # Core settings
    server_name: str = "selenium-mcp-server"
    server_version: str = "1.0.0"
    host: str = "localhost"
    port: int = 8000
    
    # Subsystem configurations
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    screenshot: ScreenshotConfig = field(default_factory=ScreenshotConfig)
    
    # Browser configurations
    browsers: Dict[str, BrowserConfig] = field(default_factory=lambda: {
        "chrome": BrowserConfig(
            name="chrome",
            enabled=True,
            default_options={
                "headless": False,
                "window_size": [1920, 1080],
                "additional_args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--remote-debugging-port=9222"
                ]
            }
        ),
        "firefox": BrowserConfig(
            name="firefox",
            enabled=True,
            default_options={
                "headless": False,
                "window_size": [1920, 1080],
                "additional_args": []
            }
        ),
        "edge": BrowserConfig(
            name="edge",
            enabled=True,
            default_options={
                "headless": False,
                "window_size": [1920, 1080],
                "additional_args": [
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            }
        )
    })
    
    def __post_init__(self):
        """Post-initialization validation and setup."""
        self._validate_configuration()
        self._create_directories()
        self._load_environment_overrides()
    
    def _validate_configuration(self):
        """Validate configuration values."""
        # Validate timeout values
        if self.performance.default_timeout_ms < 1000:
            raise ValueError("Default timeout must be at least 1000ms")
        
        if self.performance.max_sessions < 1:
            raise ValueError("Max sessions must be at least 1")
        
        # Validate logging level
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.logging.level.upper() not in valid_levels:
            raise ValueError(f"Invalid log level: {self.logging.level}")
        
        # Validate browser configurations
        for browser_name, browser_config in self.browsers.items():
            if not browser_config.name:
                raise ValueError(f"Browser name cannot be empty for {browser_name}")
        
        # Validate screenshot format
        valid_formats = ["png", "jpeg", "webp"]
        if self.screenshot.format.lower() not in valid_formats:
            raise ValueError(f"Invalid screenshot format: {self.screenshot.format}")
    
    def _create_directories(self):
        """Create necessary directories."""
        # Create screenshot directory
        Path(self.screenshot.directory).mkdir(parents=True, exist_ok=True)
        
        # Create log directory if specified
        log_dir = Path(self.logging.file_path).parent
        if str(log_dir) != ".":
            log_dir.mkdir(parents=True, exist_ok=True)
    
    def _load_environment_overrides(self):
        """Load configuration overrides from environment variables."""
        # Core settings
        self.server_name = os.getenv("SELENIUM_SERVER_NAME", self.server_name)
        self.host = os.getenv("SELENIUM_HOST", self.host)
        
        if port_env := os.getenv("SELENIUM_PORT"):
            try:
                self.port = int(port_env)
            except ValueError:
                pass
        
        # Performance settings
        if timeout_env := os.getenv("SELENIUM_DEFAULT_TIMEOUT"):
            try:
                self.performance.default_timeout_ms = int(timeout_env)
            except ValueError:
                pass
        
        if max_sessions_env := os.getenv("SELENIUM_MAX_SESSIONS"):
            try:
                self.performance.max_sessions = int(max_sessions_env)
            except ValueError:
                pass
        
        # Logging settings
        self.logging.level = os.getenv("SELENIUM_LOG_LEVEL", self.logging.level)
        self.logging.file_path = os.getenv("SELENIUM_LOG_FILE", self.logging.file_path)
        
        if console_env := os.getenv("SELENIUM_LOG_CONSOLE"):
            self.logging.console_output = console_env.lower() in ("true", "1", "yes")
        
        # Screenshot settings
        self.screenshot.directory = os.getenv("SELENIUM_SCREENSHOT_DIR", self.screenshot.directory)
        self.screenshot.format = os.getenv("SELENIUM_SCREENSHOT_FORMAT", self.screenshot.format)
        
        # Security settings
        if file_uploads_env := os.getenv("SELENIUM_ALLOW_FILE_UPLOADS"):
            self.security.allow_file_uploads = file_uploads_env.lower() in ("true", "1", "yes")
        
        if max_file_size_env := os.getenv("SELENIUM_MAX_FILE_SIZE_MB"):
            try:
                self.security.max_file_size_mb = int(max_file_size_env)
            except ValueError:
                pass
    
    def get_browser_config(self, browser_name: str) -> Optional[BrowserConfig]:
        """Get configuration for a specific browser."""
        return self.browsers.get(browser_name.lower())
    
    def is_browser_enabled(self, browser_name: str) -> bool:
        """Check if a browser is enabled."""
        config = self.get_browser_config(browser_name)
        return config is not None and config.enabled
    
    def get_supported_browsers(self) -> List[str]:
        """Get list of supported and enabled browsers."""
        return [name for name, config in self.browsers.items() if config.enabled]
    
    def update_browser_config(self, browser_name: str, **kwargs):
        """Update browser configuration."""
        if browser_name.lower() in self.browsers:
            config = self.browsers[browser_name.lower()]
            for key, value in kwargs.items():
                if hasattr(config, key):
                    setattr(config, key, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "server_name": self.server_name,
            "server_version": self.server_version,
            "host": self.host,
            "port": self.port,
            "logging": {
                "level": self.logging.level,
                "file_path": self.logging.file_path,
                "console_output": self.logging.console_output
            },
            "performance": {
                "default_timeout_ms": self.performance.default_timeout_ms,
                "max_sessions": self.performance.max_sessions,
                "session_cleanup_interval_seconds": self.performance.session_cleanup_interval_seconds
            },
            "security": {
                "allow_file_uploads": self.security.allow_file_uploads,
                "max_file_size_mb": self.security.max_file_size_mb,
                "allowed_file_extensions": self.security.allowed_file_extensions
            },
            "screenshot": {
                "directory": self.screenshot.directory,
                "format": self.screenshot.format,
                "quality": self.screenshot.quality
            },
            "browsers": {
                name: {
                    "name": config.name,
                    "enabled": config.enabled,
                    "default_options": config.default_options
                }
                for name, config in self.browsers.items()
            }
        }
    
    @classmethod
    def from_file(cls, config_file: str) -> "ServerConfig":
        """Load configuration from a JSON or YAML file."""
        import json
        
        config_path = Path(config_file)
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            if config_path.suffix.lower() == '.json':
                config_data = json.load(f)
            elif config_path.suffix.lower() in ['.yml', '.yaml']:
                try:
                    import yaml
                    config_data = yaml.safe_load(f)
                except ImportError:
                    raise ImportError("PyYAML is required to load YAML configuration files")
            else:
                raise ValueError(f"Unsupported configuration file format: {config_path.suffix}")
        
        return cls.from_dict(config_data)
    
    @classmethod
    def from_dict(cls, config_data: Dict[str, Any]) -> "ServerConfig":
        """Create configuration from dictionary."""
        # Extract subsystem configurations
        logging_data = config_data.get("logging", {})
        performance_data = config_data.get("performance", {})
        security_data = config_data.get("security", {})
        screenshot_data = config_data.get("screenshot", {})
        browsers_data = config_data.get("browsers", {})
        
        # Create configuration objects
        logging_config = LoggingConfig(**logging_data)
        performance_config = PerformanceConfig(**performance_data)
        security_config = SecurityConfig(**security_data)
        screenshot_config = ScreenshotConfig(**screenshot_data)
        
        # Create browser configurations
        browsers = {}
        for name, browser_data in browsers_data.items():
            browsers[name] = BrowserConfig(**browser_data)
        
        # Create main configuration
        config = cls(
            server_name=config_data.get("server_name", "selenium-mcp-server"),
            server_version=config_data.get("server_version", "1.0.0"),
            host=config_data.get("host", "localhost"),
            port=config_data.get("port", 8000),
            logging=logging_config,
            performance=performance_config,
            security=security_config,
            screenshot=screenshot_config,
            browsers=browsers if browsers else None
        )
        
        return config
    
    def save_to_file(self, config_file: str):
        """Save configuration to a file."""
        import json
        
        config_path = Path(config_file)
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w', encoding='utf-8') as f:
            if config_path.suffix.lower() == '.json':
                json.dump(self.to_dict(), f, indent=2)
            elif config_path.suffix.lower() in ['.yml', '.yaml']:
                try:
                    import yaml
                    yaml.dump(self.to_dict(), f, default_flow_style=False, indent=2)
                except ImportError:
                    raise ImportError("PyYAML is required to save YAML configuration files")
            else:
                raise ValueError(f"Unsupported configuration file format: {config_path.suffix}")


# Global configuration instance
_config: Optional[ServerConfig] = None


def get_config() -> ServerConfig:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = ServerConfig()
    return _config


def set_config(config: ServerConfig):
    """Set the global configuration instance."""
    global _config
    _config = config


def load_config_from_file(config_file: str):
    """Load configuration from file and set as global."""
    config = ServerConfig.from_file(config_file)
    set_config(config)
    return config


def reset_config():
    """Reset configuration to defaults."""
    global _config
    _config = None
