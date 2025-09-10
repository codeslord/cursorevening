"""
Browser management for Selenium MCP Server.
"""

import asyncio
import uuid
from typing import Dict, Optional, Any
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.safari.service import Service as SafariService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.safari.options import Options as SafariOptions


class BrowserManager:
    """Manages multiple browser sessions."""
    
    def __init__(self):
        self.browsers: Dict[str, webdriver.Remote] = {}
        self.current_browser_id: Optional[str] = None
    
    def start_browser(self, browser_type: str = "chrome", headless: bool = False, 
                     window_size: tuple = (1920, 1080), **kwargs) -> str:
        """Start a new browser session."""
        browser_id = str(uuid.uuid4())
        
        try:
            if browser_type.lower() == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                
                service = ChromeService(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                
            elif browser_type.lower() == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument(f"--width={window_size[0]}")
                options.add_argument(f"--height={window_size[1]}")
                
                service = FirefoxService(GeckoDriverManager().install())
                driver = webdriver.Firefox(service=service, options=options)
                
            elif browser_type.lower() == "edge":
                options = EdgeOptions()
                if headless:
                    options.add_argument("--headless")
                options.add_argument(f"--window-size={window_size[0]},{window_size[1]}")
                
                service = EdgeService(EdgeChromiumDriverManager().install())
                driver = webdriver.Edge(service=service, options=options)
                
            elif browser_type.lower() == "safari":
                options = SafariOptions()
                # Safari doesn't support headless mode in the same way
                driver = webdriver.Safari(options=options)
                
            else:
                raise ValueError(f"Unsupported browser type: {browser_type}")
            
            self.browsers[browser_id] = driver
            self.current_browser_id = browser_id
            
            return browser_id
            
        except Exception as e:
            raise Exception(f"Failed to start {browser_type} browser: {str(e)}")
    
    def stop_browser(self, browser_id: Optional[str] = None) -> bool:
        """Stop a browser session."""
        if browser_id is None:
            browser_id = self.current_browser_id
            
        if browser_id not in self.browsers:
            return False
            
        try:
            self.browsers[browser_id].quit()
            del self.browsers[browser_id]
            
            if self.current_browser_id == browser_id:
                self.current_browser_id = None
                if self.browsers:
                    self.current_browser_id = next(iter(self.browsers.keys()))
            
            return True
            
        except Exception as e:
            print(f"Error stopping browser {browser_id}: {str(e)}")
            return False
    
    def get_browser(self, browser_id: Optional[str] = None) -> Optional[webdriver.Remote]:
        """Get a browser instance."""
        if browser_id is None:
            browser_id = self.current_browser_id
            
        return self.browsers.get(browser_id)
    
    def switch_browser(self, browser_id: str) -> bool:
        """Switch to a different browser session."""
        if browser_id in self.browsers:
            self.current_browser_id = browser_id
            return True
        return False
    
    def list_browsers(self) -> Dict[str, Dict[str, Any]]:
        """List all active browser sessions."""
        result = {}
        for browser_id, driver in self.browsers.items():
            try:
                current_url = driver.current_url
                title = driver.title
            except:
                current_url = "Unknown"
                title = "Unknown"
                
            result[browser_id] = {
                "id": browser_id,
                "current_url": current_url,
                "title": title,
                "is_current": browser_id == self.current_browser_id
            }
        
        return result
    
    def stop_all_browsers(self):
        """Stop all browser sessions."""
        for browser_id in list(self.browsers.keys()):
            self.stop_browser(browser_id)
