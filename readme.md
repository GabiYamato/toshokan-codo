# 🏗️ としょかん コード (Toshokan-Codo)
## Library Code - Intelligent Website Assembler

**Build complete, production-ready websites from natural language descriptions using pre-built UI components.**

---

## 🌟 Features

- 🧠 **Natural Language Understanding** - Describe your website in plain English
- 🎨 **Pre-built Components** - Beautiful Tailwind CSS components ready to use
- 🔍 **Visual Validation** - Automated browser-based validation using Playwright
- 🔧 **Auto-Fix** - Intelligent HTML issue detection and correction
- 💾 **Deployment Ready** - Generates production-ready HTML files
- ⚡ **Fast** - Complete websites generated in seconds
- 🎯 **No Code** - Just describe what you want

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd toshokan-codo

# Install dependencies
pip install -r requirements.txt

# Install Playwright browsers (for validation)
playwright install chromium
```

### Usage

```bash
# Basic usage
python src/main.py "Build a portfolio for John Doe"

# With custom output name
python src/main.py "Create a landing page for TechStart" --output my_landing_page

# Skip validation (faster builds)
python src/main.py "Make a restaurant website" --no-validate

# Quiet mode (minimal output)
python src/main.py "Build a portfolio" --quiet
```

### Examples

```bash
# Portfolio website
python src/main.py "Build a professional portfolio for Sarah Miller with about, projects, and contact sections"

# Landing page
python src/main.py "Create a modern landing page for TechStart with hero, features, pricing, and CTA"

# Restaurant website
python src/main.py "Make a restaurant website with menu, gallery, and contact form"

# Business website
python src/main.py "Create a complete business website with navigation, hero, about, features, testimonials, and contact"
```

## 📦 What's Included

### Components (10 Tailwind CSS Components)
- **nav1.html** - Modern navigation bar
- **hero1.html** - Hero section with CTA
- **features1.html** - Feature showcase grid
- **gallery1.html** - Image gallery
- **contact1.html** - Contact form
- **testimonials1.html** - Customer testimonials
- **pricing1.html** - Pricing tables
- **about1.html** - About section
- **cta1.html** - Call-to-action section
- **footer1.html** - Footer with links

### Core Modules
- **Intent Parser** - Understands natural language descriptions
- **Component Mapper** - Intelligently selects appropriate components
- **HTML Assembler** - Combines components into complete websites
- **Visual Validator** - Validates layout, responsiveness, and accessibility
- **Auto Fixer** - Automatically fixes common HTML issues
- **Output Manager** - Handles file operations and deployment packages

## 🧩 Architecture

The system follows a modular, layered architecture with clear separation of concerns:

### Module Pipeline

```
User Prompt → Intent Parser → Component Mapper → Assembler → Visual Validator → Auto Fixer → Output Manager
```

### Module Overview

| Module | File | Purpose | Tests |
|--------|------|---------|-------|
| **Main Orchestrator** | `src/main.py` | Coordinates all modules | ✅ 13 tests |
| **Intent Parser** | `src/intent_parser.py` | Natural language → JSON | ✅ 14 tests |
| **Component Mapper** | `src/component_mapper.py` | Section → component files | ✅ 16 tests |
| **Assembler** | `src/assembler.py` | Merges components into HTML | ✅ 18 tests |
| **Visual Validator** | `src/visual_validator.py` | Validates via browser | ✅ 8 tests |
| **Fixer** | `src/fixer.py` | Auto-fixes issues | ✅ 15 tests |
| **Output Manager** | `src/output_manager.py` | Saves and manages output | ✅ 15 tests |

**Total: 99 tests - 100% passing**

## 📁 Project Structure

```
toshokan-codo/
├── src/                          # Core application modules
│   ├── main.py                   # Main orchestrator (✅ Complete)
│   ├── intent_parser.py          # Prompt → JSON intent (✅ Complete)
│   ├── component_mapper.py       # Section → component mapping (✅ Complete)
│   ├── assembler.py              # Component assembly (✅ Complete)
│   ├── visual_validator.py       # Visual validation (✅ Complete)
│   ├── fixer.py                  # Automatic fixes (✅ Complete)
│   └── output_manager.py         # Output & preview (✅ Complete)
├── components/                   # UI component library
│   ├── tailwind/                 # Tailwind CSS components (10 files)
│   └── component_registry.json   # Component catalog
├── dist/                         # Output directory for built sites
├── tests/                        # Test suite (99 tests)
│   ├── test_intent_parser.py
│   ├── test_component_mapper.py
│   ├── test_assembler.py
│   ├── test_validator_quick.py
│   ├── test_fixer.py
│   ├── test_output_manager.py
│   └── test_end_to_end.py        # Complete workflow tests
├── verify_complete_system.py     # System verification script
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🔑 Key Design Principles

1. **No Code Generation** - Assembles from pre-built components only
2. **Layered Architecture** - Each module has one clear responsibility
3. **Visual Feedback Loop** - Validates using headless browser
4. **Minimal AI Usage** - Mostly rule-based logic with keyword extraction
5. **Extensible** - Easy to add new frameworks and components
6. **Test-Driven** - 99 comprehensive tests ensure reliability

## 🛠️ Tech Stack

- **Language**: Python 3.x
- **Templating**: Jinja2 3.1.0
- **Visual Testing**: Playwright 1.55.0 (headless Chromium)
- **HTML Parsing**: BeautifulSoup4 4.14.2
- **UI Framework**: Tailwind CSS (via CDN)
- **Testing**: Python unittest
- **Preview Server**: Built-in HTTP server

## 📝 Development Progress

All 8 checkpoints complete! ✅

- [x] **Checkpoint 1**: Project Setup (Directory structure, module scaffolding)
- [x] **Checkpoint 2**: Intent Parser (Natural language → JSON) - 14 tests ✅
- [x] **Checkpoint 3**: Component Mapper (Section → component files) - 16 tests ✅
- [x] **Checkpoint 4**: Assembler (Merge components with Jinja2) - 18 tests ✅
- [x] **Checkpoint 5**: Visual Validator (Playwright validation) - 8 tests ✅
- [x] **Checkpoint 6**: Fixer (Auto-fix layout issues) - 15 tests ✅
- [x] **Checkpoint 7**: Output Manager (Save & preview) - 15 tests ✅
- [x] **Checkpoint 8**: Orchestration (Connect all modules) - 13 tests ✅

**Total: 99 tests, 100% passing**

## 🎨 Supported UI Frameworks

- ✅ **Tailwind CSS** - 10 components ready (fully functional)
- 🔜 **Bootstrap** - Structure ready (coming soon)
- 🔮 **Material UI** - Planned

## 🧪 Testing & Verification

### Run All Tests

```bash
# Run complete test suite (99 tests)
python -m pytest tests/

# Run specific test modules
python -m pytest tests/test_intent_parser.py
python -m pytest tests/test_end_to_end.py
```

### Quick Verification

```bash
# Run system verification (5 integration tests)
python verify_complete_system.py

# Run quick end-to-end test
python tests/test_end_to_end.py --quick
```

### Individual Module Tests

```bash
# Intent Parser (14 tests)
python tests/test_intent_parser.py

# Component Mapper (16 tests)
python tests/test_component_mapper.py

# Assembler (18 tests)
python tests/test_assembler.py

# Visual Validator (8 tests)
python tests/test_validator_quick.py

# Fixer (15 tests)
python tests/test_fixer.py

# Output Manager (15 tests)
python tests/test_output_manager.py

# End-to-End (13 tests)
python tests/test_end_to_end.py
```

## 📊 Output Files

Generated websites are saved to the `dist/` directory:

```
dist/
├── john_doe_portfolio.html
├── techstart_landing.html
├── restaurant_website.html
└── ... (your generated sites)
```

### Viewing Your Website

```bash
# Option 1: Open directly in browser
open dist/your_website.html  # macOS
start dist/your_website.html # Windows
xdg-open dist/your_website.html # Linux

# Option 2: Use preview server (from Output Manager)
# Coming soon: python src/output_manager.py --preview dist/your_website.html
```

## 🔧 Configuration

### Component Registry

Edit `components/component_registry.json` to add new components:

```json
{
  "tailwind": {
    "navigation": ["components/tailwind/nav1.html"],
    "hero": ["components/tailwind/hero1.html"],
    "your_section": ["components/tailwind/your_component.html"]
  }
}
```

### Custom Components

1. Create your component file in `components/tailwind/`
2. Use Jinja2 variables for customization: `{{ title }}`, `{{ description }}`
3. Add to component registry
4. Use in prompts: "Build a site with your_section"

## 🐛 Troubleshooting

### Common Issues

**Issue**: `Module not found` errors
- **Solution**: Make sure you're running from project root and all dependencies are installed

**Issue**: Playwright browser not found
- **Solution**: Run `playwright install chromium`

**Issue**: Permission errors when saving files
- **Solution**: Check write permissions on `dist/` directory

**Issue**: Validation taking too long
- **Solution**: Use `--no-validate` flag for faster builds

### Debug Mode

```bash
# Enable verbose output
python src/main.py "Build a portfolio" --verbose

# Run with Python debugger
python -m pdb src/main.py "Build a portfolio"
```

## 🔮 Future Enhancements

### Planned Features
- [ ] "Vibe fix" mode for existing messy HTML
- [ ] Theme support (dark/minimal/retro/corporate)
- [ ] Web dashboard with live previews (Next.js + Supabase)
- [ ] Component variant selection (nav1, nav2, nav3, etc.)
- [ ] Custom component upload
- [ ] Public component library
- [ ] Pre-built site templates
- [ ] Multi-page website support
- [ ] CSS framework mixing (Tailwind + custom CSS)
- [ ] Image optimization and CDN integration
- [ ] SEO metadata generation
- [ ] Analytics integration
- [ ] Form backend integration

### Framework Support
- [ ] Bootstrap components (structure ready)
- [ ] Material UI components
- [ ] Bulma CSS components
- [ ] Foundation components

## 📚 Additional Documentation

- [Checkpoint 1 Summary](CHECKPOINT_1_COMPLETE.md) - Project setup details
- [Checkpoint 2 Summary](CHECKPOINT_2_COMPLETE.md) - Intent Parser implementation
- [Checkpoint 3 Summary](CHECKPOINT_3_COMPLETE.md) - Component Mapper implementation
- [Checkpoint 4 Summary](CHECKPOINT_4_COMPLETE.md) - Assembler implementation
- [Checkpoint 5 Summary](CHECKPOINT5_SUMMARY.md) - Visual Validator implementation
- [Checkpoint 6 Summary](CHECKPOINT6_SUMMARY.md) - Fixer implementation
- [Checkpoint 7 Summary](CHECKPOINT7_SUMMARY.md) - Output Manager implementation
- [Intent Parser Examples](INTENT_PARSER_EXAMPLES.md) - Usage examples and supported features

## 🤝 Contributing

Contributions welcome! Areas where you can help:

1. **New Components** - Add more UI components in any framework
2. **Framework Support** - Implement Bootstrap, Material UI, etc.
3. **Validation Rules** - Add more visual validation checks
4. **Fix Strategies** - Improve auto-fix algorithms
5. **Documentation** - Improve guides and examples
6. **Testing** - Add more edge case tests

## 📄 License

[Your License Here]

## 🙏 Acknowledgments

- Tailwind CSS for beautiful utility-first CSS
- Playwright for reliable browser automation
- Jinja2 for powerful templating
- BeautifulSoup for HTML parsing

---

## 💡 The Core Philosophy

**Vibecoding is frustrating.** 
- ⏰ Waiting minutes/hours for AI to generate code
- 🐛 Debugging hundreds of lines of AI-generated mess
- 🔄 Endless context-less error loops
- 🤦 Maintaining code you didn't write

**The Solution: Pre-written modules + Smart Assembly = Fast, Maintainable Sites**

- ⚡ Websites built in seconds, not hours
- 📚 Browse and understand modular components easily
- 🔍 Debug by checking specific modules, not generated soup
- ✅ Visual validation ensures quality
- 🔧 Auto-fixing for common layout issues

**Status: ✅ COMPLETE - All 8 checkpoints implemented, 99 tests passing**

---

**Built with ❤️ to make website creation fast, reliable, and frustration-free.**
