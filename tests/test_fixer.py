"""
Tests for Fixer Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.fixer import (
    analyze_issues,
    apply_fixes,
    auto_fix_website,
    fix_from_file,
    generate_fix_summary,
    apply_min_height_fix,
    apply_overflow_fix,
    apply_viewport_meta_fix,
    apply_title_fix,
    apply_alt_text_fix
)
from bs4 import BeautifulSoup
from pathlib import Path


def test_1_analyze_scroll_issues():
    """Test analyzing scroll-related issues"""
    print("Test 1: Analyze scroll issues...")
    
    report = {
        "issues": [
            {"type": "scroll", "severity": "medium", "description": "Page not scrollable"}
        ]
    }
    
    actions = analyze_issues(report)
    
    assert len(actions) > 0
    assert any(a["type"] == "add_min_height" for a in actions)
    
    print("✅ PASS")


def test_2_analyze_overflow_issues():
    """Test analyzing overflow issues"""
    print("\nTest 2: Analyze overflow issues...")
    
    report = {
        "issues": [
            {"type": "overflow", "severity": "high", "description": "horizontal overflow detected"}
        ]
    }
    
    actions = analyze_issues(report)
    
    assert len(actions) > 0
    assert any(a["type"] == "fix_horizontal_overflow" for a in actions)
    
    print("✅ PASS")


def test_3_analyze_accessibility_issues():
    """Test analyzing accessibility issues"""
    print("\nTest 3: Analyze accessibility issues...")
    
    report = {
        "issues": [
            {"type": "accessibility", "severity": "medium", "description": "Missing title tag"},
            {"type": "accessibility", "severity": "low", "description": "Images missing alt text"}
        ]
    }
    
    actions = analyze_issues(report)
    
    assert len(actions) >= 2
    assert any(a["type"] == "add_title" for a in actions)
    assert any(a["type"] == "add_alt_text" for a in actions)
    
    print("✅ PASS")


def test_4_apply_title_fix():
    """Test adding title tag"""
    print("\nTest 4: Apply title fix...")
    
    html = "<html><head></head><body>Test</body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    
    result = apply_title_fix(soup, "Test Title")
    
    assert result == True
    assert soup.find("title") is not None
    assert soup.find("title").string == "Test Title"
    
    print("✅ PASS")


def test_5_apply_alt_text_fix():
    """Test adding alt text to images"""
    print("\nTest 5: Apply alt text fix...")
    
    html = """
    <html>
    <body>
        <img src="test1.jpg">
        <img src="test2.png">
        <img src="test3.gif" alt="Existing">
    </body>
    </html>
    """
    soup = BeautifulSoup(html, 'html.parser')
    
    count = apply_alt_text_fix(soup)
    
    assert count == 2  # Only 2 images without alt
    
    images = soup.find_all("img")
    for img in images:
        assert img.get("alt") is not None
    
    print("✅ PASS")


def test_6_apply_viewport_meta_fix():
    """Test adding viewport meta tag"""
    print("\nTest 6: Apply viewport meta fix...")
    
    html = "<html><head></head><body>Test</body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    
    result = apply_viewport_meta_fix(soup)
    
    assert result == True
    
    viewport = soup.find("meta", attrs={"name": "viewport"})
    assert viewport is not None
    assert "width=device-width" in viewport.get("content", "")
    
    print("✅ PASS")


def test_7_apply_overflow_fix():
    """Test applying overflow fix"""
    print("\nTest 7: Apply overflow fix...")
    
    html = "<html><head></head><body>Test</body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    
    result = apply_overflow_fix(soup)
    
    assert result == True
    
    style = soup.find("style")
    assert style is not None
    assert "overflow-x: hidden" in style.string
    
    print("✅ PASS")


def test_8_apply_min_height_fix():
    """Test applying min-height fix"""
    print("\nTest 8: Apply min-height fix...")
    
    html = "<html><head></head><body>Test</body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    
    action = {"target": "body", "value": "100vh"}
    result = apply_min_height_fix(soup, action)
    
    assert result == True
    
    style = soup.find("style")
    assert style is not None
    assert "min-height: 100vh" in style.string
    
    print("✅ PASS")


def test_9_apply_multiple_fixes():
    """Test applying multiple fixes at once"""
    print("\nTest 9: Apply multiple fixes...")
    
    html = """
    <html>
    <head></head>
    <body>
        <h1>Test</h1>
        <img src="test.jpg">
    </body>
    </html>
    """
    
    fix_actions = [
        {"type": "add_title", "value": "Test Page"},
        {"type": "add_viewport_meta"},
        {"type": "add_alt_text"},
        {"type": "fix_horizontal_overflow"}
    ]
    
    fixed_html, applied = apply_fixes(html, fix_actions)
    
    assert len(applied) > 0
    assert "title" in fixed_html.lower()
    assert "viewport" in fixed_html.lower()
    assert "alt=" in fixed_html.lower()
    
    print("✅ PASS")


def test_10_auto_fix_problematic_html():
    """Test auto-fixing problematic HTML"""
    print("\nTest 10: Auto-fix problematic HTML...")
    
    problematic_html = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <h1>Test</h1>
        <img src="test.jpg">
    </body>
    </html>
    """
    
    fixed_html, fix_report = auto_fix_website(problematic_html, max_attempts=2)
    
    assert fix_report["attempts"] > 0
    assert len(fix_report["fixes_applied"]) > 0
    assert fixed_html != problematic_html
    
    # Check that fixes were applied
    assert "<title>" in fixed_html
    assert 'alt="' in fixed_html
    
    print("✅ PASS")


def test_11_fix_report_structure():
    """Test fix report structure"""
    print("\nTest 11: Fix report structure...")
    
    html = "<html><head></head><body>Test</body></html>"
    
    _, fix_report = auto_fix_website(html, max_attempts=1)
    
    assert "attempts" in fix_report
    assert "fixes_applied" in fix_report
    assert "initial_issues" in fix_report
    assert "final_issues" in fix_report
    assert "success" in fix_report
    
    assert isinstance(fix_report["attempts"], int)
    assert isinstance(fix_report["fixes_applied"], list)
    assert isinstance(fix_report["success"], bool)
    
    print("✅ PASS")


def test_12_generate_fix_summary():
    """Test generating fix summary"""
    print("\nTest 12: Generate fix summary...")
    
    fix_report = {
        "attempts": 2,
        "fixes_applied": ["Added title", "Fixed overflow"],
        "initial_issues": 5,
        "final_issues": 2,
        "success": True
    }
    
    summary = generate_fix_summary(fix_report)
    
    assert "Auto-Fix Report" in summary
    assert "SUCCESS" in summary
    assert "Fix Attempts: 2" in summary
    assert "Added title" in summary
    
    print("✅ PASS")


def test_13_priority_sorting():
    """Test that fixes are sorted by priority"""
    print("\nTest 13: Priority sorting...")
    
    report = {
        "issues": [
            {"type": "accessibility", "severity": "low", "description": "alt text"},
            {"type": "overflow", "severity": "high", "description": "horizontal overflow"},
            {"type": "responsive", "severity": "high", "description": "mobile issues"}
        ]
    }
    
    actions = analyze_issues(report)
    
    # High priority fixes should come first
    assert len(actions) > 0
    # First action should be high priority (responsive or overflow)
    assert actions[0]["priority"] <= 2
    
    print("✅ PASS")


def test_14_idempotent_fixes():
    """Test that applying fixes twice doesn't duplicate"""
    print("\nTest 14: Idempotent fixes...")
    
    html = "<html><head><title>Test</title></head><body>Test</body></html>"
    soup = BeautifulSoup(html, 'html.parser')
    
    # Apply title fix twice
    result1 = apply_title_fix(soup, "New Title")
    result2 = apply_title_fix(soup, "New Title")
    
    # First should succeed, second should return False (already exists)
    assert result1 == False  # Title already exists
    assert result2 == False
    
    # Check there's only one title
    titles = soup.find_all("title")
    assert len(titles) == 1
    
    print("✅ PASS")


def test_15_fix_from_file():
    """Test fixing HTML from file"""
    print("\nTest 15: Fix from file...")
    
    # Create a test HTML file
    test_html = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <h1>Test Page</h1>
        <img src="test.jpg">
    </body>
    </html>
    """
    
    test_file = Path("dist/test_fixer_input.html")
    test_file.parent.mkdir(exist_ok=True)
    
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_html)
    
    # Fix the file
    fix_report = fix_from_file(str(test_file), max_attempts=2)
    
    assert "output_path" in fix_report
    assert Path(fix_report["output_path"]).exists()
    
    # Read fixed file
    with open(fix_report["output_path"], 'r', encoding='utf-8') as f:
        fixed_content = f.read()
    
    assert "<title>" in fixed_content
    assert 'alt="' in fixed_content
    
    # Cleanup
    test_file.unlink()
    Path(fix_report["output_path"]).unlink()
    
    print("✅ PASS")


def run_all_tests():
    """Run all fixer tests"""
    print("\n" + "="*70)
    print("🧪 FIXER MODULE TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        test_1_analyze_scroll_issues,
        test_2_analyze_overflow_issues,
        test_3_analyze_accessibility_issues,
        test_4_apply_title_fix,
        test_5_apply_alt_text_fix,
        test_6_apply_viewport_meta_fix,
        test_7_apply_overflow_fix,
        test_8_apply_min_height_fix,
        test_9_apply_multiple_fixes,
        test_10_auto_fix_problematic_html,
        test_11_fix_report_structure,
        test_12_generate_fix_summary,
        test_13_priority_sorting,
        test_14_idempotent_fixes,
        test_15_fix_from_file,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print(f"📊 RESULTS: {passed}/{passed+failed} tests passed")
    print("="*70 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    exit(0 if failed == 0 else 1)
