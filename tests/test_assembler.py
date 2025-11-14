"""
Unit tests for Assembler Module
Tests the assembly of components into complete HTML documents.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.assembler import (
    read_component,
    fill_placeholders,
    assemble_website,
    create_standalone_page,
    _prepare_template_data,
    _get_framework_head,
    _get_framework_scripts,
    _get_body_class
)
from src.intent_parser import parse_intent
from src.component_mapper import map_sections_to_components


def test_read_component():
    """Test reading a component file."""
    component_path = "components/tailwind/nav1.html"
    content = read_component(component_path)
    
    assert len(content) > 0, "Component content should not be empty"
    assert "<nav" in content, "Navbar component should contain <nav> tag"
    assert "{{" in content, "Component should contain Jinja2 placeholders"
    print("✓ Test: Read component")


def test_read_component_not_found():
    """Test reading non-existent component."""
    try:
        read_component("components/nonexistent.html")
        assert False, "Should raise FileNotFoundError"
    except FileNotFoundError:
        pass
    print("✓ Test: Read component (not found)")


def test_fill_placeholders():
    """Test filling template placeholders."""
    template_html = "<h1>{{ title }}</h1><p>{{ description }}</p>"
    data = {"title": "Test Title", "description": "Test Description"}
    
    result = fill_placeholders(template_html, data)
    
    assert "Test Title" in result, "Should fill title placeholder"
    assert "Test Description" in result, "Should fill description placeholder"
    assert "{{" not in result, "Should not have unfilled placeholders"
    print("✓ Test: Fill placeholders")


def test_fill_placeholders_with_defaults():
    """Test filling placeholders with Jinja2 defaults."""
    template_html = "<h1>{{ title|default('Default Title') }}</h1>"
    data = {}
    
    result = fill_placeholders(template_html, data)
    
    assert "Default Title" in result, "Should use default value"
    print("✓ Test: Fill placeholders (with defaults)")


def test_prepare_template_data():
    """Test preparation of template data from intent."""
    intent = {
        "framework": "tailwind",
        "style": "modern",
        "colors": ["blue", "purple"],
        "metadata": {
            "brand_name": "TestBrand"
        }
    }
    
    data = _prepare_template_data(intent)
    
    assert data["brand_name"] == "TestBrand", "Should extract brand name"
    assert data["primary_color"] == "blue", "Should extract primary color"
    assert data["secondary_color"] == "purple", "Should extract secondary color"
    assert "hero_title" in data, "Should have default hero title"
    print("✓ Test: Prepare template data")


def test_prepare_template_data_with_custom():
    """Test template data preparation with custom overrides."""
    intent = {"framework": "tailwind", "metadata": {}}
    custom_data = {"hero_title": "Custom Hero", "custom_field": "Custom Value"}
    
    data = _prepare_template_data(intent, custom_data)
    
    assert data["hero_title"] == "Custom Hero", "Should override hero title"
    assert data["custom_field"] == "Custom Value", "Should include custom fields"
    print("✓ Test: Prepare template data (with custom)")


def test_get_framework_head_tailwind():
    """Test getting framework head content for Tailwind."""
    head = _get_framework_head("tailwind", {})
    
    assert "tailwindcss.com" in head, "Should include Tailwind CDN"
    assert "<script" in head, "Should include script tag"
    print("✓ Test: Get framework head (Tailwind)")


def test_get_framework_head_bootstrap():
    """Test getting framework head content for Bootstrap."""
    head = _get_framework_head("bootstrap", {})
    
    assert "bootstrap" in head, "Should include Bootstrap CDN"
    assert "css" in head.lower(), "Should include CSS link"
    print("✓ Test: Get framework head (Bootstrap)")


def test_get_framework_scripts():
    """Test getting framework footer scripts."""
    # Tailwind doesn't need footer scripts
    tailwind_scripts = _get_framework_scripts("tailwind")
    assert tailwind_scripts == "", "Tailwind should not have footer scripts"
    
    # Bootstrap needs JS
    bootstrap_scripts = _get_framework_scripts("bootstrap")
    assert "bootstrap" in bootstrap_scripts, "Bootstrap should have footer scripts"
    print("✓ Test: Get framework scripts")


def test_get_body_class():
    """Test getting body class based on style."""
    test_cases = [
        ({"style": "dark"}, "dark"),
        ({"style": "minimal"}, "bg-white"),
        ({"style": "modern"}, "bg-white"),
    ]
    
    for intent, expected_substring in test_cases:
        body_class = _get_body_class(intent)
        assert expected_substring in body_class, f"Body class should contain '{expected_substring}' for style '{intent['style']}'"
    
    print("✓ Test: Get body class")


def test_assemble_website():
    """Test assembling a complete website."""
    intent = {
        "sections": ["navbar", "hero", "footer"],
        "framework": "tailwind",
        "style": "modern",
        "colors": ["blue", "white"],
        "metadata": {"brand_name": "TestSite"}
    }
    
    component_map = {
        "navbar": "components/tailwind/nav1.html",
        "hero": "components/tailwind/hero1.html",
        "footer": "components/tailwind/footer1.html"
    }
    
    html = assemble_website(component_map, intent)
    
    # Verify HTML structure
    assert "<!DOCTYPE html>" in html, "Should have DOCTYPE"
    assert "<html" in html, "Should have html tag"
    assert "<head>" in html, "Should have head section"
    assert "<body" in html, "Should have body tag"
    assert "tailwindcss.com" in html, "Should include Tailwind CDN"
    assert "TestSite" in html, "Should include brand name"
    
    # Verify components are included
    assert "<nav" in html, "Should include navbar"
    assert "<footer" in html, "Should include footer"
    
    print("✓ Test: Assemble website")


def test_assemble_with_custom_data():
    """Test assembling with custom template data."""
    intent = {
        "sections": ["hero"],
        "framework": "tailwind",
        "metadata": {}
    }
    
    component_map = {"hero": "components/tailwind/hero1.html"}
    custom_data = {"hero_title": "My Custom Title"}
    
    html = assemble_website(component_map, intent, custom_data)
    
    assert "My Custom Title" in html, "Should use custom hero title"
    print("✓ Test: Assemble with custom data")


def test_assemble_end_to_end():
    """Test complete end-to-end assembly flow."""
    # Parse intent
    prompt = "Create a portfolio with gallery and contact form"
    intent = parse_intent(prompt)
    
    # Map components
    component_map = map_sections_to_components(intent)
    
    # Assemble
    html = assemble_website(component_map, intent)
    
    # Verify complete HTML
    assert "<!DOCTYPE html>" in html
    assert len(html) > 1000, "Should generate substantial HTML"
    assert "<nav" in html, "Should have navigation"
    assert "<footer" in html, "Should have footer"
    
    # Check for specific sections from intent
    if "gallery" in component_map:
        assert "gallery" in html.lower() or "work" in html.lower()
    if "contact" in component_map:
        assert "contact" in html.lower() or "touch" in html.lower()
    
    print("✓ Test: Assemble end-to-end")


def test_create_standalone_page():
    """Test creating a standalone page."""
    html = create_standalone_page(
        sections=["navbar", "hero", "footer"],
        framework="tailwind",
        brand_name="StandaloneBrand"
    )
    
    assert "<!DOCTYPE html>" in html, "Should have DOCTYPE"
    assert "StandaloneBrand" in html, "Should include brand name"
    assert "tailwindcss.com" in html, "Should include Tailwind"
    print("✓ Test: Create standalone page")


def test_create_standalone_with_custom_data():
    """Test standalone page with custom data."""
    custom_data = {"hero_title": "Standalone Hero"}
    
    html = create_standalone_page(
        sections=["hero"],
        brand_name="TestBrand",
        custom_data=custom_data
    )
    
    assert "Standalone Hero" in html, "Should use custom data"
    print("✓ Test: Create standalone page (with custom data)")


def test_html_validity():
    """Test that generated HTML is structurally valid."""
    intent = {
        "sections": ["navbar", "hero", "features", "footer"],
        "framework": "tailwind",
        "metadata": {}
    }
    
    component_map = map_sections_to_components(intent)
    html = assemble_website(component_map, intent)
    
    # Check essential HTML5 elements
    assert html.count("<!DOCTYPE html>") == 1, "Should have exactly one DOCTYPE"
    assert html.count("<html") == 1, "Should have exactly one html tag"
    assert html.count("<head>") == 1, "Should have exactly one head tag"
    assert html.count("<body") == 1, "Should have exactly one body tag"
    
    # Check that tags are properly closed (basic check)
    assert html.count("</html>") == 1, "Should close html tag"
    assert html.count("</head>") == 1, "Should close head tag"
    assert html.count("</body>") == 1, "Should close body tag"
    
    print("✓ Test: HTML validity")


def test_multiple_sections():
    """Test assembling with many sections."""
    intent = {
        "sections": ["navbar", "hero", "features", "gallery", 
                    "testimonials", "pricing", "contact", "footer"],
        "framework": "tailwind",
        "metadata": {"brand_name": "BigSite"}
    }
    
    component_map = map_sections_to_components(intent)
    html = assemble_website(component_map, intent)
    
    # Should be a substantial page
    assert len(html) > 10000, "Multi-section page should be large"
    assert html.count("<section") >= 5, "Should have multiple section tags"
    assert "BigSite" in html, "Should include brand name"
    
    print("✓ Test: Multiple sections")


def test_color_customization():
    """Test that colors are properly applied."""
    intent = {
        "sections": ["navbar", "hero"],
        "framework": "tailwind",
        "colors": ["purple", "pink"],
        "metadata": {}
    }
    
    component_map = map_sections_to_components(intent)
    html = assemble_website(component_map, intent)
    
    assert "purple" in html, "Should use primary color (purple)"
    print("✓ Test: Color customization")


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("🧪 Running Assembler Unit Tests")
    print("="*60 + "\n")
    
    tests = [
        test_read_component,
        test_read_component_not_found,
        test_fill_placeholders,
        test_fill_placeholders_with_defaults,
        test_prepare_template_data,
        test_prepare_template_data_with_custom,
        test_get_framework_head_tailwind,
        test_get_framework_head_bootstrap,
        test_get_framework_scripts,
        test_get_body_class,
        test_assemble_website,
        test_assemble_with_custom_data,
        test_assemble_end_to_end,
        test_create_standalone_page,
        test_create_standalone_with_custom_data,
        test_html_validity,
        test_multiple_sections,
        test_color_customization,
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
