#!/bin/bash

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "Error: jq is not installed. Please install jq first."
    exit 1
fi

CONFIG_FILE="books/book-config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: book-config.json not found"
    exit 1
fi

echo "📚 Available Books:"
echo "=================="

jq -r '.books | to_entries[] | "📖 \(.key):\n   Title: \(.value.title)\n   Author: \(.value.author)\n   Template: \(.value.template)\n   Category: \(.value.category)\n   Description: \(.value.description)\n"' "$CONFIG_FILE"

echo ""
echo "🎨 Available Templates:"
echo "======================"

jq -r '.templates | to_entries[] | "🎨 \(.key):\n   Name: \(.value.name)\n   Description: \(.value.description)\n"' "$CONFIG_FILE"

echo ""
echo "📁 Book Files:"
echo "=============="

for book_file in books/*.md; do
    if [ -f "$book_file" ]; then
        book_name=$(basename "$book_file" .md)
        if jq -e ".books[\"$book_name\"]" "$CONFIG_FILE" > /dev/null 2>&1; then
            echo "✅ $book_name.md (configured)"
        else
            echo "⚠️  $book_name.md (not configured)"
        fi
    fi
done 