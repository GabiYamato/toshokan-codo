"""Test overflow detection specifically"""

from playwright.sync_api import sync_playwright
from pathlib import Path

html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello World</h1>
    <p>This is a test</p>
</body>
</html>
"""

# Save to temp file
temp_path = Path("dist/overflow_debug.html")
temp_path.parent.mkdir(exist_ok=True)

with open(temp_path, 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Testing overflow detection...")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page(viewport={"width": 1920, "height": 1080})
    
    page.goto(f"file://{temp_path.absolute()}")
    page.wait_for_load_state("networkidle", timeout=5000)
    
    # Test the exact JavaScript code
    wide_elements = page.evaluate("""
        () => {
            const viewportWidth = window.innerWidth;
            const wideElements = [];
            
            document.querySelectorAll('*').forEach(el => {
                const rect = el.getBoundingClientRect();
                if (rect.width > viewportWidth && el.tagName !== 'HTML' && el.tagName !== 'BODY') {
                    wideElements.push({
                        tag: el.tagName,
                        class: el.className,
                        width: rect.width
                    });
                }
            });
            
            return wideElements.slice(0, 5); // Limit to first 5
        }
    """)
    
    print(f"Type of wide_elements: {type(wide_elements)}")
    print(f"Value of wide_elements: {wide_elements}")
    print(f"Is it a list? {isinstance(wide_elements, list)}")
    
    if wide_elements:
        print(f"\nLength: {len(wide_elements)}")
        if len(wide_elements) > 0:
            print(f"First element: {wide_elements[0]}")
            print(f"Type of first element: {type(wide_elements[0])}")
    
    browser.close()
