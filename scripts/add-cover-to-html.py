#!/usr/bin/env python3
"""
Add a full-width cover image to HTML files dynamically.
This script injects a plain <img> tag for the cover image at the top of .book-container.
"""

import sys
import os
import re


def add_cover_to_html(html_file_path, book_name):
    """Add a full-width cover image to HTML file if available."""
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Check if cover image was copied by the build script
    book_output_dir = os.path.dirname(html_file_path)
    cover_dest = os.path.join(book_output_dir, "cover.jpg")

    if not os.path.exists(cover_dest):
        print(f"  ⚠️ No cover image found at {cover_dest}")
        return

    # Use the copied image in the HTML
    cover_html = f'<img src="cover.jpg" alt="Book Cover" style="width:100%;display:block;margin-bottom:2rem;">'

    # Insert the cover image at the top of .book-container
    pattern = r'(<div class="book-container">\s*)'
    replacement = r"\1" + cover_html + "\n"

    if re.search(pattern, html_content):
        new_html = re.sub(pattern, replacement, html_content)
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(new_html)
        print(f"  ✓ Added full-width cover image to {html_file_path}")
    else:
        print(f"  ⚠️ Could not find book-container div in {html_file_path}")


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 add-cover-to-html.py <html_file> <book_name>")
        sys.exit(1)
    html_file = sys.argv[1]
    book_name = sys.argv[2]
    if not os.path.exists(html_file):
        print(f"Error: HTML file {html_file} not found")
        sys.exit(1)
    add_cover_to_html(html_file, book_name)


if __name__ == "__main__":
    main()
