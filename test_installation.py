#!/usr/bin/env python3
"""
Test script to verify Selenium MCP Server installation.
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported."""
    required_modules = [
        'mcp',
        'selenium',
        'webdriver_manager',
        'PIL'
    ]
    
    print("Testing imports...")
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✅ {module}")
        except ImportError as e:
            print(f"❌ {module}: {e}")
            return False
    
    return True

def test_selenium_mcp_server():
    """Test if selenium_mcp_server can be imported."""
    try:
        from selenium_mcp_server import main, browser_manager
        print("✅ selenium_mcp_server")
        return True
    except ImportError as e:
        print(f"❌ selenium_mcp_server: {e}")
        return False

def test_chrome_webdriver():
    """Test if Chrome WebDriver is available and functional."""
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        import subprocess
        
        # Check if chromedriver is available
        result = subprocess.run(['which', 'chromedriver'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ ChromeDriver not found in PATH")
            return False
            
        # Check chromedriver version
        result = subprocess.run(['chromedriver', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ ChromeDriver available: {version}")
        else:
            print("❌ ChromeDriver not functional")
            return False
            
        # Test WebDriver initialization (headless mode)
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        try:
            driver = webdriver.Chrome(options=chrome_options)
            driver.quit()
            print("✅ Chrome WebDriver initialization successful")
            return True
        except Exception as e:
            print(f"❌ Chrome WebDriver initialization failed: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ Required modules for WebDriver test: {e}")
        return False
    except Exception as e:
        print(f"❌ Chrome WebDriver test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🧪 Testing Selenium MCP Server Installation")
    print("=" * 50)
    
    success = True
    
    # Test imports
    if not test_imports():
        success = False
    
    print()
    
    # Test selenium_mcp_server
    if not test_selenium_mcp_server():
        success = False
    
    print()
    
    # Test Chrome WebDriver
    if not test_chrome_webdriver():
        success = False
    
    print()
    
    if success:
        print("🎉 All tests passed! Installation is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the installation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())



