#!/usr/bin/env python3
"""
Testing Workflows Examples using Selenium MCP Server

This module demonstrates comprehensive QA automation patterns including
UI testing, regression testing, cross-browser testing, and performance monitoring.
"""

import asyncio
import json
import time
from typing import List, Dict, Any


class TestingWorkflowExamples:
    """Examples for QA testing automation workflows."""

    def __init__(self):
        self.session_id = None
        self.test_results = []

    async def ui_component_testing(self) -> Dict[str, Any]:
        """
        Example: Test UI components functionality and responsiveness.
        
        This demonstrates element validation, interaction testing, and visual verification.
        """
        print("Starting UI component testing example...")
        
        test_cases = [
            {"name": "Button Functionality", "component": "primary-button"},
            {"name": "Form Validation", "component": "contact-form"},
            {"name": "Navigation Menu", "component": "main-nav"},
            {"name": "Modal Dialog", "component": "modal-dialog"},
            {"name": "Data Table", "component": "data-table"}
        ]
        
        test_results = []
        
        # Step 1: Start browser session
        print("1. Starting browser session for UI testing...")
        # MCP Call: start_browser(browser="chrome", options={"window_size": [1920, 1080]})
        
        # Step 2: Navigate to test application
        print("2. Navigating to test application...")
        # MCP Call: navigate(url="https://example-testapp.com/components")
        
        # Step 3: Wait for page load
        print("3. Waiting for component page to load...")
        # MCP Call: wait_for_page_load(timeout=30000)
        
        for i, test_case in enumerate(test_cases):
            print(f"4.{i+1} Testing {test_case['name']}...")
            
            start_time = time.time()
            test_result = {
                "test_name": test_case["name"],
                "component": test_case["component"],
                "status": "PASS",
                "errors": [],
                "execution_time": 0,
                "screenshots": []
            }
            
            try:
                if test_case["component"] == "primary-button":
                    # Test button states and functionality
                    # MCP Call: find_element(by="css", value=".primary-button", timeout=5000)
                    
                    # Test button is visible
                    # MCP Call: get_element_attribute(by="css", value=".primary-button", attribute="style")
                    button_visible = True
                    
                    # Test button is enabled
                    # MCP Call: get_element_attribute(by="css", value=".primary-button", attribute="disabled")
                    button_enabled = True
                    
                    # Test button click
                    # MCP Call: click_element(by="css", value=".primary-button")
                    
                    # Verify button action
                    # MCP Call: wait_for_element(by="css", value=".button-clicked-message", timeout=3000)
                    
                    # Test hover effect
                    # MCP Call: hover(by="css", value=".primary-button")
                    
                    if not button_visible:
                        test_result["errors"].append("Button not visible")
                    if not button_enabled:
                        test_result["errors"].append("Button not enabled")
                    
                    print("     ✓ Button visibility, state, and click functionality tested")
                
                elif test_case["component"] == "contact-form":
                    # Test form validation
                    # MCP Call: find_element(by="css", value="#contact-form", timeout=5000)
                    
                    # Test required field validation
                    # MCP Call: click_element(by="css", value="input[type='submit']")
                    # MCP Call: find_elements(by="css", value=".error-message")
                    validation_errors = 3  # Simulate finding 3 required field errors
                    
                    # Test valid form submission
                    # MCP Call: send_keys(by="id", value="name", text="Test User")
                    # MCP Call: send_keys(by="id", value="email", text="test@example.com")
                    # MCP Call: send_keys(by="id", value="message", text="Test message")
                    # MCP Call: click_element(by="css", value="input[type='submit']")
                    
                    # Verify success message
                    # MCP Call: wait_for_element(by="css", value=".success-message", timeout=5000)
                    
                    if validation_errors != 3:
                        test_result["errors"].append(f"Expected 3 validation errors, got {validation_errors}")
                    
                    print(f"     ✓ Form validation tested ({validation_errors} required field errors detected)")
                
                elif test_case["component"] == "main-nav":
                    # Test navigation menu
                    nav_items = ["Home", "Products", "About", "Contact"]
                    
                    for nav_item in nav_items:
                        # MCP Call: click_element(by="css", value=f"nav a[href*='{nav_item.lower()}']")
                        # MCP Call: wait_for_page_load(timeout=10000)
                        # MCP Call: get_current_url()
                        current_url = f"https://example-testapp.com/{nav_item.lower()}"
                        
                        if nav_item.lower() not in current_url:
                            test_result["errors"].append(f"Navigation to {nav_item} failed")
                    
                    print(f"     ✓ Navigation menu tested ({len(nav_items)} items)")
                
                elif test_case["component"] == "modal-dialog":
                    # Test modal functionality
                    # MCP Call: click_element(by="css", value=".open-modal-button")
                    
                    # Wait for modal to appear
                    # MCP Call: wait_for_element(by="css", value=".modal-overlay", timeout=5000)
                    
                    # Test modal is visible
                    # MCP Call: get_element_attribute(by="css", value=".modal-dialog", attribute="style")
                    modal_visible = True
                    
                    # Test modal close button
                    # MCP Call: click_element(by="css", value=".modal-close-button")
                    
                    # Wait for modal to disappear
                    await asyncio.sleep(1)
                    # MCP Call: find_elements(by="css", value=".modal-overlay")
                    modal_closed = True
                    
                    if not modal_visible:
                        test_result["errors"].append("Modal not visible after opening")
                    if not modal_closed:
                        test_result["errors"].append("Modal not closed after clicking close button")
                    
                    print("     ✓ Modal dialog open/close functionality tested")
                
                elif test_case["component"] == "data-table":
                    # Test data table functionality
                    # MCP Call: find_element(by="css", value=".data-table", timeout=5000)
                    
                    # Test table has data
                    # MCP Call: find_elements(by="css", value=".data-table tbody tr")
                    row_count = 10  # Simulate finding 10 rows
                    
                    # Test sorting functionality
                    # MCP Call: click_element(by="css", value=".data-table th[data-sort='name']")
                    await asyncio.sleep(1)
                    
                    # MCP Call: get_element_text(by="css", value=".data-table tbody tr:first-child td:first-child")
                    first_row_text = "Adams, John"  # Simulate sorted data
                    
                    # Test pagination
                    # MCP Call: click_element(by="css", value=".pagination .next")
                    await asyncio.sleep(1)
                    
                    # MCP Call: get_element_text(by="css", value=".pagination .current-page")
                    current_page = "2"
                    
                    if row_count < 1:
                        test_result["errors"].append("No data in table")
                    if not first_row_text.startswith("Adams"):
                        test_result["errors"].append("Sorting not working correctly")
                    if current_page != "2":
                        test_result["errors"].append("Pagination not working")
                    
                    print(f"     ✓ Data table tested ({row_count} rows, sorting, pagination)")
                
                # Take screenshot for each component test
                screenshot_path = f"examples/ui_test_{test_case['component']}.png"
                # MCP Call: take_screenshot(output_path=screenshot_path)
                test_result["screenshots"].append(screenshot_path)
                
            except Exception as e:
                test_result["status"] = "FAIL"
                test_result["errors"].append(str(e))
                print(f"     ❌ Test failed: {str(e)}")
            
            test_result["execution_time"] = time.time() - start_time
            
            if test_result["errors"]:
                test_result["status"] = "FAIL"
            
            test_results.append(test_result)
            
            status_icon = "✅" if test_result["status"] == "PASS" else "❌"
            print(f"     {status_icon} {test_case['name']}: {test_result['status']} ({test_result['execution_time']:.2f}s)")
        
        # Close session
        # MCP Call: close_session()
        
        # Calculate summary
        passed_tests = len([t for t in test_results if t["status"] == "PASS"])
        failed_tests = len([t for t in test_results if t["status"] == "FAIL"])
        total_time = sum(t["execution_time"] for t in test_results)
        
        result = {
            "success": failed_tests == 0,
            "total_tests": len(test_results),
            "passed": passed_tests,
            "failed": failed_tests,
            "total_execution_time": total_time,
            "test_results": test_results
        }
        
        print(f"✅ UI component testing completed: {passed_tests}/{len(test_results)} tests passed")
        return result

    async def regression_testing_suite(self) -> Dict[str, Any]:
        """
        Example: Run a regression testing suite across critical user flows.
        
        This demonstrates automated testing of key application workflows.
        """
        print("Starting regression testing suite...")
        
        test_scenarios = [
            {"name": "User Login Flow", "priority": "HIGH", "estimated_time": 30},
            {"name": "Product Search", "priority": "HIGH", "estimated_time": 45},
            {"name": "Add to Cart", "priority": "MEDIUM", "estimated_time": 60},
            {"name": "Checkout Process", "priority": "HIGH", "estimated_time": 120},
            {"name": "User Profile Update", "priority": "MEDIUM", "estimated_time": 40}
        ]
        
        regression_results = []
        
        # Step 1: Start browser session
        print("1. Starting regression testing session...")
        # MCP Call: start_browser(browser="chrome", options={"headless": True, "window_size": [1920, 1080]})
        
        for i, scenario in enumerate(test_scenarios):
            print(f"2.{i+1} Executing {scenario['name']} ({scenario['priority']} priority)...")
            
            start_time = time.time()
            scenario_result = {
                "scenario": scenario["name"],
                "priority": scenario["priority"],
                "status": "PASS",
                "steps_executed": 0,
                "steps_failed": 0,
                "errors": [],
                "execution_time": 0,
                "expected_time": scenario["estimated_time"]
            }
            
            try:
                if scenario["name"] == "User Login Flow":
                    # Test login flow
                    # MCP Call: navigate(url="https://example-app.com/login")
                    # MCP Call: wait_for_element(by="id", value="login-form", timeout=10000)
                    scenario_result["steps_executed"] += 1
                    
                    # Enter credentials
                    # MCP Call: send_keys(by="id", value="username", text="testuser@example.com")
                    # MCP Call: send_keys(by="id", value="password", text="testpass123")
                    scenario_result["steps_executed"] += 2
                    
                    # Submit login
                    # MCP Call: click_element(by="id", value="login-button")
                    # MCP Call: wait_for_element(by="css", value=".dashboard", timeout=15000)
                    scenario_result["steps_executed"] += 2
                    
                    # Verify login success
                    # MCP Call: get_current_url()
                    current_url = "https://example-app.com/dashboard"
                    if "dashboard" not in current_url:
                        scenario_result["errors"].append("Login redirect failed")
                        scenario_result["steps_failed"] += 1
                    
                    scenario_result["steps_executed"] += 1
                    print("     ✓ Login flow completed successfully")
                
                elif scenario["name"] == "Product Search":
                    # Test product search
                    # MCP Call: navigate(url="https://example-app.com/products")
                    scenario_result["steps_executed"] += 1
                    
                    # Perform search
                    # MCP Call: send_keys(by="css", value="#search-input", text="laptop")
                    # MCP Call: press_key(key="ENTER")
                    scenario_result["steps_executed"] += 2
                    
                    # Wait for results
                    # MCP Call: wait_for_element(by="css", value=".search-results", timeout=10000)
                    scenario_result["steps_executed"] += 1
                    
                    # Verify results
                    # MCP Call: find_elements(by="css", value=".product-item")
                    result_count = 15  # Simulate finding 15 products
                    if result_count == 0:
                        scenario_result["errors"].append("No search results found")
                        scenario_result["steps_failed"] += 1
                    
                    scenario_result["steps_executed"] += 1
                    print(f"     ✓ Product search completed ({result_count} results)")
                
                elif scenario["name"] == "Add to Cart":
                    # Test add to cart functionality
                    # MCP Call: navigate(url="https://example-app.com/product/laptop-123")
                    scenario_result["steps_executed"] += 1
                    
                    # Select quantity
                    # MCP Call: select_dropdown_option(by="id", value="quantity", option_text="2")
                    scenario_result["steps_executed"] += 1
                    
                    # Add to cart
                    # MCP Call: click_element(by="css", value=".add-to-cart-button")
                    scenario_result["steps_executed"] += 1
                    
                    # Verify cart update
                    # MCP Call: wait_for_element(by="css", value=".cart-notification", timeout=5000)
                    # MCP Call: get_element_text(by="css", value=".cart-count")
                    cart_count = "2"
                    if cart_count != "2":
                        scenario_result["errors"].append("Cart count incorrect")
                        scenario_result["steps_failed"] += 1
                    
                    scenario_result["steps_executed"] += 2
                    print(f"     ✓ Add to cart completed (cart count: {cart_count})")
                
                elif scenario["name"] == "Checkout Process":
                    # Test checkout process
                    # MCP Call: navigate(url="https://example-app.com/cart")
                    # MCP Call: click_element(by="css", value=".checkout-button")
                    scenario_result["steps_executed"] += 2
                    
                    # Fill shipping info
                    # MCP Call: send_keys(by="id", value="shipping-name", text="Test User")
                    # MCP Call: send_keys(by="id", value="shipping-address", text="123 Test St")
                    # MCP Call: send_keys(by="id", value="shipping-city", text="Test City")
                    scenario_result["steps_executed"] += 3
                    
                    # Select payment method
                    # MCP Call: click_element(by="css", value="input[value='credit-card']")
                    scenario_result["steps_executed"] += 1
                    
                    # Fill payment info
                    # MCP Call: send_keys(by="id", value="card-number", text="4111111111111111")
                    # MCP Call: send_keys(by="id", value="card-expiry", text="12/25")
                    scenario_result["steps_executed"] += 2
                    
                    # Complete checkout
                    # MCP Call: click_element(by="id", value="complete-order-button")
                    # MCP Call: wait_for_element(by="css", value=".order-confirmation", timeout=20000)
                    scenario_result["steps_executed"] += 2
                    
                    # Verify order confirmation
                    # MCP Call: get_element_text(by="css", value=".order-number")
                    order_number = "ORD-123456"
                    if not order_number.startswith("ORD-"):
                        scenario_result["errors"].append("Order confirmation failed")
                        scenario_result["steps_failed"] += 1
                    
                    scenario_result["steps_executed"] += 1
                    print(f"     ✓ Checkout completed (Order: {order_number})")
                
                elif scenario["name"] == "User Profile Update":
                    # Test profile update
                    # MCP Call: navigate(url="https://example-app.com/profile")
                    scenario_result["steps_executed"] += 1
                    
                    # Update profile fields
                    # MCP Call: clear_element(by="id", value="profile-name")
                    # MCP Call: send_keys(by="id", value="profile-name", text="Updated Test User")
                    # MCP Call: send_keys(by="id", value="profile-phone", text="+1-555-0123")
                    scenario_result["steps_executed"] += 3
                    
                    # Save changes
                    # MCP Call: click_element(by="css", value=".save-profile-button")
                    # MCP Call: wait_for_element(by="css", value=".save-success", timeout=10000)
                    scenario_result["steps_executed"] += 2
                    
                    # Verify changes saved
                    # MCP Call: get_element_attribute(by="id", value="profile-name", attribute="value")
                    updated_name = "Updated Test User"
                    if updated_name != "Updated Test User":
                        scenario_result["errors"].append("Profile update failed")
                        scenario_result["steps_failed"] += 1
                    
                    scenario_result["steps_executed"] += 1
                    print("     ✓ Profile update completed")
                
            except Exception as e:
                scenario_result["status"] = "FAIL"
                scenario_result["errors"].append(str(e))
                scenario_result["steps_failed"] += 1
                print(f"     ❌ Scenario failed: {str(e)}")
            
            scenario_result["execution_time"] = time.time() - start_time
            
            if scenario_result["errors"]:
                scenario_result["status"] = "FAIL"
            
            regression_results.append(scenario_result)
            
            status_icon = "✅" if scenario_result["status"] == "PASS" else "❌"
            time_status = "⚡" if scenario_result["execution_time"] <= scenario["estimated_time"] else "⏰"
            print(f"     {status_icon} {time_status} {scenario['name']}: {scenario_result['status']} ({scenario_result['execution_time']:.1f}s)")
        
        # Take final screenshot
        # MCP Call: take_screenshot(output_path="examples/regression_test_final.png")
        
        # Close session
        # MCP Call: close_session()
        
        # Calculate summary
        total_scenarios = len(regression_results)
        passed_scenarios = len([r for r in regression_results if r["status"] == "PASS"])
        failed_scenarios = total_scenarios - passed_scenarios
        total_steps = sum(r["steps_executed"] for r in regression_results)
        failed_steps = sum(r["steps_failed"] for r in regression_results)
        total_time = sum(r["execution_time"] for r in regression_results)
        
        result = {
            "success": failed_scenarios == 0,
            "total_scenarios": total_scenarios,
            "passed_scenarios": passed_scenarios,
            "failed_scenarios": failed_scenarios,
            "total_steps": total_steps,
            "failed_steps": failed_steps,
            "total_execution_time": total_time,
            "regression_results": regression_results
        }
        
        print(f"✅ Regression testing completed: {passed_scenarios}/{total_scenarios} scenarios passed")
        return result

    async def cross_browser_testing(self) -> Dict[str, Any]:
        """
        Example: Run tests across multiple browsers for compatibility.
        
        This demonstrates browser-specific testing and compatibility validation.
        """
        print("Starting cross-browser testing...")
        
        browsers = ["chrome", "firefox", "edge"]
        test_url = "https://example-webapp.com"
        
        browser_results = {}
        
        for browser in browsers:
            print(f"Testing with {browser.title()}...")
            
            browser_result = {
                "browser": browser,
                "status": "PASS",
                "tests": [],
                "errors": [],
                "execution_time": 0,
                "screenshots": []
            }
            
            start_time = time.time()
            
            try:
                # Start browser session
                # MCP Call: start_browser(browser=browser, options={"window_size": [1920, 1080]})
                print(f"   ✓ {browser.title()} browser started")
                
                # Test 1: Page load
                test_start = time.time()
                # MCP Call: navigate(url=test_url)
                # MCP Call: wait_for_page_load(timeout=30000)
                load_time = time.time() - test_start
                
                browser_result["tests"].append({
                    "name": "Page Load",
                    "status": "PASS" if load_time < 5.0 else "SLOW",
                    "load_time": load_time
                })
                print(f"   ✓ Page loaded in {load_time:.2f}s")
                
                # Test 2: CSS rendering
                # MCP Call: execute_script(script="return getComputedStyle(document.body).backgroundColor;")
                bg_color = "rgb(255, 255, 255)"  # Simulate getting background color
                
                # MCP Call: execute_script(script="return document.querySelectorAll('.missing-styles').length;")
                missing_styles = 0  # Simulate checking for missing styles
                
                css_test = {
                    "name": "CSS Rendering",
                    "status": "PASS" if missing_styles == 0 else "FAIL",
                    "background_color": bg_color,
                    "missing_styles": missing_styles
                }
                browser_result["tests"].append(css_test)
                print(f"   ✓ CSS rendering: {css_test['status']}")
                
                # Test 3: JavaScript functionality
                # MCP Call: execute_script(script="return typeof jQuery !== 'undefined';")
                jquery_loaded = True  # Simulate jQuery check
                
                # MCP Call: execute_script(script="return document.querySelectorAll('.js-error').length;")
                js_errors = 0  # Simulate checking for JS errors
                
                js_test = {
                    "name": "JavaScript Functionality",
                    "status": "PASS" if js_errors == 0 else "FAIL",
                    "jquery_loaded": jquery_loaded,
                    "js_errors": js_errors
                }
                browser_result["tests"].append(js_test)
                print(f"   ✓ JavaScript: {js_test['status']}")
                
                # Test 4: Form interactions
                # MCP Call: find_element(by="css", value="#test-form", timeout=5000)
                form_present = True
                
                if form_present:
                    # MCP Call: send_keys(by="id", value="test-input", text="Cross-browser test")
                    # MCP Call: click_element(by="css", value="#test-submit")
                    # MCP Call: wait_for_element(by="css", value=".form-success", timeout=5000)
                    form_works = True
                else:
                    form_works = False
                
                form_test = {
                    "name": "Form Interactions",
                    "status": "PASS" if form_works else "FAIL",
                    "form_present": form_present,
                    "form_functional": form_works
                }
                browser_result["tests"].append(form_test)
                print(f"   ✓ Form interactions: {form_test['status']}")
                
                # Test 5: Responsive design
                viewports = [
                    {"name": "Desktop", "width": 1920, "height": 1080},
                    {"name": "Tablet", "width": 768, "height": 1024},
                    {"name": "Mobile", "width": 375, "height": 667}
                ]
                
                responsive_results = []
                for viewport in viewports:
                    # MCP Call: execute_script(script=f"window.resizeTo({viewport['width']}, {viewport['height']});")
                    await asyncio.sleep(1)
                    
                    # MCP Call: execute_script(script="return window.innerWidth;")
                    actual_width = viewport["width"]
                    
                    # Check if layout adapts properly
                    # MCP Call: execute_script(script="return document.querySelector('.mobile-menu').style.display;")
                    mobile_menu_display = "block" if viewport["width"] < 768 else "none"
                    
                    viewport_test = {
                        "viewport": viewport["name"],
                        "expected_width": viewport["width"],
                        "actual_width": actual_width,
                        "layout_adapted": mobile_menu_display == ("block" if viewport["width"] < 768 else "none")
                    }
                    responsive_results.append(viewport_test)
                
                responsive_test = {
                    "name": "Responsive Design",
                    "status": "PASS" if all(r["layout_adapted"] for r in responsive_results) else "FAIL",
                    "viewport_tests": responsive_results
                }
                browser_result["tests"].append(responsive_test)
                print(f"   ✓ Responsive design: {responsive_test['status']}")
                
                # Take screenshot for each browser
                screenshot_path = f"examples/cross_browser_{browser}.png"
                # MCP Call: take_screenshot(output_path=screenshot_path)
                browser_result["screenshots"].append(screenshot_path)
                
                # Check if any tests failed
                failed_tests = [t for t in browser_result["tests"] if t["status"] == "FAIL"]
                if failed_tests:
                    browser_result["status"] = "FAIL"
                    browser_result["errors"] = [f"Test failed: {t['name']}" for t in failed_tests]
                
            except Exception as e:
                browser_result["status"] = "FAIL"
                browser_result["errors"].append(str(e))
                print(f"   ❌ {browser.title()} testing failed: {str(e)}")
            
            finally:
                # Close browser session
                # MCP Call: close_session()
                print(f"   ✓ {browser.title()} session closed")
            
            browser_result["execution_time"] = time.time() - start_time
            browser_results[browser] = browser_result
            
            status_icon = "✅" if browser_result["status"] == "PASS" else "❌"
            print(f"{status_icon} {browser.title()}: {browser_result['status']} ({browser_result['execution_time']:.1f}s)")
        
        # Calculate summary
        total_browsers = len(browser_results)
        passed_browsers = len([r for r in browser_results.values() if r["status"] == "PASS"])
        failed_browsers = total_browsers - passed_browsers
        
        result = {
            "success": failed_browsers == 0,
            "total_browsers": total_browsers,
            "passed_browsers": passed_browsers,
            "failed_browsers": failed_browsers,
            "browser_results": browser_results
        }
        
        print(f"✅ Cross-browser testing completed: {passed_browsers}/{total_browsers} browsers passed")
        return result

    async def performance_monitoring(self) -> Dict[str, Any]:
        """
        Example: Monitor web application performance metrics.
        
        This demonstrates performance testing and monitoring automation.
        """
        print("Starting performance monitoring...")
        
        test_pages = [
            {"name": "Homepage", "url": "https://example-app.com/", "expected_load_time": 2.0},
            {"name": "Product Listing", "url": "https://example-app.com/products", "expected_load_time": 3.0},
            {"name": "Product Detail", "url": "https://example-app.com/product/123", "expected_load_time": 2.5},
            {"name": "Search Results", "url": "https://example-app.com/search?q=laptop", "expected_load_time": 4.0}
        ]
        
        performance_results = []
        
        # Step 1: Start browser session
        print("1. Starting performance monitoring session...")
        # MCP Call: start_browser(browser="chrome", options={
        #     "headless": True,
        #     "additional_args": ["--enable-logging", "--log-level=0"]
        # })
        
        for i, page in enumerate(test_pages):
            print(f"2.{i+1} Testing {page['name']} performance...")
            
            page_result = {
                "page_name": page["name"],
                "url": page["url"],
                "expected_load_time": page["expected_load_time"],
                "metrics": {},
                "status": "PASS",
                "issues": []
            }
            
            try:
                # Clear cache and start fresh
                # MCP Call: execute_script(script="performance.clearResourceTimings();")
                
                # Navigate and measure load time
                start_time = time.time()
                # MCP Call: navigate(url=page["url"])
                # MCP Call: wait_for_page_load(timeout=30000)
                load_time = time.time() - start_time
                
                # Get performance metrics using JavaScript
                # MCP Call: execute_script(script="""
                #     return {
                #         loadEventEnd: performance.timing.loadEventEnd,
                #         navigationStart: performance.timing.navigationStart,
                #         domContentLoaded: performance.timing.domContentLoadedEventEnd,
                #         firstPaint: performance.getEntriesByType('paint')[0]?.startTime || 0,
                #         firstContentfulPaint: performance.getEntriesByType('paint')[1]?.startTime || 0
                #     };
                # """)
                
                # Simulate performance metrics
                metrics = {
                    "page_load_time": load_time,
                    "dom_content_loaded": load_time * 0.7,
                    "first_paint": load_time * 0.5,
                    "first_contentful_paint": load_time * 0.6,
                    "time_to_interactive": load_time * 0.9
                }
                
                # Get resource metrics
                # MCP Call: execute_script(script="""
                #     return performance.getEntriesByType('resource').map(r => ({
                #         name: r.name,
                #         duration: r.duration,
                #         size: r.transferSize,
                #         type: r.initiatorType
                #     }));
                # """)
                
                # Simulate resource data
                resource_metrics = {
                    "total_resources": 45 + i * 5,
                    "total_size_kb": 850 + i * 100,
                    "largest_resource_kb": 120 + i * 20,
                    "slow_resources": 2 if i > 1 else 0
                }
                
                # Get Core Web Vitals
                # MCP Call: execute_script(script="""
                #     return new Promise(resolve => {
                #         new PerformanceObserver((list) => {
                #             const entries = list.getEntries();
                #             resolve({
                #                 lcp: entries.find(e => e.entryType === 'largest-contentful-paint')?.value || 0,
                #                 fid: entries.find(e => e.entryType === 'first-input')?.value || 0,
                #                 cls: entries.find(e => e.entryType === 'layout-shift')?.value || 0
                #             });
                #         }).observe({entryTypes: ['largest-contentful-paint', 'first-input', 'layout-shift']});
                #         
                #         setTimeout(() => resolve({lcp: 0, fid: 0, cls: 0}), 5000);
                #     });
                # """)
                
                # Simulate Core Web Vitals
                core_web_vitals = {
                    "largest_contentful_paint": 1.8 + i * 0.3,
                    "first_input_delay": 50 + i * 10,
                    "cumulative_layout_shift": 0.05 + i * 0.02
                }
                
                # Combine all metrics
                page_result["metrics"] = {
                    **metrics,
                    **resource_metrics,
                    **core_web_vitals
                }
                
                # Analyze performance issues
                if load_time > page["expected_load_time"]:
                    page_result["issues"].append(f"Page load time ({load_time:.2f}s) exceeds expected ({page['expected_load_time']}s)")
                
                if core_web_vitals["largest_contentful_paint"] > 2.5:
                    page_result["issues"].append(f"LCP too high: {core_web_vitals['largest_contentful_paint']:.2f}s")
                
                if core_web_vitals["first_input_delay"] > 100:
                    page_result["issues"].append(f"FID too high: {core_web_vitals['first_input_delay']:.1f}ms")
                
                if core_web_vitals["cumulative_layout_shift"] > 0.1:
                    page_result["issues"].append(f"CLS too high: {core_web_vitals['cumulative_layout_shift']:.3f}")
                
                if resource_metrics["total_size_kb"] > 1000:
                    page_result["issues"].append(f"Total page size too large: {resource_metrics['total_size_kb']} KB")
                
                if page_result["issues"]:
                    page_result["status"] = "WARNING" if len(page_result["issues"]) <= 2 else "FAIL"
                
                print(f"     📊 Load time: {load_time:.2f}s, LCP: {core_web_vitals['largest_contentful_paint']:.2f}s")
                print(f"     📈 Resources: {resource_metrics['total_resources']}, Size: {resource_metrics['total_size_kb']} KB")
                
                if page_result["issues"]:
                    print(f"     ⚠️  Issues found: {len(page_result['issues'])}")
                    for issue in page_result["issues"]:
                        print(f"        - {issue}")
                else:
                    print("     ✅ No performance issues detected")
                
            except Exception as e:
                page_result["status"] = "FAIL"
                page_result["issues"].append(f"Performance test failed: {str(e)}")
                print(f"     ❌ Performance test failed: {str(e)}")
            
            performance_results.append(page_result)
        
        # Take performance summary screenshot
        # MCP Call: take_screenshot(output_path="examples/performance_summary.png")
        
        # Close session
        # MCP Call: close_session()
        
        # Calculate summary
        total_pages = len(performance_results)
        good_performance = len([r for r in performance_results if r["status"] == "PASS"])
        warning_performance = len([r for r in performance_results if r["status"] == "WARNING"])
        poor_performance = len([r for r in performance_results if r["status"] == "FAIL"])
        
        avg_load_time = sum(r["metrics"].get("page_load_time", 0) for r in performance_results) / total_pages
        
        result = {
            "success": poor_performance == 0,
            "total_pages": total_pages,
            "good_performance": good_performance,
            "warning_performance": warning_performance,
            "poor_performance": poor_performance,
            "average_load_time": avg_load_time,
            "performance_results": performance_results
        }
        
        print(f"✅ Performance monitoring completed:")
        print(f"   📊 {good_performance} good, {warning_performance} warnings, {poor_performance} poor")
        print(f"   ⏱️  Average load time: {avg_load_time:.2f}s")
        
        return result


async def run_examples():
    """Run all testing workflow examples."""
    print("🚀 Starting Testing Workflow Examples")
    print("=" * 50)
    
    testing = TestingWorkflowExamples()
    
    try:
        # Example 1: UI component testing
        print("\n🔧 Example 1: UI Component Testing")
        result1 = await testing.ui_component_testing()
        print(f"Summary: {result1['passed']}/{result1['total_tests']} tests passed")
        
        # Example 2: Regression testing
        print("\n🔄 Example 2: Regression Testing Suite")
        result2 = await testing.regression_testing_suite()
        print(f"Summary: {result2['passed_scenarios']}/{result2['total_scenarios']} scenarios passed")
        
        # Example 3: Cross-browser testing
        print("\n🌐 Example 3: Cross-Browser Testing")
        result3 = await testing.cross_browser_testing()
        print(f"Summary: {result3['passed_browsers']}/{result3['total_browsers']} browsers passed")
        
        # Example 4: Performance monitoring
        print("\n📈 Example 4: Performance Monitoring")
        result4 = await testing.performance_monitoring()
        print(f"Summary: {result4['good_performance']}/{result4['total_pages']} pages with good performance")
        
        print("\n🎉 All testing workflow examples completed successfully!")
        
        # Overall summary
        total_tests = (result1['total_tests'] + result2['total_scenarios'] + 
                      result3['total_browsers'] + result4['total_pages'])
        
        total_passed = (result1['passed'] + result2['passed_scenarios'] + 
                       result3['passed_browsers'] + result4['good_performance'])
        
        print(f"\n📋 Overall Testing Summary:")
        print(f"   Total tests executed: {total_tests}")
        print(f"   Tests passed: {total_passed}")
        print(f"   Success rate: {(total_passed/total_tests)*100:.1f}%")
        
    except Exception as e:
        print(f"❌ Error running testing examples: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_examples())
