# Intent Parser Examples

This document demonstrates the Intent Parser functionality with real-world examples.

## Basic Usage

```python
from src.intent_parser import parse_intent

# Simple portfolio site
result = parse_intent("Build a modern portfolio site with a navbar, hero section, and contact form")

print(result)
# Output:
# {
#     "sections": ["navbar", "hero", "gallery", "contact", "footer"],
#     "framework": "tailwind",
#     "style": "modern",
#     "colors": ["blue", "white"],
#     "metadata": {
#         "original_prompt": "...",
#         "prompt_length": 75,
#         "is_portfolio": True
#     }
# }
```

## Example Prompts

### 1. Portfolio Website
```python
parse_intent("Create a minimal portfolio with gallery and contact form")
```
**Output:**
- Sections: navbar, hero, gallery, contact, footer
- Framework: tailwind
- Style: minimal
- Metadata: is_portfolio = True

---

### 2. Landing Page with Brand
```python
parse_intent("Build a landing page for TechStart with features and pricing using Tailwind")
```
**Output:**
- Sections: navbar, hero, features, pricing, footer
- Framework: tailwind
- Brand Name: TechStart
- Metadata: is_landing_page = True

---

### 3. Corporate Website
```python
parse_intent("Make a corporate site with blue and white colors, including about and services sections")
```
**Output:**
- Sections: navbar, about, features, footer
- Style: corporate
- Colors: blue, white

---

### 4. E-commerce Store
```python
parse_intent("Build an online shop with products, pricing, and checkout")
```
**Output:**
- Sections: navbar, hero, pricing, footer
- Metadata: is_ecommerce = True

---

### 5. Bootstrap Framework
```python
parse_intent("Create a website with testimonials using Bootstrap")
```
**Output:**
- Sections: navbar, hero, testimonials, footer
- Framework: bootstrap

---

### 6. Multiple Sections
```python
parse_intent("Site with hero, features, testimonials, pricing, contact, and about sections")
```
**Output:**
- Sections: navbar, hero, about, features, testimonials, pricing, contact, footer
- Note: Automatically ordered in logical sequence

---

### 7. Custom Colors
```python
parse_intent("Create a vibrant site with purple, orange, and pink colors")
```
**Output:**
- Colors: purple, orange, pink
- Style: creative

---

## Supported Features

### Sections Detected
- navbar / navigation / menu / header
- hero / banner / landing
- features / services / benefits
- gallery / portfolio / showcase
- testimonials / reviews
- pricing / plans / packages
- contact / contact form
- about / about us
- cta / call to action
- footer

### Frameworks Detected
- **Tailwind** (default): tailwind, tailwindcss
- **Bootstrap**: bootstrap, bootstrap 5, bs5
- **Material UI**: material, material ui, mui

### Styles Detected
- **modern** (default): modern, contemporary, sleek
- **minimal**: minimal, minimalist, simple
- **retro**: retro, vintage, classic
- **corporate**: corporate, professional, business
- **creative**: creative, artistic, colorful
- **dark**: dark, dark mode

### Colors Detected
blue, red, green, yellow, purple, pink, orange, teal, cyan, indigo, gray, black, white

### Metadata Extracted
- **Brand Name**: Extracted from "for [BrandName]" pattern
- **is_portfolio**: Detected when "portfolio" mentioned
- **is_ecommerce**: Detected for shop/store/buy keywords
- **is_landing_page**: Detected when "landing" mentioned

---

## Smart Defaults

If certain information isn't specified, the parser applies intelligent defaults:

| Property | Default |
|----------|---------|
| Framework | tailwind |
| Style | modern |
| Colors | [blue, white] |
| Sections | [navbar, hero, footer] (minimum) |

---

## Section Ordering

Sections are automatically ordered in a logical sequence:
1. navbar
2. hero
3. about
4. features
5. gallery
6. testimonials
7. pricing
8. contact
9. cta
10. footer

Example: Even if you say "footer, features, hero, navbar", the output will be properly ordered.

---

## Testing

Run the built-in tests:
```bash
python3 src/intent_parser.py
```

Run unit tests:
```bash
python3 tests/test_intent_parser.py
```

---

## Next Steps

The parsed intent is used by:
1. **Component Mapper** (Checkpoint 3) - Maps sections to component files
2. **Assembler** (Checkpoint 4) - Uses colors and brand name for customization
3. **Visual Validator** (Checkpoint 5) - Validates the final layout
