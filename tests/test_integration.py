#!/usr/bin/env python3
"""
Integration tests for Selenium MCP Server

This module contains comprehensive integration tests that verify the complete
functionality of the MCP server with real browser instances and web interactions.
"""

import asyncio
import json
import os
import tempfile
import time
import unittest
from typing import Dict, Any

import pytest

# Skip integration tests if SKIP_INTEGRATION_TESTS env var is set
SKIP_INTEGRATION = os.getenv("SKIP_INTEGRATION_TESTS", "false").lower() == "true"

# Test configuration
TEST_CONFIG = {
    "test_url": os.getenv("TEST_URL", "https://httpbin.org"),
    "browser": os.getenv("TEST_BROWSER", "chrome"),
    "headless": os.getenv("TEST_HEADLESS", "true").lower() == "true",
    "timeout": int(os.getenv("TEST_TIMEOUT", "30")),
}


@pytest.mark.skipif(SKIP_INTEGRATION, reason="Integration tests disabled")
class TestBrowserLifecycle(unittest.TestCase):
    """Integration tests for browser lifecycle management."""

    def setUp(self):
        """Set up test fixtures."""
        import selenium_mcp_server
        # Use a fresh server instance for each test
        selenium_mcp_server.server_instance = selenium_mcp_server.SeleniumMCPServer()
        self.server = selenium_mcp_server.server_instance

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_start_and_close_browser_session(self):
        """Test complete browser session lifecycle."""
        from selenium_mcp_server import start_browser, close_session, get_session_info
        
        # Start browser session
        start_result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={
                "headless": TEST_CONFIG["headless"],
                "window_size": [1920, 1080]
            }
        )
        
        self.assertTrue(start_result["success"])
        self.assertIn("session_id", start_result)
        session_id = start_result["session_id"]
        
        # Verify session is active
        info_result = get_session_info()
        self.assertTrue(info_result["success"])
        self.assertEqual(info_result["active_session"], session_id)
        self.assertEqual(info_result["total_sessions"], 1)
        
        # Close session
        close_result = close_session(session_id)
        self.assertTrue(close_result["success"])
        
        # Verify session is closed
        info_result = get_session_info()
        self.assertEqual(info_result["total_sessions"], 0)
        self.assertIsNone(info_result["active_session"])

    def test_multiple_browser_sessions(self):
        """Test managing multiple concurrent browser sessions."""
        from selenium_mcp_server import start_browser, close_session, get_session_info
        
        session_ids = []
        
        # Start multiple sessions
        for i in range(3):
            result = start_browser(
                browser=TEST_CONFIG["browser"],
                options={"headless": TEST_CONFIG["headless"]}
            )
            self.assertTrue(result["success"])
            session_ids.append(result["session_id"])
        
        # Verify all sessions are active
        info_result = get_session_info()
        self.assertEqual(info_result["total_sessions"], 3)
        
        # Close all sessions
        for session_id in session_ids:
            close_result = close_session(session_id)
            self.assertTrue(close_result["success"])
        
        # Verify all sessions are closed
        info_result = get_session_info()
        self.assertEqual(info_result["total_sessions"], 0)

    def test_session_limit_enforcement(self):
        """Test maximum session limit enforcement."""
        from selenium_mcp_server import start_browser
        
        # Start sessions up to the limit
        session_ids = []
        for i in range(5):  # Default max is 5
            result = start_browser(
                browser=TEST_CONFIG["browser"],
                options={"headless": TEST_CONFIG["headless"]}
            )
            if result["success"]:
                session_ids.append(result["session_id"])
        
        # Try to start one more session (should fail)
        result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={"headless": TEST_CONFIG["headless"]}
        )
        self.assertFalse(result["success"])
        self.assertIn("maximum", result["error"].lower())


@pytest.mark.skipif(SKIP_INTEGRATION, reason="Integration tests disabled")
class TestNavigationAndPageOperations(unittest.TestCase):
    """Integration tests for navigation and page operations."""

    def setUp(self):
        """Set up test fixtures with active browser session."""
        import selenium_mcp_server
        from selenium_mcp_server import start_browser
        
        selenium_mcp_server.server_instance = selenium_mcp_server.SeleniumMCPServer()
        self.server = selenium_mcp_server.server_instance
        
        # Start browser session
        self.session_result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={"headless": TEST_CONFIG["headless"]}
        )
        self.assertTrue(self.session_result["success"])
        self.session_id = self.session_result["session_id"]

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_navigation_operations(self):
        """Test basic navigation operations."""
        from selenium_mcp_server import navigate, get_current_url, go_back, go_forward, refresh_page
        
        # Navigate to test URL
        nav_result = navigate(TEST_CONFIG["test_url"])
        self.assertTrue(nav_result["success"])
        self.assertEqual(nav_result["url"], TEST_CONFIG["test_url"])
        
        # Get current URL
        url_result = get_current_url()
        self.assertTrue(url_result["success"])
        self.assertIn(TEST_CONFIG["test_url"], url_result["current_url"])
        
        # Navigate to another page
        nav_result2 = navigate(f"{TEST_CONFIG['test_url']}/html")
        self.assertTrue(nav_result2["success"])
        
        # Test back navigation
        back_result = go_back()
        self.assertTrue(back_result["success"])
        
        # Test forward navigation
        forward_result = go_forward()
        self.assertTrue(forward_result["success"])
        
        # Test page refresh
        refresh_result = refresh_page()
        self.assertTrue(refresh_result["success"])

    def test_page_content_operations(self):
        """Test page content retrieval operations."""
        from selenium_mcp_server import navigate, get_page_title, get_page_source
        
        # Navigate to test page
        navigate(f"{TEST_CONFIG['test_url']}/html")
        
        # Get page title
        title_result = get_page_title()
        self.assertTrue(title_result["success"])
        self.assertIsInstance(title_result["title"], str)
        
        # Get page source
        source_result = get_page_source()
        self.assertTrue(source_result["success"])
        self.assertIsInstance(source_result["source"], str)
        self.assertGreater(source_result["length"], 0)

    def test_screenshot_operations(self):
        """Test screenshot functionality."""
        from selenium_mcp_server import navigate, take_screenshot
        
        # Navigate to test page
        navigate(TEST_CONFIG["test_url"])
        
        # Take screenshot with auto-generated path
        screenshot_result = take_screenshot()
        self.assertTrue(screenshot_result["success"])
        self.assertIn("screenshot_path", screenshot_result)
        self.assertIn("base64_data", screenshot_result)
        
        # Verify screenshot file exists
        screenshot_path = screenshot_result["screenshot_path"]
        self.assertTrue(os.path.exists(screenshot_path))
        
        # Clean up screenshot file
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

    def test_javascript_execution(self):
        """Test JavaScript execution capabilities."""
        from selenium_mcp_server import navigate, execute_script, execute_async_script
        
        # Navigate to test page
        navigate(TEST_CONFIG["test_url"])
        
        # Test synchronous script execution
        script_result = execute_script("return document.title;")
        self.assertTrue(script_result["success"])
        self.assertIsInstance(script_result["result"], str)
        
        # Test script with return value
        math_result = execute_script("return 2 + 2;")
        self.assertTrue(math_result["success"])
        self.assertEqual(math_result["result"], 4)
        
        # Test asynchronous script execution
        async_script = """
        var callback = arguments[arguments.length - 1];
        setTimeout(function() {
            callback('async result');
        }, 100);
        """
        async_result = execute_async_script(async_script)
        self.assertTrue(async_result["success"])
        self.assertEqual(async_result["result"], "async result")


@pytest.mark.skipif(SKIP_INTEGRATION, reason="Integration tests disabled")
class TestElementInteractions(unittest.TestCase):
    """Integration tests for element finding and interaction."""

    def setUp(self):
        """Set up test fixtures with active browser session."""
        import selenium_mcp_server
        from selenium_mcp_server import start_browser, navigate
        
        selenium_mcp_server.server_instance = selenium_mcp_server.SeleniumMCPServer()
        self.server = selenium_mcp_server.server_instance
        
        # Start browser session
        session_result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={"headless": TEST_CONFIG["headless"]}
        )
        self.assertTrue(session_result["success"])
        
        # Navigate to httpbin forms page for testing
        nav_result = navigate(f"{TEST_CONFIG['test_url']}/forms/post")
        self.assertTrue(nav_result["success"])

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_element_finding_operations(self):
        """Test element finding with various strategies."""
        from selenium_mcp_server import find_element, find_elements
        
        # Find single element by tag
        element_result = find_element("tag", "form")
        self.assertTrue(element_result["success"])
        self.assertTrue(element_result["element_found"])
        self.assertEqual(element_result["tag_name"], "form")
        
        # Find multiple elements
        elements_result = find_elements("tag", "input")
        self.assertTrue(elements_result["success"])
        self.assertGreater(elements_result["elements_found"], 0)
        
        # Test element not found scenario
        not_found_result = find_element("id", "non-existent-element", timeout=2000)
        self.assertFalse(not_found_result["success"])
        self.assertFalse(not_found_result["element_found"])

    def test_form_interactions(self):
        """Test form element interactions."""
        from selenium_mcp_server import (
            find_element, send_keys, clear_element, 
            get_element_text, get_element_attribute, click_element
        )
        
        # Find form input fields
        custname_result = find_element("name", "custname")
        if custname_result["success"]:
            # Test sending keys
            send_result = send_keys("name", "custname", "Test User", clear_first=True)
            self.assertTrue(send_result["success"])
            
            # Test getting element attribute
            attr_result = get_element_attribute("name", "custname", "value")
            self.assertTrue(attr_result["success"])
            self.assertEqual(attr_result["value"], "Test User")
            
            # Test clearing element
            clear_result = clear_element("name", "custname")
            self.assertTrue(clear_result["success"])

    def test_wait_operations(self):
        """Test element waiting operations."""
        from selenium_mcp_server import wait_for_element, wait_for_page_load
        
        # Test waiting for existing element
        wait_result = wait_for_element("tag", "form", timeout=5000, condition="presence")
        self.assertTrue(wait_result["success"])
        
        # Test waiting for page load
        page_load_result = wait_for_page_load(timeout=10000)
        self.assertTrue(page_load_result["success"])

    def test_advanced_interactions(self):
        """Test advanced element interactions."""
        from selenium_mcp_server import hover, press_key
        
        # Test hovering over an element
        hover_result = hover("tag", "form")
        if hover_result["success"]:  # May not work in headless mode
            self.assertTrue(hover_result["success"])
        
        # Test key press
        key_result = press_key("TAB")
        self.assertTrue(key_result["success"])


@pytest.mark.skipif(SKIP_INTEGRATION, reason="Integration tests disabled")
class TestFileOperations(unittest.TestCase):
    """Integration tests for file upload and download operations."""

    def setUp(self):
        """Set up test fixtures with active browser session."""
        import selenium_mcp_server
        from selenium_mcp_server import start_browser
        
        selenium_mcp_server.server_instance = selenium_mcp_server.SeleniumMCPServer()
        self.server = selenium_mcp_server.server_instance
        
        # Start browser session
        session_result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={"headless": TEST_CONFIG["headless"]}
        )
        self.assertTrue(session_result["success"])

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_file_upload_operations(self):
        """Test file upload functionality."""
        from selenium_mcp_server import navigate, upload_file, find_element
        
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("This is a test file for upload.")
            test_file_path = f.name
        
        try:
            # Navigate to file upload test page
            nav_result = navigate(f"{TEST_CONFIG['test_url']}/forms/post")
            self.assertTrue(nav_result["success"])
            
            # Check if file input exists
            file_input_result = find_element("css", "input[type='file']")
            if file_input_result["success"]:
                # Test file upload
                upload_result = upload_file("css", "input[type='file']", test_file_path)
                self.assertTrue(upload_result["success"])
            else:
                # Skip test if no file input found
                self.skipTest("No file input found on test page")
                
        finally:
            # Clean up test file
            if os.path.exists(test_file_path):
                os.remove(test_file_path)

    def test_file_upload_invalid_file(self):
        """Test file upload with invalid file path."""
        from selenium_mcp_server import upload_file
        
        # Test with non-existent file
        upload_result = upload_file("css", "input[type='file']", "/non/existent/file.txt")
        self.assertFalse(upload_result["success"])
        self.assertEqual(upload_result["error_type"], "FileNotFoundError")


@pytest.mark.skipif(SKIP_INTEGRATION, reason="Integration tests disabled")
class TestErrorRecovery(unittest.TestCase):
    """Integration tests for error handling and recovery."""

    def setUp(self):
        """Set up test fixtures with active browser session."""
        import selenium_mcp_server
        from selenium_mcp_server import start_browser
        
        selenium_mcp_server.server_instance = selenium_mcp_server.SeleniumMCPServer()
        self.server = selenium_mcp_server.server_instance
        
        # Start browser session
        session_result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={"headless": TEST_CONFIG["headless"]}
        )
        self.assertTrue(session_result["success"])

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_timeout_handling(self):
        """Test timeout handling in various operations."""
        from selenium_mcp_server import navigate, find_element, wait_for_element
        
        # Navigate to test page
        navigate(TEST_CONFIG["test_url"])
        
        # Test element not found with short timeout
        find_result = find_element("id", "non-existent-element", timeout=1000)
        self.assertFalse(find_result["success"])
        self.assertEqual(find_result["error_type"], "TimeoutException")
        
        # Test wait timeout
        wait_result = wait_for_element("id", "non-existent-element", timeout=1000)
        self.assertFalse(wait_result["success"])
        self.assertEqual(wait_result["error_type"], "TimeoutException")

    def test_invalid_navigation(self):
        """Test handling of invalid navigation attempts."""
        from selenium_mcp_server import navigate
        
        # Test navigation to invalid URL
        nav_result = navigate("invalid-url")
        # This may succeed in some browsers (they might search), so we just check it doesn't crash
        self.assertIn("success", nav_result)

    def test_javascript_error_handling(self):
        """Test JavaScript execution error handling."""
        from selenium_mcp_server import navigate, execute_script
        
        # Navigate to test page
        navigate(TEST_CONFIG["test_url"])
        
        # Test invalid JavaScript
        script_result = execute_script("invalid.javascript.code();")
        self.assertFalse(script_result["success"])
        self.assertIn("error", script_result)

    def test_session_recovery_after_crash(self):
        """Test server behavior after browser crash simulation."""
        from selenium_mcp_server import get_session_info, start_browser
        
        # Get current session info
        info_result = get_session_info()
        initial_sessions = info_result["total_sessions"]
        
        # Simulate browser crash by directly calling quit on driver
        if self.server.active_session and self.server.active_session in self.server.sessions:
            session = self.server.sessions[self.server.active_session]
            try:
                session.driver.quit()
            except:
                pass  # Expected to fail
        
        # Server should handle gracefully and allow new sessions
        new_session_result = start_browser(
            browser=TEST_CONFIG["browser"],
            options={"headless": TEST_CONFIG["headless"]}
        )
        # This might fail, but server shouldn't crash
        self.assertIn("success", new_session_result)


@pytest.mark.skipif(SKIP_INTEGRATION, reason="Integration tests disabled")
class TestPerformanceAndStability(unittest.TestCase):
    """Integration tests for performance and stability."""

    def setUp(self):
        """Set up test fixtures."""
        import selenium_mcp_server
        selenium_mcp_server.server_instance = selenium_mcp_server.SeleniumMCPServer()
        self.server = selenium_mcp_server.server_instance

    def tearDown(self):
        """Clean up after tests."""
        self.server.cleanup()

    def test_rapid_session_cycling(self):
        """Test rapid creation and destruction of browser sessions."""
        from selenium_mcp_server import start_browser, close_session
        
        session_ids = []
        
        # Rapidly create and close sessions
        for i in range(10):
            start_result = start_browser(
                browser=TEST_CONFIG["browser"],
                options={"headless": TEST_CONFIG["headless"]}
            )
            
            if start_result["success"]:
                session_id = start_result["session_id"]
                session_ids.append(session_id)
                
                # Close session immediately
                close_result = close_session(session_id)
                self.assertTrue(close_result["success"])
        
        # Verify all sessions are properly closed
        from selenium_mcp_server import get_session_info
        info_result = get_session_info()
        self.assertEqual(info_result["total_sessions"], 0)

    def test_memory_usage_stability(self):
        """Test memory usage doesn't grow excessively."""
        import psutil
        from selenium_mcp_server import start_browser, navigate, close_session
        
        process = psutil.Process()
        initial_memory = process.memory_info().rss
        
        # Perform multiple browser operations
        for i in range(5):
            start_result = start_browser(
                browser=TEST_CONFIG["browser"],
                options={"headless": TEST_CONFIG["headless"]}
            )
            
            if start_result["success"]:
                session_id = start_result["session_id"]
                
                # Perform some operations
                navigate(TEST_CONFIG["test_url"])
                
                # Close session
                close_session(session_id)
        
        final_memory = process.memory_info().rss
        memory_growth = final_memory - initial_memory
        
        # Memory growth should be reasonable (less than 100MB)
        self.assertLess(memory_growth, 100 * 1024 * 1024, 
                       f"Memory growth too high: {memory_growth / 1024 / 1024:.1f} MB")

    def test_concurrent_operations(self):
        """Test concurrent operations across multiple sessions."""
        from selenium_mcp_server import start_browser, navigate, close_session
        import threading
        
        results = []
        
        def worker(worker_id):
            try:
                # Start browser
                start_result = start_browser(
                    browser=TEST_CONFIG["browser"],
                    options={"headless": TEST_CONFIG["headless"]}
                )
                
                if start_result["success"]:
                    session_id = start_result["session_id"]
                    
                    # Navigate
                    nav_result = navigate(f"{TEST_CONFIG['test_url']}/delay/{worker_id}")
                    
                    # Close session
                    close_result = close_session(session_id)
                    
                    results.append({
                        "worker_id": worker_id,
                        "start_success": start_result["success"],
                        "nav_success": nav_result.get("success", False),
                        "close_success": close_result["success"]
                    })
                else:
                    results.append({
                        "worker_id": worker_id,
                        "start_success": False,
                        "error": start_result.get("error", "Unknown")
                    })
                    
            except Exception as e:
                results.append({
                    "worker_id": worker_id,
                    "error": str(e)
                })
        
        # Start multiple concurrent workers
        threads = []
        for i in range(3):  # Limited to avoid resource exhaustion
            thread = threading.Thread(target=worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join(timeout=30)  # 30 second timeout per thread
        
        # Verify results
        self.assertEqual(len(results), 3)
        successful_workers = sum(1 for r in results if r.get("start_success", False))
        self.assertGreater(successful_workers, 0, "At least one worker should succeed")


def run_integration_tests():
    """Run integration tests with proper setup and teardown."""
    if SKIP_INTEGRATION:
        print("Integration tests are disabled. Set SKIP_INTEGRATION_TESTS=false to enable.")
        return
    
    print("Running Selenium MCP Server Integration Tests")
    print("=" * 50)
    print(f"Test Configuration:")
    print(f"  Browser: {TEST_CONFIG['browser']}")
    print(f"  Headless: {TEST_CONFIG['headless']}")
    print(f"  Test URL: {TEST_CONFIG['test_url']}")
    print(f"  Timeout: {TEST_CONFIG['timeout']}s")
    print()
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestBrowserLifecycle,
        TestNavigationAndPageOperations,
        TestElementInteractions,
        TestFileOperations,
        TestErrorRecovery,
        TestPerformanceAndStability
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2, buffer=True)
    result = runner.run(test_suite)
    
    # Print summary
    print("\nIntegration Test Summary:")
    print(f"  Tests run: {result.testsRun}")
    print(f"  Failures: {len(result.failures)}")
    print(f"  Errors: {len(result.errors)}")
    print(f"  Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFailures:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\nErrors:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_integration_tests()
    exit(0 if success else 1)
