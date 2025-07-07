import sys
import re

if len(sys.argv) != 2:
    print("Usage: python fix-mermaid-blocks.py <html_file>")
    sys.exit(1)

html_file = sys.argv[1]

with open(html_file, "r", encoding="utf-8") as f:
    html = f.read()


# Replace <pre class="mermaid"><code>...</code></pre> with <div class="mermaid">...</div>
def fix_mermaid_blocks(html):
    pattern = re.compile(
        r'<pre class="mermaid"><code>([\s\S]*?)</code></pre>', re.MULTILINE
    )

    def replacer(match):
        code = match.group(1)
        # Unescape HTML entities
        code = code.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")
        return f'<div class="mermaid">{code}</div>'

    return pattern.sub(replacer, html)


fixed_html = fix_mermaid_blocks(html)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(fixed_html)
