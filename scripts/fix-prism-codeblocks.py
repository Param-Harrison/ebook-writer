import sys
from bs4 import BeautifulSoup

if len(sys.argv) != 2:
    print("Usage: python fix-prism-codeblocks.py <html_file>")
    sys.exit(1)

html_file = sys.argv[1]

with open(html_file, "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "html.parser")

for div in soup.find_all("div", class_="sourceCode"):
    pre = div.find("pre")
    if pre:
        code = pre.find("code")
        if code:
            # Get language from pre class
            lang = None
            for c in pre.get("class", []):
                if c.startswith("sourceCode"):
                    continue
                lang = c
            if lang:
                code["class"] = [f"language-{lang}"]
            # Replace div with <pre><code>
            new_pre = soup.new_tag("pre")
            new_code = soup.new_tag("code", **code.attrs)
            new_code.string = code.get_text()
            new_pre.append(new_code)
            div.replace_with(new_pre)

with open(html_file, "w", encoding="utf-8") as f:
    f.write(str(soup))
