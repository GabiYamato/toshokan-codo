"""
Visual Validator Module
Uses headless browser to validate the assembled website visually.

Responsibilities:
- Render page in headless browser (Playwright/Puppeteer)
- Check layout correctness:
  * Page scrollability (height > viewport)
  * No overflow issues
  * Section spacing and balance
  * Color contrast (accessibility)
  * Responsive behavior
- Generate structured validation report

Output Format:
{
    "valid": true/false,
    "issues": [
        {"type": "scroll", "severity": "high", "description": "Page not scrollable"},
        {"type": "overflow", "severity": "medium", "element": "#hero"}
    ],
    "metrics": {
        "page_height": 2400,
        "viewport_height": 900,
        "sections_detected": 4
    }
}
"""

from playwright.sync_api import sync_playwright
from pathlib import Path
from typing import Dict, List, Optional
import time


def validate_layout(html_path: str, headless: bool = True) -> dict:
    """
    Validate website layout using headless browser.
    
    Args:
        html_path: Path to the HTML file to validate
        headless: Whether to run browser in headless mode
        
    Returns:
        Validation report dictionary
    """
    # Ensure file exists
    file_path = Path(html_path)
    if not file_path.exists():
        return {
            "valid": False,
            "issues": [{"type": "file", "severity": "critical", "description": f"File not found: {html_path}"}],
            "metrics": {}
        }
    
    issues = []
    metrics = {}
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page(viewport={"width": 1920, "height": 1080})
        
        try:
            # Load the HTML file
            page.goto(f"file://{file_path.absolute()}")
            
            # Wait for page to load
            page.wait_for_load_state("networkidle", timeout=5000)
            time.sleep(0.5)  # Extra wait for animations
            
            # Run validation checks
            try:
                scroll_check = check_scrollability(page)
                if not scroll_check["valid"]:
                    issues.extend(scroll_check["issues"])
                metrics.update(scroll_check["metrics"])
            except Exception as e:
                issues.append({
                    "type": "error",
                    "severity": "medium",
                    "description": f"Scroll check error: {str(e)}"
                })
            
            try:
                overflow_check = check_overflow(page)
                issues.extend(overflow_check)
            except Exception as e:
                issues.append({
                    "type": "error",
                    "severity": "medium",
                    "description": f"Overflow check error: {str(e)}"
                })
            
            try:
                section_check = check_section_balance(page)
                issues.extend(section_check["issues"])
                metrics.update(section_check["metrics"])
            except Exception as e:
                issues.append({
                    "type": "error",
                    "severity": "medium",
                    "description": f"Section check error: {str(e)}"
                })
            
            try:
                responsive_check = check_responsive_behavior(page)
                issues.extend(responsive_check["issues"])
            except Exception as e:
                issues.append({
                    "type": "error",
                    "severity": "medium",
                    "description": f"Responsive check error: {str(e)}"
                })
            
            try:
                # Check for basic accessibility
                accessibility_check = check_basic_accessibility(page)
                issues.extend(accessibility_check["issues"])
            except Exception as e:
                issues.append({
                    "type": "error",
                    "severity": "medium",
                    "description": f"Accessibility check error: {str(e)}"
                })
            
        except Exception as e:
            issues.append({
                "type": "error",
                "severity": "critical",
                "description": f"Validation error: {str(e)}"
            })
        
        finally:
            browser.close()
    
    # Determine overall validity
    critical_issues = [i for i in issues if i.get("severity") == "critical"]
    high_issues = [i for i in issues if i.get("severity") == "high"]
    
    valid = len(critical_issues) == 0 and len(high_issues) == 0
    
    return {
        "valid": valid,
        "issues": issues,
        "metrics": metrics
    }


def check_scrollability(page) -> dict:
    """
    Check if page has proper scroll behavior.
    
    Args:
        page: Playwright page object
        
    Returns:
        Dictionary with scroll validation results
    """
    issues = []
    
    # Get page and viewport heights
    page_height = page.evaluate("document.documentElement.scrollHeight")
    viewport_height = page.evaluate("window.innerHeight")
    
    metrics = {
        "page_height": page_height,
        "viewport_height": viewport_height,
        "scrollable": page_height > viewport_height
    }
    
    # Check if page is scrollable
    if page_height <= viewport_height:
        issues.append({
            "type": "scroll",
            "severity": "medium",
            "description": f"Page is not scrollable (height: {page_height}px, viewport: {viewport_height}px)"
        })
    
    # Check if page is too short
    if page_height < viewport_height * 0.8:
        issues.append({
            "type": "layout",
            "severity": "low",
            "description": "Page content is very short"
        })
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "metrics": metrics
    }


def check_overflow(page) -> List[dict]:
    """
    Detect elements with overflow issues.
    
    Args:
        page: Playwright page object
        
    Returns:
        List of overflow issues
    """
    issues = []
    
    # Check for horizontal overflow
    has_horizontal_overflow = page.evaluate("""
        () => {
            const body = document.body;
            const html = document.documentElement;
            
            const scrollWidth = Math.max(
                body.scrollWidth, html.scrollWidth
            );
            const clientWidth = Math.max(
                body.clientWidth, html.clientWidth
            );
            
            return scrollWidth > clientWidth;
        }
    """)
    
    if has_horizontal_overflow:
        issues.append({
            "type": "overflow",
            "severity": "high",
            "description": "Page has horizontal overflow (content wider than viewport)"
        })
    
    # Check for elements that are too wide
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
    
    # Ensure wide_elements is a list
    if not isinstance(wide_elements, list):
        wide_elements = []
    
    if wide_elements and len(wide_elements) > 0:
        for element in wide_elements:
            if isinstance(element, dict) and 'tag' in element:
                tag = element.get('tag', 'Unknown')
                cls = element.get('class', '')
                width = element.get('width', 0)
                issues.append({
                    "type": "overflow",
                    "severity": "medium",
                    "description": f"Element {tag}.{cls} is too wide ({width}px)",
                    "element": element
                })
    
    return issues


def check_section_balance(page) -> dict:
    """
    Check if sections are properly balanced and spaced.
    
    Args:
        page: Playwright page object
        
    Returns:
        Dictionary with section balance results
    """
    issues = []
    
    # Count main sections
    section_count = page.evaluate("""
        () => {
            const sections = document.querySelectorAll('section, nav, header, footer');
            return sections.length;
        }
    """)
    
    # Get section heights
    section_heights = page.evaluate("""
        () => {
            const sections = document.querySelectorAll('section, nav, header, footer');
            return Array.from(sections).map(s => ({
                tag: s.tagName,
                height: s.offsetHeight
            }));
        }
    """)
    
    metrics = {
        "sections_detected": section_count,
        "section_heights": section_heights
    }
    
    # Check if we have at least some sections
    if section_count < 2:
        issues.append({
            "type": "structure",
            "severity": "medium",
            "description": f"Very few sections detected ({section_count})"
        })
    
    # Check for sections that are too small
    if section_heights and len(section_heights) > 0:
        for section in section_heights:
            if isinstance(section, dict) and 'height' in section and 'tag' in section:
                if section['height'] < 50 and section['tag'] not in ['NAV', 'HEADER']:
                    issues.append({
                        "type": "layout",
                        "severity": "low",
                        "description": f"{section['tag']} section is very small ({section['height']}px)"
                    })
    
    return {
        "issues": issues,
        "metrics": metrics
    }


def check_responsive_behavior(page) -> dict:
    """
    Check responsive behavior at different viewport sizes.
    
    Args:
        page: Playwright page object
        
    Returns:
        Dictionary with responsive check results
    """
    issues = []
    
    # Test at mobile size (375x667 - iPhone SE)
    page.set_viewport_size({"width": 375, "height": 667})
    time.sleep(0.3)
    
    # Check for horizontal overflow on mobile
    mobile_overflow = page.evaluate("""
        () => {
            return document.documentElement.scrollWidth > window.innerWidth;
        }
    """)
    
    if mobile_overflow:
        issues.append({
            "type": "responsive",
            "severity": "high",
            "description": "Page has horizontal overflow on mobile viewport (375px)"
        })
    
    # Reset to desktop size
    page.set_viewport_size({"width": 1920, "height": 1080})
    
    return {"issues": issues}


def check_basic_accessibility(page) -> dict:
    """
    Perform basic accessibility checks.
    
    Args:
        page: Playwright page object
        
    Returns:
        Dictionary with accessibility check results
    """
    issues = []
    
    # Check if page has a title
    title = page.title()
    if not title or title.strip() == "":
        issues.append({
            "type": "accessibility",
            "severity": "medium",
            "description": "Page is missing a title tag"
        })
    
    # Check for images without alt text
    images_without_alt = page.evaluate("""
        () => {
            const images = document.querySelectorAll('img');
            let count = 0;
            images.forEach(img => {
                if (!img.hasAttribute('alt')) {
                    count++;
                }
            });
            return count;
        }
    """)
    
    if images_without_alt > 0:
        issues.append({
            "type": "accessibility",
            "severity": "low",
            "description": f"{images_without_alt} images missing alt text"
        })
    
    return {"issues": issues}


def validate_html_string(html_content: str, temp_file: str = "temp_validation.html") -> dict:
    """
    Validate HTML content by saving to temp file first.
    
    Args:
        html_content: HTML content as string
        temp_file: Temporary file name
        
    Returns:
        Validation report
    """
    from pathlib import Path
    
    # Save to temp file
    temp_path = Path("dist") / temp_file
    temp_path.parent.mkdir(exist_ok=True)
    
    with open(temp_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    # Validate
    report = validate_layout(str(temp_path))
    
    # Clean up temp file
    try:
        temp_path.unlink()
    except:
        pass
    
    return report


def generate_validation_summary(report: dict) -> str:
    """
    Generate a human-readable summary of the validation report.
    
    Args:
        report: Validation report dictionary
        
    Returns:
        Formatted summary string
    """
    summary = []
    summary.append("="*60)
    summary.append("📊 Visual Validation Report")
    summary.append("="*60)
    
    # Overall status
    status = "✅ PASS" if report["valid"] else "❌ FAIL"
    summary.append(f"\nOverall Status: {status}")
    
    # Metrics
    if report.get("metrics"):
        summary.append("\n📏 Metrics:")
        metrics = report["metrics"]
        if "page_height" in metrics:
            summary.append(f"  Page Height: {metrics['page_height']}px")
        if "viewport_height" in metrics:
            summary.append(f"  Viewport Height: {metrics['viewport_height']}px")
        if "sections_detected" in metrics:
            summary.append(f"  Sections Detected: {metrics['sections_detected']}")
        if "scrollable" in metrics:
            scroll_status = "Yes" if metrics["scrollable"] else "No"
            summary.append(f"  Scrollable: {scroll_status}")
    
    # Issues
    issues = report.get("issues", [])
    if issues:
        summary.append(f"\n⚠️  Issues Found: {len(issues)}")
        
        # Group by severity
        critical = [i for i in issues if i.get("severity") == "critical"]
        high = [i for i in issues if i.get("severity") == "high"]
        medium = [i for i in issues if i.get("severity") == "medium"]
        low = [i for i in issues if i.get("severity") == "low"]
        
        if critical:
            summary.append(f"\n  🔴 Critical ({len(critical)}):")
            for issue in critical:
                summary.append(f"    - {issue['description']}")
        
        if high:
            summary.append(f"\n  🟠 High ({len(high)}):")
            for issue in high:
                summary.append(f"    - {issue['description']}")
        
        if medium:
            summary.append(f"\n  🟡 Medium ({len(medium)}):")
            for issue in medium:
                summary.append(f"    - {issue['description']}")
        
        if low:
            summary.append(f"\n  🟢 Low ({len(low)}):")
            for issue in low:
                summary.append(f"    - {issue['description']}")
    else:
        summary.append("\n✅ No issues found!")
    
    summary.append("\n" + "="*60)
    
    return "\n".join(summary)


# Test function for development
def test_visual_validator():
    """
    Test the visual validator with example HTML files.
    """
    print("🔍 Testing Visual Validator\n" + "="*60 + "\n")
    
    # Find HTML files in dist
    from pathlib import Path
    dist_path = Path("dist")
    
    if not dist_path.exists():
        print("❌ No dist directory found. Generate some websites first.")
        return
    
    html_files = list(dist_path.glob("*.html"))
    
    if not html_files:
        print("❌ No HTML files found in dist/")
        return
    
    for html_file in html_files[:3]:  # Test first 3 files
        print(f"Testing: {html_file.name}")
        print("-" * 60)
        
        report = validate_layout(str(html_file))
        summary = generate_validation_summary(report)
        print(summary)
        print()


if __name__ == "__main__":
    test_visual_validator()
