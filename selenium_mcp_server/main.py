"""
Main MCP server for Selenium automation using FastMCP.
"""

import asyncio
import logging
from typing import Any, Dict, List, Optional
from fastmcp import FastMCP

from .browser_manager import BrowserManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global browser manager instance
browser_manager = BrowserManager()

# Create FastMCP app
mcp = FastMCP("selenium-mcp-server")


# Browser Management Tools
@mcp.tool()
def selenium_start_browser(
    browser_type: str = "chrome", 
    headless: bool = False, 
    window_size: List[int] = [1920, 1080]
) -> Dict[str, Any]:
    """
    Start a new browser session.
    
    Args:
        browser_type: Type of browser to start (chrome, firefox, edge, safari)
        headless: Run browser in headless mode
        window_size: Window size as [width, height]
    
    Returns:
        Browser session information
    """
    try:
        browser_id = browser_manager.start_browser(
            browser_type=browser_type,
            headless=headless,
            window_size=tuple(window_size)
        )
        
        return {
            "success": True,
            "browser_id": browser_id,
            "message": f"Started {browser_type} browser with ID: {browser_id}"
        }
    except Exception as e:
        logger.error(f"Failed to start browser: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to start {browser_type} browser"
        }


@mcp.tool()
def selenium_stop_browser(browser_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Stop a browser session.
    
    Args:
        browser_id: Browser ID to stop (current session if not provided)
    
    Returns:
        Operation result
    """
    try:
        success = browser_manager.stop_browser(browser_id)
        
        if success:
            return {
                "success": True,
                "message": "Browser stopped successfully"
            }
        else:
            return {
                "success": False,
                "error": "Failed to stop browser",
                "message": "Browser not found or could not be stopped"
            }
    except Exception as e:
        logger.error(f"Error stopping browser: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Error stopping browser"
        }


@mcp.tool()
def selenium_list_browsers() -> Dict[str, Any]:
    """
    List all active browser sessions.
    
    Returns:
        Active browser sessions information
    """
    try:
        browsers = browser_manager.list_browsers()
        return {
            "success": True,
            "browsers": browsers,
            "count": len(browsers)
        }
    except Exception as e:
        logger.error(f"Failed to list browsers: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to list browsers"
        }


@mcp.tool()
def selenium_switch_browser(browser_id: str) -> Dict[str, Any]:
    """
    Switch to a different browser session.
    
    Args:
        browser_id: Browser ID to switch to
    
    Returns:
        Switch operation result
    """
    try:
        success = browser_manager.switch_browser(browser_id)
        
        if success:
            return {
                "success": True,
                "message": f"Switched to browser: {browser_id}"
            }
        else:
            return {
                "success": False,
                "error": f"Browser not found: {browser_id}",
                "message": "Could not switch to specified browser"
            }
    except Exception as e:
        logger.error(f"Error switching browser: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Error switching browser"
        }


# Navigation Tools
@mcp.tool()
def selenium_navigate(url: str) -> Dict[str, Any]:
    """
    Navigate to a URL.
    
    Args:
        url: URL to navigate to
    
    Returns:
        Navigation result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        browser.get(url)
        return {
            "success": True,
            "url": url,
            "current_url": browser.current_url,
            "title": browser.title,
            "message": f"Navigated to: {url}"
        }
    except Exception as e:
        logger.error(f"Failed to navigate to {url}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to navigate to {url}"
        }


@mcp.tool()
def selenium_go_back() -> Dict[str, Any]:
    """
    Go back in browser history.
    
    Returns:
        Navigation result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        browser.back()
        return {
            "success": True,
            "current_url": browser.current_url,
            "message": "Went back in browser history"
        }
    except Exception as e:
        logger.error(f"Failed to go back: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to go back"
        }


@mcp.tool()
def selenium_go_forward() -> Dict[str, Any]:
    """
    Go forward in browser history.
    
    Returns:
        Navigation result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        browser.forward()
        return {
            "success": True,
            "current_url": browser.current_url,
            "message": "Went forward in browser history"
        }
    except Exception as e:
        logger.error(f"Failed to go forward: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to go forward"
        }


@mcp.tool()
def selenium_refresh() -> Dict[str, Any]:
    """
    Refresh the current page.
    
    Returns:
        Refresh result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        browser.refresh()
        return {
            "success": True,
            "message": "Page refreshed"
        }
    except Exception as e:
        logger.error(f"Failed to refresh page: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to refresh page"
        }


@mcp.tool()
def selenium_get_current_url() -> Dict[str, Any]:
    """
    Get the current URL.
    
    Returns:
        Current URL information
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        url = browser.current_url
        title = browser.title
        return {
            "success": True,
            "current_url": url,
            "title": title,
            "message": f"Current URL: {url}"
        }
    except Exception as e:
        logger.error(f"Failed to get current URL: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to get current URL"
        }


# Element Interaction Tools
@mcp.tool()
def selenium_find_element(strategy: str, value: str) -> Dict[str, Any]:
    """
    Find an element using various locator strategies.
    
    Args:
        strategy: Locator strategy (id, name, class_name, tag_name, css_selector, xpath, link_text, partial_link_text)
        value: Value to search for
    
    Returns:
        Element information
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names to selenium format
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        return {
            "success": True,
            "element_found": True,
            "tag_name": element.tag_name,
            "text": element.text[:100] if element.text else "",
            "is_displayed": element.is_displayed(),
            "is_enabled": element.is_enabled(),
            "message": f"Element found: {element.tag_name}"
        }
    except Exception as e:
        logger.error(f"Failed to find element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "element_found": False,
            "error": str(e),
            "message": f"Element not found: {strategy}='{value}'"
        }


@mcp.tool()
def selenium_click(strategy: str, value: str) -> Dict[str, Any]:
    """
    Click an element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
    
    Returns:
        Click result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        element.click()
        return {
            "success": True,
            "message": "Element clicked successfully"
        }
    except Exception as e:
        logger.error(f"Failed to click element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to click element: {strategy}='{value}'"
        }


@mcp.tool()
def selenium_type(strategy: str, value: str, text: str) -> Dict[str, Any]:
    """
    Type text into an element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
        text: Text to type
    
    Returns:
        Type result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        element.clear()
        element.send_keys(text)
        return {
            "success": True,
            "message": f"Typed '{text}' into element"
        }
    except Exception as e:
        logger.error(f"Failed to type into element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to type into element: {strategy}='{value}'"
        }


@mcp.tool()
def selenium_get_text(strategy: str, value: str) -> Dict[str, Any]:
    """
    Get text content from an element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
    
    Returns:
        Element text
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        text = element.text
        return {
            "success": True,
            "text": text,
            "length": len(text),
            "message": f"Element text: {text[:50]}{'...' if len(text) > 50 else ''}"
        }
    except Exception as e:
        logger.error(f"Failed to get text from element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to get text from element: {strategy}='{value}'"
        }


@mcp.tool()
def selenium_get_attribute(strategy: str, value: str, attribute: str) -> Dict[str, Any]:
    """
    Get an attribute value from an element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
        attribute: Attribute name to get
    
    Returns:
        Attribute value
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        attr_value = element.get_attribute(attribute)
        return {
            "success": True,
            "attribute": attribute,
            "value": attr_value,
            "message": f"Attribute '{attribute}': {attr_value}"
        }
    except Exception as e:
        logger.error(f"Failed to get attribute from element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to get attribute from element: {strategy}='{value}'"
        }


@mcp.tool()
def selenium_hover(strategy: str, value: str) -> Dict[str, Any]:
    """
    Hover over an element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
    
    Returns:
        Hover result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(browser).move_to_element(element).perform()
        return {
            "success": True,
            "message": "Hovered over element"
        }
    except Exception as e:
        logger.error(f"Failed to hover over element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to hover over element: {strategy}='{value}'"
        }


# Advanced Actions Tools
@mcp.tool()
def selenium_execute_script(script: str) -> Dict[str, Any]:
    """
    Execute JavaScript code.
    
    Args:
        script: JavaScript code to execute
    
    Returns:
        Script execution result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        result = browser.execute_script(script)
        return {
            "success": True,
            "result": result,
            "script": script[:100] + ("..." if len(script) > 100 else ""),
            "message": f"Script executed. Result: {result}"
        }
    except Exception as e:
        logger.error(f"Failed to execute script: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to execute script"
        }


@mcp.tool()
def selenium_take_screenshot(filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Take a screenshot.
    
    Args:
        filename: Filename to save screenshot (optional)
    
    Returns:
        Screenshot result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        if not filename:
            filename = f"screenshot_{browser_manager.current_browser_id}.png"
        
        success = browser.save_screenshot(filename)
        if success:
            return {
                "success": True,
                "filename": filename,
                "message": f"Screenshot saved to: {filename}"
            }
        else:
            return {
                "success": False,
                "error": "Failed to save screenshot",
                "message": "Screenshot could not be saved"
            }
    except Exception as e:
        logger.error(f"Failed to take screenshot: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": "Failed to take screenshot"
        }


@mcp.tool()
def selenium_wait_for_element(strategy: str, value: str, timeout: int = 10) -> Dict[str, Any]:
    """
    Wait for an element to appear.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
        timeout: Timeout in seconds
    
    Returns:
        Wait result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Convert strategy to By constant
        by_map = {
            "id": By.ID,
            "name": By.NAME,
            "class_name": By.CLASS_NAME,
            "tag_name": By.TAG_NAME,
            "css_selector": By.CSS_SELECTOR,
            "xpath": By.XPATH,
            "link_text": By.LINK_TEXT,
            "partial_link_text": By.PARTIAL_LINK_TEXT
        }
        
        by_locator = by_map.get(strategy)
        if not by_locator:
            return {
                "success": False,
                "error": f"Invalid strategy: {strategy}",
                "message": "Unsupported locator strategy"
            }
        
        wait = WebDriverWait(browser, timeout)
        element = wait.until(EC.presence_of_element_located((by_locator, value)))
        
        return {
            "success": True,
            "element_found": True,
            "tag_name": element.tag_name,
            "text": element.text[:100] if element.text else "",
            "message": f"Element found after waiting: {element.tag_name}"
        }
    except Exception as e:
        logger.error(f"Element not found within timeout {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "element_found": False,
            "error": str(e),
            "message": f"Element not found within {timeout}s: {strategy}='{value}'"
        }


@mcp.tool()
def selenium_scroll_to_element(strategy: str, value: str) -> Dict[str, Any]:
    """
    Scroll to an element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
    
    Returns:
        Scroll result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        return {
            "success": True,
            "message": "Scrolled to element"
        }
    except Exception as e:
        logger.error(f"Failed to scroll to element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to scroll to element: {strategy}='{value}'"
        }


# File Operations Tools
@mcp.tool()
def selenium_upload_file(strategy: str, value: str, file_path: str) -> Dict[str, Any]:
    """
    Upload a file to an input element.
    
    Args:
        strategy: Locator strategy
        value: Value to search for
        file_path: Path to the file to upload
    
    Returns:
        Upload result
    """
    try:
        browser = browser_manager.get_browser()
        if not browser:
            return {
                "success": False,
                "error": "No active browser session",
                "message": "Start a browser session first"
            }
        
        # Convert strategy names
        strategy_map = {
            "class_name": "class name",
            "tag_name": "tag name", 
            "css_selector": "css selector",
            "link_text": "link text",
            "partial_link_text": "partial link text"
        }
        selenium_strategy = strategy_map.get(strategy, strategy)
        
        element = browser.find_element(selenium_strategy, value)
        element.send_keys(file_path)
        return {
            "success": True,
            "file_path": file_path,
            "message": f"File uploaded: {file_path}"
        }
    except Exception as e:
        logger.error(f"Failed to upload file to element {strategy}='{value}': {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to upload file: {file_path}"
        }


@mcp.tool()
def selenium_download_file(url: str, filename: Optional[str] = None) -> Dict[str, Any]:
    """
    Download a file from a URL.
    
    Args:
        url: URL to download from
        filename: Filename to save as (optional)
    
    Returns:
        Download result
    """
    try:
        import requests
        import os
        
        response = requests.get(url)
        response.raise_for_status()
        
        if not filename:
            filename = os.path.basename(url) or "downloaded_file"
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return {
            "success": True,
            "url": url,
            "filename": filename,
            "size": len(response.content),
            "message": f"File downloaded: {filename}"
        }
    except Exception as e:
        logger.error(f"Failed to download file from {url}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to download file from: {url}"
        }


def main():
    """Main entry point."""
    try:
        logger.info("Starting Selenium MCP Server with FastMCP")
        mcp.run()
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
        browser_manager.stop_all_browsers()
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        browser_manager.stop_all_browsers()
        raise


if __name__ == "__main__":
    main()
