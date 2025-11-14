"""
Main orchestrator for the Website Assembler.
This module ties together all components of the system:
- Parses user intent
- Maps to components
- Assembles the website
- Validates visually
- Fixes issues
- Outputs final result
"""

import sys
import time
from pathlib import Path
from typing import Dict, Tuple, Optional

# Add project root to path for direct execution
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import all modules
from src.intent_parser import parse_intent
from src.component_mapper import load_component_registry, map_sections_to_components
from src.assembler import assemble_website
from src.visual_validator import validate_html_string, generate_validation_summary
from src.fixer import auto_fix_website, generate_fix_summary
from src.output_manager import (
    save_website, 
    generate_summary, 
    list_outputs, 
    print_outputs_table,
    create_deployment_package
)


def build_website(
    user_prompt: str,
    output_name: Optional[str] = None,
    auto_fix: bool = True,
    validate: bool = True,
    verbose: bool = True
) -> Tuple[bool, Dict]:
    """
    Complete end-to-end website building process.
    
    Args:
        user_prompt: Natural language description of desired website
        output_name: Optional custom output filename
        auto_fix: Whether to automatically fix validation issues
        validate: Whether to validate the generated website
        verbose: Whether to print detailed progress
        
    Returns:
        Tuple of (success, build_info)
    """
    start_time = time.time()
    build_info = {
        "success": False,
        "stages": {},
        "output_path": None,
        "errors": []
    }
    
    if verbose:
        print("\n" + "="*70)
        print("🏗️  TOSHOKAN-CODO - INTELLIGENT WEBSITE ASSEMBLER")
        print("="*70)
        print(f"\n📝 User Prompt: \"{user_prompt}\"\n")
    
    # Stage 1: Parse Intent
    if verbose:
        print("Stage 1: 🧠 Parsing Intent...")
    
    try:
        intent = parse_intent(user_prompt)
        build_info["stages"]["intent_parsing"] = {
            "success": True,
            "data": intent
        }
        
        if verbose:
            print(f"  ✅ Detected Framework: {intent.get('framework', 'N/A')}")
            print(f"  ✅ Detected Style: {intent.get('style', 'N/A')}")
            print(f"  ✅ Sections: {len(intent.get('sections', []))}")
            if intent.get('sections'):
                print(f"     {', '.join(intent['sections'][:5])}")
                if len(intent['sections']) > 5:
                    print(f"     ... and {len(intent['sections']) - 5} more")
    
    except Exception as e:
        build_info["errors"].append(f"Intent parsing failed: {str(e)}")
        if verbose:
            print(f"  ❌ Failed: {str(e)}")
        return False, build_info
    
    # Stage 2: Map Components
    if verbose:
        print("\nStage 2: 🗺️  Mapping Components...")
    
    try:
        component_registry = load_component_registry()
        component_mapping = map_sections_to_components(intent, component_registry)
        
        build_info["stages"]["component_mapping"] = {
            "success": True,
            "mapped_count": len(component_mapping)
        }
        
        if verbose:
            print(f"  ✅ Mapped {len(component_mapping)} components")
            for section_type, component_path in list(component_mapping.items())[:3]:
                print(f"     {section_type} → {Path(component_path).name}")
            if len(component_mapping) > 3:
                print(f"     ... and {len(component_mapping) - 3} more")
    
    except Exception as e:
        build_info["errors"].append(f"Component mapping failed: {str(e)}")
        if verbose:
            print(f"  ❌ Failed: {str(e)}")
        return False, build_info
    
    # Stage 3: Assemble Website
    if verbose:
        print("\nStage 3: 🔨 Assembling Website...")
    
    try:
        html_content = assemble_website(component_mapping, intent)
        
        build_info["stages"]["assembly"] = {
            "success": True,
            "html_size": len(html_content)
        }
        
        if verbose:
            size_kb = len(html_content) / 1024
            print(f"  ✅ Generated {size_kb:.2f} KB of HTML")
            print(f"  ✅ Complete HTML5 document with {len(component_mapping)} sections")
    
    except Exception as e:
        build_info["errors"].append(f"Assembly failed: {str(e)}")
        if verbose:
            print(f"  ❌ Failed: {str(e)}")
        return False, build_info
    
    # Stage 4: Visual Validation (Optional)
    validation_report = None
    if validate:
        if verbose:
            print("\nStage 4: 🔍 Visual Validation...")
        
        try:
            validation_report = validate_html_string(html_content, "temp_validation.html")
            
            build_info["stages"]["validation"] = {
                "success": True,
                "valid": validation_report["valid"],
                "issues_count": len(validation_report.get("issues", []))
            }
            
            if verbose:
                status = "✅ PASS" if validation_report["valid"] else "⚠️  ISSUES FOUND"
                print(f"  {status}")
                print(f"  Issues: {len(validation_report.get('issues', []))}")
                
                if validation_report.get("issues"):
                    # Show first 3 issues
                    for issue in validation_report["issues"][:3]:
                        severity_icon = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(
                            issue.get("severity", ""), "⚪"
                        )
                        print(f"    {severity_icon} {issue.get('description', 'Unknown issue')}")
                    
                    if len(validation_report["issues"]) > 3:
                        print(f"    ... and {len(validation_report['issues']) - 3} more")
        
        except Exception as e:
            build_info["errors"].append(f"Validation failed: {str(e)}")
            if verbose:
                print(f"  ⚠️  Validation skipped: {str(e)}")
    
    # Stage 5: Auto-Fix Issues (Optional)
    fix_report = None
    if auto_fix and validation_report and not validation_report["valid"]:
        if verbose:
            print("\nStage 5: 🔧 Auto-Fixing Issues...")
        
        try:
            html_content, fix_report = auto_fix_website(
                html_content,
                validation_report,
                max_attempts=3
            )
            
            build_info["stages"]["fixing"] = {
                "success": True,
                "fixes_applied": len(fix_report.get("fixes_applied", [])),
                "initial_issues": fix_report.get("initial_issues", 0),
                "final_issues": fix_report.get("final_issues", 0)
            }
            
            if verbose:
                print(f"  ✅ Applied {len(fix_report.get('fixes_applied', []))} fixes")
                print(f"  Issues: {fix_report.get('initial_issues', 0)} → {fix_report.get('final_issues', 0)}")
                
                # Show fixes
                for fix in fix_report.get("fixes_applied", [])[:3]:
                    print(f"    ✓ {fix}")
                
                if len(fix_report.get("fixes_applied", [])) > 3:
                    print(f"    ... and {len(fix_report['fixes_applied']) - 3} more")
        
        except Exception as e:
            build_info["errors"].append(f"Auto-fix failed: {str(e)}")
            if verbose:
                print(f"  ⚠️  Auto-fix skipped: {str(e)}")
    
    # Stage 6: Save Output
    if verbose:
        print("\nStage 6: 💾 Saving Output...")
    
    try:
        # Generate output filename
        if output_name:
            output_path = f"dist/{output_name}"
            if not output_path.endswith('.html'):
                output_path += '.html'
        else:
            # Generate from intent
            title = intent.get("metadata", {}).get("title", "")
            if title:
                # Clean title for filename
                clean_title = "".join(c if c.isalnum() or c in [' ', '-', '_'] else '' for c in title)
                clean_title = clean_title.replace(' ', '_').lower()
                output_path = f"dist/{clean_title}.html"
            else:
                output_path = f"dist/website_{int(time.time())}.html"
        
        success, msg = save_website(html_content, output_path, overwrite=False)
        
        if success:
            build_info["output_path"] = output_path
            build_info["stages"]["output"] = {
                "success": True,
                "path": output_path
            }
            
            if verbose:
                print(f"  ✅ {msg}")
                
                # Show file size
                file_size = Path(output_path).stat().st_size
                print(f"  📄 Size: {file_size / 1024:.2f} KB ({file_size:,} bytes)")
        else:
            build_info["errors"].append(f"Save failed: {msg}")
            if verbose:
                print(f"  ❌ {msg}")
            return False, build_info
    
    except Exception as e:
        build_info["errors"].append(f"Output save failed: {str(e)}")
        if verbose:
            print(f"  ❌ Failed: {str(e)}")
        return False, build_info
    
    # Calculate build time
    build_time = time.time() - start_time
    build_info["build_time"] = build_time
    build_info["success"] = True
    
    # Print final summary
    if verbose:
        summary = generate_summary(
            intent=intent,
            validation_report=validation_report,
            fix_report=fix_report,
            output_path=output_path,
            build_time=build_time
        )
        print(summary)
    
    return True, build_info


def main():
    """
    Main entry point for the Website Assembler CLI.
    
    Usage:
        python src/main.py "Build a portfolio for John Doe"
        python src/main.py "Create a modern landing page for a tech startup"
    """
    # Check command line arguments
    if len(sys.argv) < 2:
        print("\n" + "="*70)
        print("🏗️  TOSHOKAN-CODO - INTELLIGENT WEBSITE ASSEMBLER")
        print("="*70)
        print("\nUsage:")
        print("  python src/main.py \"<your website description>\"")
        print("\nExamples:")
        print("  python src/main.py \"Build a portfolio for Sarah Miller\"")
        print("  python src/main.py \"Create a modern landing page for TechStart\"")
        print("  python src/main.py \"Make a restaurant website with menu and contact\"")
        print("\nOptions:")
        print("  --output <name>     Custom output filename")
        print("  --no-validate       Skip validation")
        print("  --no-fix            Skip auto-fixing")
        print("  --quiet             Minimal output")
        print("\nFull Example:")
        print("  python src/main.py \"Build a portfolio\" --output my_portfolio --quiet")
        print("\n" + "="*70 + "\n")
        return
    
    # Parse arguments
    user_prompt = sys.argv[1]
    output_name = None
    validate = True
    auto_fix = True
    verbose = True
    
    # Parse flags
    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        
        if arg == "--output" and i + 1 < len(sys.argv):
            output_name = sys.argv[i + 1]
            i += 2
        elif arg == "--no-validate":
            validate = False
            i += 1
        elif arg == "--no-fix":
            auto_fix = False
            i += 1
        elif arg == "--quiet":
            verbose = False
            i += 1
        else:
            i += 1
    
    # Build the website
    success, build_info = build_website(
        user_prompt=user_prompt,
        output_name=output_name,
        auto_fix=auto_fix,
        validate=validate,
        verbose=verbose
    )
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
