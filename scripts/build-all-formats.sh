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

# Check if calibre is installed for EPUB/MOBI conversion
if ! command -v ebook-convert &> /dev/null; then
    echo "Warning: calibre is not installed. EPUB and MOBI conversion will be skipped."
    echo "Install calibre from https://calibre-ebook.com/download"
    CALIBRE_AVAILABLE=false
else
    CALIBRE_AVAILABLE=true
fi

# Check if weasyprint is available for PDF generation
if ! python3 -c "import weasyprint" 2>/dev/null; then
    echo "Warning: weasyprint is not installed. PDF generation will be skipped."
    echo "Install with: pip install weasyprint"
    WEASYPRINT_AVAILABLE=false
else
    WEASYPRINT_AVAILABLE=true
fi

# Function to build a single book in all formats
build_book_all_formats() {
    local book_name=$1
    echo "Building $book_name in all formats..."
    
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
    
    # Get book metadata
    title=$(echo "$book_config" | jq -r '.title // "Unknown Title"')
    author=$(echo "$book_config" | jq -r '.author // "Param Harrison"')
    
    # Use pandoc-mermaid-filter if available in venv
    FILTER=""
    if [ -n "$VIRTUAL_ENV" ] && [ -x "$VIRTUAL_ENV/bin/pandoc-mermaid-filter" ]; then
        FILTER="--filter pandoc-mermaid-filter"
    fi
    
    # Create output directories
    mkdir -p "public/$book_name"
    
    # Build HTML first (as base for other formats)
    echo "  Building HTML..."
    if [ "$template" = "backendchallenges" ]; then
        pandoc "books/$book_name.md" \
            -o "public/$book_name/$book_name.html" \
            --template="templates/$html_file" \
            --css="$css_file" \
            --standalone \
            --toc \
            --metadata title="$title" \
            --metadata author="$author" \
            $FILTER
    else
        pandoc "books/$book_name.md" \
            -o "public/$book_name/$book_name.html" \
            --template="templates/$html_file" \
            --css="$css_file" \
            --standalone \
            --toc \
            --highlight-style=pygments \
            --metadata title="$title" \
            --metadata author="$author" \
            $FILTER
    fi
    
    # Post-process HTML
    if command -v python3 &> /dev/null; then
        python3 scripts/fix-mermaid-blocks.py "public/$book_name/$book_name.html" 2>/dev/null || echo "Warning: Skipping mermaid fix."
        python3 scripts/fix-prism-codeblocks.py "public/$book_name/$book_name.html" 2>/dev/null || echo "Warning: Skipping prism fix."
        python3 scripts/fix-css-links.py "public/$book_name/$book_name.html" "$css_file" 2>/dev/null || echo "Warning: Skipping CSS fix."
        python3 scripts/fix-mermaid-and-syntax.py "public/$book_name/$book_name.html" --format html 2>/dev/null || echo "Warning: Skipping mermaid/syntax fix."
    fi
    
    # Build EPUB
    if [ "$CALIBRE_AVAILABLE" = true ]; then
        echo "  Building EPUB..."
        # Preprocess CSS for EPUB
        epub_css_path="public/$book_name/$book_name-epub.css"
        python3 scripts/preprocess-css.py "templates/$css_file" "$epub_css_path" "epub"
        
        pandoc "books/$book_name.md" \
            -o "public/$book_name/$book_name.epub" \
            --template="templates/$html_file" \
            --css="$epub_css_path" \
            --toc \
            --highlight-style=pygments \
            --metadata title="$title" \
            --metadata author="$author" \
            --metadata language=en \
            $FILTER
    fi
    
    # Build PDF using WeasyPrint
    if [ "$WEASYPRINT_AVAILABLE" = true ]; then
        echo "  Building PDF..."
        # Preprocess CSS for PDF
        pdf_css_path="public/$book_name/$book_name-pdf.css"
        python3 scripts/preprocess-css.py "templates/$css_file" "$pdf_css_path" "pdf"
        
        python3 scripts/build-pdf.py "public/$book_name/$book_name.html" "public/$book_name/$book_name.pdf" "$pdf_css_path"
    fi
    
    # Build MOBI using Calibre
    if [ "$CALIBRE_AVAILABLE" = true ]; then
        echo "  Building MOBI..."
        if [ -f "public/$book_name/$book_name.epub" ]; then
            ebook-convert "public/$book_name/$book_name.epub" "public/$book_name/$book_name.mobi" \
                --title "$title" \
                --authors "$author" \
                --language en
        else
            echo "  Warning: EPUB not available, skipping MOBI conversion"
        fi
    fi
    
    echo "✓ Built $book_name in all formats"
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
    echo "Building all books in all formats..."
    for book_file in books/*.md; do
        if [ -f "$book_file" ]; then
            book_name=$(basename "$book_file" .md)
            build_book_all_formats "$book_name"
        fi
    done
else
    # Build specific book
    book_name=$1
    if [ -f "books/$book_name.md" ]; then
        build_book_all_formats "$book_name"
    else
        echo "Error: Book $book_name.md not found"
        exit 1
    fi
fi

# Copy all CSS files to public/
cp templates/*.css public/

echo "Build complete! Check the public/ directory for output files."
echo ""
echo "Available formats:"
echo "- HTML: public/<book-name>/<book-name>.html"
if [ "$CALIBRE_AVAILABLE" = true ]; then
    echo "- EPUB: public/<book-name>/<book-name>.epub"
    echo "- MOBI: public/<book-name>/<book-name>.mobi"
fi
if [ "$WEASYPRINT_AVAILABLE" = true ]; then
    echo "- PDF: public/<book-name>/<book-name>.pdf"
fi 