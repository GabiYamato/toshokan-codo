"""
Component Mapper Module
Maps abstract section names to concrete component file paths.

Responsibilities:
- Maintain a registry of available components for each framework
- Map section names to appropriate component files
- Handle component variants (e.g., navbar1, navbar2, hero3)
- Support multiple UI frameworks

Example Registry:
{
    "tailwind": {
        "navbar": ["components/tailwind/nav1.html", "components/tailwind/nav2.html"],
        "hero": ["components/tailwind/hero1.html", "components/tailwind/hero2.html"]
    }
}
"""

import json
import os
import random
from typing import Dict, List, Optional
from pathlib import Path


# Default component registry path
REGISTRY_PATH = "components/component_registry.json"


def load_component_registry(registry_path: str = REGISTRY_PATH) -> dict:
    """
    Load the component registry from JSON file.
    
    Args:
        registry_path: Path to the component registry JSON file
        
    Returns:
        Dictionary mapping frameworks and sections to component paths
    """
    # Get absolute path relative to project root
    project_root = Path(__file__).parent.parent
    full_path = project_root / registry_path
    
    if not full_path.exists():
        raise FileNotFoundError(f"Component registry not found at {full_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        registry = json.load(f)
    
    return registry


def map_sections_to_components(
    intent: dict, 
    selection_strategy: str = "first",
    registry_path: str = REGISTRY_PATH
) -> dict:
    """
    Map each section in the intent to a specific component file.
    
    Args:
        intent: Parsed intent dictionary from intent_parser
        selection_strategy: How to select from multiple variants
            - "first": Always use first variant
            - "random": Randomly select variant
            - "round_robin": Cycle through variants
        registry_path: Path to component registry file
        
    Returns:
        Dictionary mapping sections to component file paths
        
    Example Output:
        {
            "navbar": "components/tailwind/nav1.html",
            "hero": "components/tailwind/hero1.html",
            "footer": "components/tailwind/footer1.html"
        }
    """
    registry = load_component_registry(registry_path)
    framework = intent.get("framework", "tailwind")
    sections = intent.get("sections", [])
    
    # Check if framework exists in registry
    if framework not in registry:
        raise ValueError(f"Framework '{framework}' not found in registry. Available: {list(registry.keys())}")
    
    framework_components = registry[framework]
    component_map = {}
    
    for section in sections:
        # Get available components for this section
        available_components = framework_components.get(section, [])
        
        if not available_components:
            # Try to find a fallback or skip
            print(f"⚠️  Warning: No {framework} component found for section '{section}', skipping...")
            continue
        
        # Select component based on strategy
        selected_component = _select_component(
            available_components, 
            selection_strategy,
            section
        )
        
        component_map[section] = selected_component
    
    return component_map


def _select_component(
    components: List[str], 
    strategy: str,
    section_name: str = ""
) -> str:
    """
    Select a component from available options based on strategy.
    
    Args:
        components: List of available component paths
        strategy: Selection strategy (first, random, round_robin)
        section_name: Name of the section (for round_robin state)
        
    Returns:
        Selected component path
    """
    if not components:
        raise ValueError("No components available to select from")
    
    if strategy == "first":
        return components[0]
    
    elif strategy == "random":
        return random.choice(components)
    
    elif strategy == "round_robin":
        # Simple round robin using hash of section name
        # In production, you'd track state across calls
        index = hash(section_name) % len(components)
        return components[index]
    
    else:
        # Default to first
        return components[0]


def get_available_components(
    framework: str,
    section: Optional[str] = None,
    registry_path: str = REGISTRY_PATH
) -> Dict[str, List[str]]:
    """
    Get available components for a framework and optionally a specific section.
    
    Args:
        framework: UI framework name (tailwind, bootstrap, etc.)
        section: Optional section name to filter by
        registry_path: Path to component registry file
        
    Returns:
        Dictionary of section -> component paths
    """
    registry = load_component_registry(registry_path)
    
    if framework not in registry:
        return {}
    
    framework_components = registry[framework]
    
    if section:
        return {section: framework_components.get(section, [])}
    
    return framework_components


def validate_component_paths(registry_path: str = REGISTRY_PATH) -> Dict[str, List[str]]:
    """
    Validate that all component files in the registry actually exist.
    
    Args:
        registry_path: Path to component registry file
        
    Returns:
        Dictionary of framework -> list of missing component paths
    """
    registry = load_component_registry(registry_path)
    project_root = Path(__file__).parent.parent
    
    missing_components = {}
    
    for framework, sections in registry.items():
        missing_in_framework = []
        
        for section, components in sections.items():
            for component_path in components:
                full_path = project_root / component_path
                if not full_path.exists():
                    missing_in_framework.append(component_path)
        
        if missing_in_framework:
            missing_components[framework] = missing_in_framework
    
    return missing_components


def add_component_to_registry(
    framework: str,
    section: str,
    component_path: str,
    registry_path: str = REGISTRY_PATH
) -> bool:
    """
    Add a new component to the registry.
    
    Args:
        framework: UI framework name
        section: Section name
        component_path: Path to component file
        registry_path: Path to component registry file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        registry = load_component_registry(registry_path)
        
        # Initialize framework if it doesn't exist
        if framework not in registry:
            registry[framework] = {}
        
        # Initialize section if it doesn't exist
        if section not in registry[framework]:
            registry[framework][section] = []
        
        # Add component if not already present
        if component_path not in registry[framework][section]:
            registry[framework][section].append(component_path)
        
        # Save updated registry
        project_root = Path(__file__).parent.parent
        full_path = project_root / registry_path
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(registry, f, indent=2)
        
        return True
    
    except Exception as e:
        print(f"Error adding component: {e}")
        return False


def get_component_stats(registry_path: str = REGISTRY_PATH) -> Dict:
    """
    Get statistics about the component registry.
    
    Args:
        registry_path: Path to component registry file
        
    Returns:
        Dictionary with component statistics
    """
    registry = load_component_registry(registry_path)
    
    stats = {
        "frameworks": len(registry),
        "framework_details": {}
    }
    
    for framework, sections in registry.items():
        total_components = sum(len(components) for components in sections.values())
        stats["framework_details"][framework] = {
            "sections": len(sections),
            "total_components": total_components,
            "sections_list": list(sections.keys())
        }
    
    return stats


# Test function for development
def test_component_mapper():
    """
    Test the component mapper with sample intents.
    """
    from intent_parser import parse_intent
    
    test_prompts = [
        "Build a modern portfolio site with navbar, hero, and footer",
        "Create a landing page with features using Bootstrap",
        "Simple site with hero and contact sections"
    ]
    
    print("🗺️  Testing Component Mapper\n" + "="*60 + "\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt}")
        intent = parse_intent(prompt)
        
        try:
            component_map = map_sections_to_components(intent)
            print(f"  Intent sections: {intent['sections']}")
            print(f"  Framework: {intent['framework']}")
            print(f"  Mapped components:")
            for section, path in component_map.items():
                print(f"    {section}: {path}")
        except Exception as e:
            print(f"  ❌ Error: {e}")
        
        print("-" * 60 + "\n")
    
    # Print component stats
    print("\n📊 Component Registry Statistics:")
    stats = get_component_stats()
    print(f"  Total frameworks: {stats['frameworks']}")
    for framework, details in stats['framework_details'].items():
        print(f"\n  {framework.upper()}:")
        print(f"    Sections: {details['sections']}")
        print(f"    Total components: {details['total_components']}")
        print(f"    Available sections: {', '.join(details['sections_list'])}")
    
    # Validate component paths
    print("\n🔍 Validating Component Paths...")
    missing = validate_component_paths()
    if missing:
        print("  ⚠️  Missing components found:")
        for framework, paths in missing.items():
            print(f"    {framework}: {len(paths)} missing")
            for path in paths:
                print(f"      - {path}")
    else:
        print("  ✅ All component paths are valid!")


if __name__ == "__main__":
    test_component_mapper()
