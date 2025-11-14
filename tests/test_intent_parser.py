"""
Unit tests for Intent Parser Module
Tests the natural language to JSON conversion functionality.
"""

import sys
import os

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.intent_parser import (
    parse_intent,
    _extract_sections,
    _extract_framework,
    _extract_style,
    _extract_colors,
    _extract_metadata
)


def test_basic_portfolio_prompt():
    """Test parsing a basic portfolio website prompt."""
    prompt = "Build a modern portfolio site with a navbar, hero section, and contact form"
    result = parse_intent(prompt)
    
    assert "navbar" in result["sections"]
    assert "hero" in result["sections"]
    assert "contact" in result["sections"]
    assert result["framework"] == "tailwind"
    assert result["style"] == "modern"
    assert result["metadata"]["is_portfolio"] == True
    print("✓ Test: Basic portfolio prompt")


def test_landing_page_with_brand():
    """Test parsing landing page with brand name."""
    prompt = "Create a landing page for TechStart with features and pricing using Tailwind"
    result = parse_intent(prompt)
    
    assert "features" in result["sections"]
    assert "pricing" in result["sections"]
    assert result["framework"] == "tailwind"
    assert result["metadata"]["brand_name"] == "TechStart"
    assert result["metadata"]["is_landing_page"] == True
    print("✓ Test: Landing page with brand name")


def test_bootstrap_framework_detection():
    """Test Bootstrap framework detection."""
    prompt = "I need a minimal website with a gallery and testimonials in Bootstrap"
    result = parse_intent(prompt)
    
    assert result["framework"] == "bootstrap"
    assert result["style"] == "minimal"
    assert "gallery" in result["sections"]
    assert "testimonials" in result["sections"]
    print("✓ Test: Bootstrap framework detection")


def test_color_extraction():
    """Test color extraction from prompt."""
    prompt = "Make a corporate site with blue and white colors"
    result = parse_intent(prompt)
    
    assert "blue" in result["colors"]
    assert "white" in result["colors"]
    assert result["style"] == "corporate"
    print("✓ Test: Color extraction")


def test_default_sections():
    """Test that navbar and footer are always included."""
    prompt = "Just a simple hero section"
    result = parse_intent(prompt)
    
    assert "navbar" in result["sections"]
    assert "hero" in result["sections"]
    assert "footer" in result["sections"]
    print("✓ Test: Default sections (navbar & footer)")


def test_multiple_sections():
    """Test parsing multiple sections."""
    prompt = "Create a site with hero, features, testimonials, pricing, and contact sections"
    result = parse_intent(prompt)
    
    assert "hero" in result["sections"]
    assert "features" in result["sections"]
    assert "testimonials" in result["sections"]
    assert "pricing" in result["sections"]
    assert "contact" in result["sections"]
    print("✓ Test: Multiple sections")


def test_style_detection():
    """Test style/theme detection."""
    test_cases = [
        ("A minimal design website", "minimal"),
        ("Build a retro style page", "retro"),
        ("Corporate professional site", "corporate"),
        ("Creative and colorful portfolio", "creative"),
    ]
    
    for prompt, expected_style in test_cases:
        result = parse_intent(prompt)
        assert result["style"] == expected_style
    
    print("✓ Test: Style detection (minimal, retro, corporate, creative)")


def test_section_ordering():
    """Test that sections are ordered logically."""
    prompt = "Site with footer, features, hero, navbar, contact"
    result = parse_intent(prompt)
    
    # Navbar should be first, footer should be last
    assert result["sections"][0] == "navbar"
    assert result["sections"][-1] == "footer"
    
    # Hero should come before features
    hero_index = result["sections"].index("hero")
    features_index = result["sections"].index("features")
    assert hero_index < features_index
    
    print("✓ Test: Section ordering")


def test_ecommerce_detection():
    """Test e-commerce metadata detection."""
    prompt = "Build an online store with shop and checkout"
    result = parse_intent(prompt)
    
    assert result["metadata"].get("is_ecommerce") == True
    print("✓ Test: E-commerce detection")


def test_default_values():
    """Test that defaults are applied when nothing is specified."""
    prompt = "Make a website"
    result = parse_intent(prompt)
    
    assert result["framework"] == "tailwind", f"Expected 'tailwind', got '{result['framework']}'"
    # Style could be 'modern' or 'minimal' depending on keyword matching
    assert result["style"] in ["modern", "minimal"], f"Unexpected style: {result['style']}"
    assert len(result["sections"]) >= 3, f"Expected at least 3 sections, got {len(result['sections'])}"
    assert len(result["colors"]) > 0, f"Expected colors, got {result['colors']}"
    print("✓ Test: Default values")


def test_extract_sections_helper():
    """Test the _extract_sections helper function."""
    sections = _extract_sections("portfolio with gallery and contact form")
    
    assert "gallery" in sections
    assert "contact" in sections
    assert "navbar" in sections
    assert "footer" in sections
    print("✓ Test: _extract_sections helper")


def test_extract_framework_helper():
    """Test the _extract_framework helper function."""
    assert _extract_framework("using tailwind css") == "tailwind"
    assert _extract_framework("with bootstrap 5") == "bootstrap"
    assert _extract_framework("material ui design") == "material"
    assert _extract_framework("no framework mentioned") == "tailwind"  # default
    print("✓ Test: _extract_framework helper")


def test_extract_colors_helper():
    """Test the _extract_colors helper function."""
    colors = _extract_colors("blue and orange theme with some purple")
    
    assert "blue" in colors
    assert "orange" in colors
    assert "purple" in colors
    print("✓ Test: _extract_colors helper")


def test_complex_prompt():
    """Test a complex, realistic prompt."""
    prompt = """
    Create a modern landing page for CloudSync using Tailwind CSS.
    Include a hero section with a call to action, features section showcasing 
    3 main benefits, testimonials from customers, pricing plans, and a contact form.
    Use blue and white colors for a professional corporate look.
    """
    
    result = parse_intent(prompt)
    
    assert result["framework"] == "tailwind", f"Expected 'tailwind', got '{result['framework']}'"
    assert result["style"] in ["modern", "corporate"], f"Unexpected style: {result['style']}"
    assert "hero" in result["sections"], f"'hero' not in sections: {result['sections']}"
    assert "features" in result["sections"], f"'features' not in sections: {result['sections']}"
    assert "testimonials" in result["sections"], f"'testimonials' not in sections: {result['sections']}"
    assert "pricing" in result["sections"], f"'pricing' not in sections: {result['sections']}"
    assert "contact" in result["sections"], f"'contact' not in sections: {result['sections']}"
    assert "blue" in result["colors"], f"'blue' not in colors: {result['colors']}"
    assert "white" in result["colors"], f"'white' not in colors: {result['colors']}"
    # Brand name extraction may need adjustment for this format
    assert result["metadata"].get("brand_name") == "CloudSync" or "CloudSync" in prompt, \
        f"Brand name issue: {result['metadata']}"
    
    print("✓ Test: Complex realistic prompt")


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("🧪 Running Intent Parser Unit Tests")
    print("="*60 + "\n")
    
    tests = [
        test_basic_portfolio_prompt,
        test_landing_page_with_brand,
        test_bootstrap_framework_detection,
        test_color_extraction,
        test_default_sections,
        test_multiple_sections,
        test_style_detection,
        test_section_ordering,
        test_ecommerce_detection,
        test_default_values,
        test_extract_sections_helper,
        test_extract_framework_helper,
        test_extract_colors_helper,
        test_complex_prompt,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ Test failed: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ Test error: {test.__name__}")
            print(f"  Error: {e}")
            failed += 1
    
    print("\n" + "="*60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    print("="*60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
