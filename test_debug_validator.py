"""Debug test for visual validator"""

from src.visual_validator import validate_html_string
import traceback

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

print("Testing Visual Validator with detailed error tracking...")
print("="*60)

try:
    report = validate_html_string(minimal_html, "debug_test.html")
    
    print("\n✅ Validation completed!")
    print(f"Valid: {report['valid']}")
    print(f"Issues found: {len(report['issues'])}")
    
    # Print each issue
    for i, issue in enumerate(report['issues'], 1):
        print(f"\nIssue {i}:")
        print(f"  Type: {issue.get('type')}")
        print(f"  Severity: {issue.get('severity')}")
        print(f"  Description: {issue.get('description')}")
    
except Exception as e:
    print(f"\n❌ Error occurred: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
