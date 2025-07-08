#!/usr/bin/env python3
"""
PDF generation script using WeasyPrint
Converts HTML files to PDF while preserving CSS styles
"""

import sys
import os
from pathlib import Path
from urllib.parse import urljoin, urlparse
import argparse

try:
    from weasyprint import HTML, CSS
    from weasyprint.text.fonts import FontConfiguration
except ImportError:
    print("Error: WeasyPrint is not installed. Install it with: pip install weasyprint")
    sys.exit(1)


def fix_html_for_pdf(html_file_path, css_file_path):
    """
    Fix HTML file for PDF generation by:
    1. Converting relative URLs to absolute paths
    2. Embedding CSS styles
    3. Fixing any PDF-specific issues
    """
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Get the directory of the HTML file for resolving relative paths
    html_dir = os.path.dirname(os.path.abspath(html_file_path))

    # Read and embed CSS
    if css_file_path and os.path.exists(css_file_path):
        with open(css_file_path, "r", encoding="utf-8") as f:
            css_content = f.read()

            # CSS is already preprocessed for PDF, no additional adjustments needed
        print(f"✓ Using preprocessed CSS for PDF: {css_file_path}")

    return html_content, (
        css_content if css_file_path and os.path.exists(css_file_path) else None
    )


def generate_pdf(html_file_path, output_pdf_path, css_file_path=None):
    """
    Generate PDF from HTML file using WeasyPrint
    """
    try:
        # Fix HTML for PDF generation
        html_content, css_content = fix_html_for_pdf(html_file_path, css_file_path)

        # Create font configuration
        font_config = FontConfiguration()

        # Create HTML object
        html_obj = HTML(string=html_content)

        # Create CSS object if CSS content is available
        css_obj = None
        if css_content:
            css_obj = CSS(string=css_content, font_config=font_config)

        # Generate PDF
        if css_obj:
            html_obj.write_pdf(
                output_pdf_path, stylesheets=[css_obj], font_config=font_config
            )
        else:
            html_obj.write_pdf(output_pdf_path, font_config=font_config)

        print(f"✓ PDF generated successfully: {output_pdf_path}")
        return True

    except Exception as e:
        print(f"Error generating PDF: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Generate PDF from HTML file using WeasyPrint"
    )
    parser.add_argument("html_file", help="Input HTML file path")
    parser.add_argument("output_pdf", help="Output PDF file path")
    parser.add_argument("css_file", nargs="?", help="CSS file path (optional)")

    args = parser.parse_args()

    # Check if input file exists
    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(args.output_pdf)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate PDF
    success = generate_pdf(args.html_file, args.output_pdf, args.css_file)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
