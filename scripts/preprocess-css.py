#!/usr/bin/env python3
"""
CSS Preprocessing for EPUB/PDF/MOBI compatibility
Converts modern CSS to widely-supported CSS for all formats
"""

import re
import os
import sys
from pathlib import Path


def extract_css_variables(css_content):
    """Extract CSS custom properties (variables) from :root and globally"""
    variables = {}
    # Find all --foo: value; definitions
    for match in re.finditer(r"--([a-zA-Z0-9-_]+):\s*([^;]+);", css_content):
        variables[f"--{match.group(1).strip()}"] = match.group(2).strip()
    return variables


def replace_css_variables(css_content, variables):
    """Replace all var(--foo) with their values, remove lines with unresolved var()"""
    # Replace all var(--foo) with value
    for var_name, var_value in variables.items():
        css_content = re.sub(rf"var\({re.escape(var_name)}\)", var_value, css_content)
    # Remove any lines that still contain var(
    css_content = "\n".join(
        [line for line in css_content.splitlines() if "var(" not in line]
    )
    return css_content


def remove_unsupported_css(css_content):
    """Remove or replace CSS features not supported in EPUB/PDF/MOBI"""

    # Remove all custom property definitions
    css_content = re.sub(r"--[a-zA-Z0-9-_]+:\s*[^;]+;\s*", "", css_content)

    # Remove :root section (variables are already processed)
    css_content = re.sub(r":root\s*\{[^}]*\}", "", css_content)

    # Replace complex gradients with solid colors
    css_content = re.sub(
        r"linear-gradient\([^)]+\)", "#3b82f6", css_content  # Default primary color
    )

    # Replace complex box-shadows with simpler ones
    css_content = re.sub(
        r"box-shadow:\s*[^;]+;", "box-shadow: 0 2px 4px rgba(0,0,0,0.1);", css_content
    )

    # Remove transform properties (not well supported)
    css_content = re.sub(r"transform:\s*[^;]+;", "", css_content)

    # Remove transition properties
    css_content = re.sub(r"transition:\s*[^;]+;", "", css_content)

    # Replace complex border-radius with simpler values
    css_content = re.sub(r"border-radius:\s*[^;]+;", "border-radius: 8px;", css_content)

    # Remove opacity properties that cause parsing errors
    css_content = re.sub(r"opacity:\s*[^;]+;", "", css_content)

    # Remove text-opacity (causes parsing errors)
    css_content = re.sub(r"text-opacity:\s*[^;]+;", "", css_content)

    # Remove any remaining var() functions
    css_content = re.sub(r"var\([^)]+\)", "inherit", css_content)

    # Remove any remaining calc() functions
    css_content = re.sub(r"calc\([^)]+\)", "auto", css_content)

    # Remove any remaining CSS functions that might cause issues
    css_content = re.sub(r"[a-zA-Z-]+\([^)]+\)", "auto", css_content)

    # Remove any malformed CSS properties (like "text-" without value)
    css_content = re.sub(r"text-[^:]+:\s*[^;]*;", "", css_content)

    # Remove any properties that end with just a colon
    css_content = re.sub(r"[a-zA-Z-]+:\s*;", "", css_content)

    # Remove any properties with empty values
    css_content = re.sub(
        r"([a-zA-Z-]+):\s*([^;]*)\s*;",
        lambda m: "" if not m.group(2).strip() else m.group(0),
        css_content,
    )

    # Remove any empty lines
    css_content = "\n".join([line for line in css_content.splitlines() if line.strip()])

    return css_content


def add_pdf_optimizations(css_content):
    """Add PDF-specific optimizations for better page breaks and layout"""

    # Add page break controls
    pdf_css = """
    /* PDF-specific optimizations */
    @page {
        size: A4;
    }
    
    /* Prevent page breaks in important elements */
    h1, h2, h3, h4, h5, h6 {
        page-break-after: avoid;
        page-break-inside: avoid;
    }
    
    /* Keep code blocks together */
    pre, code {
        page-break-inside: avoid;
        white-space: pre-wrap;
        word-wrap: break-word;
        max-width: 100%;
        overflow-x: auto;
    }
    
    /* Keep blockquotes together */
    blockquote {
        page-break-inside: avoid;
        margin: 1em 0;
    }
    
    /* Keep conversation blocks together */
    .conversation {
        page-break-inside: avoid;
        margin: 1.5em 0;
    }
    
    /* Keep tables together */
    table {
        page-break-inside: avoid;
        max-width: 100%;
        overflow-x: auto;
    }
    
    /* Ensure images don't overflow */
    img {
        max-width: 100%;
        height: auto;
    }
    
    /* Better list formatting for PDF */
    ul, ol {
        margin-left: 1.5em;
        page-break-inside: auto;
    }
    
    /* Ensure boxes don't break across pages */
    .box {
        page-break-inside: avoid;
        margin: 1em 0;
    }
    
    /* Ensure columns don't break */
    .columns {
        page-break-inside: avoid;
    }
    """

    return css_content + pdf_css


def add_epub_optimizations(css_content):
    """Add EPUB-specific optimizations"""

    epub_css = """
    /* EPUB-specific optimizations */
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

    return css_content + epub_css


def fix_mermaid_and_syntax_highlighting(css_content):
    """Add CSS for Mermaid diagrams and syntax highlighting that works in all formats"""

    mermaid_css = """
    /* Mermaid diagram styling for all formats */
    .mermaid {
        text-align: center;
        margin: 1em 0;
        padding: 1em;
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 4px;
    }
    
    /* WhatsApp conversation styling for all formats */
    .conversation {
        background: #F0F0F0;
        border-radius: 12px;
        padding: 1.2rem;
        margin: 2rem 0;
        border: 1px solid #e0e0e0;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    }
    
    .conversation::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: #25D366;
        border-radius: 12px 12px 0 0;
    }
    
    .conversation blockquote {
        background: #DCF8C6;
        border: none;
        border-radius: 18px;
        padding: 0.8rem 1rem;
        margin: 0.5rem 0;
        box-shadow: none;
        color: #262626;
        font-style: normal;
        max-width: 70%;
        word-wrap: break-word;
    }
    
    .conversation blockquote:nth-child(odd) {
        background: #DCF8C6;
        margin-left: auto;
        border-bottom-right-radius: 4px;
        border: none;
    }
    
    .conversation blockquote:nth-child(even) {
        background: #E8E8E8;
        margin-right: auto;
        border-bottom-left-radius: 4px;
        border: none;
    }
    
    .conversation blockquote strong {
        color: #666666;
        font-size: 0.75em;
        display: block;
        margin-bottom: 0.3rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        opacity: 0.8;
    }
    
    .conversation blockquote p {
        margin: 0;
        line-height: 1.4;
        color: #262626;
        font-size: 0.95em;
        font-weight: 400;
    }
    
    /* Syntax highlighting fallbacks */
    .highlight, pre {
        background-color: #f6f8fa;
        border: 1px solid #e1e4e8;
        border-radius: 6px;
        padding: 16px;
        overflow-x: auto;
        margin: 1em 0;
    }
    
    /* Code block styling */
    code {
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
        font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
        font-size: 0.9em;
    }
    
    /* Inline code */
    code:not(pre code) {
        background-color: #f6f8fa;
        padding: 0.2em 0.4em;
        border-radius: 3px;
    }
    
    /* Prism.js fallback styles */
    .token.comment, .token.prolog, .token.doctype, .token.cdata {
        color: #6a737d;
    }
    
    .token.punctuation {
        color: #24292e;
    }
    
    .token.property, .token.tag, .token.boolean, .token.number, .token.constant, .token.symbol, .token.deleted {
        color: #d73a49;
    }
    
    .token.selector, .token.attr-name, .token.string, .token.char, .token.builtin, .token.inserted {
        color: #032f62;
    }
    
    .token.operator, .token.entity, .token.url, .language-css .token.string, .style .token.string {
        color: #d73a49;
    }
    
    .token.atrule, .token.attr-value, .token.keyword {
        color: #d73a49;
    }
    
    .token.function {
        color: #6f42c1;
    }
    
    .token.class-name {
        color: #6f42c1;
    }
    
    .token.regex, .token.important, .token.variable {
        color: #e36209;
    }
    """

    return css_content + mermaid_css


def preprocess_css_for_format(css_file_path, output_path, format_type):
    """Preprocess CSS for specific format (pdf, epub, mobi)"""

    with open(css_file_path, "r", encoding="utf-8") as f:
        css_content = f.read()

    # Extract and replace CSS variables
    variables = extract_css_variables(css_content)
    css_content = replace_css_variables(css_content, variables)

    # Remove unsupported CSS features
    css_content = remove_unsupported_css(css_content)

    # Add format-specific optimizations
    if format_type == "pdf":
        css_content = add_pdf_optimizations(css_content)
    elif format_type in ["epub", "mobi"]:
        css_content = add_epub_optimizations(css_content)

    # Add Mermaid and syntax highlighting fixes
    css_content = fix_mermaid_and_syntax_highlighting(css_content)

    # Write processed CSS
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(css_content)

    return output_path


def main():
    if len(sys.argv) != 4:
        print("Usage: python3 preprocess-css.py <input-css> <output-css> <format>")
        print("Format options: pdf, epub, mobi")
        sys.exit(1)

    input_css = sys.argv[1]
    output_css = sys.argv[2]
    format_type = sys.argv[3]

    if not os.path.exists(input_css):
        print(f"Error: Input CSS file not found: {input_css}")
        sys.exit(1)

    if format_type not in ["pdf", "epub", "mobi"]:
        print(f"Error: Invalid format '{format_type}'. Use: pdf, epub, or mobi")
        sys.exit(1)

    try:
        processed_path = preprocess_css_for_format(input_css, output_css, format_type)
        print(f"✓ Preprocessed CSS for {format_type}: {processed_path}")
    except Exception as e:
        print(f"Error preprocessing CSS: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
