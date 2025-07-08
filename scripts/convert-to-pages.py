#!/usr/bin/env python3
"""
Convert markdown content to page-based HTML with lesson navigation.
This script takes a markdown file and converts it to HTML with page breaks
at major headings (H1, H2) to create a book-like reading experience.
"""

import sys
import re
import os
from pathlib import Path


def convert_markdown_to_pages(markdown_file, output_file):
    """Convert markdown to page-based HTML with lesson navigation."""

    with open(markdown_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split content by major headings (H1 and H2)
    sections = re.split(r"(?=^#{1,2}\s)", content, flags=re.MULTILINE)

    pages = []
    lesson_count = 0

    for i, section in enumerate(sections):
        if not section.strip():
            continue

        # Check if this is a major heading
        heading_match = re.match(r"^(#{1,2})\s+(.+)$", section.strip(), re.MULTILINE)

        if heading_match:
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            # Remove the heading line from the section content
            section_lines = section.strip().splitlines()
            content_without_heading = "\n".join(section_lines[1:]).strip()

            if level == 1:  # Main lesson/chapter
                lesson_count += 1
                # Create lesson title page
                lesson_page = create_lesson_title_page(title, lesson_count)
                pages.append(lesson_page)
                # Create content page (without the heading line)
                if content_without_heading:
                    content_page = create_content_page(content_without_heading, title)
                    pages.append(content_page)
            elif level == 2:  # Subsection
                # Create subsection page (without the heading line)
                if content_without_heading:
                    subsection_page = create_subsection_page(
                        content_without_heading, title
                    )
                    pages.append(subsection_page)
        else:
            # Regular content (no major heading)
            if pages:  # Append to last page
                pages[-1] += section
            else:
                # First section without heading
                content_page = create_content_page(section, "Introduction")
                pages.append(content_page)

    # Combine all pages
    html_content = "\n".join(pages)

    # Write to output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Converted {markdown_file} to {output_file} with {len(pages)} pages")


def create_lesson_title_page(title, page_number):
    """Create a lesson title page HTML."""
    return f"""<div class="page lesson-title-page">
  <h1>{title}</h1>
  <div class="lesson-subtitle">Lesson {page_number}</div>
  <div class="lesson-description">
    Welcome to this lesson. Use the navigation buttons below to progress through the content.
  </div>
</div>"""


def create_content_page(content, title):
    """Create a content page HTML."""
    # Convert markdown to HTML (basic conversion)
    html_content = convert_markdown_to_html(content)

    return f"""<div class="page content-page">
  {html_content}
</div>"""


def create_subsection_page(content, title):
    """Create a subsection page HTML."""
    html_content = convert_markdown_to_html(content)

    return f"""<div class="page content-page">
  <h2>{title}</h2>
  {html_content}
</div>"""


def convert_markdown_to_html(markdown):
    """Basic markdown to HTML conversion."""
    html = markdown

    # Headers (H3 and below since H1/H2 are handled separately)
    html = re.sub(r"^### (.*$)", r"<h3>\1</h3>", html, flags=re.MULTILINE)

    # Bold and italic
    html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)

    # Code blocks
    html = re.sub(
        r"```(\w+)?\n(.*?)```",
        r'<pre><code class="language-\1">\2</code></pre>',
        html,
        flags=re.DOTALL,
    )
    html = re.sub(r"`(.*?)`", r"<code>\1</code>", html)

    # Blockquotes
    html = re.sub(r"^> (.*$)", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE)

    # Lists
    html = convert_lists(html)

    # Paragraphs (only for lines that aren't already HTML)
    html = re.sub(r"^([^<].*)$", r"<p>\1</p>", html, flags=re.MULTILINE)

    # Remove empty paragraphs
    html = re.sub(r"<p>\s*</p>", "", html)

    # Fix double paragraphs
    html = re.sub(r"</p>\s*<p>", "\n", html)

    return html


def convert_lists(html):
    """Convert markdown lists to HTML lists."""
    lines = html.split("\n")
    result = []
    in_list = False
    list_type = None
    list_items = []

    for line in lines:
        # Check for unordered list
        ul_match = re.match(r"^(\s*)- (.+)$", line)
        # Check for ordered list
        ol_match = re.match(r"^(\s*)\d+\. (.+)$", line)

        if ul_match or ol_match:
            if not in_list:
                in_list = True
                list_type = "ul" if ul_match else "ol"
                list_items = []

            content = ul_match.group(2) if ul_match else ol_match.group(2)
            list_items.append(f"<li>{content}</li>")
        else:
            if in_list:
                # End the current list
                list_html = (
                    f"<{list_type}>\n" + "\n".join(list_items) + f"\n</{list_type}>"
                )
                result.append(list_html)
                in_list = False
                list_items = []

            result.append(line)

    # Handle any remaining list
    if in_list:
        list_html = f"<{list_type}>\n" + "\n".join(list_items) + f"\n</{list_type}>"
        result.append(list_html)

    return "\n".join(result)


def main():
    if len(sys.argv) != 3:
        print("Usage: python convert-to-pages.py <input.md> <output.html>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file {input_file} not found")
        sys.exit(1)

    convert_markdown_to_pages(input_file, output_file)


if __name__ == "__main__":
    main()
