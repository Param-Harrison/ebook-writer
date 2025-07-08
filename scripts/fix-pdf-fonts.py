#!/usr/bin/env python3
"""
Fix font sizes for PDF generation to make them more elegant
Reduces font sizes across all elements for better PDF readability
"""

import sys
import os
from bs4 import BeautifulSoup
import argparse


def add_pdf_font_adjustments(soup):
    """Add CSS to reduce font sizes for more elegant PDF and EPUB output."""
    font_css = """
    <style>
    /* Font Size Adjustments for Elegance (PDF & EPUB) */
    
    /* Reduce base body font size */
    body {
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
    }
    
    /* Reduce heading sizes */
    h1 {
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
    }
    
    h2 {
        font-size: 1.2rem !important;
        margin-bottom: 0.7rem !important;
    }
    
    h3 {
        font-size: 1rem !important;
        margin-bottom: 0.4rem !important;
    }
    
    /* Reduce paragraph font size */
    p {
        font-size: 0.95rem !important;
        line-height: 1.7 !important;
        margin: 1rem 0 !important;
    }
    
    /* Reduce blockquote font size */
    blockquote {
        font-size: 0.9rem !important;
        padding: 0.8rem 1.2rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce conversation font sizes */
    .conversation {
        font-size: 0.9rem !important;
        padding: 1rem !important;
    }
    
    .conversation blockquote {
        font-size: 0.85rem !important;
    }
    
    .conversation blockquote p {
        font-size: 0.85rem !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    .conversation blockquote strong {
        font-size: 0.7em !important;
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Reduce box font size */
    .box {
        font-size: 0.9rem !important;
        padding: 1rem 1.4rem !important;
        margin: 1.2rem 0 !important;
    }
    
    /* Reduce code font size */
    code {
        font-size: 0.85em !important;
    }
    
    pre {
        font-size: 0.85rem !important;
        padding: 0.8rem !important;
        margin: 1rem 0 !important;
    }
    
    /* Reduce list font size */
    ul, ol {
        font-size: 0.95rem !important;
        line-height: 1.6 !important;
    }
    
    li {
        margin: 0.3rem 0 !important;
    }
    
    /* Reduce link font size */
    a {
        font-size: 0.95rem !important;
    }
    
    /* Reduce image caption font size */
    figcaption {
        font-size: 0.8em !important;
        margin-top: 0.3rem !important;
    }
    
    /* Reduce table font size */
    table {
        font-size: 0.9rem !important;
    }
    
    th, td {
        padding: 0.4rem 0.6rem !important;
        font-size: 0.9rem !important;
    }
    
    /* Ensure proper spacing for reduced fonts */
    .book-container {
        padding: 0 !important;
        margin: 0 !important;
        border-radius: 0 !important;
        box-shadow: none !important;
        border: none !important;
        max-width: none !important;
    }
    
    /* Better line spacing for readability */
    * {
        line-height: 1.6 !important;
    }
    
    /* Ensure code blocks don't overflow */
    pre code {
        font-size: 0.8rem !important;
        line-height: 1.4 !important;
    }
    </style>
    """
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(font_css, "html.parser"))
        print("✓ Added font size adjustments for elegance (PDF & EPUB)")
    return soup


def process_html_for_pdf_fonts(html_file_path):
    """Process HTML file to add font size adjustments for PDF and EPUB."""
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Add font size adjustments
    soup = add_pdf_font_adjustments(soup)

    # Write the processed HTML
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))
    print(f"✓ Applied font size adjustments: {html_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Adjust font sizes for elegant PDF and EPUB output"
    )
    parser.add_argument("html_file", help="HTML file to process")
    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    process_html_for_pdf_fonts(args.html_file)


if __name__ == "__main__":
    main()
