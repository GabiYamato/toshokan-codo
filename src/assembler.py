"""
Assembler Module
Combines individual components into a complete HTML document.

Responsibilities:
- Read component HTML files
- Fill in placeholders (text, colors, images, etc.)
- Merge components in correct order
- Add necessary CSS/JS dependencies
- Generate complete, valid HTML document
- Use Jinja2 for templating

Output: Complete HTML file ready for validation
"""

from jinja2 import Template
from pathlib import Path
from typing import Dict, List, Optional
import re


# Framework CDN links
FRAMEWORK_CDN = {
    "tailwind": {
        "css": "https://cdn.tailwindcss.com",
        "config": """
        <script>
            tailwind.config = {
                theme: {
                    extend: {
                        colors: {
                            primary: colors.blue,
                            secondary: colors.purple,
                        }
                    }
                }
            }
        </script>
        """
    },
    "bootstrap": {
        "css": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css",
        "js": "https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"
    },
    "material": {
        "css": "https://fonts.googleapis.com/icon?family=Material+Icons",
        "js": "https://unpkg.com/material-components-web@latest/dist/material-components-web.min.js"
    }
}

# HTML template structure
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ page_title }}</title>
    {{ head_content }}
</head>
<body class="{{ body_class }}">
    {{ body_content }}
    {{ footer_scripts }}
</body>
</html>
"""


def read_component(component_path: str) -> str:
    """
    Read a component HTML file.
    
    Args:
        component_path: Path to the component file
        
    Returns:
        Component HTML content as string
    """
    project_root = Path(__file__).parent.parent
    full_path = project_root / component_path
    
    if not full_path.exists():
        raise FileNotFoundError(f"Component file not found: {component_path}")
    
    with open(full_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    return content


def fill_placeholders(component_html: str, data: dict) -> str:
    """
    Replace placeholders in component with actual data using Jinja2.
    
    Args:
        component_html: Component HTML with placeholders
        data: Dictionary of values to fill in
        
    Returns:
        Component HTML with filled placeholders
    """
    try:
        template = Template(component_html)
        rendered = template.render(**data)
        return rendered
    except Exception as e:
        print(f"⚠️  Warning: Error rendering template: {e}")
        return component_html


def assemble_website(
    component_map: dict, 
    intent: dict,
    custom_data: Optional[dict] = None
) -> str:
    """
    Combine all components into a complete website.
    
    Args:
        component_map: Mapping of sections to component paths
        intent: Original parsed intent with metadata
        custom_data: Optional custom data for template rendering
        
    Returns:
        Complete HTML document as string
    """
    # Prepare template data
    template_data = _prepare_template_data(intent, custom_data)
    
    # Load and render all components
    rendered_components = []
    for section, component_path in component_map.items():
        try:
            # Read component
            component_html = read_component(component_path)
            
            # Render with template data
            rendered = fill_placeholders(component_html, template_data)
            rendered_components.append(rendered)
            
        except Exception as e:
            print(f"⚠️  Warning: Failed to load component '{section}': {e}")
            continue
    
    # Combine all components
    body_content = "\n\n    ".join(rendered_components)
    
    # Get framework-specific head content
    framework = intent.get("framework", "tailwind")
    head_content = _get_framework_head(framework, template_data)
    footer_scripts = _get_framework_scripts(framework)
    
    # Build final HTML
    page_title = template_data.get("page_title", "My Website")
    body_class = _get_body_class(intent)
    
    final_html = HTML_TEMPLATE.replace("{{ page_title }}", page_title)
    final_html = final_html.replace("{{ head_content }}", head_content)
    final_html = final_html.replace("{{ body_content }}", body_content)
    final_html = final_html.replace("{{ footer_scripts }}", footer_scripts)
    final_html = final_html.replace("{{ body_class }}", body_class)
    
    return final_html


def _prepare_template_data(intent: dict, custom_data: Optional[dict] = None) -> dict:
    """
    Prepare data dictionary for template rendering.
    
    Args:
        intent: Parsed intent from intent_parser
        custom_data: Optional custom data to override defaults
        
    Returns:
        Dictionary with all template variables
    """
    metadata = intent.get("metadata", {})
    colors = intent.get("colors", ["blue", "white"])
    style = intent.get("style", "modern")
    
    # Default template data
    data = {
        # Brand/Identity
        "brand_name": metadata.get("brand_name", "YourBrand"),
        "page_title": metadata.get("brand_name", "My Website"),
        
        # Colors
        "primary_color": colors[0] if colors else "blue",
        "secondary_color": colors[1] if len(colors) > 1 else "purple",
        
        # Hero section
        "hero_title": f"Welcome to {metadata.get('brand_name', 'Our Platform')}",
        "hero_subtitle": "Build amazing things with our powerful tools",
        
        # Features
        "features_title": "Our Features",
        "features_subtitle": "Everything you need to succeed",
        
        # Gallery
        "gallery_title": "Our Work",
        "gallery_subtitle": "Check out our latest projects",
        
        # Testimonials
        "testimonials_title": "What Our Clients Say",
        "testimonials_subtitle": "Don't just take our word for it",
        
        # Pricing
        "pricing_title": "Simple Pricing",
        "pricing_subtitle": "Choose the plan that's right for you",
        
        # Contact
        "contact_title": "Get In Touch",
        "contact_subtitle": "We'd love to hear from you",
        "contact_email": "hello@example.com",
        "contact_phone": "+1 (555) 123-4567",
        "contact_location": "San Francisco, CA",
        
        # About
        "about_title": "About Us",
        "about_text": "We are a team of passionate individuals dedicated to creating exceptional digital experiences.",
        
        # CTA
        "cta_title": "Ready to Get Started?",
        "cta_subtitle": "Join thousands of satisfied customers today",
        "cta_primary_button": "Get Started Now",
        "cta_secondary_button": "Learn More",
    }
    
    # Apply custom data if provided
    if custom_data:
        data.update(custom_data)
    
    return data


def _get_framework_head(framework: str, template_data: dict) -> str:
    """
    Get framework-specific <head> content (CSS, fonts, etc.).
    
    Args:
        framework: UI framework name
        template_data: Template data with theme colors
        
    Returns:
        HTML content for <head> section
    """
    framework_info = FRAMEWORK_CDN.get(framework, FRAMEWORK_CDN["tailwind"])
    head_parts = []
    
    # Add CSS
    if "css" in framework_info:
        css_url = framework_info["css"]
        if framework == "tailwind":
            head_parts.append(f'    <script src="{css_url}"></script>')
        else:
            head_parts.append(f'    <link rel="stylesheet" href="{css_url}">')
    
    # Add config if needed
    if "config" in framework_info:
        head_parts.append(framework_info["config"])
    
    # Add meta tags
    head_parts.append('    <meta name="description" content="A modern website built with component assembly">')
    
    return "\n".join(head_parts)


def _get_framework_scripts(framework: str) -> str:
    """
    Get framework-specific footer scripts.
    
    Args:
        framework: UI framework name
        
    Returns:
        HTML script tags for footer
    """
    framework_info = FRAMEWORK_CDN.get(framework, {})
    
    if "js" in framework_info:
        return f'    <script src="{framework_info["js"]}"></script>'
    
    return ""


def _get_body_class(intent: dict) -> str:
    """
    Get body CSS class based on intent style.
    
    Args:
        intent: Parsed intent
        
    Returns:
        CSS class string for body tag
    """
    style = intent.get("style", "modern")
    
    # Map styles to potential body classes
    style_classes = {
        "dark": "dark bg-gray-900 text-white",
        "minimal": "bg-white text-gray-900",
        "modern": "bg-white text-gray-900",
        "retro": "bg-gray-100 text-gray-900",
        "corporate": "bg-white text-gray-900",
        "creative": "bg-white text-gray-900"
    }
    
    return style_classes.get(style, "bg-white text-gray-900")


def create_standalone_page(
    sections: List[str],
    framework: str = "tailwind",
    brand_name: str = "MyBrand",
    custom_data: Optional[dict] = None
) -> str:
    """
    Convenience function to create a standalone page without going through full pipeline.
    
    Args:
        sections: List of section names to include
        framework: UI framework to use
        brand_name: Brand name for the site
        custom_data: Optional custom template data
        
    Returns:
        Complete HTML document
    """
    from src.component_mapper import map_sections_to_components
    
    # Create minimal intent
    intent = {
        "sections": sections,
        "framework": framework,
        "style": "modern",
        "colors": ["blue", "white"],
        "metadata": {"brand_name": brand_name}
    }
    
    # Map components
    component_map = map_sections_to_components(intent)
    
    # Assemble
    html = assemble_website(component_map, intent, custom_data)
    
    return html


# Test function for development
def test_assembler():
    """
    Test the assembler with sample data.
    """
    from src.intent_parser import parse_intent
    from src.component_mapper import map_sections_to_components
    
    test_prompts = [
        "Build a modern portfolio for TechCo with hero, gallery, and contact",
        "Create a landing page with features and pricing",
        "Simple site with hero and about sections"
    ]
    
    print("🔨 Testing Assembler\n" + "="*60 + "\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt}")
        
        # Parse intent
        intent = parse_intent(prompt)
        print(f"  Framework: {intent['framework']}")
        print(f"  Sections: {intent['sections']}")
        
        # Map components
        component_map = map_sections_to_components(intent)
        print(f"  Mapped: {len(component_map)} components")
        
        # Assemble
        html = assemble_website(component_map, intent)
        
        # Show stats
        lines = html.count('\n')
        size_kb = len(html) / 1024
        print(f"  Output: {lines} lines, {size_kb:.1f} KB")
        
        # Check for key elements
        has_doctype = "<!DOCTYPE html>" in html
        has_tailwind = "tailwindcss" in html
        has_components = all(section in html.lower() for section in ["nav", "footer"])
        
        print(f"  Validation: DOCTYPE={has_doctype}, CDN={has_tailwind}, Structure={has_components}")
        print("-" * 60 + "\n")
    
    # Test standalone creation
    print("\n🎨 Testing Standalone Page Creation")
    standalone = create_standalone_page(
        sections=["navbar", "hero", "features", "footer"],
        brand_name="TestBrand",
        custom_data={"hero_title": "Custom Hero Title"}
    )
    print(f"  Created standalone page: {len(standalone)} bytes")
    print(f"  Contains custom title: {'Custom Hero Title' in standalone}")
    
    print("\n" + "="*60)
    print("✅ Assembler tests complete!")


if __name__ == "__main__":
    test_assembler()
