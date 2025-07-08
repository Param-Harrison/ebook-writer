#!/bin/bash
set -e

# Default values
DEV_MODE=false
BOOK_NAME=""
BUILD_ALL=false

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --dev|-d)
            DEV_MODE=true
            shift
            ;;
        --book|-b)
            BOOK_NAME="$2"
            shift 2
            ;;
        --all|-a)
            BUILD_ALL=true
            shift
            ;;
        --help|-h)
            echo "📚 Ebook Builder"
            echo "================"
            echo ""
            echo "Usage:"
            echo "  ./build.sh [options]"
            echo ""
            echo "Options:"
            echo "  --dev, -d          Development mode (HTML only, faster)"
            echo "  --book <name>, -b  Build specific book"
            echo "  --all, -a          Build all books (default)"
            echo "  --help, -h         Show this help"
            echo ""
            echo "Examples:"
            echo "  ./build.sh                    # Build all books in all formats"
            echo "  ./build.sh --dev              # Build all books in HTML only (dev mode)"
            echo "  ./build.sh --book mybook      # Build specific book in all formats"
            echo "  ./build.sh --dev --book mybook # Build specific book in HTML only"
            exit 0
            ;;
        *)
            echo "❌ Unknown option: $1"
            echo "Use --help for usage information"
            exit 1
            ;;
    esac
done

echo "📚 Ebook Builder"
echo "================"

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo "❌ Virtual environment not found. Please run setup first:"
    echo "   ./setup.sh"
    exit 1
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source .venv/bin/activate

# Check if we're in the virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "❌ Failed to activate virtual environment"
    exit 1
fi

echo "✅ Virtual environment activated"

# Smart cleaning based on build mode and scope
echo ""
echo "🧹 Smart cleaning based on build mode..."

if [ "$DEV_MODE" = true ]; then
    # Development mode cleaning
    if [ -n "$BOOK_NAME" ]; then
        # Dev + specific book: Only clean that book's HTML
        echo "  📖 Cleaning HTML for specific book: $BOOK_NAME"
        if [ -f "public/$BOOK_NAME/$BOOK_NAME.html" ]; then
            rm "public/$BOOK_NAME/$BOOK_NAME.html"
            echo "    ✅ Removed existing HTML for $BOOK_NAME"
        fi
    else
        # Dev + all books: Only clean HTML files of all books
        echo "  📚 Cleaning HTML files for all books..."
        for book_file in books/*.md; do
            if [ -f "$book_file" ]; then
                book_name=$(basename "$book_file" .md)
                if [ -f "public/$book_name/$book_name.html" ]; then
                    rm "public/$book_name/$book_name.html"
                    echo "    ✅ Removed HTML for $book_name"
                fi
            fi
        done
    fi
else
    # Production mode cleaning
    if [ -n "$BOOK_NAME" ]; then
        # Prod + specific book: Clean only that book's folder and CSS files
        echo "  📖 Cleaning specific book folder: $BOOK_NAME"
        if [ -d "public/$BOOK_NAME" ]; then
            rm -rf "public/$BOOK_NAME"
            echo "    ✅ Removed entire folder for $BOOK_NAME"
        fi
        # Clean CSS files in public root
        for css_file in public/*.css; do
            if [ -f "$css_file" ]; then
                rm "$css_file"
                echo "    ✅ Removed CSS file: $(basename "$css_file")"
            fi
        done
    else
        # Prod + all books: Clean everything in public
        echo "  📚 Cleaning entire public directory..."
        if [ -d "public" ]; then
            rm -rf public/*
            echo "    ✅ Public directory cleaned"
        else
            echo "    ℹ️ Public directory doesn't exist yet"
        fi
    fi
fi

# Determine build mode
if [ "$DEV_MODE" = true ]; then
    echo ""
    echo "🚀 Development mode: Building HTML only..."
    
    if [ -n "$BOOK_NAME" ]; then
        echo "📖 Building book: $BOOK_NAME"
        if [ ! -f "books/$BOOK_NAME.md" ]; then
            echo "❌ Book '$BOOK_NAME' not found in books/"
            echo "Available books:"
            ls books/*.md 2>/dev/null | sed 's|books/||' | sed 's|.md||' || echo "No books found"
            exit 1
        fi
        
        # Build single book in HTML only
        ./scripts/build-all-formats.sh "$BOOK_NAME" --html-only
    else
        echo "📚 Building all books in HTML only..."
        ./scripts/build-all-formats.sh --html-only
    fi
    
    echo ""
    echo "🎉 Development build complete!"
    echo ""
    echo "📁 Output files:"
    echo "   • HTML: public/<book-name>/<book-name>.html"
    echo ""
    echo "📖 To view your books:"
    echo "   • Open HTML files in your browser"
    echo "   • Use browser dev tools to test dark/light themes"
    
else
    echo ""
    echo "🚀 Production mode: Building all formats..."
    
    if [ -n "$BOOK_NAME" ]; then
        echo "📖 Building book: $BOOK_NAME"
        if [ ! -f "books/$BOOK_NAME.md" ]; then
            echo "❌ Book '$BOOK_NAME' not found in books/"
            echo "Available books:"
            ls books/*.md 2>/dev/null | sed 's|books/||' | sed 's|.md||' || echo "No books found"
            exit 1
        fi
        
        # Build single book in all formats
        ./scripts/build-all-formats.sh "$BOOK_NAME"
    else
        echo "📚 Building all books in all formats..."
        ./scripts/build-all-formats.sh
    fi
    
    echo ""
    echo "🎉 Production build complete!"
    echo ""
    echo "📁 Output files:"
    echo "   • HTML: public/<book-name>/<book-name>.html"
    echo "   • PDF: public/<book-name>/<book-name>.pdf (if WeasyPrint installed)"
    echo "   • EPUB: public/<book-name>/<book-name>.epub"
    echo "   • MOBI: public/<book-name>/<book-name>.mobi (if Calibre installed)"
    echo ""
    echo "📖 To view your books:"
    echo "   • Open HTML files in your browser"
    echo "   • Use any PDF viewer for PDF files"
    echo "   • Use any EPUB reader for EPUB files"
    echo "   • Transfer MOBI files to your Kindle"
fi 