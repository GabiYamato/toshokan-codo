"""
Output Manager Module
Handles final output, saving, and preview of assembled websites.

Responsibilities:
- Save final HTML to /dist/ directory
- Copy necessary assets (CSS, JS, images)
- Provide local preview server
- Generate summary report
- Export options (ZIP, deploy-ready package)
- Print formatted status and fix summary
"""

import os
import http.server
import socketserver
import threading
import webbrowser
from pathlib import Path
from datetime import datetime
import shutil
import zipfile
from typing import Dict, List, Optional, Tuple


def save_website(html_content: str, output_path: str, overwrite: bool = False) -> Tuple[bool, str]:
    """
    Save final HTML content to file.
    
    Args:
        html_content: Complete HTML content
        output_path: Path to save the file
        overwrite: Whether to overwrite existing file
        
    Returns:
        Tuple of (success, message)
    """
    try:
        output_file = Path(output_path)
        
        # Create parent directory if it doesn't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Check if file exists and handle overwrite
        if output_file.exists() and not overwrite:
            # Generate unique filename
            counter = 1
            stem = output_file.stem
            while output_file.exists():
                output_file = output_file.parent / f"{stem}_{counter}{output_file.suffix}"
                counter += 1
        
        # Save the file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return True, f"Saved to {output_file}"
        
    except Exception as e:
        return False, f"Failed to save: {str(e)}"


def copy_assets(framework: str, dist_path: str) -> List[str]:
    """
    Copy necessary framework assets to dist folder.
    
    Args:
        framework: Name of UI framework used
        dist_path: Path to dist directory
        
    Returns:
        List of copied asset paths
    """
    copied_assets = []
    
    # For now, Tailwind and Bootstrap use CDN, so no assets to copy
    # This function is a placeholder for future local asset support
    
    if framework.lower() in ["tailwind", "tw"]:
        # Tailwind uses CDN in our implementation
        copied_assets.append("Using Tailwind CDN (no local assets)")
        
    elif framework.lower() in ["bootstrap", "bs5"]:
        # Bootstrap uses CDN in our implementation
        copied_assets.append("Using Bootstrap CDN (no local assets)")
    
    return copied_assets


def start_preview_server(dist_path: str = "dist", port: int = 8000, open_browser: bool = True) -> Tuple[bool, str]:
    """
    Start a local HTTP server to preview the website.
    
    Args:
        dist_path: Path to dist directory
        port: Port number for server
        open_browser: Whether to open browser automatically
        
    Returns:
        Tuple of (success, message)
    """
    try:
        dist_dir = Path(dist_path)
        
        if not dist_dir.exists():
            return False, f"Directory {dist_path} does not exist"
        
        # Change to dist directory
        os.chdir(dist_dir)
        
        # Create handler
        Handler = http.server.SimpleHTTPRequestHandler
        
        # Try to start server on specified port, increment if busy
        max_attempts = 10
        current_port = port
        
        for attempt in range(max_attempts):
            try:
                httpd = socketserver.TCPServer(("", current_port), Handler)
                break
            except OSError:
                current_port += 1
        else:
            return False, f"Could not find available port between {port} and {port + max_attempts}"
        
        # Start server in background thread
        server_thread = threading.Thread(target=httpd.serve_forever, daemon=True)
        server_thread.start()
        
        url = f"http://localhost:{current_port}"
        
        # Open browser if requested
        if open_browser:
            webbrowser.open(url)
        
        return True, f"Server running at {url} (Press Ctrl+C to stop)"
        
    except Exception as e:
        return False, f"Failed to start server: {str(e)}"


def generate_summary(
    intent: Dict = None,
    validation_report: Dict = None,
    fix_report: Dict = None,
    output_path: str = None,
    build_time: float = None
) -> str:
    """
    Generate a formatted summary of the build process.
    
    Args:
        intent: Original parsed intent
        validation_report: Final validation report
        fix_report: Fix report from fixer
        output_path: Path where file was saved
        build_time: Time taken to build (seconds)
        
    Returns:
        Formatted summary string
    """
    summary = []
    summary.append("\n" + "="*70)
    summary.append("🎉 WEBSITE BUILD COMPLETE")
    summary.append("="*70)
    
    # Build info
    if build_time is not None:
        summary.append(f"\n⏱️  Build Time: {build_time:.2f} seconds")
    
    # Intent summary
    if intent:
        summary.append("\n📝 Intent:")
        if intent.get("sections"):
            summary.append(f"   Sections: {', '.join(intent['sections'][:5])}")
            if len(intent['sections']) > 5:
                summary.append(f"   ... and {len(intent['sections']) - 5} more")
        if intent.get("framework"):
            summary.append(f"   Framework: {intent['framework']}")
        if intent.get("style"):
            summary.append(f"   Style: {intent['style']}")
        if intent.get("colors"):
            summary.append(f"   Colors: {', '.join(intent['colors'])}")
    
    # Validation summary
    if validation_report:
        summary.append("\n🔍 Validation:")
        status = "✅ PASS" if validation_report.get("valid") else "⚠️  ISSUES FOUND"
        summary.append(f"   Status: {status}")
        
        issues = validation_report.get("issues", [])
        if issues:
            summary.append(f"   Issues: {len(issues)}")
            
            # Group by severity
            by_severity = {}
            for issue in issues:
                sev = issue.get("severity", "unknown")
                by_severity[sev] = by_severity.get(sev, 0) + 1
            
            for severity, count in sorted(by_severity.items()):
                summary.append(f"     {severity.title()}: {count}")
        else:
            summary.append("   Issues: None")
    
    # Fix summary
    if fix_report:
        summary.append("\n🔧 Fixes Applied:")
        fixes = fix_report.get("fixes_applied", [])
        if fixes:
            for fix in fixes[:5]:
                summary.append(f"   ✓ {fix}")
            if len(fixes) > 5:
                summary.append(f"   ... and {len(fixes) - 5} more")
        else:
            summary.append("   No fixes needed")
    
    # Output info
    if output_path:
        summary.append(f"\n📄 Output File:")
        summary.append(f"   {output_path}")
        
        # File size
        try:
            size = Path(output_path).stat().st_size
            size_kb = size / 1024
            summary.append(f"   Size: {size_kb:.2f} KB ({size:,} bytes)")
        except:
            pass
    
    summary.append("\n" + "="*70 + "\n")
    
    return "\n".join(summary)


def export_as_zip(dist_path: str = "dist", output_name: str = "website") -> Tuple[bool, str]:
    """
    Export dist directory as a ZIP file.
    
    Args:
        dist_path: Path to dist directory
        output_name: Name for the ZIP file (without .zip)
        
    Returns:
        Tuple of (success, message/path)
    """
    try:
        dist_dir = Path(dist_path)
        
        if not dist_dir.exists():
            return False, f"Directory {dist_path} does not exist"
        
        # Create ZIP file
        zip_path = dist_dir.parent / f"{output_name}.zip"
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files from dist
            for file in dist_dir.rglob('*'):
                if file.is_file():
                    arcname = file.relative_to(dist_dir.parent)
                    zipf.write(file, arcname)
        
        return True, str(zip_path)
        
    except Exception as e:
        return False, f"Failed to create ZIP: {str(e)}"


def create_deployment_package(
    html_path: str,
    package_name: str = "deploy",
    include_readme: bool = True
) -> Tuple[bool, str]:
    """
    Create a deployment-ready package with README and instructions.
    
    Args:
        html_path: Path to the HTML file
        package_name: Name for the deployment package
        include_readme: Whether to include deployment README
        
    Returns:
        Tuple of (success, message/path)
    """
    try:
        html_file = Path(html_path)
        
        if not html_file.exists():
            return False, f"File {html_path} does not exist"
        
        # Create deployment directory
        deploy_dir = html_file.parent / package_name
        deploy_dir.mkdir(exist_ok=True)
        
        # Copy HTML file as index.html
        shutil.copy(html_file, deploy_dir / "index.html")
        
        # Create README if requested
        if include_readme:
            readme_content = f"""# Website Deployment Package

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Files

- `index.html` - Your complete website

## Deployment Options

### Option 1: GitHub Pages
1. Create a new repository on GitHub
2. Upload this folder's contents
3. Go to Settings → Pages
4. Select branch and /root folder
5. Your site will be live at `https://username.github.io/repo-name`

### Option 2: Netlify
1. Go to https://netlify.com
2. Drag and drop this folder
3. Your site will be deployed instantly

### Option 3: Vercel
1. Go to https://vercel.com
2. Import this folder
3. Deploy with one click

### Option 4: Traditional Hosting
1. Upload `index.html` to your web server
2. Ensure it's in the public_html or www directory
3. Access via your domain

## Local Testing

To test locally:
```bash
python3 -m http.server 8000
```

Then open http://localhost:8000 in your browser.

## Notes

- This website uses CDN-hosted frameworks (no local dependencies needed)
- The HTML is self-contained and ready to deploy
- No build process required

Enjoy your new website! 🎉
"""
            with open(deploy_dir / "README.md", 'w', encoding='utf-8') as f:
                f.write(readme_content)
        
        # Create ZIP of deployment package
        success, zip_path = export_as_zip(str(deploy_dir), f"{package_name}_package")
        
        if success:
            return True, f"Deployment package created: {zip_path}"
        else:
            return True, f"Deployment folder created: {deploy_dir}"
        
    except Exception as e:
        return False, f"Failed to create deployment package: {str(e)}"


def list_outputs(dist_path: str = "dist") -> List[Dict[str, str]]:
    """
    List all HTML files in the output directory.
    
    Args:
        dist_path: Path to dist directory
        
    Returns:
        List of file information dictionaries
    """
    outputs = []
    
    dist_dir = Path(dist_path)
    
    if not dist_dir.exists():
        return outputs
    
    for html_file in dist_dir.glob("*.html"):
        stat = html_file.stat()
        
        outputs.append({
            "name": html_file.name,
            "path": str(html_file),
            "size": stat.st_size,
            "size_kb": stat.st_size / 1024,
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
        })
    
    # Sort by modification time (newest first)
    outputs.sort(key=lambda x: x["modified"], reverse=True)
    
    return outputs


def print_outputs_table(outputs: List[Dict[str, str]]) -> None:
    """
    Print a formatted table of output files.
    
    Args:
        outputs: List of file information from list_outputs()
    """
    if not outputs:
        print("\nNo output files found in dist/\n")
        return
    
    print("\n" + "="*70)
    print("📁 OUTPUT FILES")
    print("="*70)
    print(f"\n{'Filename':<30} {'Size':>10} {'Modified':>20}")
    print("-" * 70)
    
    for output in outputs:
        name = output["name"]
        size = f"{output['size_kb']:.1f} KB"
        modified = output["modified"]
        
        # Truncate long filenames
        if len(name) > 28:
            name = name[:25] + "..."
        
        print(f"{name:<30} {size:>10} {modified:>20}")
    
    print("-" * 70)
    print(f"Total: {len(outputs)} file(s)\n")


def clean_dist(dist_path: str = "dist", keep_latest: int = 0) -> Tuple[int, str]:
    """
    Clean up old files from dist directory.
    
    Args:
        dist_path: Path to dist directory
        keep_latest: Number of latest files to keep (0 = delete all)
        
    Returns:
        Tuple of (files_deleted, message)
    """
    try:
        dist_dir = Path(dist_path)
        
        if not dist_dir.exists():
            return 0, f"Directory {dist_path} does not exist"
        
        # Get all HTML files
        html_files = list(dist_dir.glob("*.html"))
        
        if not html_files:
            return 0, "No HTML files to clean"
        
        # Sort by modification time
        html_files.sort(key=lambda f: f.stat().st_mtime, reverse=True)
        
        # Determine files to delete
        if keep_latest > 0:
            to_delete = html_files[keep_latest:]
        else:
            to_delete = html_files
        
        # Delete files
        deleted = 0
        for file in to_delete:
            try:
                file.unlink()
                deleted += 1
            except:
                pass
        
        if keep_latest > 0:
            return deleted, f"Deleted {deleted} old file(s), kept {min(keep_latest, len(html_files))} latest"
        else:
            return deleted, f"Deleted {deleted} file(s)"
        
    except Exception as e:
        return 0, f"Failed to clean: {str(e)}"


# Test function for development
def test_output_manager():
    """Test the output manager functions"""
    print("📦 Testing Output Manager\n" + "="*70 + "\n")
    
    # Test 1: Save website
    print("Test 1: Saving website...")
    test_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Output</title>
    </head>
    <body>
        <h1>Output Manager Test</h1>
        <p>This is a test file.</p>
    </body>
    </html>
    """
    
    success, msg = save_website(test_html, "dist/output_test.html", overwrite=True)
    print(f"{'✅' if success else '❌'} {msg}\n")
    
    # Test 2: List outputs
    print("Test 2: Listing output files...")
    outputs = list_outputs("dist")
    print_outputs_table(outputs)
    
    # Test 3: Generate summary
    print("Test 3: Generating summary...")
    sample_intent = {
        "sections": ["nav", "hero", "features", "footer"],
        "framework": "tailwind",
        "style": "modern",
        "colors": ["blue", "white"]
    }
    
    sample_validation = {
        "valid": True,
        "issues": [],
        "metrics": {"page_height": 2400}
    }
    
    summary = generate_summary(
        intent=sample_intent,
        validation_report=sample_validation,
        output_path="dist/output_test.html",
        build_time=1.23
    )
    print(summary)
    
    # Test 4: Create deployment package
    print("Test 4: Creating deployment package...")
    if outputs:
        success, msg = create_deployment_package(outputs[0]["path"], "test_deploy")
        print(f"{'✅' if success else '❌'} {msg}\n")


if __name__ == "__main__":
    test_output_manager()
