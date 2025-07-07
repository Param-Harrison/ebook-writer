#!/bin/bash
set -e

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq first."
    exit 1
fi

if [ $# -lt 2 ]; then
    echo "Usage: $0 <book-name> <template> [title] [author]"
    echo "Available templates:"
    jq -r '.templates | to_entries[] | "  \(.key): \(.value.name)"' books/book-config.json
    exit 1
fi

BOOK_NAME=$1
TEMPLATE=$2
TITLE=${3:-"$BOOK_NAME"}
AUTHOR=${4:-"Author"}

CONFIG_FILE="books/book-config.json"

# Check if template exists
if ! jq -e ".templates[\"$TEMPLATE\"]" "$CONFIG_FILE" > /dev/null 2>&1; then
    echo "Error: Template '$TEMPLATE' not found"
    echo "Available templates:"
    jq -r '.templates | to_entries[] | "  \(.key): \(.value.name)"' "$CONFIG_FILE"
    exit 1
fi

# Create book file
BOOK_FILE="books/$BOOK_NAME.md"
if [ -f "$BOOK_FILE" ]; then
    echo "Warning: Book file $BOOK_FILE already exists"
    read -p "Overwrite? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create the book file with basic structure
cat > "$BOOK_FILE" << EOF
# $TITLE

> Created with Ebook Writer

## Introduction

Welcome to your new book!

## Chapter 1

Your content goes here...

## Chapter 2

More content...

## Conclusion

Thank you for reading!
EOF

# Add to configuration
jq ".books[\"$BOOK_NAME\"] = {
  \"title\": \"$TITLE\",
  \"author\": \"$AUTHOR\",
  \"template\": \"$TEMPLATE\",
  \"category\": \"general\",
  \"description\": \"A new book created with Ebook Writer\"
}" "$CONFIG_FILE" > "$CONFIG_FILE.tmp" && mv "$CONFIG_FILE.tmp" "$CONFIG_FILE"

echo "✓ Created book: $BOOK_NAME.md"
echo "✓ Added to configuration with template: $TEMPLATE"
echo ""
echo "Next steps:"
echo "1. Edit books/$BOOK_NAME.md to add your content"
echo "2. Run './scripts/build-html.sh $BOOK_NAME' to build"
echo "3. Check public/$BOOK_NAME.html for the result" 