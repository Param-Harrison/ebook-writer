#!/usr/bin/env python3
"""
EPUB generation script using pandoc with custom styling
Creates EPUB files with preserved CSS styles and proper metadata
"""

import sys
import os
import json
import subprocess
import argparse
from pathlib import Path
from bs4 import BeautifulSoup


def get_book_metadata(book_name, config_file="books/book-config.json"):
    """Get book metadata from configuration file"""
    try:
        with open(config_file, "r") as f:
            config = json.load(f)

        book_config = config.get("books", {}).get(book_name, {})
        template_config = config.get("templates", {}).get(
            book_config.get("template", "afrinenglish"), {}
        )

        return {
            "title": book_config.get("title", "Unknown Title"),
            "author": book_config.get("author", "Unknown Author"),
            "template": book_config.get("template", "afrinenglish"),
            "css_file": template_config.get("css", "afrinenglish.css"),
            "html_file": template_config.get("html", "afrinenglish.html"),
            "category": book_config.get("category", "general"),
            "description": book_config.get("description", ""),
        }
    except Exception as e:
        print(f"Warning: Could not read book config: {e}")
        return {
            "title": book_name,
            "author": "Unknown Author",
            "template": "afrinenglish",
            "css_file": "afrinenglish.css",
            "html_file": "afrinenglish.html",
            "category": "general",
            "description": "",
        }


def create_epub_css(css_file_path, output_css_path):
    """Create EPUB-optimized CSS file"""
    if not os.path.exists(css_file_path):
        print(f"Warning: CSS file not found: {css_file_path}")
        return None

    with open(css_file_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    # Add EPUB-specific CSS adjustments
    epub_css_adjustments = """
    /* EPUB-specific adjustments */
    body {
        font-family: serif;
        line-height: 1.6;
        margin: 1em;
    }
    
    /* Ensure code blocks are readable */
    pre, code {
        font-family: monospace;
        background-color: #f5f5f5;
        border: 1px solid #ddd;
        padding: 0.5em;
        border-radius: 3px;
        overflow-x: auto;
    }
    
    /* Ensure images scale properly */
    img {
        max-width: 100%;
        height: auto;
    }
    
    /* Better heading hierarchy */
    h1, h2, h3, h4, h5, h6 {
        margin-top: 1.5em;
        margin-bottom: 0.5em;
    }
    
    /* Better list formatting */
    ul, ol {
        margin-left: 1.5em;
    }
    
    /* Ensure tables are readable */
    table {
        border-collapse: collapse;
        width: 100%;
        margin: 1em 0;
    }
    
    th, td {
        border: 1px solid #ddd;
        padding: 0.5em;
        text-align: left;
    }
    
    th {
        background-color: #f5f5f5;
    }
    
    /* Ensure blockquotes are distinct */
    blockquote {
        border-left: 4px solid #ddd;
        margin: 1em 0;
        padding-left: 1em;
        font-style: italic;
    }
    """

    # Combine original CSS with EPUB adjustments
    epub_css = css_content + epub_css_adjustments

    # Write EPUB-optimized CSS
    with open(output_css_path, "w", encoding="utf-8") as f:
        f.write(epub_css)

    return output_css_path


def generate_epub(book_name, output_dir="public"):
    """Generate EPUB file for a book"""
    # Get book metadata
    metadata = get_book_metadata(book_name)

    # Create output directory
    book_output_dir = os.path.join(output_dir, book_name)
    os.makedirs(book_output_dir, exist_ok=True)

    # Create EPUB-optimized CSS
    epub_css_path = os.path.join(book_output_dir, f"{book_name}-epub.css")
    css_file_path = os.path.join("templates", metadata["css_file"])
    epub_css_file = create_epub_css(css_file_path, epub_css_path)

    # Build EPUB using pandoc
    epub_output = os.path.join(book_output_dir, f"{book_name}.epub")
    markdown_file = os.path.join("books", f"{book_name}.md")

    if not os.path.exists(markdown_file):
        print(f"Error: Markdown file not found: {markdown_file}")
        return False

    # Check if pandoc-mermaid-filter is available
    filter_cmd = ""
    try:
        subprocess.run(
            ["pandoc-mermaid-filter", "--help"], capture_output=True, check=True
        )
        filter_cmd = "--filter pandoc-mermaid-filter"
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Warning: pandoc-mermaid-filter not available, skipping mermaid diagrams")

    # Create a temporary HTML file with embedded CSS for EPUB
    temp_html_path = os.path.join(book_output_dir, f"{book_name}_epub_temp.html")

    # First generate HTML with pandoc
    html_cmd = [
        "pandoc",
        markdown_file,
        "-o",
        temp_html_path,
        "--template",
        os.path.join("templates", metadata["html_file"]),
        "--css",
        epub_css_file if epub_css_file else css_file_path,
        "--highlight-style",
        "pygments",
        "--metadata",
        f"title={metadata['title']}",
        "--metadata",
        f"author={metadata['author']}",
        "--metadata",
        "language=en",
        "--metadata",
        f"category={metadata['category']}",
        "--metadata",
        f"description={metadata['description']}",
    ]

    if filter_cmd:
        html_cmd.extend(filter_cmd.split())

    try:
        # Generate HTML first
        result = subprocess.run(html_cmd, capture_output=True, text=True, check=True)

        # Read the generated HTML and embed CSS
        with open(temp_html_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Parse HTML and embed CSS
        soup = BeautifulSoup(html_content, "html.parser")

        # Remove external CSS links
        for link in soup.find_all("link", rel="stylesheet"):
            link.decompose()

        # Add embedded CSS
        if epub_css_file and os.path.exists(epub_css_file):
            with open(epub_css_file, "r", encoding="utf-8") as f:
                css_content = f.read()

            style_tag = soup.new_tag("style")
            style_tag.string = css_content
            head = soup.find("head")
            if head:
                head.append(style_tag)

        # Write HTML with embedded CSS
        with open(temp_html_path, "w", encoding="utf-8") as f:
            f.write(str(soup))

        # Now convert HTML to EPUB
        epub_cmd = [
            "pandoc",
            temp_html_path,
            "-o",
            epub_output,
            "--toc",
            "--highlight-style",
            "pygments",
            "--metadata",
            f"title={metadata['title']}",
            "--metadata",
            f"author={metadata['author']}",
            "--metadata",
            "language=en",
            "--metadata",
            f"category={metadata['category']}",
            "--metadata",
            f"description={metadata['description']}",
        ]

        # Convert to EPUB
        result = subprocess.run(epub_cmd, capture_output=True, text=True, check=True)
        print(f"✓ EPUB generated successfully: {epub_output}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"Error generating EPUB: {e}")
        print(f"stderr: {e.stderr}")
        return False
    finally:
        # Clean up temporary file
        if os.path.exists(temp_html_path):
            os.remove(temp_html_path)

    print(f"Generating EPUB for {book_name}...")


def main():
    parser = argparse.ArgumentParser(description="Generate EPUB from Markdown file")
    parser.add_argument("book_name", help="Name of the book to generate EPUB for")
    parser.add_argument("--output-dir", default="public", help="Output directory")

    args = parser.parse_args()

    success = generate_epub(args.book_name, args.output_dir)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
