#!/bin/bash
set -e

echo "📚 Building All Books in All Formats"
echo "===================================="

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

# Clean up public directory to avoid accumulating files
echo ""
echo "🧹 Cleaning up public directory..."
if [ -d "public" ]; then
    rm -rf public/*
    echo "✅ Public directory cleaned"
else
    echo "ℹ️ Public directory doesn't exist yet"
fi

# Build all books in all formats
echo ""
echo "🚀 Building all books in all formats..."
./scripts/build-all-formats.sh

echo ""
echo "🎉 Build complete!"
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