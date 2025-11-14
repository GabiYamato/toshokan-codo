"""
End-to-End Tests for Website Assembler
Tests the complete workflow from user prompt to final output
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.main import build_website


class TestEndToEnd(unittest.TestCase):
    """Test complete website building workflow"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Clean up any previous test outputs
        dist_dir = Path("dist")
        if dist_dir.exists():
            for file in dist_dir.glob("test_*.html"):
                file.unlink()
    
    def test_simple_portfolio(self):
        """Test building a simple portfolio website"""
        success, build_info = build_website(
            user_prompt="Build a portfolio for John Doe",
            output_name="test_simple_portfolio",
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        self.assertTrue(build_info["success"], "Build info should indicate success")
        self.assertIsNotNone(build_info["output_path"], "Should have output path")
        
        # Check output file exists
        output_path = Path(build_info["output_path"])
        self.assertTrue(output_path.exists(), "Output file should exist")
        
        # Check file has content
        content = output_path.read_text(encoding='utf-8')
        self.assertGreater(len(content), 1000, "Should generate substantial HTML")
        self.assertIn("<!DOCTYPE html>", content, "Should be valid HTML5")
        self.assertIn("John Doe", content, "Should include person name")
    
    def test_landing_page_with_features(self):
        """Test building a landing page with specific features"""
        success, build_info = build_website(
            user_prompt="Create a modern landing page for TechStart with hero, features, and pricing sections",
            output_name="test_landing_page",
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Check all stages completed
        stages = build_info.get("stages", {})
        self.assertIn("intent_parsing", stages, "Should parse intent")
        self.assertIn("component_mapping", stages, "Should map components")
        self.assertIn("assembly", stages, "Should assemble website")
        
        # Check output
        output_path = Path(build_info["output_path"])
        content = output_path.read_text(encoding='utf-8')
        
        # Should include requested sections
        self.assertIn("TechStart", content, "Should include company name")
    
    def test_restaurant_website(self):
        """Test building a restaurant website"""
        success, build_info = build_website(
            user_prompt="Make a restaurant website with menu, gallery, and contact form",
            output_name="test_restaurant",
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Check stages
        self.assertEqual(build_info["stages"]["intent_parsing"]["success"], True)
        self.assertEqual(build_info["stages"]["component_mapping"]["success"], True)
        self.assertEqual(build_info["stages"]["assembly"]["success"], True)
        
        # Check component count
        mapped_count = build_info["stages"]["component_mapping"]["mapped_count"]
        self.assertGreater(mapped_count, 0, "Should map at least one component")
    
    def test_complete_workflow_with_validation(self):
        """Test complete workflow including validation"""
        success, build_info = build_website(
            user_prompt="Build a professional portfolio for Sarah Miller with about, projects, and contact sections",
            output_name="test_complete_workflow",
            auto_fix=True,
            validate=True,
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Check all stages present
        stages = build_info.get("stages", {})
        self.assertIn("intent_parsing", stages)
        self.assertIn("component_mapping", stages)
        self.assertIn("assembly", stages)
        self.assertIn("validation", stages)
        self.assertIn("output", stages)
        
        # Check validation ran
        validation = stages.get("validation", {})
        self.assertTrue(validation.get("success"), "Validation should run")
        
        # Check output quality
        output_path = Path(build_info["output_path"])
        content = output_path.read_text(encoding='utf-8')
        
        # Basic HTML structure
        self.assertIn("<html", content)
        self.assertIn("</html>", content)
        self.assertIn("<head", content)
        self.assertIn("</head>", content)
        self.assertIn("<body", content)
        self.assertIn("</body>", content)
        
        # Tailwind CSS included
        self.assertIn("tailwindcss", content.lower())
    
    def test_build_without_validation(self):
        """Test building without validation step"""
        success, build_info = build_website(
            user_prompt="Create a simple landing page",
            output_name="test_no_validation",
            validate=False,
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Validation stage should not exist
        stages = build_info.get("stages", {})
        self.assertNotIn("validation", stages, "Should skip validation")
        self.assertNotIn("fixing", stages, "Should skip fixing")
    
    def test_build_without_autofix(self):
        """Test building with validation but no auto-fix"""
        success, build_info = build_website(
            user_prompt="Build a portfolio",
            output_name="test_no_autofix",
            auto_fix=False,
            validate=True,
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Should have validation but not fixing
        stages = build_info.get("stages", {})
        self.assertIn("validation", stages, "Should validate")
        self.assertNotIn("fixing", stages, "Should not auto-fix")
    
    def test_custom_output_name(self):
        """Test using custom output filename"""
        custom_name = "test_custom_output"
        
        success, build_info = build_website(
            user_prompt="Build a portfolio",
            output_name=custom_name,
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Check output path contains custom name
        output_path = build_info["output_path"]
        self.assertIn(custom_name, output_path, "Should use custom name")
        
        # Check file exists
        self.assertTrue(Path(output_path).exists())
    
    def test_multiple_sections(self):
        """Test building website with many sections"""
        success, build_info = build_website(
            user_prompt="Create a complete business website with navigation, hero, about, features, pricing, testimonials, gallery, and contact sections",
            output_name="test_multiple_sections",
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Should map multiple components
        mapped_count = build_info["stages"]["component_mapping"]["mapped_count"]
        self.assertGreater(mapped_count, 3, "Should map multiple components")
        
        # Check output size is substantial
        html_size = build_info["stages"]["assembly"]["html_size"]
        self.assertGreater(html_size, 5000, "Should generate substantial HTML")
    
    def test_build_time_tracking(self):
        """Test that build time is tracked"""
        success, build_info = build_website(
            user_prompt="Build a simple portfolio",
            output_name="test_build_time",
            verbose=False
        )
        
        self.assertTrue(success, "Build should succeed")
        
        # Should have build time
        self.assertIn("build_time", build_info, "Should track build time")
        self.assertGreater(build_info["build_time"], 0, "Build time should be positive")
        self.assertLess(build_info["build_time"], 60, "Build should complete in reasonable time")
    
    def test_error_handling(self):
        """Test error handling with invalid input"""
        # Empty prompt should still work (will use defaults)
        success, build_info = build_website(
            user_prompt="",
            output_name="test_error_handling",
            verbose=False
        )
        
        # Should complete (intent parser handles empty prompts)
        # Just verify no crashes occurred
        self.assertIsInstance(build_info, dict, "Should return build info dict")


class TestWorkflowStages(unittest.TestCase):
    """Test individual workflow stages"""
    
    def test_intent_parsing_stage(self):
        """Test intent parsing stage completes"""
        success, build_info = build_website(
            user_prompt="Build a portfolio for Alex Chen",
            output_name="test_intent_stage",
            verbose=False
        )
        
        self.assertTrue(success)
        
        # Check intent parsing stage
        intent_stage = build_info["stages"]["intent_parsing"]
        self.assertTrue(intent_stage["success"])
        self.assertIn("data", intent_stage)
        
        # Check intent data structure
        intent = intent_stage["data"]
        self.assertIn("framework", intent)
        self.assertIn("sections", intent)
        self.assertIn("metadata", intent)
    
    def test_component_mapping_stage(self):
        """Test component mapping stage"""
        success, build_info = build_website(
            user_prompt="Create a landing page with hero and features",
            output_name="test_mapping_stage",
            verbose=False
        )
        
        self.assertTrue(success)
        
        # Check mapping stage
        mapping_stage = build_info["stages"]["component_mapping"]
        self.assertTrue(mapping_stage["success"])
        self.assertGreater(mapping_stage["mapped_count"], 0)
    
    def test_assembly_stage(self):
        """Test assembly stage"""
        success, build_info = build_website(
            user_prompt="Build a portfolio",
            output_name="test_assembly_stage",
            verbose=False
        )
        
        self.assertTrue(success)
        
        # Check assembly stage
        assembly_stage = build_info["stages"]["assembly"]
        self.assertTrue(assembly_stage["success"])
        self.assertGreater(assembly_stage["html_size"], 0)
    
    def test_output_stage(self):
        """Test output stage"""
        success, build_info = build_website(
            user_prompt="Build a portfolio",
            output_name="test_output_stage",
            verbose=False
        )
        
        self.assertTrue(success)
        
        # Check output stage
        output_stage = build_info["stages"]["output"]
        self.assertTrue(output_stage["success"])
        self.assertIn("path", output_stage)
        
        # Verify file exists
        self.assertTrue(Path(output_stage["path"]).exists())


def run_quick_test():
    """Quick test for verification"""
    print("\n" + "="*70)
    print("Running Quick End-to-End Test...")
    print("="*70 + "\n")
    
    # Test 1: Simple build
    print("Test 1: Simple Portfolio Build")
    success, build_info = build_website(
        user_prompt="Build a portfolio for Test User",
        output_name="test_quick_e2e",
        verbose=True
    )
    
    if success:
        print("\n✅ Quick E2E Test PASSED")
        return True
    else:
        print("\n❌ Quick E2E Test FAILED")
        print(f"Errors: {build_info.get('errors', [])}")
        return False


if __name__ == "__main__":
    # Run quick test or full suite
    if "--quick" in sys.argv:
        success = run_quick_test()
        sys.exit(0 if success else 1)
    else:
        unittest.main()
