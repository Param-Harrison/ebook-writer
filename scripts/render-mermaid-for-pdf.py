#!/usr/bin/env python3
"""
Render Mermaid diagrams as SVG for PDF generation
Replaces mermaid divs with rendered SVG images for PDF compatibility
"""

import sys
import os
import re
import base64
import tempfile
import subprocess
from pathlib import Path
from bs4 import BeautifulSoup
import argparse


def check_mermaid_cli():
    """Check if mermaid-cli is available"""
    try:
        result = subprocess.run(
            ["mmdc", "--version"], capture_output=True, text=True, timeout=5
        )
        return result.returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False


def render_mermaid_to_svg(mermaid_code, output_dir):
    """Render Mermaid code to SVG using mermaid-cli"""
    try:
        # Create temporary input file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".mmd", delete=False) as f:
            f.write(mermaid_code)
            input_file = f.name

        # Create output file path
        output_file = os.path.join(
            output_dir, f"mermaid_{hash(mermaid_code) % 10000}.svg"
        )

        # Render using mermaid-cli
        cmd = [
            "mmdc",
            "-i",
            input_file,
            "-o",
            output_file,
            "--backgroundColor",
            "transparent",
            "--width",
            "800",
        ]

        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)

        # Clean up temp file
        os.unlink(input_file)

        if result.returncode == 0 and os.path.exists(output_file):
            return output_file
        else:
            print(f"Warning: Failed to render mermaid diagram: {result.stderr}")
            return None

    except Exception as e:
        print(f"Error rendering mermaid diagram: {e}")
        return None


def embed_svg_as_data_url(svg_file_path):
    """Convert SVG file to data URL for embedding in HTML"""
    try:
        with open(svg_file_path, "r", encoding="utf-8") as f:
            svg_content = f.read()

        # Encode as base64
        svg_encoded = base64.b64encode(svg_content.encode("utf-8")).decode("utf-8")
        return f"data:image/svg+xml;base64,{svg_encoded}"

    except Exception as e:
        print(f"Error encoding SVG: {e}")
        return None


def process_html_for_pdf(html_file_path, output_dir=None):
    """Process HTML file to render Mermaid diagrams for PDF"""

    if not check_mermaid_cli():
        print(
            "Warning: mermaid-cli (mmdc) not found. Install with: npm install -g @mermaid-js/mermaid-cli"
        )
        print("Mermaid diagrams will not be rendered in PDF.")
        return False

    # Create output directory for SVG files
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(html_file_path), "mermaid-images")

    os.makedirs(output_dir, exist_ok=True)

    # Read HTML file
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, "html.parser")

    # Find all mermaid divs
    mermaid_divs = soup.find_all("div", class_="mermaid")

    if not mermaid_divs:
        print("No Mermaid diagrams found in HTML")
        return True

    print(f"Found {len(mermaid_divs)} Mermaid diagrams to render...")

    for i, div in enumerate(mermaid_divs):
        mermaid_code = div.get_text().strip()

        if not mermaid_code:
            continue

        print(f"Rendering diagram {i+1}/{len(mermaid_divs)}...")

        # Render to SVG
        svg_file = render_mermaid_to_svg(mermaid_code, output_dir)

        if svg_file:
            # Convert to data URL
            data_url = embed_svg_as_data_url(svg_file)

            if data_url:
                # Replace div with img
                img_tag = soup.new_tag("img")
                img_tag["src"] = data_url
                img_tag["alt"] = f"Mermaid diagram {i+1}"
                img_tag["style"] = (
                    "max-width: 100%; height: auto; display: block; margin: 1em auto;"
                )
                img_tag["class"] = "mermaid-rendered"

                # Replace the div with the img
                div.replace_with(img_tag)

                print(f"✓ Rendered diagram {i+1}")
            else:
                print(f"✗ Failed to encode diagram {i+1}")
        else:
            print(f"✗ Failed to render diagram {i+1}")

    # Write the modified HTML
    with open(html_file_path, "w", encoding="utf-8") as f:
        f.write(str(soup))

    print(f"✓ Processed HTML file: {html_file_path}")
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Render Mermaid diagrams as SVG for PDF generation"
    )
    parser.add_argument("html_file", help="HTML file to process")
    parser.add_argument(
        "--output-dir",
        help="Directory to store SVG files (default: mermaid-images/ in same dir as HTML)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.html_file):
        print(f"Error: HTML file not found: {args.html_file}")
        sys.exit(1)

    success = process_html_for_pdf(args.html_file, args.output_dir)

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
