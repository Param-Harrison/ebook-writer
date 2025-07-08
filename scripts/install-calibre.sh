#!/bin/bash
set -e

echo "Installing Calibre for EPUB/MOBI conversion..."

# Detect OS and install Calibre
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if command -v brew &> /dev/null; then
        echo "Installing Calibre via Homebrew..."
        brew install --cask calibre
    else
        echo "Homebrew not found. Please install Calibre manually:"
        echo "1. Download from https://calibre-ebook.com/download"
        echo "2. Install the downloaded package"
    fi
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v apt-get &> /dev/null; then
        echo "Installing Calibre via apt..."
        sudo apt-get update
        sudo apt-get install -y calibre
    elif command -v yum &> /dev/null; then
        echo "Installing Calibre via yum..."
        sudo yum install -y calibre
    else
        echo "Package manager not found. Please install Calibre manually:"
        echo "1. Download from https://calibre-ebook.com/download"
        echo "2. Follow installation instructions for your distribution"
    fi
else
    echo "Unsupported OS. Please install Calibre manually:"
    echo "1. Download from https://calibre-ebook.com/download"
    echo "2. Follow installation instructions for your OS"
fi

echo ""
echo "After installation, you can generate MOBI files with:"
echo "./scripts/build-all-formats.sh <book-name>" 