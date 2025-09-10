from setuptools import setup, find_packages

setup(
    name="selenium-mcp-server",
    version="1.0.0",
    description="MCP server for Selenium WebDriver automation",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "mcp>=1.0.0",
        "selenium>=4.15.0",
        "webdriver-manager>=4.0.0",
        "Pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "selenium-mcp-server=selenium_mcp_server.main:main",
        ],
    },
    python_requires=">=3.8",
)
