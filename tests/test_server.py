#!/usr/bin/env python3
"""
Unit tests for Selenium MCP Server

This module contains comprehensive unit tests for the core server functionality,
configuration management, and tool implementations.
"""

import asyncio
import json
import os
import tempfile
import unittest
from unittest.mock import Mock, patch, MagicMock
from typing import Dict, Any

import pytest

# Import server components
from config.server_config import ServerConfig, BrowserConfig, SecurityConfig
from selenium_mcp_server import SeleniumMCPServer


class TestServerConfig(unittest.TestCase):
    """Test cases for server configuration."""

    def setUp(self):
        """Set up test fixtures."""
        self.config = ServerConfig()

    def test_default_configuration(self):
        """Test default configuration values."""
        self.assertEqual(self.config.server_name, "selenium-mcp-server")
        self.assertEqual(self.config.server_version, "1.0.0")
        self.assertEqual(self.config.performance.default_timeout_ms, 10000)
        self.assertEqual(self.config.performance.max_sessions, 5)
        self.assertTrue(self.config.security.allow_file_uploads)

    def test_browser_configuration(self):
        """Test browser configuration management."""
        # Test getting browser config
        chrome_config = self.config.get_browser_config("chrome")
        self.assertIsNotNone(chrome_config)
        self.assertEqual(chrome_config.name, "chrome")
        self.assertTrue(chrome_config.enabled)

        # Test invalid browser
        invalid_config = self.config.get_browser_config("invalid")
        self.assertIsNone(invalid_config)

    def test_supported_browsers(self):
        """Test supported browsers list."""
        browsers = self.config.get_supported_browsers()
        self.assertIn("chrome", browsers)
        self.assertIn("firefox", browsers)
        self.assertIn("edge", browsers)

    def test_browser_enable_disable(self):
        """Test enabling/disabling browsers."""
        # Disable Firefox
        self.config.update_browser_config("firefox", enabled=False)
        self.assertFalse(self.config.is_browser_enabled("firefox"))

        # Re-enable Firefox
        self.config.update_browser_config("firefox", enabled=True)
        self.assertTrue(self.config.is_browser_enabled("firefox"))

    def test_environment_overrides(self):
        """Test environment variable overrides."""
        with patch.dict(os.environ, {
            'SELENIUM_DEFAULT_TIMEOUT': '15000',
            'SELENIUM_MAX_SESSIONS': '10',
            'SELENIUM_LOG_LEVEL': 'DEBUG'
        }):
            config = ServerConfig()
            self.assertEqual(config.performance.default_timeout_ms, 15000)
            self.assertEqual(config.performance.max_sessions, 10)
            self.assertEqual(config.logging.level, 'DEBUG')

    def test_configuration_validation(self):
        """Test configuration validation."""
        # Test invalid timeout
        with self.assertRaises(ValueError):
            config = ServerConfig()
            config.performance.default_timeout_ms = 500
            config._validate_configuration()

        # Test invalid max sessions
        with self.assertRaises(ValueError):
            config = ServerConfig()
            config.performance.max_sessions = 0
            config._validate_configuration()

    def test_config_serialization(self):
        """Test configuration serialization to dictionary."""
        config_dict = self.config.to_dict()
        self.assertIn("server_name", config_dict)
        self.assertIn("logging", config_dict)
        self.assertIn("performance", config_dict)
        self.assertIn("browsers", config_dict)

    def test_config_from_dict(self):
        """Test configuration creation from dictionary."""
        config_data = {
            "server_name": "test-server",
            "performance": {"default_timeout_ms": 20000},
            "logging": {"level": "WARNING"}
        }
        config = ServerConfig.from_dict(config_data)
        self.assertEqual(config.server_name, "test-server")
        self.assertEqual(config.performance.default_timeout_ms, 20000)
        self.assertEqual(config.logging.level, "WARNING")

    def test_config_file_operations(self):
        """Test configuration file save/load operations."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            config_file = f.name

        try:
            # Save configuration
            self.config.save_to_file(config_file)
            self.assertTrue(os.path.exists(config_file))

            # Load configuration
            loaded_config = ServerConfig.from_file(config_file)
            self.assertEqual(loaded_config.server_name, self.config.server_name)
            self.assertEqual(loaded_config.performance.default_timeout_ms, 
                           self.config.performance.default_timeout_ms)

        finally:
            if os.path.exists(config_file):
                os.unlink(config_file)


class TestSeleniumMCPServer(unittest.TestCase):
    """Test cases for Selenium MCP Server."""

    def setUp(self):
        """Set up test fixtures."""
        self.server = SeleniumMCPServer()

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_server_initialization(self):
        """Test server initialization."""
        self.assertIsNotNone(self.server.logger)
        self.assertEqual(len(self.server.sessions), 0)
        self.assertIsNone(self.server.active_session)
        self.assertIsNotNone(self.server.locator_strategies)

    def test_locator_validation(self):
        """Test locator strategy validation."""
        # Test valid locator
        by, value = self.server._validate_locator("id", "test-id")
        self.assertEqual(value, "test-id")

        # Test invalid locator
        with self.assertRaises(ValueError):
            self.server._validate_locator("invalid", "test")

    def test_browser_options_generation(self):
        """Test browser options generation."""
        # Test Chrome options
        chrome_options = self.server._get_driver_options("chrome", {
            "headless": True,
            "window_size": [1024, 768]
        })
        self.assertIsNotNone(chrome_options)

        # Test Firefox options
        firefox_options = self.server._get_driver_options("firefox", {
            "headless": False
        })
        self.assertIsNotNone(firefox_options)

        # Test unsupported browser
        with self.assertRaises(ValueError):
            self.server._get_driver_options("unsupported", {})

    @patch('selenium_mcp_server.webdriver.Chrome')
    def test_driver_creation_mock(self, mock_chrome):
        """Test WebDriver creation with mocking."""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver

        driver = self.server._create_driver("chrome", {"headless": True})
        self.assertEqual(driver, mock_driver)
        mock_chrome.assert_called_once()

    def test_file_path_sanitization(self):
        """Test file path sanitization for security."""
        # Create a temporary file for testing
        with tempfile.NamedTemporaryFile(delete=False) as f:
            temp_file = f.name

        try:
            # Test valid file path
            sanitized_path = self.server._sanitize_file_path(temp_file)
            self.assertEqual(os.path.abspath(temp_file), sanitized_path)

            # Test non-existent file
            with self.assertRaises(FileNotFoundError):
                self.server._sanitize_file_path("/non/existent/file.txt")

        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)

    def test_session_management(self):
        """Test session management operations."""
        # Test getting driver when no active session
        with self.assertRaises(RuntimeError):
            self.server._get_current_driver()

        # Test activity update with no session
        self.server._update_activity("non-existent")
        # Should not raise an error

    def test_cleanup(self):
        """Test server cleanup functionality."""
        # Mock a session
        mock_driver = Mock()
        session_id = "test-session"
        
        from selenium_mcp_server import BrowserSession
        from datetime import datetime
        
        mock_session = BrowserSession(
            driver=mock_driver,
            browser_type="chrome",
            session_id=session_id,
            options={},
            created_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat()
        )
        
        self.server.sessions[session_id] = mock_session
        self.server.active_session = session_id

        # Test cleanup
        self.server.cleanup()
        mock_driver.quit.assert_called_once()
        self.assertEqual(len(self.server.sessions), 0)
        self.assertIsNone(self.server.active_session)


class TestMCPTools(unittest.TestCase):
    """Test cases for MCP tool functions."""

    def setUp(self):
        """Set up test fixtures."""
        # Reset server instance
        import selenium_mcp_server
        selenium_mcp_server.server_instance = SeleniumMCPServer()

    def tearDown(self):
        """Clean up after tests."""
        import selenium_mcp_server
        selenium_mcp_server.server_instance.cleanup()

    @patch('selenium_mcp_server.server_instance._create_driver')
    def test_start_browser_tool(self, mock_create_driver):
        """Test start_browser MCP tool."""
        from selenium_mcp_server import start_browser
        
        mock_driver = Mock()
        mock_create_driver.return_value = mock_driver

        # Test successful browser start
        result = start_browser("chrome", {"headless": True})
        
        self.assertTrue(result["success"])
        self.assertIn("session_id", result)
        self.assertEqual(result["browser_type"], "chrome")
        mock_create_driver.assert_called_once()

    def test_start_browser_max_sessions(self):
        """Test start_browser with maximum sessions limit."""
        from selenium_mcp_server import start_browser, server_instance
        
        # Mock sessions at maximum
        server_instance.sessions = {f"session_{i}": Mock() for i in range(5)}
        
        result = start_browser("chrome")
        self.assertFalse(result["success"])
        self.assertIn("maximum", result["error"].lower())

    def test_close_session_tool(self):
        """Test close_session MCP tool."""
        from selenium_mcp_server import close_session, server_instance, BrowserSession
        from datetime import datetime
        
        # Create mock session
        mock_driver = Mock()
        session_id = "test-session"
        
        mock_session = BrowserSession(
            driver=mock_driver,
            browser_type="chrome",
            session_id=session_id,
            options={},
            created_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat()
        )
        
        server_instance.sessions[session_id] = mock_session
        server_instance.active_session = session_id

        # Test successful session close
        result = close_session(session_id)
        
        self.assertTrue(result["success"])
        mock_driver.quit.assert_called_once()
        self.assertNotIn(session_id, server_instance.sessions)

    def test_close_session_invalid(self):
        """Test close_session with invalid session ID."""
        from selenium_mcp_server import close_session
        
        result = close_session("invalid-session")
        self.assertFalse(result["success"])
        self.assertIn("invalid", result["error"].lower())

    def test_get_session_info_tool(self):
        """Test get_session_info MCP tool."""
        from selenium_mcp_server import get_session_info, server_instance, BrowserSession
        from datetime import datetime
        
        # Create mock session
        mock_driver = Mock()
        mock_driver.current_url = "https://example.com"
        mock_driver.title = "Example Page"
        
        session_id = "test-session"
        mock_session = BrowserSession(
            driver=mock_driver,
            browser_type="chrome",
            session_id=session_id,
            options={},
            created_at=datetime.now().isoformat(),
            last_activity=datetime.now().isoformat()
        )
        
        server_instance.sessions[session_id] = mock_session
        server_instance.active_session = session_id

        result = get_session_info()
        
        self.assertTrue(result["success"])
        self.assertEqual(result["active_session"], session_id)
        self.assertEqual(result["total_sessions"], 1)
        self.assertIn(session_id, result["sessions"])

    @patch('selenium_mcp_server.server_instance._get_current_driver')
    def test_navigate_tool(self, mock_get_driver):
        """Test navigate MCP tool."""
        from selenium_mcp_server import navigate
        
        mock_driver = Mock()
        mock_driver.current_url = "https://example.com"
        mock_driver.title = "Example Page"
        mock_get_driver.return_value = mock_driver

        result = navigate("https://example.com")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["url"], "https://example.com")
        mock_driver.get.assert_called_once_with("https://example.com")

    def test_navigate_no_session(self):
        """Test navigate tool with no active session."""
        from selenium_mcp_server import navigate
        
        result = navigate("https://example.com")
        self.assertFalse(result["success"])
        self.assertIn("no active", result["error"].lower())

    @patch('selenium_mcp_server.server_instance._find_element_with_timeout')
    def test_find_element_tool(self, mock_find_element):
        """Test find_element MCP tool."""
        from selenium_mcp_server import find_element
        
        mock_element = Mock()
        mock_element.tag_name = "div"
        mock_element.text = "Test text"
        mock_element.location = {"x": 100, "y": 200}
        mock_element.size = {"width": 300, "height": 50}
        mock_element.is_displayed.return_value = True
        mock_element.is_enabled.return_value = True
        mock_find_element.return_value = mock_element

        result = find_element("id", "test-id")
        
        self.assertTrue(result["success"])
        self.assertTrue(result["element_found"])
        self.assertEqual(result["tag_name"], "div")
        mock_find_element.assert_called_once_with("id", "test-id", 10000)

    @patch('selenium_mcp_server.server_instance._find_element_with_timeout')
    def test_click_element_tool(self, mock_find_element):
        """Test click_element MCP tool."""
        from selenium_mcp_server import click_element, server_instance
        
        mock_element = Mock()
        mock_element.tag_name = "button"
        mock_find_element.return_value = mock_element
        
        # Mock the driver for execute_script call
        mock_driver = Mock()
        with patch.object(server_instance, '_get_current_driver', return_value=mock_driver):
            with patch('selenium_mcp_server.WebDriverWait') as mock_wait:
                mock_wait_instance = Mock()
                mock_wait.return_value = mock_wait_instance
                mock_wait_instance.until.return_value = mock_element
                
                result = click_element("id", "test-button")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["element_tag"], "button")
        mock_element.click.assert_called_once()

    @patch('selenium_mcp_server.server_instance._find_element_with_timeout')
    def test_send_keys_tool(self, mock_find_element):
        """Test send_keys MCP tool."""
        from selenium_mcp_server import send_keys
        
        mock_element = Mock()
        mock_find_element.return_value = mock_element

        result = send_keys("id", "test-input", "Hello World", clear_first=True)
        
        self.assertTrue(result["success"])
        mock_element.clear.assert_called_once()
        mock_element.send_keys.assert_called_once_with("Hello World")

    @patch('selenium_mcp_server.server_instance._get_current_driver')
    def test_execute_script_tool(self, mock_get_driver):
        """Test execute_script MCP tool."""
        from selenium_mcp_server import execute_script
        
        mock_driver = Mock()
        mock_driver.execute_script.return_value = "script result"
        mock_get_driver.return_value = mock_driver

        result = execute_script("return document.title;")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["result"], "script result")
        mock_driver.execute_script.assert_called_once_with("return document.title;")

    @patch('selenium_mcp_server.server_instance._get_current_driver')
    @patch('selenium_mcp_server.datetime')
    @patch('selenium_mcp_server.base64')
    @patch('selenium_mcp_server.os.path.getsize')
    @patch('builtins.open', create=True)
    def test_take_screenshot_tool(self, mock_open, mock_getsize, mock_base64, 
                                 mock_datetime, mock_get_driver):
        """Test take_screenshot MCP tool."""
        from selenium_mcp_server import take_screenshot
        
        # Setup mocks
        mock_driver = Mock()
        mock_driver.save_screenshot.return_value = True
        mock_get_driver.return_value = mock_driver
        
        mock_datetime.now.return_value.strftime.return_value = "20240101_120000"
        mock_getsize.return_value = 1024
        mock_base64.b64encode.return_value.decode.return_value = "encoded_image_data"
        
        # Mock file operations
        mock_file = Mock()
        mock_file.read.return_value = b"image_data"
        mock_open.return_value.__enter__ = Mock(return_value=mock_file)

        result = take_screenshot()
        
        self.assertTrue(result["success"])
        self.assertIn("screenshot_path", result)
        self.assertEqual(result["file_size"], 1024)
        self.assertEqual(result["base64_data"], "encoded_image_data")

    def test_health_check_tool(self):
        """Test health_check MCP tool."""
        from selenium_mcp_server import health_check
        
        result = health_check()
        
        self.assertEqual(result["status"], "healthy")
        self.assertIn("active_sessions", result)
        self.assertIn("version", result)
        self.assertIn("supported_browsers", result)


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling and edge cases."""

    def setUp(self):
        """Set up test fixtures."""
        import selenium_mcp_server
        selenium_mcp_server.server_instance = SeleniumMCPServer()

    def test_timeout_exception_handling(self):
        """Test TimeoutException handling in find operations."""
        from selenium_mcp_server import find_element, server_instance
        from selenium.common.exceptions import TimeoutException
        
        with patch.object(server_instance, '_find_element_with_timeout', 
                         side_effect=TimeoutException("Element not found")):
            result = find_element("id", "non-existent")
            
            self.assertFalse(result["success"])
            self.assertFalse(result["element_found"])
            self.assertEqual(result["error_type"], "TimeoutException")

    def test_webdriver_exception_handling(self):
        """Test WebDriverException handling."""
        from selenium_mcp_server import start_browser, server_instance
        from selenium.common.exceptions import WebDriverException
        
        with patch.object(server_instance, '_create_driver', 
                         side_effect=WebDriverException("Driver failed")):
            result = start_browser("chrome")
            
            self.assertFalse(result["success"])
            self.assertIn("webdriverexception", result["error_type"].lower())

    def test_element_not_interactable_exception(self):
        """Test ElementNotInteractableException handling."""
        from selenium_mcp_server import click_element, server_instance
        from selenium.common.exceptions import ElementNotInteractableException
        
        mock_element = Mock()
        mock_element.click.side_effect = ElementNotInteractableException("Not interactable")
        
        with patch.object(server_instance, '_find_element_with_timeout', return_value=mock_element):
            with patch.object(server_instance, '_get_current_driver', return_value=Mock()):
                with patch('selenium_mcp_server.WebDriverWait') as mock_wait:
                    mock_wait_instance = Mock()
                    mock_wait.return_value = mock_wait_instance
                    mock_wait_instance.until.side_effect = ElementNotInteractableException("Not interactable")
                    
                    result = click_element("id", "disabled-button")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "ElementNotInteractableException")

    def test_file_not_found_exception(self):
        """Test FileNotFoundError handling in file upload."""
        from selenium_mcp_server import upload_file
        
        result = upload_file("id", "file-input", "/non/existent/file.txt")
        
        self.assertFalse(result["success"])
        self.assertEqual(result["error_type"], "FileNotFoundError")

    def test_invalid_locator_strategy(self):
        """Test invalid locator strategy handling."""
        from selenium_mcp_server import find_element
        
        # This should be handled by the _validate_locator method
        with patch('selenium_mcp_server.server_instance._validate_locator', 
                  side_effect=ValueError("Invalid locator")):
            result = find_element("invalid", "test")
            
            self.assertFalse(result["success"])
            self.assertIn("invalid", result["error"].lower())


if __name__ == '__main__':
    # Run tests with detailed output
    unittest.main(verbosity=2)
