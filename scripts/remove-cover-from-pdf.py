#!/usr/bin/env python3
"""
Remove cover images from HTML files for PDF generation.
This script removes the cover image img tag from HTML files.
"""

import sys
import os
import re


def remove_cover_from_html(html_file_path):
    """Remove cover image from HTML file."""
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Remove the cover image img tag - more generic pattern
    patterns = [
        # Pattern 1: Exact match for cover.jpg
        r'<img[^>]*src="cover\.jpg"[^>]*>',
        # Pattern 2: Any img tag with cover.jpg in src (more flexible)
        r'<img[^>]*src="[^"]*cover\.jpg[^"]*"[^>]*>',
        # Pattern 3: Any img tag with "Book Cover" alt text
        r'<img[^>]*alt="[^"]*Book Cover[^"]*"[^>]*>',
        # Pattern 4: Any img tag with both cover.jpg and Book Cover
        r'<img[^>]*src="[^"]*cover\.jpg[^"]*"[^>]*alt="[^"]*Book Cover[^"]*"[^>]*>',
    ]

    new_content = html_content
    for pattern in patterns:
        new_content = re.sub(pattern, "", new_content, flags=re.IGNORECASE)

    if new_content != html_content:
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"  ✓ Removed cover image from {html_file_path}")
    else:
        print(f"  ℹ️ No cover image found in {html_file_path}")


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 remove-cover-from-pdf.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]

    if not os.path.exists(html_file):
        print(f"Error: HTML file {html_file} not found")
        sys.exit(1)

    remove_cover_from_html(html_file)


if __name__ == "__main__":
    main()
