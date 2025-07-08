import sys
import os
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name, guess_lexer
from pygments.formatters import HtmlFormatter

if len(sys.argv) != 2:
    print("Usage: python pygmentsify_codeblocks.py <html_file>")
    sys.exit(1)

html_file = sys.argv[1]
if not os.path.exists(html_file):
    print(f"Error: HTML file not found: {html_file}")
    sys.exit(1)

with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

formatter = HtmlFormatter(style="monokai", noclasses=False)
css = formatter.get_style_defs(".highlight")

# Embed Pygments CSS in <head>
head = soup.find("head")
if head:
    style_tag = soup.new_tag("style")
    style_tag.string = css
    head.append(style_tag)
    print("✓ Embedded Pygments CSS in HTML head")

# Highlight all code blocks
for pre in soup.find_all("pre"):
    code = pre.find("code")
    if code and code.has_attr("class"):
        lang_class = next((c for c in code["class"] if c.startswith("language-")), None)
        if lang_class:
            lang = lang_class.replace("language-", "")
            try:
                lexer = get_lexer_by_name(lang)
            except Exception:
                lexer = guess_lexer(code.get_text())
            highlighted = highlight(code.get_text(), lexer, formatter)
            # Replace <pre><code>...</code></pre> with highlighted HTML
            new_soup = BeautifulSoup(highlighted, "html.parser")
            pre.replace_with(new_soup)
            print(f"✓ Highlighted code block: {lang}")

with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))
    print(f"✓ Updated HTML with Pygments highlighting: {html_file}")
