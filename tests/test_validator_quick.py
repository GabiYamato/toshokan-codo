"""
Streamlined Tests for Visual Validator Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.visual_validator import (
    validate_layout,
    validate_html_string,
    generate_validation_summary
)
from pathlib import Path


def test_1_validate_nonexistent_file():
    """Test validation of non-existent file"""
    print("Test 1: Validate non-existent file...")
    
    report = validate_layout("nonexistent_file.html")
    
    assert report["valid"] == False
    assert len(report["issues"]) > 0
    assert report["issues"][0]["type"] == "file"
    assert report["issues"][0]["severity"] == "critical"
    
    print("✅ PASS")


def test_2_validate_minimal_html():
    """Test validation of minimal HTML"""
    print("\nTest 2: Validate minimal HTML...")
    
    minimal_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Minimal</title></head>
    <body><h1>Test</h1></body>
    </html>
    """
    
    report = validate_html_string(minimal_html, "test_minimal.html")
    
    assert "valid" in report
    assert "issues" in report
    assert "metrics" in report
    
    critical_issues = [i for i in report["issues"] if i.get("severity") == "critical"]
    assert len(critical_issues) == 0
    
    print("✅ PASS")


def test_3_validate_scrollable_page():
    """Test validation of a scrollable page"""
    print("\nTest 3: Validate scrollable page...")
    
    tall_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Tall Page</title></head>
    <body>
        <div style="height: 2000px;"><h1>Tall Content</h1></div>
    </body>
    </html>
    """
    
    report = validate_html_string(tall_html, "test_tall.html")
    
    assert "page_height" in report["metrics"]
    assert "viewport_height" in report["metrics"]
    assert report["metrics"]["page_height"] > report["metrics"]["viewport_height"]
    
    print("✅ PASS")


def test_4_section_detection():
    """Test section detection"""
    print("\nTest 4: Section detection...")
    
    sections_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Sections</title></head>
    <body>
        <header>Header</header>
        <section>Section 1</section>
        <section>Section 2</section>
        <footer>Footer</footer>
    </body>
    </html>
    """
    
    report = validate_html_string(sections_html, "test_sections.html")
    
    assert "sections_detected" in report["metrics"]
    assert report["metrics"]["sections_detected"] >= 3
    
    print("✅ PASS")


def test_5_generate_summary():
    """Test summary generation"""
    print("\nTest 5: Generate summary...")
    
    sample_report = {
        "valid": False,
        "issues": [
            {"type": "scroll", "severity": "high", "description": "Page not scrollable"}
        ],
        "metrics": {
            "page_height": 800,
            "viewport_height": 1080,
            "sections_detected": 3
        }
    }
    
    summary = generate_validation_summary(sample_report)
    
    assert "FAIL" in summary
    assert "Page Height" in summary
    
    print("✅ PASS")


def test_6_report_structure():
    """Test report structure"""
    print("\nTest 6: Report structure...")
    
    simple_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body><h1>Test</h1></body>
    </html>
    """
    
    report = validate_html_string(simple_html, "test_struct.html")
    
    assert "valid" in report
    assert "issues" in report
    assert "metrics" in report
    assert isinstance(report["valid"], bool)
    assert isinstance(report["issues"], list)
    assert isinstance(report["metrics"], dict)
    
    for issue in report["issues"]:
        assert "type" in issue
        assert "severity" in issue
        assert "description" in issue
    
    print("✅ PASS")


def test_7_well_formed_website():
    """Test that a well-formed website passes"""
    print("\nTest 7: Well-formed website...")
    
    good_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Well-Formed</title>
        <style>body { margin: 0; } section { padding: 60px 20px; }</style>
    </head>
    <body>
        <nav style="height: 70px;">Nav</nav>
        <section style="min-height: 500px;"><h1>Hero</h1></section>
        <section style="min-height: 400px;"><h2>Features</h2></section>
        <footer style="padding: 40px;"><p>Footer</p></footer>
    </body>
    </html>
    """
    
    report = validate_html_string(good_html, "test_good.html")
    
    critical = [i for i in report["issues"] if i.get("severity") == "critical"]
    high = [i for i in report["issues"] if i.get("severity") == "high"]
    
    assert len(critical) == 0
    assert len(high) == 0
    
    print("✅ PASS")


def test_8_validate_existing_file():
    """Test validation of existing HTML files"""
    print("\nTest 8: Validate existing files...")
    
    dist_path = Path("dist")
    html_files = list(dist_path.glob("*.html"))
    
    if html_files:
        report = validate_layout(str(html_files[0]))
        
        assert "valid" in report
        assert "issues" in report
        assert "metrics" in report
        
        print(f"✅ PASS - Validated {html_files[0].name}")
    else:
        print("⚠️  SKIP - No HTML files in dist/")


def run_tests():
    """Run all tests"""
    print("\n" + "="*70)
    print("🧪 VISUAL VALIDATOR - STREAMLINED TEST SUITE")
    print("="*70)
    
    tests = [
        test_1_validate_nonexistent_file,
        test_2_validate_minimal_html,
        test_3_validate_scrollable_page,
        test_4_section_detection,
        test_5_generate_summary,
        test_6_report_structure,
        test_7_well_formed_website,
        test_8_validate_existing_file,
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
            failed += 1
    
    print("\n" + "="*70)
    print(f"📊 RESULTS: {passed}/{passed+failed} tests passed")
    print("="*70 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_tests()
    exit(0 if failed == 0 else 1)
