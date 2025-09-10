# Selenium MCP Server

A Model Context Protocol (MCP) server for Selenium WebDriver automation, enabling AI assistants to control web browsers programmatically.

## Features

- **Multi-browser support**: Chrome, Firefox, Edge, Safari
- **Session management**: Start, stop, and switch between browser sessions
- **Navigation**: Navigate to URLs, go back/forward, refresh pages
- **Element interaction**: Find elements, click, type, get text, hover
- **Advanced actions**: Execute JavaScript, take screenshots, wait for elements
- **File operations**: Upload and download files
- **Robust error handling**: Comprehensive error messages and recovery

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running the Server

```bash
python -m selenium_mcp_server
```

### MCP Client Configuration

Add to your MCP client configuration (e.g., Claude Desktop):

```json
{
  "mcpServers": {
    "selenium": {
      "command": "python",
      "args": ["-m", "selenium_mcp_server"]
    }
  }
}
```

## Available Tools

### Browser Management
- `selenium_start_browser`: Start a new browser session
- `selenium_stop_browser`: Stop the current browser session
- `selenium_list_browsers`: List active browser sessions
- `selenium_switch_browser`: Switch to a different browser session

### Navigation
- `selenium_navigate`: Navigate to a URL
- `selenium_go_back`: Go back in browser history
- `selenium_go_forward`: Go forward in browser history
- `selenium_refresh`: Refresh the current page
- `selenium_get_current_url`: Get the current URL

### Element Interaction
- `selenium_find_element`: Find an element by various locator strategies
- `selenium_click`: Click an element
- `selenium_type`: Type text into an element
- `selenium_get_text`: Get text content from an element
- `selenium_get_attribute`: Get an attribute value from an element
- `selenium_hover`: Hover over an element

### Advanced Actions
- `selenium_execute_script`: Execute JavaScript code
- `selenium_take_screenshot`: Take a screenshot
- `selenium_wait_for_element`: Wait for an element to appear
- `selenium_scroll_to_element`: Scroll to an element

### File Operations
- `selenium_upload_file`: Upload a file to an input element
- `selenium_download_file`: Download a file from a URL

## Requirements

- Python 3.8+
- Chrome, Firefox, Edge, or Safari browser
- Appropriate WebDriver (automatically managed by webdriver-manager)

## License

MIT
