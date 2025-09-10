# Selenium MCP Server

[![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-green.svg)](https://github.com/features/actions)

A production-ready **Model Context Protocol (MCP) server** that provides comprehensive browser automation capabilities using Selenium WebDriver. This server enables Large Language Models (LLMs) to interact with web browsers for testing, automation, web scraping, and data extraction tasks through a standardized protocol interface.

## 🚀 Features

### Core Browser Automation
- **Multi-browser Support**: Chrome, Firefox, Edge with automatic driver management
- **Session Management**: Concurrent browser instances with intelligent resource management
- **Element Interactions**: Click, type, hover, drag-and-drop, form submissions
- **Navigation Control**: URL navigation, back/forward, refresh, window management
- **Wait Strategies**: Smart waiting for elements, page loads, and dynamic content

### Advanced Capabilities
- **Screenshot & Media**: Full page and element-specific screenshot capture with base64 encoding
- **JavaScript Execution**: Synchronous and asynchronous script execution
- **File Operations**: Secure file uploads with path sanitization
- **Form Automation**: Complex form filling, dropdown selection, multi-step wizards
- **Performance Monitoring**: Page load times, resource metrics, Core Web Vitals

### Production Features
- **Robust Error Handling**: Comprehensive exception handling with detailed error messages
- **Security**: Input validation, file path sanitization, configurable restrictions
- **Logging**: Rotating file logs with configurable levels and structured output
- **Configuration Management**: Environment variables, YAML/JSON config files
- **Health Monitoring**: Built-in health checks and session monitoring
- **Resource Management**: Automatic cleanup, memory management, session limits

## 📦 Installation

### Quick Install
```bash
pip install selenium-mcp-server
```

### From Source
```bash
git clone https://github.com/example/selenium-mcp-server.git
cd selenium-mcp-server
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/example/selenium-mcp-server.git
cd selenium-mcp-server
pip install -e ".[dev,test,yaml]"
```

## 🤖 Claude Desktop Integration - Quick Setup

### TL;DR - Get Started in 3 Steps:

1. **Install:** `pip install -e .`
2. **Configure Claude:** Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:
   ```json
   {
     "mcpServers": {
       "selenium": {
         "command": "python",
         "args": ["-m", "selenium_mcp_server"],
         "env": {"SELENIUM_HEADLESS": "false"}
       }
     }
   }
   ```
3. **Restart Claude** and ask: *"Start a browser and navigate to google.com"*

## 🏃 Quick Start

### 1. Installation & Setup
```bash
# Install the server
pip install -e .

# Install browser drivers (Chrome recommended)
# Drivers are automatically managed by webdriver-manager
```

### 2. Configure for Claude Desktop

#### Step 1: Locate Claude Desktop Configuration
**macOS:**
```bash
# Open configuration file
code ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
# Open configuration file
notepad %APPDATA%\Claude\claude_desktop_config.json
```

#### Step 2: Add MCP Server Configuration
Add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": [
        "-m", 
        "selenium_mcp_server"
      ],
      "env": {
        "SELENIUM_LOG_LEVEL": "INFO",
        "SELENIUM_HEADLESS": "false",
        "SELENIUM_DEFAULT_TIMEOUT": "10000",
        "SELENIUM_MAX_SESSIONS": "3"
      }
    }
  }
}
```

#### Step 3: Alternative - Use Absolute Path (Recommended)
For more reliability, use the absolute path to your Python installation:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "/usr/bin/python3",
      "args": [
        "/Users/yourusername/path/to/selenium-mcp-server/selenium_mcp_server.py"
      ],
      "env": {
        "SELENIUM_LOG_LEVEL": "INFO",
        "SELENIUM_HEADLESS": "false",
        "SELENIUM_DEFAULT_TIMEOUT": "10000",
        "SELENIUM_MAX_SESSIONS": "3"
      }
    }
  }
}
```

#### Step 4: Verify Installation
1. **Restart Claude Desktop** completely
2. **Create a new conversation**
3. **Check for MCP connection** - you should see a small plug icon 🔌 indicating MCP servers are connected
4. **Test the connection** by asking Claude: "Can you list the available browser automation tools?"

### 3. Using with Claude - Step by Step

#### Basic Web Automation Example

**Prompt to Claude:**
```
I want to automate browsing to Google and searching for "Python automation". Can you help me do this step by step using the browser automation tools?
```

**Claude will then use the MCP tools like this:**

1. **Start Browser Session**
   ```
   start_browser with browser="chrome" and options={"headless": false, "window_size": [1920, 1080]}
   ```

2. **Navigate to Google**
   ```
   navigate to "https://google.com"
   ```

3. **Find Search Box and Enter Query**
   ```
   find_element using "name" locator with value "q"
   send_keys to search box with text "Python automation"
   ```

4. **Submit Search**
   ```
   press_key "ENTER"
   ```

5. **Take Screenshot**
   ```
   take_screenshot for verification
   ```

6. **Clean Up**
   ```
   close_session
   ```

#### Advanced Example: Form Automation

**Prompt to Claude:**
```
I need you to fill out a contact form on example.com. The form has fields for name, email, and message. Use "John Doe", "john@example.com", and "Hello from automation!" respectively.
```

**Claude will execute:**
```
1. start_browser("chrome")
2. navigate("https://example.com/contact")
3. send_keys("id", "name", "John Doe")
4. send_keys("id", "email", "john@example.com") 
5. send_keys("id", "message", "Hello from automation!")
6. click_element("css", "input[type='submit']")
7. take_screenshot("form_submitted.png")
8. close_session()
```

### 4. Environment Configuration

You can customize the server behavior through environment variables in the Claude config:

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"],
      "env": {
        "SELENIUM_DEFAULT_TIMEOUT": "15000",
        "SELENIUM_MAX_SESSIONS": "5",
        "SELENIUM_LOG_LEVEL": "DEBUG",
        "SELENIUM_SCREENSHOT_DIR": "/Users/yourusername/selenium-screenshots",
        "SELENIUM_HEADLESS": "false",
        "SELENIUM_ALLOW_FILE_UPLOADS": "true",
        "SELENIUM_MAX_FILE_SIZE_MB": "10"
      }
    }
  }
}
```

### 5. Testing the Setup

#### Quick Test Commands for Claude:

1. **Test Browser Start:**
   ```
   "Start a Chrome browser session for me"
   ```

2. **Test Navigation:**
   ```
   "Navigate to https://httpbin.org and take a screenshot"
   ```

3. **Test Element Interaction:**
   ```
   "Go to https://httpbin.org/forms/post and fill out the form with test data"
   ```

4. **Test Health Check:**
   ```
   "Check the health status of the browser automation server"
   ```

### 6. Troubleshooting Claude Integration

#### Common Issues:

**🔧 Issue: Claude doesn't see the MCP server**
- ✅ **Solution**: Restart Claude Desktop completely
- ✅ Check that the JSON syntax in config file is valid
- ✅ Verify Python path is correct

**🔧 Issue: "Command not found" error**
- ✅ **Solution**: Use absolute Python path instead of just "python"
- ✅ Make sure selenium_mcp_server.py is executable: `chmod +x selenium_mcp_server.py`

**🔧 Issue: Browser doesn't start**
- ✅ **Solution**: Install Chrome browser if not present
- ✅ Check that webdriver-manager can download drivers
- ✅ Try with `"SELENIUM_HEADLESS": "true"` for server environments

**🔧 Issue: Permission errors**
- ✅ **Solution**: Ensure screenshot directory is writable
- ✅ Check file permissions on the server script

#### Debug Mode:
```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"],
      "env": {
        "SELENIUM_LOG_LEVEL": "DEBUG",
        "SELENIUM_LOG_CONSOLE": "true"
      }
    }
  }
}
```

### 7. Example Prompts for Claude

Once configured, try these example prompts:

#### Web Scraping:
```
"Please scrape the product names and prices from the first page of https://books.toscrape.com and show me the results in a table format."
```

#### Testing:
```
"I need you to test the login functionality on https://the-internet.herokuapp.com/login. Use username 'tomsmith' and password 'SuperSecretPassword!'. Verify that login was successful."
```

#### Form Automation:
```
"Navigate to https://httpbin.org/forms/post and fill out all the form fields with appropriate test data, then submit the form and show me the response."
```

#### Performance Testing:
```
"Measure the page load time for https://example.com and take a screenshot. Also check if there are any JavaScript errors on the page."
```

## 🛠️ MCP Tools Reference

### Browser Management
| Tool | Description | Parameters |
|------|-------------|------------|
| `start_browser` | Start new browser session | `browser`, `options` |
| `close_session` | Close browser session | `session_id` (optional) |
| `get_session_info` | Get active session information | None |
| `health_check` | Server health status | None |

### Navigation & Page Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `navigate` | Navigate to URL | `url` |
| `get_current_url` | Get current page URL | None |
| `refresh_page` | Refresh current page | None |
| `go_back` | Navigate back in history | None |
| `go_forward` | Navigate forward in history | None |
| `get_page_title` | Get page title | None |
| `get_page_source` | Get page HTML source | None |

### Element Interactions
| Tool | Description | Parameters |
|------|-------------|------------|
| `find_element` | Find single element | `by`, `value`, `timeout` |
| `find_elements` | Find multiple elements | `by`, `value`, `timeout` |
| `click_element` | Click element | `by`, `value`, `timeout` |
| `double_click_element` | Double-click element | `by`, `value`, `timeout` |
| `right_click_element` | Right-click element | `by`, `value`, `timeout` |
| `send_keys` | Send text to element | `by`, `value`, `text`, `clear_first` |
| `clear_element` | Clear element content | `by`, `value`, `timeout` |
| `hover` | Hover over element | `by`, `value`, `timeout` |

### Advanced Interactions
| Tool | Description | Parameters |
|------|-------------|------------|
| `drag_and_drop` | Drag element to target | `source_by`, `source_value`, `target_by`, `target_value` |
| `upload_file` | Upload file to input | `by`, `value`, `file_path`, `timeout` |
| `select_dropdown_option` | Select dropdown option | `by`, `value`, `option_text`, `timeout` |
| `press_key` | Press keyboard key | `key` |

### Data Extraction
| Tool | Description | Parameters |
|------|-------------|------------|
| `get_element_text` | Get element text content | `by`, `value`, `timeout` |
| `get_element_attribute` | Get element attribute | `by`, `value`, `attribute`, `timeout` |

### Wait Operations
| Tool | Description | Parameters |
|------|-------------|------------|
| `wait_for_element` | Wait for element condition | `by`, `value`, `timeout`, `condition` |
| `wait_for_page_load` | Wait for page to load | `timeout` |

### JavaScript & Screenshots
| Tool | Description | Parameters |
|------|-------------|------------|
| `execute_script` | Execute JavaScript | `script` |
| `execute_async_script` | Execute async JavaScript | `script`, `timeout` |
| `take_screenshot` | Take page screenshot | `output_path` (optional) |
| `take_element_screenshot` | Take element screenshot | `by`, `value`, `output_path`, `timeout` |

### Locator Strategies
Supported element locator strategies:
- `id` - Element ID
- `css` - CSS selector
- `xpath` - XPath expression
- `name` - Element name attribute
- `tag` - HTML tag name
- `class` - CSS class name
- `link_text` - Exact link text
- `partial_link_text` - Partial link text

## ⚙️ Configuration

### Configuration File Example
```yaml
# config.yaml
server_name: "selenium-mcp-server"
host: "localhost"
port: 8000

logging:
  level: "INFO"
  file_path: "logs/server.log"
  max_file_size_mb: 10
  backup_count: 5

performance:
  default_timeout_ms: 10000
  max_sessions: 5
  session_cleanup_interval_seconds: 300

security:
  allow_file_uploads: true
  max_file_size_mb: 10
  allowed_file_extensions: [".txt", ".csv", ".json", ".png", ".jpg"]

screenshot:
  directory: "screenshots"
  format: "png"
  quality: 95

browsers:
  chrome:
    enabled: true
    default_options:
      headless: false
      window_size: [1920, 1080]
      additional_args:
        - "--no-sandbox"
        - "--disable-dev-shm-usage"
  firefox:
    enabled: true
    default_options:
      headless: false
      window_size: [1920, 1080]
```

### Environment Variables
```bash
# Core Configuration
SELENIUM_SERVER_NAME=selenium-mcp-server
SELENIUM_HOST=localhost
SELENIUM_PORT=8000
SELENIUM_DEFAULT_TIMEOUT=10000
SELENIUM_MAX_SESSIONS=5

# Logging
SELENIUM_LOG_LEVEL=INFO
SELENIUM_LOG_FILE=logs/server.log
SELENIUM_LOG_CONSOLE=false

# Security
SELENIUM_ALLOW_FILE_UPLOADS=true
SELENIUM_MAX_FILE_SIZE_MB=10

# Screenshots
SELENIUM_SCREENSHOT_DIR=screenshots
SELENIUM_SCREENSHOT_FORMAT=png
```

## 📚 Examples & Use Cases

### Web Scraping
```python
# Extract product data from e-commerce site
def scrape_products():
    start_browser("chrome", {"headless": True})
    navigate("https://shop.example.com/products")
    
    products = find_elements("css", ".product-item")
    for i in range(products["elements_found"]):
        name = get_element_text("css", f".product-item:nth-child({i+1}) .name")
        price = get_element_text("css", f".product-item:nth-child({i+1}) .price")
        print(f"Product: {name['text']}, Price: {price['text']}")
    
    close_session()
```

### Form Automation
```python
# Complete user registration
def register_user(user_data):
    start_browser("chrome")
    navigate("https://app.example.com/register")
    
    send_keys("id", "firstName", user_data["first_name"])
    send_keys("id", "lastName", user_data["last_name"])
    send_keys("id", "email", user_data["email"])
    select_dropdown_option("id", "country", user_data["country"])
    click_element("id", "submitButton")
    
    # Wait for confirmation
    wait_for_element("css", ".success-message", timeout=10000)
    close_session()
```

### Testing Workflows
```python
# E2E testing scenario
def test_checkout_flow():
    start_browser("chrome", {"headless": False})
    
    # Login
    navigate("https://store.example.com/login")
    send_keys("id", "username", "testuser@example.com")
    send_keys("id", "password", "testpass123")
    click_element("id", "loginButton")
    
    # Add product to cart
    navigate("https://store.example.com/products/laptop")
    click_element("css", ".add-to-cart")
    
    # Checkout
    click_element("css", ".cart-icon")
    click_element("css", ".checkout-button")
    
    # Fill shipping info
    send_keys("id", "shippingAddress", "123 Test St")
    send_keys("id", "shippingCity", "Test City")
    
    # Take screenshot for verification
    take_screenshot("checkout_final.png")
    close_session()
```

## 🔧 Development

### Project Structure
```
selenium-mcp-server/
├── selenium_mcp_server.py      # Main server implementation
├── config/
│   ├── __init__.py
│   └── server_config.py        # Configuration management
├── examples/
│   ├── __init__.py
│   ├── web_scraping.py         # Web scraping examples
│   ├── form_automation.py      # Form automation examples
│   └── testing_workflows.py    # QA testing examples
├── tests/
│   ├── __init__.py
│   ├── test_server.py          # Unit tests
│   └── test_integration.py     # Integration tests
├── requirements.txt            # Dependencies
├── pyproject.toml             # Modern Python packaging
└── README.md                  # This file
```

### Running Tests
```bash
# Unit tests only
pytest tests/test_server.py -v

# Integration tests (requires browser drivers)
pytest tests/test_integration.py -v

# All tests with coverage
pytest --cov=selenium_mcp_server --cov-report=html

# Skip integration tests
SKIP_INTEGRATION_TESTS=true pytest

# Test specific browser
TEST_BROWSER=firefox pytest tests/test_integration.py
```

### Code Quality
```bash
# Format code
black selenium_mcp_server.py config/ tests/ examples/

# Sort imports
isort selenium_mcp_server.py config/ tests/ examples/

# Type checking
mypy selenium_mcp_server.py config/

# Linting
flake8 selenium_mcp_server.py config/ tests/ examples/
```

## 🔒 Security Considerations

### Input Validation
- All user inputs are validated and sanitized
- File paths are resolved and checked for security
- JavaScript execution is sandboxed
- URL validation prevents malicious redirects

### File Upload Security
```python
# Secure file upload configuration
ALLOWED_EXTENSIONS = ['.txt', '.csv', '.json', '.png', '.jpg', '.pdf']
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
UPLOAD_DIRECTORY = '/secure/uploads'

# File validation
def validate_upload(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError("File not found")
    
    if os.path.getsize(file_path) > MAX_FILE_SIZE:
        raise ValueError("File too large")
    
    ext = os.path.splitext(file_path)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("File type not allowed")
```

### Browser Isolation
- Each session runs in isolated browser instance
- Automatic cleanup of browser data
- Configurable resource limits
- Session timeout management

## 📊 Monitoring & Observability

### Health Checks
```python
# Health check endpoint
health_status = health_check()
{
    "status": "healthy",
    "active_sessions": 2,
    "max_sessions": 5,
    "uptime_seconds": 3600,
    "version": "1.0.0"
}
```

### Logging
```python
# Structured logging output
{
    "timestamp": "2024-01-15T10:30:45.123Z",
    "level": "INFO",
    "component": "browser_manager",
    "session_id": "uuid-1234",
    "action": "start_browser",
    "browser": "chrome",
    "duration_ms": 2341,
    "success": true
}
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
# Fork and clone the repository
git clone https://github.com/yourusername/selenium-mcp-server.git
cd selenium-mcp-server

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install development dependencies
pip install -e ".[dev,test,yaml]"

# Run tests
pytest
```

### Pull Request Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass (`pytest`)
6. Update documentation if needed
7. Commit your changes (`git commit -m 'Add amazing feature'`)
8. Push to the branch (`git push origin feature/amazing-feature`)
9. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Selenium WebDriver](https://selenium.dev/) for browser automation capabilities
- [Model Context Protocol](https://github.com/modelcontextprotocol) for the standardized interface
- [FastMCP](https://github.com/jlowin/fastmcp) for the MCP server framework
- All contributors and maintainers

## 📞 Support

- **Documentation**: [https://selenium-mcp-server.readthedocs.io/](https://selenium-mcp-server.readthedocs.io/)
- **Issue Tracker**: [GitHub Issues](https://github.com/example/selenium-mcp-server/issues)
- **Discussions**: [GitHub Discussions](https://github.com/example/selenium-mcp-server/discussions)
- **Email**: team@example.com

---

**Made with ❤️ for the automation community**
