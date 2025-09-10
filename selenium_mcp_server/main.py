"""
Main MCP server for Selenium automation.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
    LoggingLevel
)

from .browser_manager import BrowserManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global browser manager instance
browser_manager = BrowserManager()

# MCP Server instance
server = Server("selenium-mcp-server")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """List available tools."""
    tools = [
        # Browser Management
        Tool(
            name="selenium_start_browser",
            description="Start a new browser session",
            inputSchema={
                "type": "object",
                "properties": {
                    "browser_type": {
                        "type": "string",
                        "enum": ["chrome", "firefox", "edge", "safari"],
                        "default": "chrome",
                        "description": "Type of browser to start"
                    },
                    "headless": {
                        "type": "boolean",
                        "default": False,
                        "description": "Run browser in headless mode"
                    },
                    "window_size": {
                        "type": "array",
                        "items": {"type": "integer"},
                        "default": [1920, 1080],
                        "description": "Window size as [width, height]"
                    }
                }
            }
        ),
        Tool(
            name="selenium_stop_browser",
            description="Stop the current browser session",
            inputSchema={
                "type": "object",
                "properties": {
                    "browser_id": {
                        "type": "string",
                        "description": "Browser ID to stop (optional, stops current if not provided)"
                    }
                }
            }
        ),
        Tool(
            name="selenium_list_browsers",
            description="List all active browser sessions",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="selenium_switch_browser",
            description="Switch to a different browser session",
            inputSchema={
                "type": "object",
                "properties": {
                    "browser_id": {
                        "type": "string",
                        "description": "Browser ID to switch to"
                    }
                },
                "required": ["browser_id"]
            }
        ),
        
        # Navigation
        Tool(
            name="selenium_navigate",
            description="Navigate to a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to navigate to"
                    }
                },
                "required": ["url"]
            }
        ),
        Tool(
            name="selenium_go_back",
            description="Go back in browser history",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="selenium_go_forward",
            description="Go forward in browser history",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="selenium_refresh",
            description="Refresh the current page",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        Tool(
            name="selenium_get_current_url",
            description="Get the current URL",
            inputSchema={
                "type": "object",
                "properties": {}
            }
        ),
        
        # Element Interaction
        Tool(
            name="selenium_find_element",
            description="Find an element using various locator strategies",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    }
                },
                "required": ["strategy", "value"]
            }
        ),
        Tool(
            name="selenium_click",
            description="Click an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    }
                },
                "required": ["strategy", "value"]
            }
        ),
        Tool(
            name="selenium_type",
            description="Type text into an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    },
                    "text": {
                        "type": "string",
                        "description": "Text to type"
                    }
                },
                "required": ["strategy", "value", "text"]
            }
        ),
        Tool(
            name="selenium_get_text",
            description="Get text content from an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    }
                },
                "required": ["strategy", "value"]
            }
        ),
        Tool(
            name="selenium_get_attribute",
            description="Get an attribute value from an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    },
                    "attribute": {
                        "type": "string",
                        "description": "Attribute name to get"
                    }
                },
                "required": ["strategy", "value", "attribute"]
            }
        ),
        Tool(
            name="selenium_hover",
            description="Hover over an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    }
                },
                "required": ["strategy", "value"]
            }
        ),
        
        # Advanced Actions
        Tool(
            name="selenium_execute_script",
            description="Execute JavaScript code",
            inputSchema={
                "type": "object",
                "properties": {
                    "script": {
                        "type": "string",
                        "description": "JavaScript code to execute"
                    }
                },
                "required": ["script"]
            }
        ),
        Tool(
            name="selenium_take_screenshot",
            description="Take a screenshot",
            inputSchema={
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "Filename to save screenshot (optional)"
                    }
                }
            }
        ),
        Tool(
            name="selenium_wait_for_element",
            description="Wait for an element to appear",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    },
                    "timeout": {
                        "type": "integer",
                        "default": 10,
                        "description": "Timeout in seconds"
                    }
                },
                "required": ["strategy", "value"]
            }
        ),
        Tool(
            name="selenium_scroll_to_element",
            description="Scroll to an element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    }
                },
                "required": ["strategy", "value"]
            }
        ),
        
        # File Operations
        Tool(
            name="selenium_upload_file",
            description="Upload a file to an input element",
            inputSchema={
                "type": "object",
                "properties": {
                    "strategy": {
                        "type": "string",
                        "enum": ["id", "name", "class_name", "tag_name", "css_selector", "xpath", "link_text", "partial_link_text"],
                        "description": "Locator strategy to use"
                    },
                    "value": {
                        "type": "string",
                        "description": "Value to search for"
                    },
                    "file_path": {
                        "type": "string",
                        "description": "Path to the file to upload"
                    }
                },
                "required": ["strategy", "value", "file_path"]
            }
        ),
        Tool(
            name="selenium_download_file",
            description="Download a file from a URL",
            inputSchema={
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL to download from"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Filename to save as (optional)"
                    }
                },
                "required": ["url"]
            }
        )
    ]
    
    return ListToolsResult(tools=tools)

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle tool calls."""
    try:
        if name == "selenium_start_browser":
            return await handle_start_browser(arguments)
        elif name == "selenium_stop_browser":
            return await handle_stop_browser(arguments)
        elif name == "selenium_list_browsers":
            return await handle_list_browsers(arguments)
        elif name == "selenium_switch_browser":
            return await handle_switch_browser(arguments)
        elif name == "selenium_navigate":
            return await handle_navigate(arguments)
        elif name == "selenium_go_back":
            return await handle_go_back(arguments)
        elif name == "selenium_go_forward":
            return await handle_go_forward(arguments)
        elif name == "selenium_refresh":
            return await handle_refresh(arguments)
        elif name == "selenium_get_current_url":
            return await handle_get_current_url(arguments)
        elif name == "selenium_find_element":
            return await handle_find_element(arguments)
        elif name == "selenium_click":
            return await handle_click(arguments)
        elif name == "selenium_type":
            return await handle_type(arguments)
        elif name == "selenium_get_text":
            return await handle_get_text(arguments)
        elif name == "selenium_get_attribute":
            return await handle_get_attribute(arguments)
        elif name == "selenium_hover":
            return await handle_hover(arguments)
        elif name == "selenium_execute_script":
            return await handle_execute_script(arguments)
        elif name == "selenium_take_screenshot":
            return await handle_take_screenshot(arguments)
        elif name == "selenium_wait_for_element":
            return await handle_wait_for_element(arguments)
        elif name == "selenium_scroll_to_element":
            return await handle_scroll_to_element(arguments)
        elif name == "selenium_upload_file":
            return await handle_upload_file(arguments)
        elif name == "selenium_download_file":
            return await handle_download_file(arguments)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Unknown tool: {name}")],
                isError=True
            )
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        return CallToolResult(
            content=[TextContent(type="text", text=f"Error: {str(e)}")],
            isError=True
        )

# Browser Management Handlers
async def handle_start_browser(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle start browser tool."""
    browser_type = arguments.get("browser_type", "chrome")
    headless = arguments.get("headless", False)
    window_size = tuple(arguments.get("window_size", [1920, 1080]))
    
    browser_id = browser_manager.start_browser(
        browser_type=browser_type,
        headless=headless,
        window_size=window_size
    )
    
    return CallToolResult(
        content=[TextContent(
            type="text", 
            text=f"Started {browser_type} browser with ID: {browser_id}"
        )]
    )

async def handle_stop_browser(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle stop browser tool."""
    browser_id = arguments.get("browser_id")
    success = browser_manager.stop_browser(browser_id)
    
    if success:
        return CallToolResult(
            content=[TextContent(type="text", text="Browser stopped successfully")]
        )
    else:
        return CallToolResult(
            content=[TextContent(type="text", text="Failed to stop browser")],
            isError=True
        )

async def handle_list_browsers(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle list browsers tool."""
    browsers = browser_manager.list_browsers()
    result_text = "Active browser sessions:\n"
    
    for browser_id, info in browsers.items():
        status = " (current)" if info["is_current"] else ""
        result_text += f"- {browser_id}: {info['title']} - {info['current_url']}{status}\n"
    
    if not browsers:
        result_text = "No active browser sessions"
    
    return CallToolResult(
        content=[TextContent(type="text", text=result_text)]
    )

async def handle_switch_browser(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle switch browser tool."""
    browser_id = arguments["browser_id"]
    success = browser_manager.switch_browser(browser_id)
    
    if success:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Switched to browser: {browser_id}")]
        )
    else:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Browser not found: {browser_id}")],
            isError=True
        )

# Navigation Handlers
async def handle_navigate(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle navigate tool."""
    url = arguments["url"]
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    browser.get(url)
    return CallToolResult(
        content=[TextContent(type="text", text=f"Navigated to: {url}")]
    )

async def handle_go_back(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle go back tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    browser.back()
    return CallToolResult(
        content=[TextContent(type="text", text="Went back in browser history")]
    )

async def handle_go_forward(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle go forward tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    browser.forward()
    return CallToolResult(
        content=[TextContent(type="text", text="Went forward in browser history")]
    )

async def handle_refresh(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle refresh tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    browser.refresh()
    return CallToolResult(
        content=[TextContent(type="text", text="Page refreshed")]
    )

async def handle_get_current_url(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle get current URL tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    url = browser.current_url
    return CallToolResult(
        content=[TextContent(type="text", text=f"Current URL: {url}")]
    )

# Element Interaction Handlers
async def handle_find_element(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle find element tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"Element found: {element.tag_name}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Element not found: {str(e)}")],
            isError=True
        )

async def handle_click(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle click tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        element.click()
        return CallToolResult(
            content=[TextContent(type="text", text="Element clicked successfully")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to click element: {str(e)}")],
            isError=True
        )

async def handle_type(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle type tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    text = arguments["text"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        element.clear()
        element.send_keys(text)
        return CallToolResult(
            content=[TextContent(type="text", text=f"Typed '{text}' into element")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to type into element: {str(e)}")],
            isError=True
        )

async def handle_get_text(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle get text tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        text = element.text
        return CallToolResult(
            content=[TextContent(type="text", text=f"Element text: {text}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to get element text: {str(e)}")],
            isError=True
        )

async def handle_get_attribute(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle get attribute tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    attribute = arguments["attribute"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        attr_value = element.get_attribute(attribute)
        return CallToolResult(
            content=[TextContent(type="text", text=f"Attribute '{attribute}': {attr_value}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to get attribute: {str(e)}")],
            isError=True
        )

async def handle_hover(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle hover tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        from selenium.webdriver.common.action_chains import ActionChains
        ActionChains(browser).move_to_element(element).perform()
        return CallToolResult(
            content=[TextContent(type="text", text="Hovered over element")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to hover over element: {str(e)}")],
            isError=True
        )

# Advanced Actions Handlers
async def handle_execute_script(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle execute script tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    script = arguments["script"]
    
    try:
        result = browser.execute_script(script)
        return CallToolResult(
            content=[TextContent(type="text", text=f"Script executed. Result: {result}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to execute script: {str(e)}")],
            isError=True
        )

async def handle_take_screenshot(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle take screenshot tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    filename = arguments.get("filename", f"screenshot_{browser_manager.current_browser_id}.png")
    
    try:
        screenshot_path = browser.get_screenshot_as_file(filename)
        return CallToolResult(
            content=[TextContent(type="text", text=f"Screenshot saved to: {screenshot_path}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to take screenshot: {str(e)}")],
            isError=True
        )

async def handle_wait_for_element(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle wait for element tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    timeout = arguments.get("timeout", 10)
    
    try:
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        wait = WebDriverWait(browser, timeout)
        
        if strategy == "id":
            element = wait.until(EC.presence_of_element_located((By.ID, value)))
        elif strategy == "name":
            element = wait.until(EC.presence_of_element_located((By.NAME, value)))
        elif strategy == "class_name":
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, value)))
        elif strategy == "tag_name":
            element = wait.until(EC.presence_of_element_located((By.TAG_NAME, value)))
        elif strategy == "css_selector":
            element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, value)))
        elif strategy == "xpath":
            element = wait.until(EC.presence_of_element_located((By.XPATH, value)))
        elif strategy == "link_text":
            element = wait.until(EC.presence_of_element_located((By.LINK_TEXT, value)))
        elif strategy == "partial_link_text":
            element = wait.until(EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, value)))
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"Element found after waiting: {element.tag_name}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Element not found within timeout: {str(e)}")],
            isError=True
        )

async def handle_scroll_to_element(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle scroll to element tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        return CallToolResult(
            content=[TextContent(type="text", text="Scrolled to element")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to scroll to element: {str(e)}")],
            isError=True
        )

# File Operations Handlers
async def handle_upload_file(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle upload file tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    strategy = arguments["strategy"]
    value = arguments["value"]
    file_path = arguments["file_path"]
    
    try:
        if strategy == "id":
            element = browser.find_element("id", value)
        elif strategy == "name":
            element = browser.find_element("name", value)
        elif strategy == "class_name":
            element = browser.find_element("class name", value)
        elif strategy == "tag_name":
            element = browser.find_element("tag name", value)
        elif strategy == "css_selector":
            element = browser.find_element("css selector", value)
        elif strategy == "xpath":
            element = browser.find_element("xpath", value)
        elif strategy == "link_text":
            element = browser.find_element("link text", value)
        elif strategy == "partial_link_text":
            element = browser.find_element("partial link text", value)
        else:
            return CallToolResult(
                content=[TextContent(type="text", text=f"Invalid strategy: {strategy}")],
                isError=True
            )
        
        element.send_keys(file_path)
        return CallToolResult(
            content=[TextContent(type="text", text=f"File uploaded: {file_path}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to upload file: {str(e)}")],
            isError=True
        )

async def handle_download_file(arguments: Dict[str, Any]) -> CallToolResult:
    """Handle download file tool."""
    browser = browser_manager.get_browser()
    
    if not browser:
        return CallToolResult(
            content=[TextContent(type="text", text="No active browser session")],
            isError=True
        )
    
    url = arguments["url"]
    filename = arguments.get("filename")
    
    try:
        import requests
        import os
        
        response = requests.get(url)
        response.raise_for_status()
        
        if not filename:
            filename = os.path.basename(url)
        
        with open(filename, 'wb') as f:
            f.write(response.content)
        
        return CallToolResult(
            content=[TextContent(type="text", text=f"File downloaded: {filename}")]
        )
        
    except Exception as e:
        return CallToolResult(
            content=[TextContent(type="text", text=f"Failed to download file: {str(e)}")],
            isError=True
        )

async def main():
    """Main entry point."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="selenium-mcp-server",
                server_version="1.0.0",
                capabilities=server.get_capabilities(
                    notification_options=None,
                    experimental_capabilities={}
                )
            )
        )

if __name__ == "__main__":
    asyncio.run(main())
