#!/usr/bin/env python3
"""
Generate a dynamic table of contents for HTML and PDF formats.
This script parses the markdown file to extract headings and creates a TOC.
"""

import re
import sys
import argparse
from pathlib import Path
from bs4 import BeautifulSoup
import html


def extract_headings_from_markdown(md_file):
    """Extract headings from markdown file and return a list of (level, text, id) tuples."""
    headings = []

    with open(md_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split into lines and process
    lines = content.split("\n")
    for line in lines:
        # Match markdown headings (# ## ### etc.)
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()

            # Remove leading number, dot, and spaces (e.g. '1. ', '2.3. ', etc.)
            text_for_id = re.sub(r"^\d+(?:\.\d+)*\.\s*", "", text)

            # Generate ID from text (to match Pandoc)
            id_text = re.sub(r"[^a-zA-Z0-9\s-]", "", text_for_id.lower())
            id_text = re.sub(r"\s+", "-", id_text)
            id_text = re.sub(r"-+", "-", id_text)
            id_text = id_text.strip("-")

            headings.append((level, text, id_text))

    return headings


def generate_toc_html(headings, title="Table of Contents"):
    """Generate HTML for the table of contents using divs, not ul/li."""
    if not headings:
        return ""

    toc_html = f'<div class="toc-container">\n'
    toc_html += f'  <h2 class="toc-title">{title}</h2>\n'
    toc_html += f'  <nav class="toc-nav">\n'

    for level, text, id_text in headings:
        toc_html += f'    <div class="toc-row toc-level-{level}"><a href="#{id_text}" class="toc-link">{html.escape(text)}</a></div>\n'

    toc_html += f"  </nav>\n"
    toc_html += f"</div>\n"

    return toc_html


def insert_toc_into_html(html_file, toc_html, toc_css, after_cover=True):
    """Insert the TOC into an HTML file after the cover image or at the beginning."""
    with open(html_file, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    # Find the book container
    book_container = soup.find("div", class_="book-container")
    if not book_container:
        print("Warning: Could not find book-container div")
        return False

    # Create the TOC element
    toc_soup = BeautifulSoup(toc_html, "html.parser")
    toc_element = toc_soup.find("div", class_="toc-container")

    if after_cover:
        # Insert after cover image if it exists
        cover_img = book_container.find("img", src=lambda x: x and "cover" in x)
        if cover_img:
            cover_img.insert_after(toc_element)
        else:
            # Insert after the first h1 if no cover image
            first_h1 = book_container.find("h1")
            if first_h1:
                first_h1.insert_after(toc_element)
            else:
                # Insert at the beginning of the container
                book_container.insert(0, toc_element)
    else:
        # Insert at the beginning of the container
        book_container.insert(0, toc_element)

    # Write the modified HTML back
    with open(html_file, "w", encoding="utf-8") as f:
        f.write(str(soup))

    return True


def main():
    parser = argparse.ArgumentParser(
        description="Generate dynamic table of contents for HTML and PDF"
    )
    parser.add_argument("markdown_file", help="Path to the markdown file")
    parser.add_argument("html_file", help="Path to the HTML file to modify")
    parser.add_argument(
        "--title", default="Table of Contents", help="Title for the TOC"
    )
    parser.add_argument(
        "--after-cover",
        action="store_true",
        default=True,
        help="Insert TOC after cover image (default: True)",
    )
    parser.add_argument(
        "--css-only", action="store_true", help="Only output CSS styles"
    )

    args = parser.parse_args()

    # Extract headings from markdown
    headings = extract_headings_from_markdown(args.markdown_file)

    if not headings:
        print("Warning: No headings found in markdown file")
        return

    # Generate TOC HTML (CSS is now in template files)
    toc_html = generate_toc_html(headings, args.title)

    if args.css_only:
        print("CSS styles are now in the template files (templates/afrinenglish.css)")
        return

    # Insert TOC into HTML file
    if insert_toc_into_html(args.html_file, toc_html, "", args.after_cover):
        print(f"✓ Successfully added TOC to {args.html_file}")
        print(f"  - Found {len(headings)} headings")
    else:
        print(f"✗ Failed to add TOC to {args.html_file}")
        sys.exit(1)


if __name__ == "__main__":
    main()
