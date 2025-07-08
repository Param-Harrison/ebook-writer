#!/bin/bash
set -e

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed. Please install pandoc first."
    exit 1
fi

# Check if jq is installed for JSON parsing
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq first."
    exit 1
fi

CONFIG_FILE="books/book-config.json"

# Function to build a single book
build_book() {
    local book_name=$1
    echo "Building $book_name..."

    # Get book config from JSON
    book_config=$(jq -r ".books[\"$book_name\"]" "$CONFIG_FILE" 2>/dev/null)

    if [ "$book_config" = "null" ]; then
        echo "Warning: No configuration found for $book_name, using default template"
        template="afrinenglish"
        css_file="afrinenglish.css"
        html_file="afrinenglish.html"
        title="$book_name"
        author="Param Harrison"
    else
        template=$(echo "$book_config" | jq -r '.template')
        css_file=$(jq -r ".templates[\"$template\"].css" "$CONFIG_FILE")
        html_file=$(jq -r ".templates[\"$template\"].html" "$CONFIG_FILE")
        title=$(echo "$book_config" | jq -r '.title // "'"$book_name"'"')
        author=$(echo "$book_config" | jq -r '.author // "Param Harrison"')
    fi

    # Output directory for this book
    out_dir="public/$book_name"
    mkdir -p "$out_dir"

    # Use pandoc-mermaid-filter if available in venv
    FILTER=""
    if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/pandoc-mermaid-filter" ]; then
        FILTER="--filter pandoc-mermaid-filter"
    fi

    # Build HTML
    pandoc "books/$book_name.md" \
        -o "$out_dir/$book_name.html" \
        --template="templates/$html_file" \
        --css="templates/$css_file" \
        --standalone \
        --toc \
        --highlight-style=pygments \
        --metadata title="$title" \
        --metadata author="$author" \
        $FILTER

    # Post-process HTML (fix mermaid, prism, css links, and syntax highlighting)
    if command -v python3 &> /dev/null; then
        python3 scripts/fix-mermaid-blocks.py "$out_dir/$book_name.html" 2>/dev/null || echo "Warning: Skipping mermaid fix."
        python3 scripts/fix-prism-codeblocks.py "$out_dir/$book_name.html" 2>/dev/null || echo "Warning: Skipping prism fix."
        python3 scripts/fix-css-links.py "$out_dir/$book_name.html" "$css_file" 2>/dev/null || echo "Warning: Skipping CSS fix."
        python3 scripts/fix-mermaid-and-syntax.py "$out_dir/$book_name.html" --format html 2>/dev/null || echo "Warning: Skipping mermaid/syntax fix."
    else
        echo "Warning: python3 not found, skipping post-processing."
    fi

    echo "✓ Built $out_dir/$book_name.html using $template template"
}

# Read book configuration
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: book-config.json not found"
    exit 1
fi

mkdir -p public

# Build all books or specific book
if [ $# -eq 0 ]; then
    # Build all books
    echo "Building all books..."
    for book_file in books/*.md; do
        if [ -f "$book_file" ]; then
            book_name=$(basename "$book_file" .md)
            build_book "$book_name"
        fi
    done
else
    # Build specific book
    book_name=$1
    if [ -f "books/$book_name.md" ]; then
        build_book "$book_name"
    else
        echo "Error: Book $book_name.md not found"
        exit 1
    fi
fi

echo "Build complete! Check the public/<book-name>/<book-name>.html files for output." 