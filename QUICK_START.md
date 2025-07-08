# Quick Start Guide

Get your beautiful ebooks in multiple formats with full styling in just 2 steps!

## 🚀 Two-Step Setup

### Step 1: Setup Everything

```bash
./setup.sh
```

This automatically:

- ✅ Creates Python virtual environment
- ✅ Installs all dependencies (pandoc, jq, WeasyPrint, Calibre)
- ✅ Sets up all tools
- ✅ Tests the installation

### Step 2: Build All Books

```bash
./build.sh
```

This automatically:

- ✅ Activates virtual environment
- ✅ Builds all books in all formats
- ✅ Embeds CSS styling in all formats
- ✅ Generates HTML, EPUB, PDF, and MOBI

## 📚 What You Get

After running the build, you'll have:

```
public/
├── afrinenglish-sample/
│   ├── afrinenglish-sample.html    # Beautiful web version
│   ├── afrinenglish-sample.epub    # E-reader format
│   ├── afrinenglish-sample.pdf     # Print-ready PDF
│   └── afrinenglish-sample.mobi    # Kindle format
└── backendchallenges-sample/
    ├── backendchallenges-sample.html
    ├── backendchallenges-sample.epub
    ├── backendchallenges-sample.pdf
    └── backendchallenges-sample.mobi
```

## 🎨 Styling Features

All formats preserve your beautiful styling:

- ✅ **HTML**: Full CSS with interactive elements
- ✅ **EPUB**: Embedded CSS for e-readers
- ✅ **PDF**: Print-ready with preserved layout
- ✅ **MOBI**: Kindle-optimized styling

## 📖 Viewing Your Books

- **HTML**: Open in any web browser
- **EPUB**: Use any e-reader app (Apple Books, Calibre, etc.)
- **PDF**: Use any PDF viewer
- **MOBI**: Transfer to Kindle device

## 🔧 Advanced Usage

### Build Specific Book

```bash
./scripts/build-all-formats.sh <book-name>
```

### Build Only HTML

```bash
./scripts/build-html.sh
```

### List Available Books

```bash
./scripts/list-books.sh
```

### Create New Book

```bash
./scripts/new-book.sh <name> <template> [title] [author]
```

## 🛠️ Troubleshooting

### If setup fails:

1. Make sure Python 3 is installed
2. On macOS: `brew install python3`
3. On Ubuntu: `sudo apt-get install python3`

### If build fails:

1. Activate virtual environment: `source .venv/bin/activate`
2. Check if pandoc is installed: `pandoc --version`
3. Check if WeasyPrint is working: `python3 -c "import weasyprint"`

### For MOBI generation:

1. Install Calibre: `./scripts/install-calibre.sh`
2. Or manually: `brew install --cask calibre`

## 📋 Requirements

- **Python 3.7+**
- **macOS/Linux/Windows**
- **Internet connection** (for initial setup)

## 🎯 Supported Formats

| Format | Purpose     | Requirements |
| ------ | ----------- | ------------ |
| HTML   | Web viewing | None         |
| EPUB   | E-readers   | Pandoc       |
| PDF    | Printing    | WeasyPrint   |
| MOBI   | Kindle      | Calibre      |

## 🎉 That's It!

Your ebook writer is now ready to create beautiful, professional ebooks in all major formats with full styling preserved!
