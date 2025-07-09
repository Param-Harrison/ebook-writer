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

# Check if weasyprint is available for PDF generation
if ! python3 -c "import weasyprint" 2>/dev/null; then
    echo "Warning: weasyprint is not installed. PDF generation will be skipped."
    echo "Install with: pip install weasyprint"
    WEASYPRINT_AVAILABLE=false
else
    WEASYPRINT_AVAILABLE=true
fi

# Check if calibre is available for MOBI generation
if ! command -v ebook-convert &> /dev/null; then
    echo "Warning: calibre is not installed. MOBI generation will be skipped."
    echo "Install with: brew install --cask calibre"
    CALIBRE_AVAILABLE=false
else
    CALIBRE_AVAILABLE=true
fi

# Function to build a single book in all formats
build_book_all_formats() {
    local book_name=$1
    local html_only=$2
    
    if [ "$html_only" = "--html-only" ]; then
        echo "Building $book_name in HTML only (dev mode)..."
    else
        echo "Building $book_name in all formats..."
    fi
    
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
    
    # Create output directories and clean up any existing mermaid-images
    mkdir -p "public/$book_name"
    if [ -d "public/$book_name/mermaid-images" ]; then
        rm -rf "public/$book_name/mermaid-images"
    fi
    
    # Find cover image for EPUB/MOBI
    COVER_IMAGE=""
    if [ -f "books/images/${book_name}.jpg" ]; then
        COVER_IMAGE="books/images/${book_name}.jpg"
    elif [ -f "books/images/default.jpg" ]; then
        COVER_IMAGE="books/images/default.jpg"
    fi
    COVER_OPTION=""
    if [ -n "$COVER_IMAGE" ]; then
        COVER_OPTION="--epub-cover-image=$COVER_IMAGE"
        echo "  Found cover image for EPUB/MOBI: $COVER_IMAGE"
    fi
    
    # Build HTML first (as base for other formats)
    echo "  Building HTML..."
    pandoc "books/$book_name.md" \
        -o "public/$book_name/$book_name.html" \
        --template="templates/$html_file" \
        --css="$css_file" \
        --standalone \
        --toc \
        --metadata title="$title" \
        --metadata author="$author" \
        $FILTER

    # Post-process HTML
    if command -v python3 &> /dev/null; then
        python3 scripts/fix-mermaid-blocks.py "public/$book_name/$book_name.html" 2>/dev/null || echo "Warning: Skipping mermaid fix."
        python3 scripts/fix-prism-codeblocks.py "public/$book_name/$book_name.html" 2>/dev/null || echo "Warning: Skipping prism fix."
        python3 scripts/fix-css-links.py "public/$book_name/$book_name.html" "$css_file" 2>/dev/null || echo "Warning: Skipping CSS fix."
        python3 scripts/fix-mermaid-and-syntax.py "public/$book_name/$book_name.html" --format html 2>/dev/null || echo "Warning: Skipping mermaid/syntax fix."
        
        # Render mermaid images only for production builds (not for HTML-only dev mode)
        if [ "$html_only" != "--html-only" ]; then
            python3 scripts/render-mermaid-for-pdf.py "public/$book_name/$book_name.html" 2>/dev/null || echo "Warning: Skipping mermaid rendering for EPUB."
        fi
    fi

    # Build PDF using WeasyPrint (first, so we can use its processed HTML for EPUB)
    if [ "$html_only" != "--html-only" ] && [ "$WEASYPRINT_AVAILABLE" = true ]; then
        echo "  Building PDF..."
        
        # Create a copy of HTML for PDF processing
        pdf_html_path="public/$book_name/$book_name-pdf.html"
        cp "public/$book_name/$book_name.html" "$pdf_html_path"
        
        # Process HTML specifically for PDF (highlight code, render mermaid, fix code blocks)
        if command -v python3 &> /dev/null; then
            echo "    Highlighting code blocks for PDF (Pygments)..."
            python3 scripts/pygmentsify_codeblocks.py "$pdf_html_path" 2>/dev/null || echo "Warning: Skipping Pygments highlighting."
            echo "    Processing HTML for PDF..."
            python3 scripts/render-mermaid-for-pdf.py "$pdf_html_path" 2>/dev/null || echo "Warning: Skipping mermaid rendering for PDF."
            python3 scripts/fix-pdf-code-blocks.py "$pdf_html_path" 2>/dev/null || echo "Warning: Skipping PDF code block fixes."
            echo "    Adjusting font sizes for elegant PDF output..."
            python3 scripts/fix-pdf-fonts.py "$pdf_html_path" 2>/dev/null || echo "Warning: Skipping PDF font adjustments."
        fi
        
        # Preprocess CSS for PDF
        pdf_css_path="public/$book_name/$book_name-pdf.css"
        python3 scripts/preprocess-css.py "templates/$css_file" "$pdf_css_path" "pdf"
        
        # Build PDF using the processed HTML
        python3 scripts/build-pdf.py "$pdf_html_path" "public/$book_name/$book_name.pdf" "$pdf_css_path"
    fi

    # Build EPUB using PDF-processed HTML (better code highlighting and mermaid rendering)
    if [ "$html_only" != "--html-only" ]; then
        echo "  Building EPUB..."
        
        # Use PDF-processed HTML for EPUB if available, otherwise use regular HTML
        if [ "$WEASYPRINT_AVAILABLE" = true ] && [ -f "public/$book_name/$book_name-pdf.html" ]; then
            echo "    Using PDF-processed HTML for EPUB (better code highlighting and font adjustments)..."
            epub_html_path="public/$book_name/$book_name-epub.html"
            cp "public/$book_name/$book_name-pdf.html" "$epub_html_path"
        else
            echo "    Using regular HTML for EPUB..."
            epub_html_path="public/$book_name/$book_name-epub.html"
            cp "public/$book_name/$book_name.html" "$epub_html_path"
        fi
        
        # Inject EPUB-specific styles
        if command -v python3 &> /dev/null; then
            echo "    Injecting EPUB-specific styles..."
            python3 scripts/fix-epub-styles.py "$epub_html_path" 2>/dev/null || echo "Warning: Skipping EPUB style injection."
        fi
        
        # Build EPUB using the processed HTML
        pandoc "$epub_html_path" \
            -o "public/$book_name/$book_name.epub" \
            --toc \
            --standalone \
            --metadata title="$title" \
            --metadata author="$author" \
            $COVER_OPTION
        if [ "$CALIBRE_AVAILABLE" = true ]; then
            echo "  Building MOBI from EPUB..."
            ebook-convert "public/$book_name/$book_name.epub" "public/$book_name/$book_name.mobi" \
                --title "$title" \
                --authors "$author" \
                --mobi-file-type both \
                --pretty-print
            echo "    ✓ MOBI built successfully"
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
            build_book_all_formats "$book_name" ""
        fi
    done
elif [ "$1" = "--html-only" ]; then
    # Build all books in HTML only
    echo "Building all books in HTML only (dev mode)..."
    for book_file in books/*.md; do
        if [ -f "$book_file" ]; then
            book_name=$(basename "$book_file" .md)
            build_book_all_formats "$book_name" "--html-only"
        fi
    done
else
    # Build specific book
    book_name=$1
    html_only=$2
    
    if [ -f "books/$book_name.md" ]; then
        build_book_all_formats "$book_name" "$html_only"
    else
        echo "Error: Book $book_name.md not found"
        exit 1
    fi
fi

# Copy all CSS files to public/
cp templates/*.css public/

# Clean up temporary PDF HTML files to reduce git folder size
echo "Cleaning up temporary files..."
for book_dir in public/*/; do
    if [ -d "$book_dir" ]; then
        # Remove temporary PDF HTML files
        find "$book_dir" -name "*-pdf.html" -delete 2>/dev/null || true
        # Remove PDF CSS files (they're regenerated each time)
        find "$book_dir" -name "*-pdf.css" -delete 2>/dev/null || true
        # Remove any temporary EPUB HTML files
        find "$book_dir" -name "*-epub.html" -delete 2>/dev/null || true
        # Remove any temporary MOBI HTML files
        find "$book_dir" -name "*-mobi*.html" -delete 2>/dev/null || true
    fi
done

echo "Build complete! Check the public/ directory for output files."
echo ""
echo "Available formats:"
echo "- HTML: public/<book-name>/<book-name>.html"
if [ "$WEASYPRINT_AVAILABLE" = true ]; then
    echo "- PDF: public/<book-name>/<book-name>.pdf"
fi
echo "- EPUB: public/<book-name>/<book-name>.epub"
if [ "$CALIBRE_AVAILABLE" = true ]; then
    echo "- MOBI: public/<book-name>/<book-name>.mobi"
fi 