"""Manual test of visual validator"""

from src.visual_validator import validate_layout, generate_validation_summary
from pathlib import Path

print("Testing Visual Validator on Generated Websites")
print("="*70 + "\n")

dist_path = Path("dist")
html_files = list(dist_path.glob("*.html"))

if html_files:
    test_file = html_files[0]
    print(f"Testing: {test_file.name}\n")
    
    report = validate_layout(str(test_file))
    summary = generate_validation_summary(report)
    
    print(summary)
    print("\n✅ Visual Validator is working!\n")
    
    # Print report details
    print("Report Details:")
    print(f"  Valid: {report['valid']}")
    print(f"  Total Issues: {len(report['issues'])}")
    print(f"  Metrics: {report['metrics']}")
    
else:
    print("No HTML files found in dist/")
