#!/usr/bin/env python3
"""
Fix CSS links in generated HTML files
Embeds CSS content directly or updates paths for proper styling
"""

import sys
import os
import re
from pathlib import Path
import argparse


def embed_css_in_html(html_file_path, css_file_path):
    """
    Embed CSS content directly into HTML file
    """
    try:
        # Read HTML content
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Read CSS content
        if css_file_path and os.path.exists(css_file_path):
            with open(css_file_path, "r", encoding="utf-8") as f:
                css_content = f.read()

            # Create embedded CSS
            embedded_css = f'<style type="text/css">\n{css_content}\n</style>'

            # Replace CSS link with embedded CSS
            # Pattern to match: <link rel="stylesheet" href="filename.css"/>
            css_link_pattern = r'<link\s+rel="stylesheet"\s+href="[^"]*\.css"[^>]*>'

            if re.search(css_link_pattern, html_content):
                html_content = re.sub(css_link_pattern, embedded_css, html_content)
                print(f"✓ Embedded CSS from {css_file_path}")
            else:
                # If no CSS link found, add embedded CSS in head
                head_pattern = r"(<head[^>]*>)"
                if re.search(head_pattern, html_content):
                    html_content = re.sub(
                        head_pattern, r"\1\n  " + embedded_css, html_content
                    )
                    print(f"✓ Added embedded CSS from {css_file_path}")
                else:
                    print(f"Warning: Could not find <head> tag in {html_file_path}")
                    return False

            # Write updated HTML
            with open(html_file_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            return True
        else:
            print(f"Warning: CSS file not found: {css_file_path}")
            return False

    except Exception as e:
        print(f"Error embedding CSS: {e}")
        return False


def fix_css_paths(html_file_path, css_file_name):
    """
    Fix CSS paths to be relative to the HTML file location
    """
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        # Get the directory of the HTML file
        html_dir = os.path.dirname(os.path.abspath(html_file_path))

        # Check if CSS file exists in the same directory as HTML
        css_in_same_dir = os.path.join(html_dir, css_file_name)
        if os.path.exists(css_in_same_dir):
            # CSS is already in the right place, just update the link
            pattern = r'href="[^"]*\.css"'
            replacement = f'href="{css_file_name}"'
            html_content = re.sub(pattern, replacement, html_content)
        else:
            # Copy CSS file to HTML directory
            template_css_path = os.path.join("templates", css_file_name)
            if os.path.exists(template_css_path):
                import shutil

                shutil.copy2(template_css_path, css_in_same_dir)
                print(f"✓ Copied {css_file_name} to {html_dir}")
            else:
                print(f"Warning: CSS file not found: {template_css_path}")
                return False

        # Write updated HTML
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        return True

    except Exception as e:
        print(f"Error fixing CSS paths: {e}")
        return False


def process_html_file(html_file_path, css_file_name, embed_css=True):
    """
    Process HTML file to fix CSS styling
    """
    if embed_css:
        # Embed CSS content directly
        css_file_path = os.path.join("templates", css_file_name)
        return embed_css_in_html(html_file_path, css_file_path)
    else:
        # Fix CSS paths
        return fix_css_paths(html_file_path, css_file_name)


def main():
    parser = argparse.ArgumentParser(description="Fix CSS links in HTML files")
    parser.add_argument("html_file", help="HTML file to process")
    parser.add_argument("css_file", help="CSS file name (e.g., afrinenglish.css)")
    parser.add_argument(
        "--embed",
        action="store_true",
        default=True,
        help="Embed CSS content directly (default)",
    )
    parser.add_argument(
        "--fix-paths", action="store_true", help="Fix CSS paths instead of embedding"
    )

    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    if args.fix_paths:
        success = process_html_file(args.html_file, args.css_file, embed_css=False)
    else:
        success = process_html_file(args.html_file, args.css_file, embed_css=True)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
