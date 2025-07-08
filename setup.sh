#!/bin/bash
set -e

echo "🚀 Setting up Ebook Writer - Complete Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_info() {
    echo -e "${BLUE}ℹ${NC} $1"
}

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

print_status "Python 3 found: $(python3 --version)"

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    print_info "Creating virtual environment..."
    python3 -m venv .venv
    print_status "Virtual environment created"
else
    print_status "Virtual environment already exists"
fi

# Activate virtual environment
print_info "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
print_info "Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
print_info "Installing Python dependencies..."
pip install -r requirements.txt
print_status "Python dependencies installed"

# Check and install system tools
print_info "Checking system tools..."

# Check pandoc
if ! command -v pandoc &> /dev/null; then
    print_warning "Pandoc is not installed."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "Installing pandoc via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install pandoc
            print_status "Pandoc installed via Homebrew"
        else
            print_error "Homebrew not found. Please install pandoc manually:"
            print_info "brew install pandoc"
            print_info "Or download from: https://pandoc.org/installing.html"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Installing pandoc via apt..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y pandoc
            print_status "Pandoc installed via apt"
        else
            print_error "apt-get not found. Please install pandoc manually:"
            print_info "sudo apt-get install pandoc"
        fi
    else
        print_error "Please install pandoc manually:"
        print_info "Download from: https://pandoc.org/installing.html"
    fi
else
    print_status "Pandoc found: $(pandoc --version | head -n 1)"
fi

# Check jq
if ! command -v jq &> /dev/null; then
    print_warning "jq is not installed."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "Installing jq via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install jq
            print_status "jq installed via Homebrew"
        else
            print_error "Homebrew not found. Please install jq manually:"
            print_info "brew install jq"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Installing jq via apt..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get install -y jq
            print_status "jq installed via apt"
        else
            print_error "apt-get not found. Please install jq manually:"
            print_info "sudo apt-get install jq"
        fi
    else
        print_error "Please install jq manually:"
        print_info "Download from: https://jqlang.github.io/jq/download/"
    fi
else
    print_status "jq found: $(jq --version)"
fi

# Check WeasyPrint
if ! python3 -c "import weasyprint" 2>/dev/null; then
    print_warning "WeasyPrint is not installed in virtual environment."
    print_info "Installing WeasyPrint..."
    pip install weasyprint
    print_status "WeasyPrint installed"
else
    print_status "WeasyPrint found"
fi

# Check and install Calibre
if ! command -v ebook-convert &> /dev/null; then
    print_warning "Calibre is not installed. Installing Calibre for EPUB/MOBI conversion..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        print_info "Installing Calibre via Homebrew..."
        if command -v brew &> /dev/null; then
            brew install --cask calibre
            print_status "Calibre installed via Homebrew"
        else
            print_error "Homebrew not found. Please install Calibre manually:"
            print_info "brew install --cask calibre"
            print_info "Or download from: https://calibre-ebook.com/download"
        fi
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        print_info "Installing Calibre via apt..."
        if command -v apt-get &> /dev/null; then
            sudo apt-get update
            sudo apt-get install -y calibre
            print_status "Calibre installed via apt"
        else
            print_error "apt-get not found. Please install Calibre manually:"
            print_info "sudo apt-get install calibre"
        fi
    else
        print_error "Please install Calibre manually:"
        print_info "Download from: https://calibre-ebook.com/download"
    fi
else
    print_status "Calibre found: $(ebook-convert --version | head -n 1)"
fi

# Make scripts executable
print_info "Making scripts executable..."
chmod +x scripts/*.sh
chmod +x scripts/*.py
print_status "Scripts made executable"

# Create necessary directories
print_info "Creating output directories..."
mkdir -p public
print_status "Directories created"

# Test the setup
print_info "Testing setup..."

# Test pandoc
if command -v pandoc &> /dev/null; then
    print_status "Pandoc is working"
else
    print_error "Pandoc is not working"
fi

# Test jq
if command -v jq &> /dev/null; then
    print_status "jq is working"
else
    print_error "jq is not working"
fi

# Test WeasyPrint
if python3 -c "import weasyprint" 2>/dev/null; then
    print_status "WeasyPrint is working"
else
    print_error "WeasyPrint is not working"
fi

# Test Calibre
if command -v ebook-convert &> /dev/null; then
    print_status "Calibre is working"
else
    print_error "Calibre installation failed"
fi

# Check and install mermaid-cli for PDF mermaid rendering
if ! command -v mmdc &> /dev/null; then
    print_warning "mermaid-cli is not installed. Installing for PDF mermaid diagram rendering..."
    if command -v npm &> /dev/null; then
        print_info "Installing mermaid-cli via npm..."
        npm install -g @mermaid-js/mermaid-cli
        print_status "mermaid-cli installed via npm"
    else
        print_error "npm is not installed. Please install Node.js and npm first:"
        print_info "Download from: https://nodejs.org/"
        print_info "Then run: npm install -g @mermaid-js/mermaid-cli"
    fi
else
    print_status "mermaid-cli found: $(mmdc --version)"
fi

# Test mermaid-cli
if command -v mmdc &> /dev/null; then
    print_status "mermaid-cli is working"
else
    print_warning "mermaid-cli is not available (PDF mermaid diagrams will not render)"
fi

echo ""
echo "🎉 Setup Complete!"
echo "=================="
echo ""
echo "Available commands:"
echo "  • Build all formats: ./scripts/build-all-formats.sh"
echo "  • Build specific book: ./scripts/build-all-formats.sh <book-name>"
echo "  • Build HTML only: ./scripts/build-html.sh"
echo "  • List books: ./scripts/list-books.sh"
echo "  • Create new book: ./scripts/new-book.sh <name> <template> [title] [author]"
echo ""
echo "Supported formats:"
echo "  • HTML: Always available"
echo "  • EPUB: Full support (pandoc + Calibre)"
echo "  • PDF: Full support (WeasyPrint + mermaid-cli for diagrams)"
echo "  • MOBI: Full support (Calibre)"
echo ""
echo "Next steps:"
echo "  1. Activate virtual environment: source .venv/bin/activate"
echo "  2. List available books: ./scripts/list-books.sh"
echo "  3. Build all formats: ./scripts/build-all-formats.sh"