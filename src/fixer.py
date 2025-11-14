"""
Fixer Module
Automatically applies fixes based on validation feedback.

Responsibilities:
- Analyze validation report
- Apply common layout fixes:
  * Remove overflow:hidden if scroll needed
  * Adjust min-heights and margins
  * Fix spacing issues
  * Add missing accessibility attributes
- Re-validate after fixes
- Iterate until valid or max attempts reached

Fix Strategies:
- Scroll issues: Adjust container heights, remove overflow constraints
- Overflow: Add responsive classes, adjust padding/margins, add max-width
- Spacing: Balance section heights, add proper gaps
- Accessibility: Add missing title, alt text
- Responsive: Add viewport meta tag, responsive CSS
"""

import re
from pathlib import Path
from typing import Dict, List, Tuple
from bs4 import BeautifulSoup


def analyze_issues(validation_report: dict) -> List[dict]:
    """
    Analyze validation report and determine fix strategies.
    
    Args:
        validation_report: Report from visual_validator
        
    Returns:
        List of fix actions to apply
    """
    fix_actions = []
    
    for issue in validation_report.get("issues", []):
        issue_type = issue.get("type", "")
        severity = issue.get("severity", "")
        description = issue.get("description", "")
        
        # Analyze and create fix actions based on issue type
        if issue_type == "scroll":
            fix_actions.append({
                "type": "add_min_height",
                "target": "body",
                "value": "100vh",
                "reason": "Ensure page is scrollable",
                "priority": 2
            })
            
        elif issue_type == "overflow":
            if "horizontal" in description.lower():
                fix_actions.append({
                    "type": "fix_horizontal_overflow",
                    "target": "body",
                    "reason": "Prevent horizontal scrolling",
                    "priority": 1
                })
                
        elif issue_type == "responsive":
            fix_actions.append({
                "type": "add_viewport_meta",
                "reason": "Enable responsive behavior",
                "priority": 1
            })
            fix_actions.append({
                "type": "add_responsive_css",
                "reason": "Ensure mobile compatibility",
                "priority": 2
            })
            
        elif issue_type == "accessibility":
            if "title" in description.lower():
                fix_actions.append({
                    "type": "add_title",
                    "value": "Generated Website",
                    "reason": "Add missing page title",
                    "priority": 2
                })
            if "alt" in description.lower():
                fix_actions.append({
                    "type": "add_alt_text",
                    "reason": "Add alt text to images",
                    "priority": 3
                })
                
        elif issue_type == "structure":
            if "few sections" in description.lower():
                fix_actions.append({
                    "type": "verify_structure",
                    "reason": "Check page structure",
                    "priority": 3
                })
    
    # Sort by priority (lower number = higher priority)
    fix_actions.sort(key=lambda x: x.get("priority", 999))
    
    return fix_actions


def apply_fixes(html_content: str, fix_actions: List[dict]) -> Tuple[str, List[str]]:
    """
    Apply fix actions to HTML content.
    
    Args:
        html_content: Original HTML content
        fix_actions: List of fixes to apply
        
    Returns:
        Tuple of (modified HTML content, list of applied fixes)
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    applied_fixes = []
    
    for action in fix_actions:
        action_type = action.get("type", "")
        
        try:
            if action_type == "add_min_height":
                if apply_min_height_fix(soup, action):
                    applied_fixes.append(f"Added min-height to {action['target']}")
                    
            elif action_type == "fix_horizontal_overflow":
                if apply_overflow_fix(soup):
                    applied_fixes.append("Fixed horizontal overflow")
                    
            elif action_type == "add_viewport_meta":
                if apply_viewport_meta_fix(soup):
                    applied_fixes.append("Added viewport meta tag")
                    
            elif action_type == "add_responsive_css":
                if apply_responsive_css_fix(soup):
                    applied_fixes.append("Added responsive CSS")
                    
            elif action_type == "add_title":
                if apply_title_fix(soup, action.get("value", "Website")):
                    applied_fixes.append("Added page title")
                    
            elif action_type == "add_alt_text":
                count = apply_alt_text_fix(soup)
                if count > 0:
                    applied_fixes.append(f"Added alt text to {count} images")
                    
        except Exception as e:
            # Log error but continue with other fixes
            applied_fixes.append(f"Failed to apply {action_type}: {str(e)}")
    
    return str(soup), applied_fixes


def apply_min_height_fix(soup: BeautifulSoup, action: dict) -> bool:
    """Add min-height to target element"""
    target = action.get("target", "body")
    value = action.get("value", "100vh")
    
    # Find or create style tag
    style_tag = soup.find("style")
    if not style_tag:
        style_tag = soup.new_tag("style")
        head = soup.find("head")
        if head:
            head.append(style_tag)
        else:
            return False
    
    # Add min-height rule
    current_style = style_tag.string or ""
    new_rule = f"\n{target} {{ min-height: {value}; }}"
    
    if new_rule not in current_style:
        style_tag.string = current_style + new_rule
        return True
    
    return False


def apply_overflow_fix(soup: BeautifulSoup) -> bool:
    """Fix horizontal overflow issues"""
    # Find or create style tag
    style_tag = soup.find("style")
    if not style_tag:
        style_tag = soup.new_tag("style")
        head = soup.find("head")
        if head:
            head.append(style_tag)
        else:
            return False
    
    # Add overflow prevention CSS
    overflow_css = """
body {
    overflow-x: hidden;
}
* {
    max-width: 100%;
    box-sizing: border-box;
}
img, video, iframe {
    max-width: 100%;
    height: auto;
}
"""
    
    current_style = style_tag.string or ""
    if "overflow-x: hidden" not in current_style:
        style_tag.string = current_style + overflow_css
        return True
    
    return False


def apply_viewport_meta_fix(soup: BeautifulSoup) -> bool:
    """Add viewport meta tag for responsive design"""
    head = soup.find("head")
    if not head:
        return False
    
    # Check if viewport meta already exists
    existing_viewport = head.find("meta", attrs={"name": "viewport"})
    if existing_viewport:
        return False
    
    # Create and add viewport meta tag
    viewport_meta = soup.new_tag(
        "meta",
        attrs={
            "name": "viewport",
            "content": "width=device-width, initial-scale=1.0"
        }
    )
    head.insert(0, viewport_meta)
    return True


def apply_responsive_css_fix(soup: BeautifulSoup) -> bool:
    """Add responsive CSS rules"""
    # Find or create style tag
    style_tag = soup.find("style")
    if not style_tag:
        style_tag = soup.new_tag("style")
        head = soup.find("head")
        if head:
            head.append(style_tag)
        else:
            return False
    
    # Add responsive CSS
    responsive_css = """
@media (max-width: 768px) {
    body {
        padding: 10px;
    }
    section {
        padding: 30px 15px !important;
    }
    h1 {
        font-size: 1.8rem !important;
    }
    h2 {
        font-size: 1.5rem !important;
    }
}
"""
    
    current_style = style_tag.string or ""
    if "@media" not in current_style:
        style_tag.string = current_style + responsive_css
        return True
    
    return False


def apply_title_fix(soup: BeautifulSoup, title: str) -> bool:
    """Add or update page title"""
    head = soup.find("head")
    if not head:
        # Create head if it doesn't exist
        head = soup.new_tag("head")
        if soup.html:
            soup.html.insert(0, head)
        else:
            return False
    
    # Check if title exists
    title_tag = head.find("title")
    if title_tag:
        # Update existing title if it's empty
        if not title_tag.string or title_tag.string.strip() == "":
            title_tag.string = title
            return True
        return False
    else:
        # Create new title tag
        title_tag = soup.new_tag("title")
        title_tag.string = title
        head.insert(0, title_tag)
        return True


def apply_alt_text_fix(soup: BeautifulSoup) -> int:
    """Add alt text to images that don't have it"""
    count = 0
    images = soup.find_all("img")
    
    for img in images:
        if not img.get("alt"):
            # Generate alt text based on src or use generic
            src = img.get("src", "")
            if src:
                # Extract filename without extension
                alt_text = Path(src).stem.replace("-", " ").replace("_", " ").title()
            else:
                alt_text = "Image"
            
            img["alt"] = alt_text
            count += 1
    
    return count


def auto_fix_website(html_content: str, validation_report: dict = None, max_attempts: int = 3) -> Tuple[str, dict]:
    """
    Automatically fix website based on validation issues.
    
    Args:
        html_content: HTML content to fix
        validation_report: Validation report with issues (optional - will validate if not provided)
        max_attempts: Maximum fix iterations
        
    Returns:
        Tuple of (fixed HTML content, fix report)
    """
    from src.visual_validator import validate_html_string
    
    fix_report = {
        "attempts": 0,
        "fixes_applied": [],
        "initial_issues": 0,
        "final_issues": 0,
        "success": False
    }
    
    current_html = html_content
    
    # Get initial validation if not provided
    if validation_report is None:
        validation_report = validate_html_string(current_html, f"fix_attempt_0.html")
    
    fix_report["initial_issues"] = len(validation_report.get("issues", []))
    
    # Iterate fix attempts
    for attempt in range(max_attempts):
        fix_report["attempts"] = attempt + 1
        
        # Analyze issues and get fix actions
        fix_actions = analyze_issues(validation_report)
        
        if not fix_actions:
            # No more fixes to apply
            break
        
        # Apply fixes
        current_html, applied = apply_fixes(current_html, fix_actions)
        fix_report["fixes_applied"].extend(applied)
        
        # Re-validate
        validation_report = validate_html_string(current_html, f"fix_attempt_{attempt + 1}.html")
        
        # Check if we've fixed critical/high issues
        critical_high_issues = [
            i for i in validation_report.get("issues", [])
            if i.get("severity") in ["critical", "high"]
        ]
        
        if len(critical_high_issues) == 0:
            fix_report["success"] = True
            break
    
    fix_report["final_issues"] = len(validation_report.get("issues", []))
    
    return current_html, fix_report


def fix_from_file(html_path: str, output_path: str = None, max_attempts: int = 3) -> dict:
    """
    Fix HTML file and save the result.
    
    Args:
        html_path: Path to HTML file to fix
        output_path: Path to save fixed HTML (defaults to original with _fixed suffix)
        max_attempts: Maximum fix iterations
        
    Returns:
        Fix report dictionary
    """
    # Read original HTML
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Apply fixes
    fixed_html, fix_report = auto_fix_website(html_content, max_attempts=max_attempts)
    
    # Determine output path
    if output_path is None:
        path = Path(html_path)
        output_path = path.parent / f"{path.stem}_fixed{path.suffix}"
    
    # Save fixed HTML
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(fixed_html)
    
    fix_report["output_path"] = str(output_path)
    
    return fix_report


def generate_fix_summary(fix_report: dict) -> str:
    """
    Generate human-readable fix summary.
    
    Args:
        fix_report: Fix report from auto_fix_website
        
    Returns:
        Formatted summary string
    """
    summary = []
    summary.append("="*60)
    summary.append("🔧 Auto-Fix Report")
    summary.append("="*60)
    
    # Status
    status = "✅ SUCCESS" if fix_report["success"] else "⚠️  PARTIAL"
    summary.append(f"\nStatus: {status}")
    
    # Attempts
    summary.append(f"Fix Attempts: {fix_report['attempts']}")
    
    # Issues
    initial = fix_report["initial_issues"]
    final = fix_report["final_issues"]
    fixed = initial - final
    
    summary.append(f"\nInitial Issues: {initial}")
    summary.append(f"Final Issues: {final}")
    summary.append(f"Issues Fixed: {fixed}")
    
    # Fixes applied
    if fix_report["fixes_applied"]:
        summary.append(f"\n🔨 Fixes Applied ({len(fix_report['fixes_applied'])}):")
        for fix in fix_report["fixes_applied"]:
            summary.append(f"  ✓ {fix}")
    else:
        summary.append("\n✓ No fixes needed")
    
    # Output file
    if "output_path" in fix_report:
        summary.append(f"\n📄 Saved to: {fix_report['output_path']}")
    
    summary.append("\n" + "="*60)
    
    return "\n".join(summary)


# Test function for development
def test_fixer():
    """Test the fixer with sample HTML"""
    print("🔧 Testing Auto-Fixer\n" + "="*60 + "\n")
    
    # Sample HTML with issues
    problematic_html = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <h1>Test Page</h1>
        <img src="test.jpg">
        <div style="width: 3000px;">Wide content</div>
    </body>
    </html>
    """
    
    print("Fixing problematic HTML...")
    fixed_html, fix_report = auto_fix_website(problematic_html, max_attempts=2)
    
    print(generate_fix_summary(fix_report))
    
    # Test with existing files
    from pathlib import Path
    dist_path = Path("dist")
    html_files = list(dist_path.glob("*.html"))
    
    if html_files:
        test_file = html_files[0]
        print(f"\n\nTesting with: {test_file.name}")
        print("-" * 60)
        
        report = fix_from_file(str(test_file), max_attempts=2)
        print(generate_fix_summary(report))


if __name__ == "__main__":
    test_fixer()
