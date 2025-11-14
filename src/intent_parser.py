"""
Intent Parser Module
Converts natural language user prompts into structured JSON specifications.

Responsibilities:
- Extract key sections (navbar, hero, features, footer, etc.)
- Identify preferred UI framework (Tailwind, Bootstrap, Material UI)
- Detect style preferences (modern, minimal, retro, etc.)
- Use lightweight keyword extraction (minimal AI usage)

Output Format:
{
    "sections": ["navbar", "hero", "features", "footer"],
    "framework": "tailwind",
    "style": "modern",
    "colors": ["blue", "white"],
    "metadata": {}
}
"""

import re
from typing import Dict, List


# Keyword mappings for section detection
SECTION_KEYWORDS = {
    "navbar": ["navbar", "nav", "navigation", "menu", "header"],
    "hero": ["hero", "banner", "landing", "jumbotron", "main section"],
    "features": ["features", "services", "benefits", "capabilities", "what we offer"],
    "footer": ["footer", "bottom", "contact info"],
    "gallery": ["gallery", "portfolio", "showcase", "images"],
    "testimonials": ["testimonials", "reviews", "feedback", "testimonial"],
    "pricing": ["pricing", "plans", "packages", "subscription"],
    "contact": ["contact", "contact form", "get in touch", "reach us"],
    "about": ["about", "about us", "who we are", "our story"],
    "cta": ["call to action", "cta", "sign up", "get started"],
}

# Framework detection keywords
FRAMEWORK_KEYWORDS = {
    "tailwind": ["tailwind", "tailwindcss", "tailwind css"],
    "bootstrap": ["bootstrap", "bootstrap 5", "bootstrap5", "bs5"],
    "material": ["material", "material ui", "mui", "material design"],
}

# Style/theme detection keywords
STYLE_KEYWORDS = {
    "modern": ["modern", "contemporary", "sleek", "clean"],
    "minimal": ["minimal", "minimalist", "simple", "minimalistic"],
    "retro": ["retro", "vintage", "classic", "old school"],
    "corporate": ["corporate", "professional", "business", "enterprise"],
    "creative": ["creative", "artistic", "colorful", "vibrant"],
    "dark": ["dark", "dark mode", "dark theme"],
}

# Color extraction keywords
COLOR_KEYWORDS = [
    "blue", "red", "green", "yellow", "purple", "pink", "orange", 
    "teal", "cyan", "indigo", "gray", "black", "white"
]


def parse_intent(user_prompt: str) -> dict:
    """
    Parse user's natural language prompt into structured intent.
    
    Args:
        user_prompt: Natural language description of desired website
        
    Returns:
        Dictionary with sections, framework, style, and other metadata
    """
    prompt_lower = user_prompt.lower()
    
    # Extract sections
    sections = _extract_sections(prompt_lower)
    
    # Determine framework (default to tailwind if not specified)
    framework = _extract_framework(prompt_lower)
    
    # Determine style
    style = _extract_style(prompt_lower)
    
    # Extract colors
    colors = _extract_colors(prompt_lower)
    
    # Extract additional metadata
    metadata = _extract_metadata(user_prompt, prompt_lower)
    
    return {
        "sections": sections,
        "framework": framework,
        "style": style,
        "colors": colors,
        "metadata": metadata
    }


def _extract_sections(prompt_lower: str) -> List[str]:
    """
    Extract section names from the prompt.
    
    Args:
        prompt_lower: Lowercase version of user prompt
        
    Returns:
        List of section names to include
    """
    detected_sections = []
    
    for section, keywords in SECTION_KEYWORDS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                if section not in detected_sections:
                    detected_sections.append(section)
                break
    
    # Default sections if none detected
    if not detected_sections:
        detected_sections = ["navbar", "hero", "footer"]
    
    # Ensure navbar and footer are always included
    if "navbar" not in detected_sections:
        detected_sections.insert(0, "navbar")
    if "footer" not in detected_sections:
        detected_sections.append("footer")
    
    # Order sections logically
    section_order = ["navbar", "hero", "about", "features", "gallery", 
                     "testimonials", "pricing", "contact", "cta", "footer"]
    
    ordered_sections = [s for s in section_order if s in detected_sections]
    
    return ordered_sections


def _extract_framework(prompt_lower: str) -> str:
    """
    Determine which UI framework to use.
    
    Args:
        prompt_lower: Lowercase version of user prompt
        
    Returns:
        Framework name (default: "tailwind")
    """
    for framework, keywords in FRAMEWORK_KEYWORDS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                return framework
    
    # Default to Tailwind
    return "tailwind"


def _extract_style(prompt_lower: str) -> str:
    """
    Determine the style/theme preference.
    
    Args:
        prompt_lower: Lowercase version of user prompt
        
    Returns:
        Style name (default: "modern")
    """
    for style, keywords in STYLE_KEYWORDS.items():
        for keyword in keywords:
            if keyword in prompt_lower:
                return style
    
    # Default to modern
    return "modern"


def _extract_colors(prompt_lower: str) -> List[str]:
    """
    Extract color preferences from the prompt.
    
    Args:
        prompt_lower: Lowercase version of user prompt
        
    Returns:
        List of color names
    """
    colors = []
    
    for color in COLOR_KEYWORDS:
        if color in prompt_lower:
            colors.append(color)
    
    # Default colors if none specified
    if not colors:
        colors = ["blue", "white"]
    
    return colors


def _extract_metadata(original_prompt: str, prompt_lower: str) -> Dict:
    """
    Extract additional metadata from the prompt.
    
    Args:
        original_prompt: Original user prompt (case-preserved)
        prompt_lower: Lowercase version
        
    Returns:
        Dictionary with additional metadata
    """
    metadata = {
        "original_prompt": original_prompt,
        "prompt_length": len(original_prompt)
    }
    
    # Extract brand name if mentioned (look for quotes or "for X" pattern)
    brand_match = re.search(r'for ([A-Z][a-zA-Z0-9\s]+?)(?:\s+with|\s+that|\.|$)', original_prompt)
    if brand_match:
        metadata["brand_name"] = brand_match.group(1).strip()
    
    # Check if portfolio is mentioned
    if "portfolio" in prompt_lower:
        metadata["is_portfolio"] = True
    
    # Check if e-commerce is mentioned
    if any(word in prompt_lower for word in ["shop", "store", "ecommerce", "e-commerce", "buy", "sell"]):
        metadata["is_ecommerce"] = True
    
    # Check if landing page is mentioned
    if "landing" in prompt_lower or "landing page" in prompt_lower:
        metadata["is_landing_page"] = True
    
    return metadata


# Test function for development
def test_intent_parser():
    """
    Test the intent parser with sample prompts.
    """
    test_prompts = [
        "Build a modern portfolio site with a navbar, hero section, and contact form",
        "Create a landing page for TechStart with features and pricing using Tailwind",
        "I need a minimal website with a gallery and testimonials in Bootstrap",
        "Make a corporate site with blue and white colors, including about and services sections",
        "Simple one-page site with hero, features, and footer"
    ]
    
    print("🧪 Testing Intent Parser\n" + "="*60 + "\n")
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Test {i}: {prompt}")
        result = parse_intent(prompt)
        print(f"Result:")
        print(f"  Sections: {result['sections']}")
        print(f"  Framework: {result['framework']}")
        print(f"  Style: {result['style']}")
        print(f"  Colors: {result['colors']}")
        print(f"  Metadata: {result['metadata']}")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    test_intent_parser()
