#!/usr/bin/env python3
"""
Fix code block styling for PDF generation
Removes conflicting Prism CSS and ensures readable code blocks in PDF
"""

import sys
import os
from bs4 import BeautifulSoup
import argparse

PRISM_CSS_PATH = os.path.join(os.path.dirname(__file__), "prism-vsc-dark-plus.min.css")


def embed_prism_css(soup):
    """Embed Prism VSCode theme CSS into the HTML head."""
    if not os.path.exists(PRISM_CSS_PATH):
        print(f"Warning: Prism VSCode CSS not found at {PRISM_CSS_PATH}")
        return soup
    with open(PRISM_CSS_PATH, "r", encoding="utf-8") as f:
        css = f.read()
    style_tag = soup.new_tag("style")
    style_tag.string = css
    head = soup.find("head")
    if head:
        head.append(style_tag)
        print("✓ Embedded Prism VSCode CSS for PDF")
    return soup


def minimal_code_layout_css(soup):
    """Add minimal layout CSS for code blocks (no color overrides)."""
    layout_css = """
    <style>
    pre {
        padding: 1em;
        border-radius: 6px;
        overflow-x: auto;
        margin: 1.2em 0;
    }
    code:not(pre code) {
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-size: 0.97em;
        background: rgba(110, 118, 129, 0.15);
        color: inherit;
        border: none;
    }
    </style>
    """
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(layout_css, "html.parser"))
        print("✓ Added minimal code block layout CSS for PDF")
    return soup


def override_highlight_border(soup):
    """Add CSS to remove all external box styling from code blocks in PDF, but keep a little padding for readability."""
    override_css = """
    <style>
    .highlight, .highlight pre, pre {
        border: none !important;
        box-shadow: none !important;
        margin: 0.5em 0 !important;
        padding: 0.5em 1em !important;
        background-clip: padding-box !important;
        border-radius: 0.3em !important;
    }
    </style>
    """
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(override_css, "html.parser"))
        print(
            "✓ Removed external box from code snippets for PDF (with padding for readability)"
        )
    return soup


def remove_prism_links(html_content):
    """Remove Prism.js CSS/JS links from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    for link in soup.find_all("link", href=lambda x: x and "prism" in x.lower()):
        link.decompose()
    for script in soup.find_all("script", src=lambda x: x and "prism" in x.lower()):
        script.decompose()
    return str(soup)


def process_html_for_pdf(html_file_path):
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    # Remove Prism CDN links
    html_content = remove_prism_links(html_content)
    soup = BeautifulSoup(html_content, "html.parser")
    # Embed Prism VSCode CSS
    soup = embed_prism_css(soup)
    # Add minimal layout CSS
    soup = minimal_code_layout_css(soup)
    # Remove highlight border
    soup = override_highlight_border(soup)
    # Write the processed HTML
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"✓ Fixed code blocks for PDF: {html_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fix code block styling for PDF generation (Prism VSCode theme)"
    )
    parser.add_argument("html_file", help="HTML file to process")
    args = parser.parse_args()
    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)
    process_html_for_pdf(args.html_file)


if __name__ == "__main__":
    main()
