#!/usr/bin/env python3
"""
Inject EPUB-specific styles into HTML files
Adds styles to override container constraints for EPUB format
"""

import sys
import os
import re
from pathlib import Path
import argparse


def inject_epub_styles(html_file_path):
    """
    Inject EPUB-specific styles into HTML file
    """
    try:
        # Read HTML content
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # EPUB-specific styles to inject
        epub_styles = """
<style type="text/css">
/* EPUB-specific overrides */
.book-container {
    max-width: none !important;
    border-radius: 0 !important;
    box-shadow: none !important;
    margin: 0 !important;
    padding: 0 !important;
}

/* Ensure content flows properly in EPUB */
body {
    margin: 0 !important;
    padding: 0 !important;
}

/* Remove any container constraints for EPUB */
.container, .content, .main {
    max-width: none !important;
    width: auto !important;
    margin: 0 !important;
    padding: 0 !important;
}
</style>
"""

        # Find the head tag and inject styles
        head_pattern = r"(<head[^>]*>)"
        if re.search(head_pattern, html_content):
            html_content = re.sub(
                head_pattern, r"\1\n  " + epub_styles.strip(), html_content
            )
            print(f"✓ Injected EPUB-specific styles into {html_file_path}")
        else:
            print(f"Warning: Could not find <head> tag in {html_file_path}")
            return False

        # Write updated HTML
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return True

    except Exception as e:
        print(f"Error injecting EPUB styles: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Inject EPUB-specific styles into HTML files"
    )
    parser.add_argument("html_file", help="HTML file to process")

    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    success = inject_epub_styles(args.html_file)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
