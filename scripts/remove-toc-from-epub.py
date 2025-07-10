#!/usr/bin/env python3
"""
Remove table of contents from HTML files for EPUB generation.
This script removes the TOC container from HTML files.
"""

import sys
import os
import re
from bs4 import BeautifulSoup


def remove_toc_from_html(html_file_path):
    """Remove table of contents from HTML file."""
    with open(html_file_path, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Find and remove the TOC container
    toc_container = soup.find("div", class_="toc-container")
    if toc_container:
        toc_container.decompose()
        print(f"  ✓ Removed TOC from {html_file_path}")
    else:
        print(f"  ℹ️ No TOC found in {html_file_path}")

    # Write the modified HTML back
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 remove-toc-from-epub.py <html_file>")
        sys.exit(1)

    html_file = sys.argv[1]
    if not os.path.exists(html_file):
        print(f"Error: HTML file not found: {html_file}")
        sys.exit(1)

    remove_toc_from_html(html_file)


if __name__ == "__main__":
    main()
