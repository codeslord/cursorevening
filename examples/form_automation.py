#!/usr/bin/env python3
"""
Form Automation Examples using Selenium MCP Server

This module demonstrates comprehensive form automation patterns including
registration forms, multi-step wizards, file uploads, and e-commerce checkout flows.
"""

import asyncio
import json
import time
from typing import List, Dict, Any


class FormAutomationExamples:
    """Examples for form automation workflows."""

    def __init__(self):
        self.session_id = None

    async def user_registration_form(self) -> Dict[str, Any]:
        """
        Example: Complete user registration form with validation handling.
        
        This demonstrates form filling, dropdown selection, and error handling.
        """
        print("Starting user registration form example...")
        
        # Sample user data
        user_data = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "password": "SecurePass123!",
            "confirm_password": "SecurePass123!",
            "phone": "+1-555-0123",
            "country": "United States",
            "state": "California",
            "city": "San Francisco",
            "zip_code": "94105",
            "birth_date": "1990-05-15",
            "terms_accepted": True
        }
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome", options={"headless": False, "window_size": [1920, 1080]})
        
        # Step 2: Navigate to registration page
        print("2. Navigating to registration page...")
        # MCP Call: navigate(url="https://example-app.com/register")
        
        # Step 3: Wait for form to load
        print("3. Waiting for registration form...")
        # MCP Call: wait_for_element(by="css", value="#registration-form", timeout=10000)
        
        # Step 4: Fill basic information
        print("4. Filling basic information...")
        
        # Fill first name
        # MCP Call: send_keys(by="id", value="first-name", text=user_data["first_name"], clear_first=True)
        print(f"   ✓ First name: {user_data['first_name']}")
        
        # Fill last name
        # MCP Call: send_keys(by="id", value="last-name", text=user_data["last_name"], clear_first=True)
        print(f"   ✓ Last name: {user_data['last_name']}")
        
        # Fill email
        # MCP Call: send_keys(by="id", value="email", text=user_data["email"], clear_first=True)
        print(f"   ✓ Email: {user_data['email']}")
        
        # Fill password
        # MCP Call: send_keys(by="id", value="password", text=user_data["password"], clear_first=True)
        print("   ✓ Password: [HIDDEN]")
        
        # Confirm password
        # MCP Call: send_keys(by="id", value="confirm-password", text=user_data["confirm_password"], clear_first=True)
        print("   ✓ Password confirmation: [HIDDEN]")
        
        # Step 5: Fill contact information
        print("5. Filling contact information...")
        
        # Fill phone number
        # MCP Call: send_keys(by="id", value="phone", text=user_data["phone"], clear_first=True)
        print(f"   ✓ Phone: {user_data['phone']}")
        
        # Select country from dropdown
        # MCP Call: select_dropdown_option(by="id", value="country", option_text=user_data["country"])
        print(f"   ✓ Country: {user_data['country']}")
        
        # Wait for state dropdown to populate
        await asyncio.sleep(1)
        
        # Select state
        # MCP Call: select_dropdown_option(by="id", value="state", option_text=user_data["state"])
        print(f"   ✓ State: {user_data['state']}")
        
        # Fill city
        # MCP Call: send_keys(by="id", value="city", text=user_data["city"], clear_first=True)
        print(f"   ✓ City: {user_data['city']}")
        
        # Fill zip code
        # MCP Call: send_keys(by="id", value="zip", text=user_data["zip_code"], clear_first=True)
        print(f"   ✓ ZIP Code: {user_data['zip_code']}")
        
        # Step 6: Fill birth date
        print("6. Setting birth date...")
        # MCP Call: send_keys(by="id", value="birth-date", text=user_data["birth_date"], clear_first=True)
        print(f"   ✓ Birth date: {user_data['birth_date']}")
        
        # Step 7: Accept terms and conditions
        print("7. Accepting terms and conditions...")
        # MCP Call: click_element(by="id", value="terms-checkbox")
        print("   ✓ Terms accepted")
        
        # Step 8: Validate form before submission
        print("8. Validating form data...")
        
        # Check for any validation errors
        # MCP Call: find_elements(by="css", value=".error-message")
        errors_found = 0  # Simulate no errors
        
        if errors_found > 0:
            print(f"   ❌ Found {errors_found} validation errors")
            # Handle errors here
        else:
            print("   ✅ No validation errors found")
        
        # Step 9: Take screenshot before submission
        print("9. Taking screenshot before submission...")
        # MCP Call: take_screenshot(output_path="examples/registration_form_filled.png")
        
        # Step 10: Submit form
        print("10. Submitting registration form...")
        # MCP Call: click_element(by="id", value="submit-button")
        
        # Wait for submission result
        # MCP Call: wait_for_element(by="css", value=".success-message, .error-message", timeout=15000)
        
        # Check submission result
        # MCP Call: find_element(by="css", value=".success-message", timeout=5000)
        success = True  # Simulate successful registration
        
        if success:
            # MCP Call: get_element_text(by="css", value=".success-message")
            success_message = "Registration completed successfully! Please check your email for verification."
            print(f"   ✅ {success_message}")
        
        # Take final screenshot
        # MCP Call: take_screenshot(output_path="examples/registration_success.png")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": success,
            "user_data": {k: v if k not in ["password", "confirm_password"] else "[HIDDEN]" for k, v in user_data.items()},
            "validation_errors": errors_found,
            "success_message": success_message if success else None,
            "timestamp": time.time()
        }
        
        print("✅ User registration completed!")
        return result

    async def multi_step_wizard_form(self) -> Dict[str, Any]:
        """
        Example: Complete a multi-step wizard form (e.g., survey or onboarding).
        
        This demonstrates navigation between form steps and progress tracking.
        """
        print("Starting multi-step wizard form example...")
        
        # Survey data for each step
        survey_data = {
            "step1": {
                "age_range": "25-34",
                "occupation": "Software Developer",
                "experience": "5-10 years"
            },
            "step2": {
                "interests": ["Technology", "Programming", "AI/ML"],
                "skills": ["Python", "JavaScript", "React"]
            },
            "step3": {
                "preferences": {
                    "newsletter": True,
                    "notifications": False,
                    "frequency": "Weekly"
                }
            }
        }
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome")
        
        # Step 2: Navigate to survey
        print("2. Navigating to multi-step survey...")
        # MCP Call: navigate(url="https://example-survey.com/wizard")
        
        # Step 3: Process Step 1 - Basic Information
        print("3. Processing Step 1 - Basic Information...")
        
        # Wait for step 1 form
        # MCP Call: wait_for_element(by="css", value="#step-1", timeout=10000)
        
        # Select age range
        # MCP Call: select_dropdown_option(by="id", value="age-range", option_text=survey_data["step1"]["age_range"])
        print(f"   ✓ Age range: {survey_data['step1']['age_range']}")
        
        # Select occupation
        # MCP Call: select_dropdown_option(by="id", value="occupation", option_text=survey_data["step1"]["occupation"])
        print(f"   ✓ Occupation: {survey_data['step1']['occupation']}")
        
        # Select experience
        # MCP Call: click_element(by="css", value=f"input[value='{survey_data['step1']['experience']}']")
        print(f"   ✓ Experience: {survey_data['step1']['experience']}")
        
        # Check progress indicator
        # MCP Call: get_element_text(by="css", value=".progress-indicator")
        progress = "Step 1 of 3"
        print(f"   📊 Progress: {progress}")
        
        # Click Next button
        # MCP Call: click_element(by="css", value=".next-button")
        print("   → Moving to Step 2...")
        
        # Step 4: Process Step 2 - Interests and Skills
        print("4. Processing Step 2 - Interests and Skills...")
        
        # Wait for step 2 form
        # MCP Call: wait_for_element(by="css", value="#step-2", timeout=10000)
        
        # Select interests (multiple checkboxes)
        for interest in survey_data["step2"]["interests"]:
            # MCP Call: click_element(by="css", value=f"input[value='{interest}']")
            print(f"   ✓ Interest: {interest}")
        
        # Add skills (dynamic input)
        for skill in survey_data["step2"]["skills"]:
            # MCP Call: send_keys(by="css", value="#skills-input", text=skill)
            # MCP Call: press_key(key="ENTER")
            print(f"   ✓ Skill: {skill}")
        
        # Check progress
        # MCP Call: get_element_text(by="css", value=".progress-indicator")
        progress = "Step 2 of 3"
        print(f"   📊 Progress: {progress}")
        
        # Take screenshot of step 2
        # MCP Call: take_screenshot(output_path="examples/wizard_step2.png")
        
        # Click Next button
        # MCP Call: click_element(by="css", value=".next-button")
        print("   → Moving to Step 3...")
        
        # Step 5: Process Step 3 - Preferences
        print("5. Processing Step 3 - Preferences...")
        
        # Wait for step 3 form
        # MCP Call: wait_for_element(by="css", value="#step-3", timeout=10000)
        
        # Set newsletter preference
        if survey_data["step3"]["preferences"]["newsletter"]:
            # MCP Call: click_element(by="id", value="newsletter-checkbox")
            print("   ✓ Newsletter subscription: Enabled")
        
        # Set notification preference
        if not survey_data["step3"]["preferences"]["notifications"]:
            # MCP Call: click_element(by="id", value="notifications-checkbox")
            print("   ✓ Notifications: Disabled")
        
        # Set frequency
        # MCP Call: select_dropdown_option(by="id", value="frequency", option_text=survey_data["step3"]["preferences"]["frequency"])
        print(f"   ✓ Frequency: {survey_data['step3']['preferences']['frequency']}")
        
        # Check final progress
        # MCP Call: get_element_text(by="css", value=".progress-indicator")
        progress = "Step 3 of 3"
        print(f"   📊 Progress: {progress}")
        
        # Step 6: Review and submit
        print("6. Reviewing and submitting...")
        
        # Scroll to review section
        # MCP Call: execute_script(script="document.querySelector('.review-section').scrollIntoView();")
        
        # Take screenshot of review
        # MCP Call: take_screenshot(output_path="examples/wizard_review.png")
        
        # Submit the wizard
        # MCP Call: click_element(by="css", value=".submit-button")
        
        # Wait for completion
        # MCP Call: wait_for_element(by="css", value=".completion-message", timeout=15000)
        
        # Get completion message
        # MCP Call: get_element_text(by="css", value=".completion-message")
        completion_message = "Thank you for completing the survey! Your responses have been recorded."
        
        # Take final screenshot
        # MCP Call: take_screenshot(output_path="examples/wizard_complete.png")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "steps_completed": 3,
            "survey_data": survey_data,
            "completion_message": completion_message,
            "timestamp": time.time()
        }
        
        print("✅ Multi-step wizard completed!")
        return result

    async def file_upload_form(self) -> Dict[str, Any]:
        """
        Example: Handle file upload forms with multiple file types.
        
        This demonstrates file selection, upload progress, and validation.
        """
        print("Starting file upload form example...")
        
        # Sample files to upload
        files_to_upload = [
            {"path": "/tmp/sample_document.pdf", "type": "PDF Document"},
            {"path": "/tmp/sample_image.jpg", "type": "Image"},
            {"path": "/tmp/sample_data.csv", "type": "CSV Data"}
        ]
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome")
        
        # Step 2: Navigate to upload form
        print("2. Navigating to file upload form...")
        # MCP Call: navigate(url="https://example-filehost.com/upload")
        
        # Step 3: Wait for upload form
        print("3. Waiting for upload form...")
        # MCP Call: wait_for_element(by="css", value="#upload-form", timeout=10000)
        
        uploaded_files = []
        
        # Step 4: Upload each file
        for i, file_info in enumerate(files_to_upload):
            print(f"4.{i+1} Uploading {file_info['type']}...")
            
            # Click add file button (if multiple uploads)
            if i > 0:
                # MCP Call: click_element(by="css", value=".add-file-button")
            
            # Upload file
            # MCP Call: upload_file(by="css", value=f"input[type='file']:nth-of-type({i+1})", file_path=file_info["path"])
            
            # Wait for file to be processed
            await asyncio.sleep(2)
            
            # Check upload status
            # MCP Call: get_element_text(by="css", value=f".file-status-{i+1}")
            status = "Upload successful"
            
            # Get file size
            # MCP Call: get_element_text(by="css", value=f".file-size-{i+1}")
            file_size = f"{(i+1) * 256} KB"
            
            uploaded_file = {
                "original_path": file_info["path"],
                "type": file_info["type"],
                "status": status,
                "size": file_size
            }
            uploaded_files.append(uploaded_file)
            
            print(f"   ✓ {file_info['type']}: {status} ({file_size})")
        
        # Step 5: Fill form metadata
        print("5. Filling upload metadata...")
        
        # Add title
        # MCP Call: send_keys(by="id", value="upload-title", text="Sample File Upload Batch")
        print("   ✓ Title: Sample File Upload Batch")
        
        # Add description
        description = "This is a test upload containing multiple file types for demonstration purposes."
        # MCP Call: send_keys(by="id", value="upload-description", text=description)
        print("   ✓ Description added")
        
        # Select category
        # MCP Call: select_dropdown_option(by="id", value="category", option_text="Test Files")
        print("   ✓ Category: Test Files")
        
        # Set privacy level
        # MCP Call: click_element(by="css", value="input[value='private']")
        print("   ✓ Privacy: Private")
        
        # Step 6: Review uploads
        print("6. Reviewing uploads...")
        
        # Get total file count
        # MCP Call: get_element_text(by="css", value=".file-count")
        total_files = len(uploaded_files)
        
        # Get total size
        # MCP Call: get_element_text(by="css", value=".total-size")
        total_size = "768 KB"
        
        print(f"   📊 Total files: {total_files}")
        print(f"   📊 Total size: {total_size}")
        
        # Take screenshot before submit
        # MCP Call: take_screenshot(output_path="examples/upload_form_ready.png")
        
        # Step 7: Submit upload
        print("7. Submitting upload...")
        # MCP Call: click_element(by="id", value="submit-upload")
        
        # Wait for processing
        # MCP Call: wait_for_element(by="css", value=".upload-complete", timeout=30000)
        
        # Get upload confirmation
        # MCP Call: get_element_text(by="css", value=".upload-confirmation")
        confirmation = "Files uploaded successfully! Upload ID: UP123456789"
        
        # Get download links
        download_links = []
        for i in range(len(uploaded_files)):
            # MCP Call: get_element_attribute(by="css", value=f".download-link-{i+1}", attribute="href")
            link = f"https://example-filehost.com/download/{i+1}"
            download_links.append(link)
        
        # Take final screenshot
        # MCP Call: take_screenshot(output_path="examples/upload_complete.png")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "files_uploaded": len(uploaded_files),
            "uploaded_files": uploaded_files,
            "total_size": total_size,
            "confirmation": confirmation,
            "download_links": download_links,
            "timestamp": time.time()
        }
        
        print("✅ File upload completed!")
        return result

    async def ecommerce_checkout_flow(self) -> Dict[str, Any]:
        """
        Example: Complete an e-commerce checkout process.
        
        This demonstrates cart management, shipping/billing forms, and payment.
        """
        print("Starting e-commerce checkout flow example...")
        
        # Customer and order data
        customer_data = {
            "email": "customer@example.com",
            "shipping": {
                "first_name": "Jane",
                "last_name": "Smith",
                "address": "123 Main Street",
                "city": "New York",
                "state": "NY",
                "zip": "10001",
                "country": "United States"
            },
            "billing": {
                "same_as_shipping": True
            },
            "payment": {
                "card_number": "4111111111111111",
                "expiry": "12/25",
                "cvv": "123",
                "cardholder": "Jane Smith"
            }
        }
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome", options={"window_size": [1920, 1080]})
        
        # Step 2: Navigate to product page
        print("2. Adding items to cart...")
        # MCP Call: navigate(url="https://example-store.com/products/laptop")
        
        # Add product to cart
        # MCP Call: click_element(by="css", value=".add-to-cart-button")
        print("   ✓ Added laptop to cart")
        
        # Go to another product
        # MCP Call: navigate(url="https://example-store.com/products/mouse")
        # MCP Call: click_element(by="css", value=".add-to-cart-button")
        print("   ✓ Added mouse to cart")
        
        # Step 3: Go to cart
        print("3. Reviewing cart...")
        # MCP Call: click_element(by="css", value=".cart-icon")
        
        # Wait for cart page
        # MCP Call: wait_for_element(by="css", value=".cart-items", timeout=10000)
        
        # Review cart items
        # MCP Call: find_elements(by="css", value=".cart-item")
        cart_items = [
            {"name": "Gaming Laptop", "price": "$1,299.99", "quantity": 1},
            {"name": "Wireless Mouse", "price": "$29.99", "quantity": 1}
        ]
        
        # Get cart total
        # MCP Call: get_element_text(by="css", value=".cart-total")
        cart_total = "$1,329.98"
        
        print(f"   📊 Cart total: {cart_total}")
        for item in cart_items:
            print(f"   - {item['name']}: {item['price']} x {item['quantity']}")
        
        # Proceed to checkout
        # MCP Call: click_element(by="css", value=".checkout-button")
        
        # Step 4: Fill shipping information
        print("4. Filling shipping information...")
        
        # Wait for checkout form
        # MCP Call: wait_for_element(by="css", value="#checkout-form", timeout=10000)
        
        # Fill email
        # MCP Call: send_keys(by="id", value="email", text=customer_data["email"])
        print(f"   ✓ Email: {customer_data['email']}")
        
        # Fill shipping address
        shipping = customer_data["shipping"]
        # MCP Call: send_keys(by="id", value="shipping-first-name", text=shipping["first_name"])
        # MCP Call: send_keys(by="id", value="shipping-last-name", text=shipping["last_name"])
        # MCP Call: send_keys(by="id", value="shipping-address", text=shipping["address"])
        # MCP Call: send_keys(by="id", value="shipping-city", text=shipping["city"])
        # MCP Call: select_dropdown_option(by="id", value="shipping-state", option_text=shipping["state"])
        # MCP Call: send_keys(by="id", value="shipping-zip", text=shipping["zip"])
        # MCP Call: select_dropdown_option(by="id", value="shipping-country", option_text=shipping["country"])
        
        print("   ✓ Shipping address completed")
        
        # Select shipping method
        # MCP Call: click_element(by="css", value="input[value='standard']")
        print("   ✓ Shipping method: Standard (5-7 days)")
        
        # Step 5: Handle billing information
        print("5. Setting billing information...")
        
        if customer_data["billing"]["same_as_shipping"]:
            # MCP Call: click_element(by="id", value="same-as-shipping")
            print("   ✓ Billing same as shipping")
        
        # Step 6: Fill payment information
        print("6. Filling payment information...")
        
        # Wait for payment section
        # MCP Call: wait_for_element(by="css", value="#payment-section", timeout=10000)
        
        payment = customer_data["payment"]
        
        # Fill card number
        # MCP Call: send_keys(by="id", value="card-number", text=payment["card_number"])
        print("   ✓ Card number: ****-****-****-1111")
        
        # Fill expiry
        # MCP Call: send_keys(by="id", value="card-expiry", text=payment["expiry"])
        print(f"   ✓ Expiry: {payment['expiry']}")
        
        # Fill CVV
        # MCP Call: send_keys(by="id", value="card-cvv", text=payment["cvv"])
        print("   ✓ CVV: ***")
        
        # Fill cardholder name
        # MCP Call: send_keys(by="id", value="cardholder-name", text=payment["cardholder"])
        print(f"   ✓ Cardholder: {payment['cardholder']}")
        
        # Step 7: Review order
        print("7. Reviewing order...")
        
        # Take screenshot of order review
        # MCP Call: take_screenshot(output_path="examples/checkout_review.png")
        
        # Get order summary
        # MCP Call: get_element_text(by="css", value=".order-summary")
        order_summary = {
            "subtotal": "$1,329.98",
            "shipping": "$9.99",
            "tax": "$93.10",
            "total": "$1,433.07"
        }
        
        print("   📊 Order Summary:")
        for key, value in order_summary.items():
            print(f"      {key.title()}: {value}")
        
        # Step 8: Place order
        print("8. Placing order...")
        
        # Accept terms
        # MCP Call: click_element(by="id", value="accept-terms")
        
        # Submit order
        # MCP Call: click_element(by="id", value="place-order-button")
        
        # Wait for order confirmation
        # MCP Call: wait_for_element(by="css", value=".order-confirmation", timeout=20000)
        
        # Get order number
        # MCP Call: get_element_text(by="css", value=".order-number")
        order_number = "ORD-2024-001234"
        
        # Get confirmation message
        # MCP Call: get_element_text(by="css", value=".confirmation-message")
        confirmation_message = "Your order has been placed successfully! You will receive a confirmation email shortly."
        
        # Take final screenshot
        # MCP Call: take_screenshot(output_path="examples/order_confirmation.png")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "order_number": order_number,
            "order_total": order_summary["total"],
            "items_ordered": len(cart_items),
            "customer_email": customer_data["email"],
            "confirmation_message": confirmation_message,
            "timestamp": time.time()
        }
        
        print(f"✅ Order placed successfully! Order #: {order_number}")
        return result


async def run_examples():
    """Run all form automation examples."""
    print("🚀 Starting Form Automation Examples")
    print("=" * 50)
    
    automation = FormAutomationExamples()
    
    try:
        # Example 1: User registration
        print("\n👤 Example 1: User Registration Form")
        result1 = await automation.user_registration_form()
        print(f"Result: {json.dumps(result1, indent=2)}")
        
        # Example 2: Multi-step wizard
        print("\n📋 Example 2: Multi-step Wizard Form")
        result2 = await automation.multi_step_wizard_form()
        print(f"Result: {json.dumps(result2, indent=2)}")
        
        # Example 3: File upload
        print("\n📁 Example 3: File Upload Form")
        result3 = await automation.file_upload_form()
        print(f"Result: {json.dumps(result3, indent=2)}")
        
        # Example 4: E-commerce checkout
        print("\n🛒 Example 4: E-commerce Checkout Flow")
        result4 = await automation.ecommerce_checkout_flow()
        print(f"Result: {json.dumps(result4, indent=2)}")
        
        print("\n🎉 All form automation examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_examples())
