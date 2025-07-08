#!/usr/bin/env python3
"""
Fix code block styling for PDF generation
Removes conflicting Prism CSS and ensures readable code blocks in PDF
"""

import sys
import os
from bs4 import BeautifulSoup
import argparse


def remove_prism_css(html_content):
    """Remove Prism.js CSS links that can cause conflicts in PDF"""
    soup = BeautifulSoup(html_content, "html.parser")

    # Remove Prism CSS links
    prism_css_links = soup.find_all("link", href=lambda x: x and "prism" in x.lower())
    for link in prism_css_links:
        link.decompose()
        print("✓ Removed Prism CSS link")

    # Remove Prism JS scripts
    prism_scripts = soup.find_all("script", src=lambda x: x and "prism" in x.lower())
    for script in prism_scripts:
        script.decompose()
        print("✓ Removed Prism JS script")

    return str(soup)


def add_pdf_code_styles(html_content):
    """Add PDF-specific code block styles to ensure readability"""
    soup = BeautifulSoup(html_content, "html.parser")

    # Create CSS for PDF code blocks
    pdf_code_css = """
    <style>
    /* PDF Code Block Overrides - Ensure readability */
    pre, code {
        background-color: #f6f8fa !important;
        color: #24292e !important;
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        padding: 16px !important;
        margin: 1em 0 !important;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace !important;
        font-size: 0.9em !important;
        line-height: 1.4 !important;
        overflow-x: auto !important;
        white-space: pre-wrap !important;
        word-wrap: break-word !important;
    }
    
    /* Inline code */
    code:not(pre code) {
        background-color: #f6f8fa !important;
        color: #24292e !important;
        padding: 0.2em 0.4em !important;
        border-radius: 3px !important;
        font-size: 0.9em !important;
    }
    
    /* Code inside pre blocks */
    pre code {
        background: transparent !important;
        padding: 0 !important;
        border-radius: 0 !important;
        font-size: inherit !important;
        color: inherit !important;
    }
    
    /* Remove any dark overlays */
    .token, .highlight, .highlight * {
        color: inherit !important;
        background: transparent !important;
    }
    
    /* Ensure syntax highlighting colors work */
    .token.comment, .token.prolog, .token.doctype, .token.cdata {
        color: #6a737d !important;
    }
    
    .token.punctuation {
        color: #24292e !important;
    }
    
    .token.property, .token.tag, .token.boolean, .token.number, .token.constant, .token.symbol, .token.deleted {
        color: #d73a49 !important;
    }
    
    .token.selector, .token.attr-name, .token.string, .token.char, .token.builtin, .token.inserted {
        color: #032f62 !important;
    }
    
    .token.operator, .token.entity, .token.url, .language-css .token.string, .style .token.string {
        color: #d73a49 !important;
    }
    
    .token.atrule, .token.attr-value, .token.keyword {
        color: #d73a49 !important;
    }
    
    .token.function {
        color: #6f42c1 !important;
    }
    
    .token.class-name {
        color: #6f42c1 !important;
    }
    
    .token.regex, .token.important, .token.variable {
        color: #e36209 !important;
    }
    
    /* Code wrapper styling */
    .code-wrapper {
        border: 1px solid #e1e4e8 !important;
        border-radius: 6px !important;
        margin: 1em 0 !important;
        overflow: hidden !important;
    }
    
    .code-header {
        background: #f6f8fa !important;
        padding: 8px 16px !important;
        border-bottom: 1px solid #e1e4e8 !important;
        font-size: 12px !important;
        color: #586069 !important;
        font-weight: 600 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.5px !important;
    }
    
    /* Hide interactive elements in PDF */
    .mermaid-interactive {
        display: none !important;
    }
    
    .mermaid-fallback {
        display: block !important;
    }
    
    /* Ensure rendered mermaid images are visible */
    .mermaid-rendered {
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
        margin: 1em auto !important;
    }
    </style>
    """

    # Add the CSS to the head
    head = soup.find("head")
    if head:
        head.append(BeautifulSoup(pdf_code_css, "html.parser"))
        print("✓ Added PDF code block styles")

    return str(soup)


def process_html_for_pdf(html_file_path):
    """Process HTML file to fix code blocks for PDF"""

    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    # Remove Prism CSS that can cause conflicts
    html_content = remove_prism_css(html_content)

    # Add PDF-specific code styles
    html_content = add_pdf_code_styles(html_content)

    # Write the processed HTML
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✓ Fixed code blocks for PDF: {html_file_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Fix code block styling for PDF generation"
    )
    parser.add_argument("html_file", help="HTML file to process")

    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    process_html_for_pdf(args.html_file)


if __name__ == "__main__":
    main()
