#!/bin/bash
set -e

echo "Installing mermaid-cli for PDF mermaid diagram rendering..."

# Check if npm is available
if ! command -v npm &> /dev/null; then
    echo "Error: npm is not installed. Please install Node.js and npm first."
    echo "Download from: https://nodejs.org/"
    exit 1
fi

# Check if mermaid-cli is already installed
if command -v mmdc &> /dev/null; then
    echo "✓ mermaid-cli is already installed"
    mmdc --version
    exit 0
fi

# Install mermaid-cli globally
echo "Installing mermaid-cli globally..."
npm install -g @mermaid-js/mermaid-cli

# Verify installation
if command -v mmdc &> /dev/null; then
    echo "✓ mermaid-cli installed successfully"
    mmdc --version
else
    echo "Error: Failed to install mermaid-cli"
    exit 1
fi

echo ""
echo "mermaid-cli is now ready for PDF mermaid diagram rendering!"
echo "You can now build PDFs with rendered mermaid diagrams using:"
echo "  ./scripts/build-all-formats.sh <book-name>" 