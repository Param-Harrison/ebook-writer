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
    else
        template=$(echo "$book_config" | jq -r '.template')
        css_file=$(jq -r ".templates[\"$template\"].css" "$CONFIG_FILE")
        html_file=$(jq -r ".templates[\"$template\"].html" "$CONFIG_FILE")
    fi
    
    # Use pandoc-mermaid-filter if available in venv
    FILTER=""
    if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/pandoc-mermaid-filter" ]; then
        FILTER="--filter pandoc-mermaid-filter"
    fi
    
    # For backendchallenges, disable pandoc code highlighting (let Prism handle it)
    if [ "$template" = "backendchallenges" ]; then
        pandoc "books/$book_name.md" \
            -o "public/$book_name.html" \
            --template="templates/$html_file" \
            --css="$css_file" \
            --standalone \
            --toc \
            --metadata title="$book_name" \
            $FILTER
    elif [ "$template" = "paged" ]; then
        # For paged template, use custom conversion
        if command -v python3 &> /dev/null; then
            # First convert to page-based HTML
            python3 scripts/convert-to-pages.py "books/$book_name.md" "temp_pages.html"
            
            # Then use pandoc with the converted content
            pandoc "temp_pages.html" \
                -o "public/$book_name.html" \
                --template="templates/$html_file" \
                --css="$css_file" \
                --standalone \
                --metadata title="$book_name" \
                $FILTER
                
            # Clean up temp file
            rm -f "temp_pages.html"
        else
            echo "Warning: python3 not found, falling back to standard pandoc for paged template"
            pandoc "books/$book_name.md" \
                -o "public/$book_name.html" \
                --template="templates/$html_file" \
                --css="$css_file" \
                --standalone \
                --toc \
                --highlight-style=pygments \
                --metadata title="$book_name" \
                $FILTER
        fi
    else
        pandoc "books/$book_name.md" \
            -o "public/$book_name.html" \
            --template="templates/$html_file" \
            --css="$css_file" \
            --standalone \
            --toc \
            --highlight-style=pygments \
            --metadata title="$book_name" \
            $FILTER
    fi
    
    # Post-process to fix mermaid blocks
    if command -v python3 &> /dev/null; then
        python3 scripts/fix-mermaid-blocks.py "public/$book_name.html" 2>/dev/null || echo "Warning: Skipping mermaid fix."
        python3 scripts/fix-prism-codeblocks.py "public/$book_name.html" 2>/dev/null || echo "Warning: Skipping prism fix."
    else
        echo "Warning: python3 not found, skipping mermaid/code block fix."
    fi
    
    echo "✓ Built $book_name.html using $template template"
}

mkdir -p public

# Read book configuration
CONFIG_FILE="books/book-config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: book-config.json not found"
    exit 1
fi

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

# Copy all CSS files to public/
cp templates/*.css public/

echo "Build complete! Check the public/ directory for output files." 