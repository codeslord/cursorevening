#!/usr/bin/env python3
"""
Web Scraping Examples using Selenium MCP Server

This module demonstrates various web scraping patterns using the MCP server,
including data extraction, pagination handling, and dynamic content scraping.
"""

import asyncio
import json
import time
from typing import List, Dict, Any

# Note: In actual usage, you would interact with the MCP server through the protocol
# These examples show the conceptual workflow and expected tool calls


class WebScrapingExamples:
    """Examples for web scraping automation."""

    def __init__(self):
        self.session_id = None

    async def basic_data_extraction(self) -> Dict[str, Any]:
        """
        Example: Extract product information from an e-commerce site.
        
        This demonstrates basic element finding and text extraction.
        """
        print("Starting basic data extraction example...")
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome", options={"headless": True})
        
        # Step 2: Navigate to target page
        print("2. Navigating to example e-commerce site...")
        # MCP Call: navigate(url="https://example-shop.com/products")
        
        # Step 3: Wait for page to load
        print("3. Waiting for page load...")
        # MCP Call: wait_for_page_load(timeout=30000)
        
        # Step 4: Find product containers
        print("4. Finding product containers...")
        # MCP Call: find_elements(by="css", value=".product-item", timeout=10000)
        
        products = []
        
        # Step 5: Extract data from each product
        print("5. Extracting product data...")
        for i in range(5):  # Simulate 5 products found
            product_data = {}
            
            # Extract product name
            # MCP Call: get_element_text(by="css", value=f".product-item:nth-child({i+1}) .product-name")
            product_data["name"] = f"Sample Product {i+1}"
            
            # Extract price
            # MCP Call: get_element_text(by="css", value=f".product-item:nth-child({i+1}) .price")
            product_data["price"] = f"${99.99 + i*10}"
            
            # Extract rating
            # MCP Call: get_element_attribute(by="css", value=f".product-item:nth-child({i+1}) .rating", attribute="data-rating")
            product_data["rating"] = f"{4.0 + i*0.1:.1f}"
            
            # Extract image URL
            # MCP Call: get_element_attribute(by="css", value=f".product-item:nth-child({i+1}) img", attribute="src")
            product_data["image_url"] = f"https://example-shop.com/images/product{i+1}.jpg"
            
            products.append(product_data)
        
        # Step 6: Take screenshot for verification
        print("6. Taking screenshot...")
        # MCP Call: take_screenshot(output_path="examples/products_page.png")
        
        # Step 7: Close session
        print("7. Closing browser session...")
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "products_extracted": len(products),
            "products": products,
            "timestamp": time.time()
        }
        
        print(f"✅ Extracted {len(products)} products successfully!")
        return result

    async def pagination_scraping(self) -> Dict[str, Any]:
        """
        Example: Scrape data across multiple pages with pagination.
        
        This demonstrates handling pagination and collecting data from multiple pages.
        """
        print("Starting pagination scraping example...")
        
        all_data = []
        current_page = 1
        max_pages = 3
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome", options={"headless": False, "window_size": [1920, 1080]})
        
        # Step 2: Navigate to first page
        print("2. Navigating to first page...")
        # MCP Call: navigate(url="https://example-news.com/articles?page=1")
        
        while current_page <= max_pages:
            print(f"Processing page {current_page}...")
            
            # Wait for content to load
            # MCP Call: wait_for_element(by="css", value=".article-list", timeout=15000)
            
            # Extract articles from current page
            page_articles = []
            
            # Find all article elements
            # MCP Call: find_elements(by="css", value=".article-item")
            
            # Simulate extracting 10 articles per page
            for i in range(10):
                article = {
                    "title": f"Article {current_page}-{i+1}: Sample News Title",
                    "author": f"Author {i+1}",
                    "date": f"2024-01-{current_page:02d}",
                    "url": f"https://example-news.com/article/{current_page}-{i+1}",
                    "page": current_page
                }
                
                # Extract title
                # MCP Call: get_element_text(by="css", value=f".article-item:nth-child({i+1}) .title")
                
                # Extract author
                # MCP Call: get_element_text(by="css", value=f".article-item:nth-child({i+1}) .author")
                
                # Extract date
                # MCP Call: get_element_text(by="css", value=f".article-item:nth-child({i+1}) .date")
                
                # Extract URL
                # MCP Call: get_element_attribute(by="css", value=f".article-item:nth-child({i+1}) a", attribute="href")
                
                page_articles.append(article)
            
            all_data.extend(page_articles)
            print(f"   ✓ Extracted {len(page_articles)} articles from page {current_page}")
            
            # Check if next page exists
            if current_page < max_pages:
                # Scroll to bottom to ensure pagination is visible
                # MCP Call: execute_script(script="window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait a bit for any dynamic loading
                await asyncio.sleep(2)
                
                # Look for next page button
                try:
                    # MCP Call: find_element(by="css", value=".pagination .next", timeout=5000)
                    next_button_exists = True
                except:
                    next_button_exists = False
                
                if next_button_exists:
                    # Click next page
                    # MCP Call: click_element(by="css", value=".pagination .next")
                    print(f"   → Navigating to page {current_page + 1}")
                    
                    # Wait for new page to load
                    # MCP Call: wait_for_page_load(timeout=15000)
                else:
                    print("   ✗ No more pages found")
                    break
            
            current_page += 1
        
        # Take final screenshot
        # MCP Call: take_screenshot(output_path="examples/final_pagination_page.png")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "total_articles": len(all_data),
            "pages_processed": current_page - 1,
            "articles": all_data
        }
        
        print(f"✅ Pagination scraping completed! Extracted {len(all_data)} articles from {current_page-1} pages")
        return result

    async def dynamic_content_scraping(self) -> Dict[str, Any]:
        """
        Example: Scrape dynamically loaded content using JavaScript execution.
        
        This demonstrates handling AJAX content and infinite scroll.
        """
        print("Starting dynamic content scraping example...")
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome", options={"headless": False})
        
        # Step 2: Navigate to dynamic content page
        print("2. Navigating to dynamic content page...")
        # MCP Call: navigate(url="https://example-social.com/feed")
        
        # Step 3: Wait for initial content
        print("3. Waiting for initial content...")
        # MCP Call: wait_for_element(by="css", value=".post-item", timeout=15000)
        
        all_posts = []
        scroll_count = 0
        max_scrolls = 5
        
        while scroll_count < max_scrolls:
            print(f"Processing scroll {scroll_count + 1}...")
            
            # Get current post count using JavaScript
            # MCP Call: execute_script(script="return document.querySelectorAll('.post-item').length;")
            current_post_count = 10 + (scroll_count * 5)  # Simulate increasing posts
            
            # Extract posts that are currently visible
            # MCP Call: find_elements(by="css", value=".post-item")
            
            # Simulate extracting new posts
            for i in range(5):  # 5 new posts per scroll
                post_index = scroll_count * 5 + i
                post = {
                    "id": f"post_{post_index}",
                    "content": f"Sample post content {post_index}",
                    "author": f"User{post_index % 10}",
                    "likes": f"{post_index * 3 + 15}",
                    "timestamp": f"2024-01-01T{(post_index % 24):02d}:00:00Z"
                }
                
                # Extract post content
                # MCP Call: get_element_text(by="css", value=f".post-item:nth-child({current_post_count - 5 + i + 1}) .content")
                
                # Extract author
                # MCP Call: get_element_text(by="css", value=f".post-item:nth-child({current_post_count - 5 + i + 1}) .author")
                
                # Extract likes using JavaScript (dynamic counter)
                # MCP Call: execute_script(script=f"return document.querySelector('.post-item:nth-child({current_post_count - 5 + i + 1}) .likes').textContent;")
                
                all_posts.append(post)
            
            print(f"   ✓ Extracted {len(all_posts)} total posts so far")
            
            # Scroll to trigger more content loading
            if scroll_count < max_scrolls - 1:
                print("   → Scrolling to load more content...")
                
                # Scroll down to trigger infinite scroll
                # MCP Call: execute_script(script="window.scrollTo(0, document.body.scrollHeight);")
                
                # Wait for new content to load
                await asyncio.sleep(3)
                
                # Check if new content loaded using JavaScript
                # MCP Call: execute_script(script="return document.querySelectorAll('.post-item').length;")
                new_post_count = current_post_count + 5  # Simulate new posts loaded
                
                if new_post_count > current_post_count:
                    print(f"   ✓ New content loaded ({new_post_count - current_post_count} new posts)")
                else:
                    print("   ✗ No new content loaded, stopping")
                    break
            
            scroll_count += 1
        
        # Execute custom JavaScript to get page analytics
        print("4. Gathering page analytics...")
        # MCP Call: execute_script(script="""
        #     return {
        #         totalPosts: document.querySelectorAll('.post-item').length,
        #         pageHeight: document.body.scrollHeight,
        #         viewportHeight: window.innerHeight,
        #         loadTime: performance.now()
        #     };
        # """)
        
        analytics = {
            "total_posts": len(all_posts),
            "page_height": 5000,
            "viewport_height": 1080,
            "load_time": 2345.67
        }
        
        # Take screenshot of final state
        # MCP Call: take_screenshot(output_path="examples/dynamic_content_final.png")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "posts_extracted": len(all_posts),
            "scrolls_performed": scroll_count,
            "analytics": analytics,
            "posts": all_posts[:10]  # Return first 10 for brevity
        }
        
        print(f"✅ Dynamic content scraping completed! Extracted {len(all_posts)} posts with {scroll_count} scrolls")
        return result

    async def form_based_data_extraction(self) -> Dict[str, Any]:
        """
        Example: Extract data by submitting forms and processing results.
        
        This demonstrates form interaction and result processing.
        """
        print("Starting form-based data extraction example...")
        
        search_results = []
        search_terms = ["python", "javascript", "machine learning"]
        
        # Step 1: Start browser session
        print("1. Starting browser session...")
        # MCP Call: start_browser(browser="chrome")
        
        # Step 2: Navigate to search site
        print("2. Navigating to search site...")
        # MCP Call: navigate(url="https://example-search.com")
        
        for i, term in enumerate(search_terms):
            print(f"Processing search term {i+1}: '{term}'...")
            
            # Clear and fill search box
            # MCP Call: clear_element(by="css", value="#search-input")
            # MCP Call: send_keys(by="css", value="#search-input", text=term)
            
            # Submit search
            # MCP Call: click_element(by="css", value="#search-button")
            
            # Wait for results
            # MCP Call: wait_for_element(by="css", value=".search-results", timeout=10000)
            
            # Extract result count
            # MCP Call: get_element_text(by="css", value=".result-count")
            result_count = f"{(i+1) * 1000 + 234}"
            
            # Extract top 5 results
            term_results = []
            for j in range(5):
                result = {
                    "title": f"Result {j+1} for {term}",
                    "url": f"https://example.com/result-{term.replace(' ', '-')}-{j+1}",
                    "snippet": f"This is a sample snippet for {term} result {j+1}...",
                    "search_term": term
                }
                
                # Extract title
                # MCP Call: get_element_text(by="css", value=f".result-item:nth-child({j+1}) .title")
                
                # Extract URL
                # MCP Call: get_element_attribute(by="css", value=f".result-item:nth-child({j+1}) a", attribute="href")
                
                # Extract snippet
                # MCP Call: get_element_text(by="css", value=f".result-item:nth-child({j+1}) .snippet")
                
                term_results.append(result)
            
            search_results.extend(term_results)
            
            # Take screenshot of results
            # MCP Call: take_screenshot(output_path=f"examples/search_results_{term.replace(' ', '_')}.png")
            
            print(f"   ✓ Found {len(term_results)} results for '{term}' (total: {result_count})")
        
        # Close session
        # MCP Call: close_session()
        
        result = {
            "success": True,
            "search_terms": search_terms,
            "total_results_extracted": len(search_results),
            "results": search_results
        }
        
        print(f"✅ Form-based extraction completed! Processed {len(search_terms)} search terms")
        return result


async def run_examples():
    """Run all web scraping examples."""
    print("🚀 Starting Web Scraping Examples")
    print("=" * 50)
    
    scraper = WebScrapingExamples()
    
    try:
        # Example 1: Basic data extraction
        print("\n📊 Example 1: Basic Data Extraction")
        result1 = await scraper.basic_data_extraction()
        print(f"Result: {json.dumps(result1, indent=2)}")
        
        # Example 2: Pagination scraping
        print("\n📄 Example 2: Pagination Scraping")
        result2 = await scraper.pagination_scraping()
        print(f"Result: {json.dumps(result2, indent=2)}")
        
        # Example 3: Dynamic content scraping
        print("\n🔄 Example 3: Dynamic Content Scraping")
        result3 = await scraper.dynamic_content_scraping()
        print(f"Result: {json.dumps(result3, indent=2)}")
        
        # Example 4: Form-based data extraction
        print("\n📝 Example 4: Form-based Data Extraction")
        result4 = await scraper.form_based_data_extraction()
        print(f"Result: {json.dumps(result4, indent=2)}")
        
        print("\n🎉 All web scraping examples completed successfully!")
        
    except Exception as e:
        print(f"❌ Error running examples: {str(e)}")


if __name__ == "__main__":
    asyncio.run(run_examples())
