#!/usr/bin/env python3
"""
Production-ready Selenium MCP Server

A comprehensive Model Context Protocol server for Selenium browser automation
with enterprise-grade features, error handling, and monitoring capabilities.
"""

import asyncio
import atexit
import base64
import json
import logging
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

# Core MCP and async libraries
from mcp.server.fastmcp import FastMCP
from mcp.types import Tool, TextContent, ImageContent

# Selenium WebDriver imports
from selenium import webdriver
from selenium.common.exceptions import (
    ElementNotInteractableException,
    NoSuchElementException,
    TimeoutException,
    WebDriverException,
)
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

# Environment configuration
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration constants
DEFAULT_TIMEOUT = int(os.getenv("SELENIUM_DEFAULT_TIMEOUT", "10000"))
MAX_SESSIONS = int(os.getenv("SELENIUM_MAX_SESSIONS", "5"))
LOG_LEVEL = os.getenv("SELENIUM_LOG_LEVEL", "INFO")
SCREENSHOT_DIR = os.getenv("SELENIUM_SCREENSHOT_DIR", "screenshots")

# Ensure screenshots directory exists
Path(SCREENSHOT_DIR).mkdir(exist_ok=True)


@dataclass
class BrowserSession:
    """Browser session data structure."""
    driver: webdriver.Remote
    browser_type: str
    session_id: str
    options: Dict[str, Any]
    created_at: str
    last_activity: str


class SeleniumMCPServer:
    """Production Selenium MCP Server with advanced session management."""

    def __init__(self):
        """Initialize the Selenium MCP Server."""
        self.sessions: Dict[str, BrowserSession] = {}
        self.active_session: Optional[str] = None
        self.start_time = time.time()
        
        # Setup logging
        self.logger = self._setup_logging()
        
        # Locator strategy mapping
        self.locator_strategies = {
            "id": By.ID,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "name": By.NAME,
            "tag": By.TAG_NAME,
            "class": By.CLASS_NAME,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        
        # Register cleanup on exit
        atexit.register(self.cleanup)
        
        self.logger.info("Selenium MCP Server initialized")

    def _setup_logging(self) -> logging.Logger:
        """Setup comprehensive logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, LOG_LEVEL.upper()))
        
        # Create rotating file handler
        handler = RotatingFileHandler(
            "selenium_mcp_server.log",
            maxBytes=10485760,  # 10MB
            backupCount=5
        )
        
        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
        )
        handler.setFormatter(formatter)
        
        # Add handler to logger
        if not logger.handlers:
            logger.addHandler(handler)
            
        # Also log to console in development
        if LOG_LEVEL.upper() == "DEBUG":
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)
            
        return logger

    def _validate_locator(self, by: str, value: str) -> tuple:
        """Validate and convert locator strategy."""
        if by not in self.locator_strategies:
            raise ValueError(f"Invalid locator strategy: {by}. Valid strategies: {list(self.locator_strategies.keys())}")
        return self.locator_strategies[by], value

    def _get_driver_options(self, browser: str, options: Dict[str, Any] = None) -> Any:
        """Get configured browser options."""
        options = options or {}
        
        if browser.lower() == "chrome":
            chrome_options = ChromeOptions()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--remote-debugging-port=9222")
            
            if options.get("headless", False):
                chrome_options.add_argument("--headless")
            
            window_size = options.get("window_size", [1920, 1080])
            chrome_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
            
            # Additional Chrome options
            for arg in options.get("additional_args", []):
                chrome_options.add_argument(arg)
                
            return chrome_options
            
        elif browser.lower() == "firefox":
            firefox_options = FirefoxOptions()
            
            if options.get("headless", False):
                firefox_options.add_argument("--headless")
                
            window_size = options.get("window_size", [1920, 1080])
            firefox_options.add_argument(f"--width={window_size[0]}")
            firefox_options.add_argument(f"--height={window_size[1]}")
            
            return firefox_options
            
        elif browser.lower() == "edge":
            edge_options = EdgeOptions()
            edge_options.add_argument("--no-sandbox")
            edge_options.add_argument("--disable-dev-shm-usage")
            
            if options.get("headless", False):
                edge_options.add_argument("--headless")
                
            window_size = options.get("window_size", [1920, 1080])
            edge_options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
            
            return edge_options
            
        else:
            raise ValueError(f"Unsupported browser: {browser}")

    def _create_driver(self, browser: str, options: Dict[str, Any] = None) -> webdriver.Remote:
        """Create a new WebDriver instance."""
        browser_options = self._get_driver_options(browser, options)
        
        try:
            if browser.lower() == "chrome":
                return webdriver.Chrome(options=browser_options)
            elif browser.lower() == "firefox":
                return webdriver.Firefox(options=browser_options)
            elif browser.lower() == "edge":
                return webdriver.Edge(options=browser_options)
            else:
                raise ValueError(f"Unsupported browser: {browser}")
                
        except Exception as e:
            self.logger.error(f"Failed to create {browser} driver: {str(e)}")
            raise WebDriverException(f"Failed to create {browser} driver: {str(e)}")

    def _get_current_driver(self) -> webdriver.Remote:
        """Get the current active driver."""
        if not self.active_session or self.active_session not in self.sessions:
            raise RuntimeError("No active browser session")
        return self.sessions[self.active_session].driver

    def _update_activity(self, session_id: str = None):
        """Update last activity timestamp for a session."""
        session_id = session_id or self.active_session
        if session_id and session_id in self.sessions:
            self.sessions[session_id].last_activity = datetime.now().isoformat()

    def _find_element_with_timeout(self, by: str, value: str, timeout: int = None) -> Any:
        """Find element with explicit timeout and better error handling."""
        timeout = timeout or DEFAULT_TIMEOUT
        driver = self._get_current_driver()
        locator_by, locator_value = self._validate_locator(by, value)
        
        try:
            wait = WebDriverWait(driver, timeout / 1000)  # Convert ms to seconds
            element = wait.until(EC.presence_of_element_located((locator_by, locator_value)))
            self._update_activity()
            return element
        except TimeoutException:
            raise TimeoutException(f"Element not found within {timeout}ms: {by}='{value}'")

    def _find_elements_with_timeout(self, by: str, value: str, timeout: int = None) -> List[Any]:
        """Find multiple elements with explicit timeout."""
        timeout = timeout or DEFAULT_TIMEOUT
        driver = self._get_current_driver()
        locator_by, locator_value = self._validate_locator(by, value)
        
        try:
            wait = WebDriverWait(driver, timeout / 1000)
            elements = wait.until(EC.presence_of_all_elements_located((locator_by, locator_value)))
            self._update_activity()
            return elements
        except TimeoutException:
            raise TimeoutException(f"Elements not found within {timeout}ms: {by}='{value}'")

    def _sanitize_file_path(self, file_path: str) -> str:
        """Sanitize and validate file path for security."""
        # Convert to absolute path and resolve any relative components
        resolved_path = os.path.abspath(file_path)
        
        # Ensure the file exists
        if not os.path.isfile(resolved_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        return resolved_path

    def cleanup(self):
        """Cleanup all browser sessions."""
        self.logger.info("Cleaning up browser sessions...")
        for session_id in list(self.sessions.keys()):
            try:
                self.sessions[session_id].driver.quit()
                del self.sessions[session_id]
            except Exception as e:
                self.logger.error(f"Error closing session {session_id}: {str(e)}")
        self.active_session = None
        self.logger.info("Cleanup completed")


# Initialize server instance
server_instance = SeleniumMCPServer()

# Create FastMCP app
mcp = FastMCP("Selenium MCP Server")


@mcp.tool()
def start_browser(browser: str = "chrome", options: Dict[str, Any] = None) -> Dict[str, Any]:
    """
    Start a new browser session.
    
    Args:
        browser: Browser type (chrome, firefox, edge)
        options: Browser configuration options
    
    Returns:
        Dictionary with session information
    """
    try:
        if len(server_instance.sessions) >= MAX_SESSIONS:
            return {
                "success": False,
                "error": f"Maximum number of sessions ({MAX_SESSIONS}) reached",
                "error_type": "ResourceLimitError"
            }
        
        options = options or {}
        session_id = str(uuid.uuid4())
        
        driver = server_instance._create_driver(browser, options)
        
        session = BrowserSession(
            driver=driver,
            browser_type=browser,
            session_id=session_id,
            options=options,
            created_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat()
        )
        
        server_instance.sessions[session_id] = session
        server_instance.active_session = session_id
        
        server_instance.logger.info(f"Started {browser} browser session: {session_id}")
        
        return {
            "success": True,
            "session_id": session_id,
            "browser_type": browser,
            "message": f"Started {browser} browser session"
        }
        
    except Exception as e:
        error_msg = f"Failed to start browser: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def close_session(session_id: str = None) -> Dict[str, Any]:
    """
    Close a browser session.
    
    Args:
        session_id: Session ID to close (current session if not provided)
    
    Returns:
        Operation result
    """
    try:
        session_id = session_id or server_instance.active_session
        
        if not session_id or session_id not in server_instance.sessions:
            return {
                "success": False,
                "error": "Invalid session ID",
                "error_type": "InvalidSessionError"
            }
        
        server_instance.sessions[session_id].driver.quit()
        del server_instance.sessions[session_id]
        
        if server_instance.active_session == session_id:
            server_instance.active_session = next(iter(server_instance.sessions.keys()), None)
        
        server_instance.logger.info(f"Closed browser session: {session_id}")
        
        return {
            "success": True,
            "message": f"Session {session_id} closed successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to close session: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def get_session_info() -> Dict[str, Any]:
    """
    Get information about active sessions.
    
    Returns:
        Session information
    """
    try:
        sessions_info = {}
        
        for session_id, session in server_instance.sessions.items():
            try:
                current_url = session.driver.current_url
                title = session.driver.title
            except:
                current_url = "Unknown"
                title = "Unknown"
            
            sessions_info[session_id] = {
                "browser_type": session.browser_type,
                "current_url": current_url,
                "title": title,
                "created_at": session.created_at,
                "last_activity": session.last_activity,
                "is_active": session_id == server_instance.active_session
            }
        
        return {
            "success": True,
            "active_session": server_instance.active_session,
            "total_sessions": len(server_instance.sessions),
            "sessions": sessions_info
        }
        
    except Exception as e:
        error_msg = f"Failed to get session info: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def navigate(url: str) -> Dict[str, Any]:
    """
    Navigate to a URL.
    
    Args:
        url: URL to navigate to
    
    Returns:
        Navigation result
    """
    try:
        driver = server_instance._get_current_driver()
        driver.get(url)
        server_instance._update_activity()
        
        server_instance.logger.info(f"Navigated to: {url}")
        
        return {
            "success": True,
            "url": url,
            "current_url": driver.current_url,
            "title": driver.title
        }
        
    except Exception as e:
        error_msg = f"Failed to navigate to {url}: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__,
            "suggestion": "Check if the URL is valid and accessible"
        }


@mcp.tool()
def get_current_url() -> Dict[str, Any]:
    """
    Get the current URL of the active browser.
    
    Returns:
        Current URL information
    """
    try:
        driver = server_instance._get_current_driver()
        url = driver.current_url
        title = driver.title
        
        return {
            "success": True,
            "current_url": url,
            "title": title
        }
        
    except Exception as e:
        error_msg = f"Failed to get current URL: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def refresh_page() -> Dict[str, Any]:
    """
    Refresh the current page.
    
    Returns:
        Refresh result
    """
    try:
        driver = server_instance._get_current_driver()
        driver.refresh()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Page refreshed successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to refresh page: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def go_back() -> Dict[str, Any]:
    """
    Go back in browser history.
    
    Returns:
        Navigation result
    """
    try:
        driver = server_instance._get_current_driver()
        driver.back()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Navigated back in history",
            "current_url": driver.current_url
        }
        
    except Exception as e:
        error_msg = f"Failed to go back: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def go_forward() -> Dict[str, Any]:
    """
    Go forward in browser history.
    
    Returns:
        Navigation result
    """
    try:
        driver = server_instance._get_current_driver()
        driver.forward()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Navigated forward in history",
            "current_url": driver.current_url
        }
        
    except Exception as e:
        error_msg = f"Failed to go forward: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def find_element(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Find an element on the page.
    
    Args:
        by: Locator strategy (id, css, xpath, name, tag, class, link_text, partial_link_text)
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Element information
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        
        return {
            "success": True,
            "element_found": True,
            "tag_name": element.tag_name,
            "text": element.text[:100] if element.text else "",
            "location": element.location,
            "size": element.size,
            "is_displayed": element.is_displayed(),
            "is_enabled": element.is_enabled()
        }
        
    except TimeoutException as e:
        return {
            "success": False,
            "element_found": False,
            "error": str(e),
            "error_type": "TimeoutException",
            "suggestion": "Try increasing timeout or verifying locator"
        }
    except Exception as e:
        error_msg = f"Failed to find element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def find_elements(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Find multiple elements on the page.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Elements information
    """
    try:
        elements = server_instance._find_elements_with_timeout(by, value, timeout)
        
        elements_info = []
        for i, element in enumerate(elements):
            elements_info.append({
                "index": i,
                "tag_name": element.tag_name,
                "text": element.text[:100] if element.text else "",
                "location": element.location,
                "size": element.size,
                "is_displayed": element.is_displayed(),
                "is_enabled": element.is_enabled()
            })
        
        return {
            "success": True,
            "elements_found": len(elements),
            "elements": elements_info
        }
        
    except Exception as e:
        error_msg = f"Failed to find elements: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def click_element(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Click an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Click result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        
        # Scroll to element if needed
        driver = server_instance._get_current_driver()
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        
        # Wait for element to be clickable
        wait = WebDriverWait(driver, timeout / 1000)
        clickable_element = wait.until(EC.element_to_be_clickable(element))
        
        clickable_element.click()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Element clicked successfully",
            "element_tag": element.tag_name
        }
        
    except ElementNotInteractableException as e:
        return {
            "success": False,
            "error": f"Element not interactable: {str(e)}",
            "error_type": "ElementNotInteractableException",
            "suggestion": "Element may be hidden or disabled"
        }
    except Exception as e:
        error_msg = f"Failed to click element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def double_click_element(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Double-click an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Double-click result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        driver = server_instance._get_current_driver()
        
        actions = ActionChains(driver)
        actions.double_click(element).perform()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Element double-clicked successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to double-click element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def right_click_element(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Right-click an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Right-click result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        driver = server_instance._get_current_driver()
        
        actions = ActionChains(driver)
        actions.context_click(element).perform()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Element right-clicked successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to right-click element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def send_keys(by: str, value: str, text: str, timeout: int = 10000, clear_first: bool = True) -> Dict[str, Any]:
    """
    Send keys to an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        text: Text to send
        timeout: Timeout in milliseconds
        clear_first: Clear element before typing
    
    Returns:
        Send keys result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        
        if clear_first:
            element.clear()
        
        element.send_keys(text)
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": f"Sent keys to element: '{text[:50]}{'...' if len(text) > 50 else ''}'"
        }
        
    except Exception as e:
        error_msg = f"Failed to send keys: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def clear_element(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Clear an element's content.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Clear result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        element.clear()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Element cleared successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to clear element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def hover(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Hover over an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Hover result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        driver = server_instance._get_current_driver()
        
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Hovered over element successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to hover over element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def drag_and_drop(source_by: str, source_value: str, target_by: str, target_value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Drag and drop from source to target element.
    
    Args:
        source_by: Source element locator strategy
        source_value: Source element locator value
        target_by: Target element locator strategy
        target_value: Target element locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Drag and drop result
    """
    try:
        source_element = server_instance._find_element_with_timeout(source_by, source_value, timeout)
        target_element = server_instance._find_element_with_timeout(target_by, target_value, timeout)
        driver = server_instance._get_current_driver()
        
        actions = ActionChains(driver)
        actions.drag_and_drop(source_element, target_element).perform()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Drag and drop completed successfully"
        }
        
    except Exception as e:
        error_msg = f"Failed to perform drag and drop: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def press_key(key: str) -> Dict[str, Any]:
    """
    Press a special key.
    
    Args:
        key: Key to press (e.g., 'ENTER', 'TAB', 'ESCAPE')
    
    Returns:
        Key press result
    """
    try:
        driver = server_instance._get_current_driver()
        
        # Map key names to Selenium Keys
        key_mapping = {
            'ENTER': Keys.ENTER,
            'TAB': Keys.TAB,
            'ESCAPE': Keys.ESCAPE,
            'SPACE': Keys.SPACE,
            'BACKSPACE': Keys.BACKSPACE,
            'DELETE': Keys.DELETE,
            'F1': Keys.F1, 'F2': Keys.F2, 'F3': Keys.F3, 'F4': Keys.F4,
            'F5': Keys.F5, 'F6': Keys.F6, 'F7': Keys.F7, 'F8': Keys.F8,
            'F9': Keys.F9, 'F10': Keys.F10, 'F11': Keys.F11, 'F12': Keys.F12,
            'ARROW_UP': Keys.ARROW_UP, 'ARROW_DOWN': Keys.ARROW_DOWN,
            'ARROW_LEFT': Keys.ARROW_LEFT, 'ARROW_RIGHT': Keys.ARROW_RIGHT
        }
        
        if key.upper() not in key_mapping:
            return {
                "success": False,
                "error": f"Unsupported key: {key}",
                "supported_keys": list(key_mapping.keys())
            }
        
        actions = ActionChains(driver)
        actions.send_keys(key_mapping[key.upper()]).perform()
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": f"Pressed key: {key}"
        }
        
    except Exception as e:
        error_msg = f"Failed to press key: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def upload_file(by: str, value: str, file_path: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Upload a file to a file input element.
    
    Args:
        by: Locator strategy
        value: Locator value
        file_path: Path to the file to upload
        timeout: Timeout in milliseconds
    
    Returns:
        Upload result
    """
    try:
        # Sanitize and validate file path
        safe_file_path = server_instance._sanitize_file_path(file_path)
        
        element = server_instance._find_element_with_timeout(by, value, timeout)
        element.send_keys(safe_file_path)
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": f"File uploaded successfully: {os.path.basename(safe_file_path)}"
        }
        
    except FileNotFoundError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "FileNotFoundError",
            "suggestion": "Check if the file path is correct and the file exists"
        }
    except Exception as e:
        error_msg = f"Failed to upload file: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def select_dropdown_option(by: str, value: str, option_text: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Select an option from a dropdown.
    
    Args:
        by: Locator strategy
        value: Locator value
        option_text: Text of the option to select
        timeout: Timeout in milliseconds
    
    Returns:
        Selection result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        select = Select(element)
        select.select_by_visible_text(option_text)
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": f"Selected option: {option_text}"
        }
        
    except Exception as e:
        error_msg = f"Failed to select dropdown option: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__,
            "suggestion": "Check if the element is a dropdown and the option text exists"
        }


@mcp.tool()
def get_element_text(by: str, value: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Get text content from an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
    
    Returns:
        Element text
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        text = element.text
        
        return {
            "success": True,
            "text": text,
            "length": len(text)
        }
        
    except Exception as e:
        error_msg = f"Failed to get element text: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def get_element_attribute(by: str, value: str, attribute: str, timeout: int = 10000) -> Dict[str, Any]:
    """
    Get an attribute value from an element.
    
    Args:
        by: Locator strategy
        value: Locator value
        attribute: Attribute name
        timeout: Timeout in milliseconds
    
    Returns:
        Attribute value
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        attr_value = element.get_attribute(attribute)
        
        return {
            "success": True,
            "attribute": attribute,
            "value": attr_value
        }
        
    except Exception as e:
        error_msg = f"Failed to get element attribute: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def get_page_source() -> Dict[str, Any]:
    """
    Get the page source.
    
    Returns:
        Page source
    """
    try:
        driver = server_instance._get_current_driver()
        source = driver.page_source
        
        return {
            "success": True,
            "source": source,
            "length": len(source)
        }
        
    except Exception as e:
        error_msg = f"Failed to get page source: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def get_page_title() -> Dict[str, Any]:
    """
    Get the page title.
    
    Returns:
        Page title
    """
    try:
        driver = server_instance._get_current_driver()
        title = driver.title
        
        return {
            "success": True,
            "title": title
        }
        
    except Exception as e:
        error_msg = f"Failed to get page title: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def take_screenshot(output_path: str = None) -> Dict[str, Any]:
    """
    Take a screenshot of the current page.
    
    Args:
        output_path: Path to save screenshot (auto-generated if not provided)
    
    Returns:
        Screenshot result with base64 data
    """
    try:
        driver = server_instance._get_current_driver()
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{timestamp}.png")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Take screenshot
        success = driver.save_screenshot(output_path)
        
        if success:
            # Read screenshot and encode as base64
            with open(output_path, "rb") as f:
                screenshot_data = base64.b64encode(f.read()).decode()
            
            file_size = os.path.getsize(output_path)
            
            return {
                "success": True,
                "screenshot_path": output_path,
                "file_size": file_size,
                "base64_data": screenshot_data
            }
        else:
            return {
                "success": False,
                "error": "Failed to save screenshot",
                "error_type": "ScreenshotError"
            }
        
    except Exception as e:
        error_msg = f"Failed to take screenshot: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def take_element_screenshot(by: str, value: str, output_path: str = None, timeout: int = 10000) -> Dict[str, Any]:
    """
    Take a screenshot of a specific element.
    
    Args:
        by: Locator strategy
        value: Locator value
        output_path: Path to save screenshot
        timeout: Timeout in milliseconds
    
    Returns:
        Element screenshot result
    """
    try:
        element = server_instance._find_element_with_timeout(by, value, timeout)
        
        if output_path is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = os.path.join(SCREENSHOT_DIR, f"element_screenshot_{timestamp}.png")
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Take element screenshot
        success = element.screenshot(output_path)
        
        if success:
            # Read screenshot and encode as base64
            with open(output_path, "rb") as f:
                screenshot_data = base64.b64encode(f.read()).decode()
            
            file_size = os.path.getsize(output_path)
            
            return {
                "success": True,
                "screenshot_path": output_path,
                "file_size": file_size,
                "base64_data": screenshot_data
            }
        else:
            return {
                "success": False,
                "error": "Failed to save element screenshot",
                "error_type": "ScreenshotError"
            }
        
    except Exception as e:
        error_msg = f"Failed to take element screenshot: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def wait_for_element(by: str, value: str, timeout: int = 10000, condition: str = "presence") -> Dict[str, Any]:
    """
    Wait for an element with specific condition.
    
    Args:
        by: Locator strategy
        value: Locator value
        timeout: Timeout in milliseconds
        condition: Wait condition (presence, visible, clickable)
    
    Returns:
        Wait result
    """
    try:
        driver = server_instance._get_current_driver()
        locator_by, locator_value = server_instance._validate_locator(by, value)
        wait = WebDriverWait(driver, timeout / 1000)
        
        if condition == "presence":
            element = wait.until(EC.presence_of_element_located((locator_by, locator_value)))
        elif condition == "visible":
            element = wait.until(EC.visibility_of_element_located((locator_by, locator_value)))
        elif condition == "clickable":
            element = wait.until(EC.element_to_be_clickable((locator_by, locator_value)))
        else:
            return {
                "success": False,
                "error": f"Invalid condition: {condition}",
                "supported_conditions": ["presence", "visible", "clickable"]
            }
        
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": f"Element found with condition '{condition}'",
            "element_info": {
                "tag_name": element.tag_name,
                "text": element.text[:100] if element.text else "",
                "is_displayed": element.is_displayed(),
                "is_enabled": element.is_enabled()
            }
        }
        
    except TimeoutException:
        return {
            "success": False,
            "error": f"Element not found within {timeout}ms with condition '{condition}'",
            "error_type": "TimeoutException",
            "suggestion": "Try increasing timeout or checking the locator"
        }
    except Exception as e:
        error_msg = f"Failed to wait for element: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def wait_for_page_load(timeout: int = 30000) -> Dict[str, Any]:
    """
    Wait for page to load completely.
    
    Args:
        timeout: Timeout in milliseconds
    
    Returns:
        Page load result
    """
    try:
        driver = server_instance._get_current_driver()
        wait = WebDriverWait(driver, timeout / 1000)
        
        # Wait for page to be ready
        wait.until(lambda driver: driver.execute_script("return document.readyState") == "complete")
        server_instance._update_activity()
        
        return {
            "success": True,
            "message": "Page loaded successfully",
            "current_url": driver.current_url,
            "title": driver.title
        }
        
    except TimeoutException:
        return {
            "success": False,
            "error": f"Page did not load within {timeout}ms",
            "error_type": "TimeoutException"
        }
    except Exception as e:
        error_msg = f"Failed to wait for page load: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def execute_script(script: str) -> Dict[str, Any]:
    """
    Execute JavaScript code.
    
    Args:
        script: JavaScript code to execute
    
    Returns:
        Script execution result
    """
    try:
        driver = server_instance._get_current_driver()
        result = driver.execute_script(script)
        server_instance._update_activity()
        
        return {
            "success": True,
            "result": result,
            "script": script[:100] + ("..." if len(script) > 100 else "")
        }
        
    except Exception as e:
        error_msg = f"Failed to execute script: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__,
            "suggestion": "Check JavaScript syntax and ensure script is safe"
        }


@mcp.tool()
def execute_async_script(script: str, timeout: int = 30000) -> Dict[str, Any]:
    """
    Execute asynchronous JavaScript code.
    
    Args:
        script: JavaScript code to execute
        timeout: Timeout in milliseconds
    
    Returns:
        Async script execution result
    """
    try:
        driver = server_instance._get_current_driver()
        driver.set_script_timeout(timeout / 1000)
        result = driver.execute_async_script(script)
        server_instance._update_activity()
        
        return {
            "success": True,
            "result": result,
            "script": script[:100] + ("..." if len(script) > 100 else "")
        }
        
    except Exception as e:
        error_msg = f"Failed to execute async script: {str(e)}"
        server_instance.logger.error(error_msg)
        return {
            "success": False,
            "error": error_msg,
            "error_type": type(e).__name__
        }


@mcp.tool()
def health_check() -> Dict[str, Any]:
    """
    Check server health and status.
    
    Returns:
        Health status information
    """
    try:
        return {
            "status": "healthy",
            "active_sessions": len(server_instance.sessions),
            "max_sessions": MAX_SESSIONS,
            "current_session": server_instance.active_session,
            "uptime_seconds": int(time.time() - server_instance.start_time),
            "version": "1.0.0",
            "supported_browsers": ["chrome", "firefox", "edge"],
            "log_level": LOG_LEVEL,
            "screenshot_directory": SCREENSHOT_DIR
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "error_type": type(e).__name__
        }


def main():
    """Main entry point with proper error handling."""
    try:
        server_instance.logger.info("Starting Selenium MCP Server")
        mcp.run()
    except KeyboardInterrupt:
        server_instance.logger.info("Server stopped by user")
        server_instance.cleanup()
    except Exception as e:
        server_instance.logger.error(f"Server error: {str(e)}")
        server_instance.cleanup()
        sys.exit(1)


if __name__ == "__main__":
    main()
