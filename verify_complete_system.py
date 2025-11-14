"""
Quick verification script for the complete Website Assembler system.
Tests the full end-to-end workflow.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.main import build_website


def verify_system():
    """Run verification tests"""
    print("\n" + "="*70)
    print("🔍 COMPLETE SYSTEM VERIFICATION")
    print("="*70 + "\n")
    
    tests_passed = 0
    tests_failed = 0
    
    # Test 1: Simple Portfolio
    print("Test 1: Simple Portfolio Build")
    print("-" * 70)
    try:
        success, build_info = build_website(
            user_prompt="Build a portfolio for John Doe",
            output_name="verify_simple_portfolio",
            verbose=False
        )
        
        if success and build_info["success"]:
            output_file = Path(build_info["output_path"])
            if output_file.exists():
                size = output_file.stat().st_size
                print(f"✅ PASS - Generated {size:,} bytes")
                tests_passed += 1
            else:
                print(f"❌ FAIL - Output file not found")
                tests_failed += 1
        else:
            print(f"❌ FAIL - Build unsuccessful")
            print(f"   Errors: {build_info.get('errors', [])}")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        tests_failed += 1
    
    print()
    
    # Test 2: Landing Page with Validation
    print("Test 2: Landing Page with Validation")
    print("-" * 70)
    try:
        success, build_info = build_website(
            user_prompt="Create a modern landing page for TechStart with hero, features, and pricing",
            output_name="verify_landing_page",
            auto_fix=True,
            validate=True,
            verbose=False
        )
        
        if success:
            stages = build_info.get("stages", {})
            
            # Check all expected stages
            expected_stages = ["intent_parsing", "component_mapping", "assembly", "validation", "output"]
            missing_stages = [s for s in expected_stages if s not in stages]
            
            if not missing_stages:
                validation = stages.get("validation", {})
                print(f"✅ PASS - All stages completed")
                print(f"   Valid: {validation.get('valid', False)}")
                print(f"   Issues: {validation.get('issues_count', 0)}")
                tests_passed += 1
            else:
                print(f"❌ FAIL - Missing stages: {missing_stages}")
                tests_failed += 1
        else:
            print(f"❌ FAIL - Build unsuccessful")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        tests_failed += 1
    
    print()
    
    # Test 3: Multiple Sections
    print("Test 3: Website with Multiple Sections")
    print("-" * 70)
    try:
        success, build_info = build_website(
            user_prompt="Create a complete website with navigation, hero, about, features, gallery, testimonials, and contact sections",
            output_name="verify_multiple_sections",
            verbose=False
        )
        
        if success:
            mapped_count = build_info["stages"]["component_mapping"]["mapped_count"]
            html_size = build_info["stages"]["assembly"]["html_size"]
            
            if mapped_count >= 5 and html_size > 10000:
                print(f"✅ PASS - {mapped_count} components, {html_size:,} bytes")
                tests_passed += 1
            else:
                print(f"❌ FAIL - Too few components ({mapped_count}) or small size ({html_size})")
                tests_failed += 1
        else:
            print(f"❌ FAIL - Build unsuccessful")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        tests_failed += 1
    
    print()
    
    # Test 4: Build Time Performance
    print("Test 4: Build Time Performance")
    print("-" * 70)
    try:
        success, build_info = build_website(
            user_prompt="Build a portfolio",
            output_name="verify_performance",
            verbose=False
        )
        
        if success:
            build_time = build_info.get("build_time", 999)
            
            if build_time < 30:  # Should complete in under 30 seconds
                print(f"✅ PASS - Completed in {build_time:.2f}s")
                tests_passed += 1
            else:
                print(f"❌ FAIL - Too slow ({build_time:.2f}s)")
                tests_failed += 1
        else:
            print(f"❌ FAIL - Build unsuccessful")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        tests_failed += 1
    
    print()
    
    # Test 5: Output File Quality
    print("Test 5: Output File Quality Check")
    print("-" * 70)
    try:
        success, build_info = build_website(
            user_prompt="Build a professional portfolio for Sarah Miller",
            output_name="verify_quality",
            verbose=False
        )
        
        if success:
            output_file = Path(build_info["output_path"])
            content = output_file.read_text(encoding='utf-8')
            
            # Check for essential HTML structure
            checks = {
                "DOCTYPE": "<!DOCTYPE html>" in content,
                "HTML tags": "<html" in content and "</html>" in content,
                "Head section": "<head" in content and "</head>" in content,
                "Body section": "<body" in content and "</body>" in content,
                "Tailwind CSS": "tailwindcss" in content.lower(),
                "Content": "Sarah Miller" in content
            }
            
            passed_checks = sum(checks.values())
            total_checks = len(checks)
            
            if passed_checks == total_checks:
                print(f"✅ PASS - All {total_checks} quality checks passed")
                tests_passed += 1
            else:
                print(f"❌ FAIL - {passed_checks}/{total_checks} checks passed")
                for check, result in checks.items():
                    status = "✓" if result else "✗"
                    print(f"   {status} {check}")
                tests_failed += 1
        else:
            print(f"❌ FAIL - Build unsuccessful")
            tests_failed += 1
    except Exception as e:
        print(f"❌ FAIL - Exception: {str(e)}")
        tests_failed += 1
    
    # Final Summary
    print("\n" + "="*70)
    print("VERIFICATION SUMMARY")
    print("="*70)
    print(f"✅ Passed: {tests_passed}")
    print(f"❌ Failed: {tests_failed}")
    print(f"📊 Total:  {tests_passed + tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 ALL TESTS PASSED - System is fully operational!")
        return True
    else:
        print(f"\n⚠️  {tests_failed} test(s) failed - Please review")
        return False


if __name__ == "__main__":
    success = verify_system()
    sys.exit(0 if success else 1)
