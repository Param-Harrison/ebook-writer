#!/usr/bin/env python3
"""
Fix Mermaid diagrams and syntax highlighting for all formats
Ensures diagrams and code highlighting work in PDF, EPUB, and MOBI
"""

import sys
import os
import re
from bs4 import BeautifulSoup
import argparse


def fix_mermaid_diagrams(html_content):
    """Fix Mermaid diagrams to work in all formats"""

    # Find all Mermaid diagrams
    soup = BeautifulSoup(html_content, "html.parser")

    # Find all pre tags with mermaid class
    mermaid_blocks = soup.find_all("pre", class_="mermaid")

    for block in mermaid_blocks:
        # Get the Mermaid code
        mermaid_code = block.get_text().strip()

        # Create a simple text representation for non-interactive formats
        # This will be a fallback for PDF/EPUB/MOBI where Mermaid doesn't render
        text_fallback = f"""
<div class="mermaid-fallback">
<h4>Diagram</h4>
<pre>{mermaid_code}</pre>
<p><em>Note: This is a Mermaid diagram. View in HTML format for interactive rendering.</em></p>
</div>
"""

        # Replace the mermaid block with both interactive and fallback versions
        new_div = soup.new_tag("div")
        new_div["class"] = "mermaid-container"

        # Keep the original for HTML
        original_div = soup.new_tag("div")
        original_div["class"] = "mermaid-interactive"
        original_div.append(block)

        # Add fallback for other formats
        fallback_div = soup.new_tag("div")
        fallback_div["class"] = "mermaid-fallback"
        fallback_div["style"] = "display: none;"
        fallback_div.append(BeautifulSoup(text_fallback, "html.parser"))

        new_div.append(original_div)
        new_div.append(fallback_div)

        # Replace the original block
        block.replace_with(new_div)

    return str(soup)


def fix_syntax_highlighting(html_content):
    """Fix syntax highlighting to work in all formats"""

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all code blocks
    code_blocks = soup.find_all("pre")

    for block in code_blocks:
        # Skip if it's a mermaid block (handled separately)
        if "mermaid" in block.get("class", []):
            continue

        # Get the language class
        language = None
        for cls in block.get("class", []):
            if cls.startswith("language-"):
                language = cls.replace("language-", "")
                break

        # Add fallback styling for non-interactive formats
        block["class"] = block.get("class", []) + ["code-block"]

        # Add language indicator
        if language:
            # Create a header for the code block
            header = soup.new_tag("div")
            header["class"] = "code-header"
            header["style"] = (
                "background: #f6f8fa; padding: 8px 16px; border-bottom: 1px solid #e1e4e8; font-size: 12px; color: #586069;"
            )
            header.string = f"Language: {language.upper()}"

            # Wrap the code block
            wrapper = soup.new_tag("div")
            wrapper["class"] = "code-wrapper"
            wrapper["style"] = (
                "border: 1px solid #e1e4e8; border-radius: 6px; margin: 1em 0;"
            )

            # Move the block into the wrapper
            block.wrap(wrapper)
            wrapper.insert(0, header)

    return str(soup)


def add_format_specific_css(html_content, format_type):
    """Add format-specific CSS for better compatibility"""

    if format_type == "pdf":
        # Add CSS to show fallbacks in PDF
        css_addition = """
        <style>
        .mermaid-interactive { display: none; }
        .mermaid-fallback { display: block !important; }
        .code-wrapper { page-break-inside: avoid; }
        </style>
        """
    elif format_type in ["epub", "mobi"]:
        # Add CSS to show fallbacks in EPUB/MOBI
        css_addition = """
        <style>
        .mermaid-interactive { display: none; }
        .mermaid-fallback { display: block !important; }
        </style>
        """
    else:
        # For HTML, show interactive versions
        css_addition = """
        <style>
        .mermaid-interactive { display: block; }
        .mermaid-fallback { display: none; }
        </style>
        """

    # Insert the CSS in the head
    soup = BeautifulSoup(html_content, "html.parser")
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(css_addition, "html.parser"))

    return str(soup)


def process_html_file(html_file_path, format_type="html"):
    """Process HTML file to fix Mermaid and syntax highlighting"""

    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Fix Mermaid diagrams
    html_content = fix_mermaid_diagrams(html_content)

    # Fix syntax highlighting
    html_content = fix_syntax_highlighting(html_content)

    # Add format-specific CSS
    html_content = add_format_specific_css(html_content, format_type)

    # Write the processed HTML
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✓ Fixed Mermaid and syntax highlighting for {format_type}")


def main():
    parser = argparse.ArgumentParser(
        description="Fix Mermaid diagrams and syntax highlighting"
    )
    parser.add_argument("html_file", help="HTML file to process")
    parser.add_argument(
        "--format",
        default="html",
        choices=["html", "pdf", "epub", "mobi"],
        help="Target format for processing",
    )

    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    process_html_file(args.html_file, args.format)


if __name__ == "__main__":
    main()
