#!/bin/bash
set -e

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq first."
    exit 1
fi

if [ $# -lt 3 ]; then
    echo "Usage: $0 <template-name> <template-title> <description>"
    echo "Example: $0 modern 'Modern Template' 'Clean and modern design'"
    exit 1
fi

TEMPLATE_NAME=$1
TEMPLATE_TITLE=$2
DESCRIPTION=$3

CONFIG_FILE="books/book-config.json"

# Check if template already exists
if jq -e ".templates[\"$TEMPLATE_NAME\"]" "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "Error: Template '$TEMPLATE_NAME' already exists"
    exit 1
fi

# Create template files
HTML_FILE="templates/$TEMPLATE_NAME.html"
CSS_FILE="templates/$TEMPLATE_NAME.css"

if [ -f "$HTML_FILE" ] || [ -f "$CSS_FILE" ]; then
    echo "Warning: Template files already exist"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create HTML template
cat > "$HTML_FILE" << EOF
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8"/>
  <title>\$title\$</title>
  <link rel="stylesheet" href="$TEMPLATE_NAME.css"/>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({ startOnLoad: true });
  </script>
</head>
<body>
  <div class="book-container">
    \$body\$
  </div>
</body>
</html>
EOF

# Create CSS template
cat > "$CSS_FILE" << EOF
body {
  font-family: 'Georgia', serif;
  background: #f7f9fb;
  color: #222;
  margin: 0;
  padding: 0;
}
.book-container {
  max-width: 800px;
  margin: 2rem auto;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0,0,0,0.08);
  padding: 2rem 2.5rem;
}
h1, h2, h3 {
  color: #2a6f97;
  margin-top: 2rem;
}
blockquote {
  border-left: 4px solid #2a6f97;
  background: #e3f2fd;
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
  font-style: italic;
}
.box {
  background: linear-gradient(90deg, #f9d29d 0%, #ffd6e0 100%);
  border-radius: 10px;
  padding: 1.2rem 1.5rem;
  margin: 1.5rem 0;
  box-shadow: 0 2px 8px rgba(255, 214, 224, 0.15);
  font-weight: 500;
}
.columns {
  display: flex;
  gap: 2rem;
  margin: 1.5rem 0;
}
.columns > * {
  flex: 1;
}
code, pre {
  background: #f0f4f8;
  border-radius: 6px;
  padding: 0.2em 0.5em;
  font-family: 'Fira Mono', monospace;
  color: #1a3a4a;
}
EOF

# Add to configuration
jq ".templates[\"$TEMPLATE_NAME\"] = {
  \"name\": \"$TEMPLATE_TITLE\",
  \"description\": \"$DESCRIPTION\",
  \"css\": \"$TEMPLATE_NAME.css\",
  \"html\": \"$TEMPLATE_NAME.html\"
}" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

echo "✓ Created template: $TEMPLATE_NAME"
echo "✓ Files created:"
echo "  - templates/$TEMPLATE_NAME.html"
echo "  - templates/$TEMPLATE_NAME.css"
echo "✓ Added to configuration"
echo ""
echo "Next steps:"
echo "1. Customize templates/$TEMPLATE_NAME.css for your design"
echo "2. Create a book with: ./scripts/new-book.sh mybook $TEMPLATE_NAME" 