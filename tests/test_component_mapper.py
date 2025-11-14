"""
Unit tests for Component Mapper Module
Tests the mapping of sections to component file paths.
"""

import sys
import os
import json
from pathlib import Path

# Add parent directory to path to import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.component_mapper import (
    load_component_registry,
    map_sections_to_components,
    get_available_components,
    validate_component_paths,
    add_component_to_registry,
    get_component_stats,
    _select_component
)
from src.intent_parser import parse_intent


def test_load_component_registry():
    """Test loading the component registry."""
    registry = load_component_registry()
    
    assert isinstance(registry, dict), "Registry should be a dictionary"
    assert "tailwind" in registry, "Registry should contain tailwind framework"
    assert isinstance(registry["tailwind"], dict), "Tailwind entry should be a dictionary"
    print("✓ Test: Load component registry")


def test_map_sections_to_components():
    """Test mapping sections to component paths."""
    intent = {
        "sections": ["navbar", "hero", "footer"],
        "framework": "tailwind"
    }
    
    component_map = map_sections_to_components(intent)
    
    assert "navbar" in component_map, "navbar should be mapped"
    assert "hero" in component_map, "hero should be mapped"
    assert "footer" in component_map, "footer should be mapped"
    assert component_map["navbar"].endswith(".html"), "Component paths should be HTML files"
    print("✓ Test: Map sections to components")


def test_map_with_intent_parser():
    """Test mapping with real intent parser output."""
    prompt = "Build a portfolio with gallery and contact form"
    intent = parse_intent(prompt)
    
    component_map = map_sections_to_components(intent)
    
    assert len(component_map) > 0, "Should map at least one component"
    assert "gallery" in component_map, "gallery should be mapped"
    assert "contact" in component_map, "contact should be mapped"
    print("✓ Test: Map with intent parser integration")


def test_framework_selection():
    """Test that framework selection works correctly."""
    tailwind_intent = {
        "sections": ["navbar", "hero"],
        "framework": "tailwind"
    }
    
    component_map = map_sections_to_components(tailwind_intent)
    
    for path in component_map.values():
        assert "tailwind" in path, "Tailwind components should be selected for tailwind framework"
    
    print("✓ Test: Framework selection")


def test_invalid_framework():
    """Test handling of invalid framework."""
    intent = {
        "sections": ["navbar"],
        "framework": "nonexistent"
    }
    
    try:
        map_sections_to_components(intent)
        assert False, "Should raise ValueError for invalid framework"
    except ValueError as e:
        assert "not found in registry" in str(e)
    
    print("✓ Test: Invalid framework handling")


def test_missing_section():
    """Test handling of sections not in registry."""
    intent = {
        "sections": ["navbar", "nonexistent_section", "footer"],
        "framework": "tailwind"
    }
    
    # Should skip missing section without crashing
    component_map = map_sections_to_components(intent)
    
    assert "navbar" in component_map
    assert "footer" in component_map
    assert "nonexistent_section" not in component_map
    print("✓ Test: Missing section handling")


def test_get_available_components():
    """Test getting available components for a framework."""
    components = get_available_components("tailwind")
    
    assert isinstance(components, dict), "Should return a dictionary"
    assert len(components) > 0, "Should have at least one section"
    assert "navbar" in components, "Should have navbar components"
    print("✓ Test: Get available components")


def test_get_available_components_filtered():
    """Test getting components filtered by section."""
    components = get_available_components("tailwind", section="hero")
    
    assert "hero" in components, "Should filter to hero section"
    assert len(components) == 1, "Should only return one section"
    assert isinstance(components["hero"], list), "Section should map to list of paths"
    print("✓ Test: Get available components (filtered)")


def test_validate_component_paths():
    """Test validation of component file paths."""
    missing = validate_component_paths()
    
    # For tailwind, all paths should exist
    assert "tailwind" not in missing or len(missing["tailwind"]) == 0, \
        f"All Tailwind components should exist, missing: {missing.get('tailwind', [])}"
    
    print("✓ Test: Validate component paths")


def test_get_component_stats():
    """Test getting component registry statistics."""
    stats = get_component_stats()
    
    assert "frameworks" in stats, "Stats should include frameworks count"
    assert "framework_details" in stats, "Stats should include framework details"
    assert "tailwind" in stats["framework_details"], "Stats should include tailwind"
    
    tailwind_stats = stats["framework_details"]["tailwind"]
    assert "sections" in tailwind_stats, "Should have sections count"
    assert "total_components" in tailwind_stats, "Should have total components count"
    assert tailwind_stats["total_components"] >= 10, "Should have at least 10 tailwind components"
    
    print("✓ Test: Get component stats")


def test_selection_strategy_first():
    """Test 'first' selection strategy."""
    components = ["comp1.html", "comp2.html", "comp3.html"]
    selected = _select_component(components, "first")
    
    assert selected == "comp1.html", "Should select first component"
    print("✓ Test: Selection strategy - first")


def test_selection_strategy_random():
    """Test 'random' selection strategy."""
    components = ["comp1.html", "comp2.html", "comp3.html"]
    selected = _select_component(components, "random")
    
    assert selected in components, "Should select one of the available components"
    print("✓ Test: Selection strategy - random")


def test_selection_strategy_round_robin():
    """Test 'round_robin' selection strategy."""
    components = ["comp1.html", "comp2.html", "comp3.html"]
    selected = _select_component(components, "round_robin", "test_section")
    
    assert selected in components, "Should select one of the available components"
    print("✓ Test: Selection strategy - round_robin")


def test_all_sections_have_components():
    """Test that all common sections have Tailwind components."""
    common_sections = ["navbar", "hero", "features", "footer", "gallery", 
                      "contact", "testimonials", "pricing", "about", "cta"]
    
    components = get_available_components("tailwind")
    
    for section in common_sections:
        assert section in components, f"Section '{section}' should have components"
        assert len(components[section]) > 0, f"Section '{section}' should have at least one component"
    
    print("✓ Test: All common sections have components")


def test_component_paths_format():
    """Test that component paths follow expected format."""
    components = get_available_components("tailwind")
    
    for section, paths in components.items():
        for path in paths:
            assert path.startswith("components/tailwind/"), \
                f"Path should start with 'components/tailwind/', got: {path}"
            assert path.endswith(".html"), \
                f"Path should end with '.html', got: {path}"
            assert section in path or section[:3] in path, \
                f"Path should contain section identifier, section: {section}, path: {path}"
    
    print("✓ Test: Component paths format")


def test_end_to_end_mapping():
    """Test complete end-to-end mapping flow."""
    # Parse intent
    prompt = "Create a modern site with hero, features, testimonials, and pricing"
    intent = parse_intent(prompt)
    
    # Map to components
    component_map = map_sections_to_components(intent)
    
    # Verify all sections mapped
    assert "hero" in component_map
    assert "features" in component_map
    assert "testimonials" in component_map
    assert "pricing" in component_map
    
    # Verify paths are valid
    project_root = Path(__file__).parent.parent
    for section, path in component_map.items():
        full_path = project_root / path
        assert full_path.exists(), f"Component file should exist: {path}"
    
    print("✓ Test: End-to-end mapping flow")


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("🧪 Running Component Mapper Unit Tests")
    print("="*60 + "\n")
    
    tests = [
        test_load_component_registry,
        test_map_sections_to_components,
        test_map_with_intent_parser,
        test_framework_selection,
        test_invalid_framework,
        test_missing_section,
        test_get_available_components,
        test_get_available_components_filtered,
        test_validate_component_paths,
        test_get_component_stats,
        test_selection_strategy_first,
        test_selection_strategy_random,
        test_selection_strategy_round_robin,
        test_all_sections_have_components,
        test_component_paths_format,
        test_end_to_end_mapping,
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
