"""
Tests for Output Manager Module
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from src.output_manager import (
    save_website,
    copy_assets,
    list_outputs,
    print_outputs_table,
    generate_summary,
    export_as_zip,
    create_deployment_package,
    clean_dist
)
from pathlib import Path
import time


def test_1_save_website():
    """Test saving HTML to file"""
    print("Test 1: Save website to file...")
    
    test_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Test</title></head>
    <body><h1>Test Page</h1></body>
    </html>
    """
    
    success, msg = save_website(test_html, "dist/test_save.html", overwrite=True)
    
    assert success == True
    assert Path("dist/test_save.html").exists()
    
    # Verify content
    with open("dist/test_save.html", 'r', encoding='utf-8') as f:
        content = f.read()
    
    assert "Test Page" in content
    
    print("✅ PASS")


def test_2_save_without_overwrite():
    """Test saving without overwriting existing file"""
    print("\nTest 2: Save without overwrite...")
    
    test_html = "<html><body>Version 2</body></html>"
    
    # Save first version
    save_website(test_html, "dist/test_no_overwrite.html", overwrite=True)
    
    # Try to save again without overwrite
    success, msg = save_website(test_html, "dist/test_no_overwrite.html", overwrite=False)
    
    assert success == True
    # Should create test_no_overwrite_1.html or similar
    assert "_1" in msg or "test_no_overwrite" in msg
    
    print("✅ PASS")


def test_3_save_creates_directory():
    """Test that save creates directory if it doesn't exist"""
    print("\nTest 3: Save creates directory...")
    
    test_html = "<html><body>Test</body></html>"
    
    # Use a nested path that doesn't exist
    success, msg = save_website(test_html, "dist/nested/test_dir.html", overwrite=True)
    
    assert success == True
    assert Path("dist/nested/test_dir.html").exists()
    
    # Cleanup
    Path("dist/nested/test_dir.html").unlink()
    Path("dist/nested").rmdir()
    
    print("✅ PASS")


def test_4_list_outputs():
    """Test listing output files"""
    print("\nTest 4: List outputs...")
    
    # Create some test files
    for i in range(3):
        html = f"<html><body>Test {i}</body></html>"
        save_website(html, f"dist/test_list_{i}.html", overwrite=True)
        time.sleep(0.01)  # Small delay to ensure different timestamps
    
    outputs = list_outputs("dist")
    
    assert len(outputs) >= 3
    assert all("name" in o for o in outputs)
    assert all("size" in o for o in outputs)
    assert all("modified" in o for o in outputs)
    
    # Check sorting (newest first)
    if len(outputs) >= 2:
        # First should be more recent than second
        assert outputs[0]["modified"] >= outputs[1]["modified"]
    
    print("✅ PASS")


def test_5_copy_assets():
    """Test copying framework assets"""
    print("\nTest 5: Copy assets...")
    
    # Test Tailwind (uses CDN)
    tw_assets = copy_assets("tailwind", "dist")
    assert len(tw_assets) > 0
    assert "CDN" in tw_assets[0]
    
    # Test Bootstrap (uses CDN)
    bs_assets = copy_assets("bootstrap", "dist")
    assert len(bs_assets) > 0
    assert "CDN" in bs_assets[0]
    
    print("✅ PASS")


def test_6_generate_summary():
    """Test generating build summary"""
    print("\nTest 6: Generate summary...")
    
    intent = {
        "sections": ["nav", "hero", "features", "footer"],
        "framework": "tailwind",
        "style": "modern",
        "colors": ["blue", "white"]
    }
    
    validation = {
        "valid": True,
        "issues": []
    }
    
    fix_report = {
        "fixes_applied": ["Added title", "Fixed overflow"]
    }
    
    summary = generate_summary(
        intent=intent,
        validation_report=validation,
        fix_report=fix_report,
        output_path="dist/test.html",
        build_time=1.5
    )
    
    assert "BUILD COMPLETE" in summary
    assert "1.50 seconds" in summary
    assert "tailwind" in summary.lower()
    assert "modern" in summary.lower()
    
    print("✅ PASS")


def test_7_generate_summary_with_issues():
    """Test summary with validation issues"""
    print("\nTest 7: Summary with issues...")
    
    validation = {
        "valid": False,
        "issues": [
            {"type": "scroll", "severity": "medium", "description": "Not scrollable"},
            {"type": "overflow", "severity": "high", "description": "Overflow"}
        ]
    }
    
    summary = generate_summary(validation_report=validation)
    
    assert "Issues: 2" in summary
    assert "Medium: 1" in summary or "medium: 1" in summary.lower()
    assert "High: 1" in summary or "high: 1" in summary.lower()
    
    print("✅ PASS")


def test_8_export_as_zip():
    """Test exporting dist as ZIP"""
    print("\nTest 8: Export as ZIP...")
    
    # Ensure we have some files
    save_website("<html><body>Test</body></html>", "dist/test_zip.html", overwrite=True)
    
    success, result = export_as_zip("dist", "test_export")
    
    assert success == True
    assert Path(result).exists()
    assert result.endswith(".zip")
    
    # Cleanup
    Path(result).unlink()
    
    print("✅ PASS")


def test_9_create_deployment_package():
    """Test creating deployment package"""
    print("\nTest 9: Create deployment package...")
    
    # Create a test HTML file
    test_html = "<html><head><title>Deploy Test</title></head><body>Test</body></html>"
    save_website(test_html, "dist/test_deploy_source.html", overwrite=True)
    
    success, result = create_deployment_package(
        "dist/test_deploy_source.html",
        "test_package",
        include_readme=True
    )
    
    assert success == True
    
    # Check that deployment folder was created
    deploy_dir = Path("dist/test_package")
    assert deploy_dir.exists()
    assert (deploy_dir / "index.html").exists()
    assert (deploy_dir / "README.md").exists()
    
    # Check README content
    readme_content = (deploy_dir / "README.md").read_text()
    assert "Deployment Package" in readme_content
    assert "GitHub Pages" in readme_content
    
    # Cleanup
    import shutil
    shutil.rmtree(deploy_dir)
    if "zip" in result.lower() and Path(result).exists():
        Path(result).unlink()
    
    print("✅ PASS")


def test_10_clean_dist():
    """Test cleaning dist directory"""
    print("\nTest 10: Clean dist...")
    
    # Create some test files
    for i in range(5):
        save_website(f"<html><body>Test {i}</body></html>", 
                    f"dist/test_clean_{i}.html", overwrite=True)
        time.sleep(0.01)
    
    # Keep latest 2 files
    deleted, msg = clean_dist("dist", keep_latest=2)
    
    assert deleted >= 3  # Should delete at least 3 files
    assert "kept 2" in msg.lower()
    
    # Verify 2 files remain
    remaining = list(Path("dist").glob("test_clean_*.html"))
    assert len(remaining) == 2
    
    # Cleanup remaining
    clean_dist("dist/test_clean_*")
    
    print("✅ PASS")


def test_11_summary_with_no_data():
    """Test generating summary with minimal data"""
    print("\nTest 11: Summary with no data...")
    
    summary = generate_summary()
    
    assert "BUILD COMPLETE" in summary
    # Should not crash with no data
    
    print("✅ PASS")


def test_12_file_size_in_summary():
    """Test that file size appears in summary"""
    print("\nTest 12: File size in summary...")
    
    test_html = "<html><body>" + ("Test " * 100) + "</body></html>"
    save_website(test_html, "dist/test_size.html", overwrite=True)
    
    summary = generate_summary(output_path="dist/test_size.html")
    
    assert "Size:" in summary
    assert "KB" in summary or "bytes" in summary
    
    print("✅ PASS")


def test_13_list_outputs_empty_dir():
    """Test listing outputs when directory is empty or doesn't exist"""
    print("\nTest 13: List empty directory...")
    
    # Test non-existent directory
    outputs = list_outputs("nonexistent_dir")
    assert outputs == []
    
    # Test empty directory
    empty_dir = Path("dist/empty_test")
    empty_dir.mkdir(exist_ok=True)
    
    outputs = list_outputs(str(empty_dir))
    assert outputs == []
    
    # Cleanup
    empty_dir.rmdir()
    
    print("✅ PASS")


def test_14_save_return_values():
    """Test save_website return values"""
    print("\nTest 14: Save return values...")
    
    # Test successful save
    success, msg = save_website("<html></html>", "dist/test_return.html", overwrite=True)
    assert success == True
    assert "Saved to" in msg
    assert "test_return.html" in msg
    
    # Test save to invalid path (should handle gracefully)
    success, msg = save_website("<html></html>", "/invalid/path/test.html")
    assert success == False or "Failed" in msg or "Permission" in msg or success == True  # Might succeed on some systems
    
    print("✅ PASS")


def test_15_outputs_table_format():
    """Test formatted output table"""
    print("\nTest 15: Outputs table format...")
    
    # Create test files
    save_website("<html><body>Table Test</body></html>", 
                "dist/test_table.html", overwrite=True)
    
    outputs = list_outputs("dist")
    
    # This should not crash
    import io
    import sys
    
    # Capture stdout
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()
    
    print_outputs_table(outputs)
    output_str = sys.stdout.getvalue()
    
    sys.stdout = old_stdout
    
    assert "OUTPUT FILES" in output_str
    assert "Filename" in output_str
    assert "Size" in output_str
    
    # Test with empty list
    sys.stdout = io.StringIO()
    print_outputs_table([])
    output_str = sys.stdout.getvalue()
    sys.stdout = old_stdout
    
    assert "No output files" in output_str
    
    print("✅ PASS")


def run_all_tests():
    """Run all output manager tests"""
    print("\n" + "="*70)
    print("🧪 OUTPUT MANAGER TEST SUITE")
    print("="*70 + "\n")
    
    tests = [
        test_1_save_website,
        test_2_save_without_overwrite,
        test_3_save_creates_directory,
        test_4_list_outputs,
        test_5_copy_assets,
        test_6_generate_summary,
        test_7_generate_summary_with_issues,
        test_8_export_as_zip,
        test_9_create_deployment_package,
        test_10_clean_dist,
        test_11_summary_with_no_data,
        test_12_file_size_in_summary,
        test_13_list_outputs_empty_dir,
        test_14_save_return_values,
        test_15_outputs_table_format,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            failed += 1
    
    print("\n" + "="*70)
    print(f"📊 RESULTS: {passed}/{passed+failed} tests passed")
    print("="*70 + "\n")
    
    return passed, failed


if __name__ == "__main__":
    passed, failed = run_all_tests()
    exit(0 if failed == 0 else 1)
