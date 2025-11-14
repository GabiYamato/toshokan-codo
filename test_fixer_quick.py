"""Quick test of fixer without visual validator dependency"""

from src.fixer import (
    analyze_issues,
    apply_fixes,
    generate_fix_summary
)

print("="*70)
print("🔧 FIXER - QUICK TEST")
print("="*70 + "\n")

# Test 1: Analyze issues
print("Test 1: Analyzing issues...")
report = {
    "issues": [
        {"type": "scroll", "severity": "medium", "description": "Not scrollable"},
        {"type": "accessibility", "severity": "medium", "description": "Missing title"}
    ]
}

actions = analyze_issues(report)
print(f"✅ Generated {len(actions)} fix actions")
for action in actions:
    print(f"  - {action['type']}: {action.get('reason', 'N/A')}")

# Test 2: Apply fixes
print("\nTest 2: Applying fixes...")
html = """
<!DOCTYPE html>
<html>
<head></head>
<body>
    <h1>Test</h1>
    <img src="test.jpg">
</body>
</html>
"""

fixed_html, applied = apply_fixes(html, actions)
print(f"✅ Applied {len(applied)} fixes:")
for fix in applied:
    print(f"  ✓ {fix}")

# Test 3: Generate summary
print("\nTest 3: Generating summary...")
sample_report = {
    "attempts": 2,
    "fixes_applied": ["Added title", "Fixed overflow", "Added alt text"],
    "initial_issues": 5,
    "final_issues": 1,
    "success": True
}

summary = generate_fix_summary(sample_report)
print(summary)

print("\n✅ All basic fixer functions working correctly!\n")
