#!/usr/bin/env python3
"""
Example usage of the Selenium MCP Server.

This script demonstrates how to use the MCP server programmatically.
"""

import asyncio
import json
from selenium_mcp_server.main import server
from selenium_mcp_server.browser_manager import BrowserManager

async def example_usage():
    """Example of using the Selenium MCP Server."""
    
    # Initialize browser manager
    browser_manager = BrowserManager()
    
    print("🚀 Starting Selenium MCP Server Example")
    print("=" * 50)
    
    try:
        # Start a browser
        print("1. Starting Chrome browser...")
        browser_id = browser_manager.start_browser("chrome", headless=False)
        print(f"   ✅ Browser started with ID: {browser_id}")
        
        # Navigate to a website
        print("\n2. Navigating to Google...")
        browser = browser_manager.get_browser()
        browser.get("https://www.google.com")
        print(f"   ✅ Navigated to: {browser.current_url}")
        
        # Find and interact with search box
        print("\n3. Finding search box...")
        search_box = browser.find_element("name", "q")
        print("   ✅ Search box found")
        
        # Type in search box
        print("\n4. Typing search query...")
        search_box.send_keys("Selenium MCP Server")
        print("   ✅ Search query typed")
        
        # Submit search
        print("\n5. Submitting search...")
        search_box.submit()
        print("   ✅ Search submitted")
        
        # Wait a moment for results
        print("\n6. Waiting for results...")
        await asyncio.sleep(2)
        
        # Get page title
        print(f"\n7. Page title: {browser.title}")
        
        # Take a screenshot
        print("\n8. Taking screenshot...")
        screenshot_path = browser.get_screenshot_as_file("example_screenshot.png")
        print(f"   ✅ Screenshot saved to: {screenshot_path}")
        
        # List all browsers
        print("\n9. Listing active browsers...")
        browsers = browser_manager.list_browsers()
        for bid, info in browsers.items():
            print(f"   - {bid}: {info['title']} - {info['current_url']}")
        
        print("\n✅ Example completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during example: {str(e)}")
        
    finally:
        # Clean up
        print("\n10. Cleaning up...")
        browser_manager.stop_all_browsers()
        print("   ✅ All browsers stopped")

if __name__ == "__main__":
    asyncio.run(example_usage())
