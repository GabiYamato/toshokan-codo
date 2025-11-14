"""Quick test for visual validator"""

from src.visual_validator import validate_html_string, generate_validation_summary

# Test minimal HTML
minimal_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
</head>
<body>
    <h1>Hello World</h1>
    <p>This is a test</p>
</body>
</html>
"""

print("Testing Visual Validator...")
print("="*60)

try:
    report = validate_html_string(minimal_html, "quick_test.html")
    
    print("\n✅ Validation completed successfully!")
    print(f"Valid: {report['valid']}")
    print(f"Issues found: {len(report['issues'])}")
    print(f"Metrics: {report['metrics']}")
    
    print("\n" + "="*60)
    print("Summary:")
    print(generate_validation_summary(report))
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
