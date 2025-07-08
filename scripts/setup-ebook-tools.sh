#!/bin/bash
set -e

echo "Setting up ebook generation tools..."

# Check if we're in a virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Not in a virtual environment. Consider activating one first."
    echo "Run: source .venv/bin/activate"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Check for pandoc
if ! command -v pandoc &> /dev/null; then
    echo "Error: pandoc is not installed."
    echo "Please install pandoc from https://pandoc.org/installing.html"
    echo ""
    echo "On macOS: brew install pandoc"
    echo "On Ubuntu/Debian: sudo apt-get install pandoc"
    echo "On Windows: Download from https://pandoc.org/installing.html"
    exit 1
else
    echo "✓ pandoc is installed"
fi

# Check for jq
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed."
    echo "Please install jq for JSON parsing."
    echo ""
    echo "On macOS: brew install jq"
    echo "On Ubuntu/Debian: sudo apt-get install jq"
    echo "On Windows: Download from https://jqlang.github.io/jq/download/"
    exit 1
else
    echo "✓ jq is installed"
fi

# Check for calibre (for EPUB/MOBI conversion)
if ! command -v ebook-convert &> /dev/null; then
    echo "Warning: calibre is not installed. EPUB and MOBI conversion will be limited."
    echo "Install calibre from https://calibre-ebook.com/download"
    echo ""
    echo "On macOS: brew install --cask calibre"
    echo "On Ubuntu/Debian: sudo apt-get install calibre"
    echo "On Windows: Download from https://calibre-ebook.com/download"
else
    echo "✓ calibre is installed"
fi

# Check for WeasyPrint
if ! python3 -c "import weasyprint" 2>/dev/null; then
    echo "Warning: WeasyPrint is not installed. PDF generation will not work."
    echo "Install with: pip install weasyprint"
    echo ""
    echo "Note: WeasyPrint requires system dependencies:"
    echo "On macOS: brew install cairo pango gdk-pixbuf libffi"
    echo "On Ubuntu/Debian: sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev"
else
    echo "✓ WeasyPrint is installed"
fi

# Make scripts executable
echo "Making scripts executable..."
chmod +x scripts/*.sh
chmod +x scripts/*.py

echo ""
echo "Setup complete!"
echo ""
echo "Available commands:"
echo "- Build all formats: ./scripts/build-all-formats.sh"
echo "- Build specific book: ./scripts/build-all-formats.sh <book-name>"
echo ""
echo "Supported formats:"
echo "- HTML (always available)"
echo "- EPUB (requires pandoc)"
echo "- PDF (requires WeasyPrint)"
echo "- MOBI (requires calibre)" 