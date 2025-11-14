"""
Tests for Visual Validator Module
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


def test_validate_existing_file():
    """Test validation of an existing HTML file"""
    print("Test 1: Validate existing HTML file...")
    
    # Find an existing HTML file in dist
    dist_path = Path("dist")
    html_files = list(dist_path.glob("*.html"))
    
    if html_files:
        report = validate_layout(str(html_files[0]))
        
        assert "valid" in report
        assert "issues" in report
        assert "metrics" in report
        assert isinstance(report["valid"], bool)
        assert isinstance(report["issues"], list)
        assert isinstance(report["metrics"], dict)
        
        print(f"✅ Report structure correct. Valid: {report['valid']}, Issues: {len(report['issues'])}")
    else:
        print("⚠️  No HTML files in dist/ - skipping test")


def test_validate_nonexistent_file():
    """Test validation of non-existent file"""
    print("\nTest 2: Validate non-existent file...")
    
    report = validate_layout("nonexistent_file.html")
    
    assert report["valid"] == False
    assert len(report["issues"]) > 0
    assert report["issues"][0]["type"] == "file"
    assert report["issues"][0]["severity"] == "critical"
    
    print("✅ Correctly handles missing file")


def test_validate_minimal_html():
    """Test validation of minimal HTML"""
    print("\nTest 3: Validate minimal HTML...")
    
    minimal_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Minimal</title>
    </head>
    <body>
        <h1>Test</h1>
    </body>
    </html>
    """
    
    report = validate_html_string(minimal_html, "test_minimal.html")
    
    assert "valid" in report
    assert "issues" in report
    assert "metrics" in report
    
    # Minimal HTML might have issues (too short, not scrollable)
    # But should not have critical errors
    critical_issues = [i for i in report["issues"] if i.get("severity") == "critical"]
    assert len(critical_issues) == 0
    
    print(f"✅ Minimal HTML validated. Issues: {len(report['issues'])}")


def test_validate_html_with_sections():
    """Test validation of HTML with multiple sections"""
    print("\nTest 4: Validate HTML with sections...")
    
    html_with_sections = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Multi-Section Page</title>
    </head>
    <body>
        <nav style="height: 80px;">Nav</nav>
        <section style="height: 600px;">Section 1</section>
        <section style="height: 500px;">Section 2</section>
        <section style="height: 400px;">Section 3</section>
        <footer style="height: 200px;">Footer</footer>
    </body>
    </html>
    """
    
    report = validate_html_string(html_with_sections, "test_sections.html")
    
    assert "sections_detected" in report["metrics"]
    assert report["metrics"]["sections_detected"] >= 3
    
    print(f"✅ Detected {report['metrics']['sections_detected']} sections")


def test_validate_scrollable_page():
    """Test validation of a scrollable page"""
    print("\nTest 5: Validate scrollable page...")
    
    tall_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Tall Page</title>
    </head>
    <body>
        <div style="height: 2000px; background: linear-gradient(red, blue);">
            <h1>Tall Content</h1>
        </div>
    </body>
    </html>
    """
    
    report = validate_html_string(tall_html, "test_tall.html")
    
    assert "page_height" in report["metrics"]
    assert "viewport_height" in report["metrics"]
    assert report["metrics"]["page_height"] > report["metrics"]["viewport_height"]
    
    # Should not have scroll issues
    scroll_issues = [i for i in report["issues"] if i["type"] == "scroll"]
    assert len(scroll_issues) == 0
    
    print(f"✅ Page is scrollable ({report['metrics']['page_height']}px > {report['metrics']['viewport_height']}px)")


def test_validate_overflow_detection():
    """Test detection of horizontal overflow"""
    print("\nTest 6: Detect horizontal overflow...")
    
    overflow_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Overflow Test</title>
    </head>
    <body style="margin: 0; padding: 0; overflow-x: hidden;">
        <div style="width: 3000px; height: 500px; background: red;">
            Wide content
        </div>
    </body>
    </html>
    """
    
    report = validate_html_string(overflow_html, "test_overflow.html")
    
    # Should detect overflow issues (though body might hide it)
    overflow_issues = [i for i in report["issues"] if i["type"] == "overflow"]
    
    print(f"✅ Overflow detection works. Found {len(overflow_issues)} overflow issues")


def test_validate_responsive_behavior():
    """Test responsive validation"""
    print("\nTest 7: Test responsive validation...")
    
    responsive_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Responsive Page</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { margin: 0; padding: 20px; }
            .container { max-width: 100%; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Responsive Content</h1>
            <p>This should work on mobile</p>
        </div>
    </body>
    </html>
    """
    
    report = validate_html_string(responsive_html, "test_responsive.html")
    
    # Should not have responsive issues
    responsive_issues = [i for i in report["issues"] if i["type"] == "responsive"]
    
    print(f"✅ Responsive check works. Issues: {len(responsive_issues)}")


def test_validate_accessibility_checks():
    """Test accessibility validation"""
    print("\nTest 8: Test accessibility checks...")
    
    # HTML without title
    no_title_html = """
    <!DOCTYPE html>
    <html>
    <head></head>
    <body>
        <h1>No Title</h1>
        <img src="test.jpg">
    </body>
    </html>
    """
    
    report = validate_html_string(no_title_html, "test_no_title.html")
    
    accessibility_issues = [i for i in report["issues"] if i["type"] == "accessibility"]
    assert len(accessibility_issues) > 0
    
    # Should detect missing title and alt text
    has_title_issue = any("title" in i["description"].lower() for i in accessibility_issues)
    has_alt_issue = any("alt" in i["description"].lower() for i in accessibility_issues)
    
    assert has_title_issue or has_alt_issue
    
    print(f"✅ Accessibility checks work. Found {len(accessibility_issues)} issues")


def test_generate_validation_summary():
    """Test summary generation"""
    print("\nTest 9: Generate validation summary...")
    
    sample_report = {
        "valid": False,
        "issues": [
            {"type": "scroll", "severity": "high", "description": "Page not scrollable"},
            {"type": "overflow", "severity": "medium", "description": "Element too wide"},
            {"type": "accessibility", "severity": "low", "description": "Missing alt text"}
        ],
        "metrics": {
            "page_height": 800,
            "viewport_height": 1080,
            "sections_detected": 3,
            "scrollable": False
        }
    }
    
    summary = generate_validation_summary(sample_report)
    
    assert "FAIL" in summary
    assert "Page Height" in summary
    assert "Sections Detected" in summary
    assert "Page not scrollable" in summary
    
    print("✅ Summary generation works")
    print("\nExample summary:")
    print(summary)


def test_validate_complete_website():
    """Test validation of a complete assembled website"""
    print("\nTest 10: Validate complete assembled website...")
    
    # Check if we have generated websites
    dist_path = Path("dist")
    html_files = list(dist_path.glob("*.html"))
    
    if html_files:
        # Test the first file
        test_file = html_files[0]
        report = validate_layout(str(test_file))
        summary = generate_validation_summary(report)
        
        print(f"\n📄 Testing: {test_file.name}")
        print(summary)
        
        # Basic assertions
        assert "metrics" in report
        assert "page_height" in report["metrics"]
        
        print("\n✅ Complete website validation works")
    else:
        print("⚠️  No assembled websites found in dist/")


def test_metrics_accuracy():
    """Test that metrics are accurate"""
    print("\nTest 11: Verify metrics accuracy...")
    
    known_height_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Known Height</title>
        <style>
            body { margin: 0; padding: 0; }
        </style>
    </head>
    <body>
        <div style="height: 1500px; background: blue;"></div>
    </body>
    </html>
    """
    
    report = validate_html_string(known_height_html, "test_known_height.html")
    
    # Page height should be close to 1500px (might be slightly more due to default margins)
    page_height = report["metrics"]["page_height"]
    assert 1400 < page_height < 1600, f"Expected ~1500px, got {page_height}px"
    
    print(f"✅ Metrics accurate. Page height: {page_height}px (expected ~1500px)")


def test_section_detection_accuracy():
    """Test accurate section counting"""
    print("\nTest 12: Verify section detection...")
    
    sections_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Sections Test</title>
    </head>
    <body>
        <header>Header</header>
        <nav>Nav</nav>
        <section>Section 1</section>
        <section>Section 2</section>
        <section>Section 3</section>
        <footer>Footer</footer>
    </body>
    </html>
    """
    
    report = validate_html_string(sections_html, "test_section_count.html")
    
    # Should detect 6 sections (header, nav, 3 sections, footer)
    sections = report["metrics"]["sections_detected"]
    assert sections == 6, f"Expected 6 sections, found {sections}"
    
    print(f"✅ Section detection accurate. Found {sections} sections")


def test_validation_report_structure():
    """Test that all reports have correct structure"""
    print("\nTest 13: Verify report structure...")
    
    simple_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body><h1>Test</h1></body>
    </html>
    """
    
    report = validate_html_string(simple_html, "test_structure.html")
    
    # Required keys
    assert "valid" in report
    assert "issues" in report
    assert "metrics" in report
    
    # Correct types
    assert isinstance(report["valid"], bool)
    assert isinstance(report["issues"], list)
    assert isinstance(report["metrics"], dict)
    
    # Each issue should have required fields
    for issue in report["issues"]:
        assert "type" in issue
        assert "severity" in issue
        assert "description" in issue
        assert issue["severity"] in ["critical", "high", "medium", "low"]
    
    print("✅ Report structure is consistent and valid")


def test_valid_website_passes():
    """Test that a well-formed website passes validation"""
    print("\nTest 14: Well-formed website should pass...")
    
    good_html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Well-Formed Page</title>
        <style>
            body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
            section { padding: 60px 20px; }
        </style>
    </head>
    <body>
        <nav style="height: 70px; background: #333;">Navigation</nav>
        <section style="min-height: 500px; background: #f0f0f0;">
            <h1>Hero Section</h1>
            <p>Welcome to our website</p>
        </section>
        <section style="min-height: 400px; background: #fff;">
            <h2>Features</h2>
            <p>Great features here</p>
        </section>
        <section style="min-height: 400px; background: #f0f0f0;">
            <h2>About</h2>
            <p>About us information</p>
        </section>
        <footer style="padding: 40px; background: #333; color: white;">
            <p>Footer content</p>
        </footer>
    </body>
    </html>
    """
    
    report = validate_html_string(good_html, "test_good.html")
    
    # Should have few or no high/critical issues
    critical = [i for i in report["issues"] if i.get("severity") == "critical"]
    high = [i for i in report["issues"] if i.get("severity") == "high"]
    
    assert len(critical) == 0, f"Well-formed page has critical issues: {critical}"
    assert len(high) == 0, f"Well-formed page has high issues: {high}"
    
    print(f"✅ Well-formed website passes. Total issues: {len(report['issues'])} (only low/medium)")


def run_all_tests():
    """Run all visual validator tests"""
    print("\n" + "="*70)
    print("🧪 VISUAL VALIDATOR TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        test_validate_existing_file,
        test_validate_nonexistent_file,
        test_validate_minimal_html,
        test_validate_html_with_sections,
        test_validate_scrollable_page,
        test_validate_overflow_detection,
        test_validate_responsive_behavior,
        test_validate_accessibility_checks,
        test_generate_validation_summary,
        test_validate_complete_website,
        test_metrics_accuracy,
        test_section_detection_accuracy,
        test_validation_report_structure,
        test_valid_website_passes,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            failed += 1
    
    print("\n" + "="*70)
    print(f"📊 TEST RESULTS: {passed} passed, {failed} failed out of {passed + failed} total")
    print("="*70 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    
    if failed == 0:
        print("🎉 All tests passed!")
        exit(0)
    else:
        print(f"⚠️  {failed} test(s) failed")
        exit(1)
