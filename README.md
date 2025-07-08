# Ebook Writer

A beautiful, automated ebook generator that creates professional books in multiple formats with full styling preserved. Features dark/light theme support, smart build modes, and intelligent cleaning.

## ✨ Features

- **Multiple Formats**: HTML, PDF, EPUB, and MOBI
- **Dark/Light Themes**: Automatic theme switching based on user preferences
- **Beautiful Design**: Responsive layouts with embedded CSS
- **Mermaid Diagrams**: Interactive charts and flowcharts (rendered as PNG for PDF/EPUB)
- **Syntax Highlighting**: Code blocks with proper formatting (optimized for all formats)
- **Multiple Templates**: Different styles for different content types
- **Smart Build System**: Development and production modes
- **Intelligent Cleaning**: Targeted cleanup based on build scope
- **Automated Build**: One command builds everything

## 🚀 Quick Start

```bash
# Setup everything
./setup.sh

# Development mode (HTML only, fast)
./build.sh --dev

# Production mode (all formats)
./build.sh
```

## 📁 Project Structure

```
ebook-writer/
├── books/                    # Your markdown files
│   ├── afrinenglish-sample.md
│   ├── backendchallenges-sample.md
│   └── book-config.json     # Book configuration
├── templates/                # Design templates
│   ├── afrinenglish.css     # Light/dark theme support
│   ├── afrinenglish.html
│   ├── backendchallenges.css # Light/dark theme support
│   └── backendchallenges.html
├── public/                   # Generated output
│   ├── afrinenglish-sample/
│   │   ├── afrinenglish-sample.html
│   │   ├── afrinenglish-sample.pdf
│   │   ├── afrinenglish-sample.epub
│   │   └── afrinenglish-sample.mobi
│   └── backendchallenges-sample/
│       ├── backendchallenges-sample.html
│       ├── backendchallenges-sample.pdf
│       ├── backendchallenges-sample.epub
│       └── backendchallenges-sample.mobi
└── scripts/                  # Build automation
```

## 🛠️ Installation

### Prerequisites

- Python 3.7+
- Git

### Setup

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd ebook-writer
   ```

2. **Run the setup script:**

   ```bash
   ./setup.sh
   ```

   This will:

   - Create a Python virtual environment
   - Install all dependencies (pandoc, jq, WeasyPrint, Calibre)
   - Set up all tools
   - Test the installation

## 📖 Usage

### Build Modes

#### Development Mode (Fast)

```bash
# Build all books in HTML only (fast iteration)
./build.sh --dev

# Build specific book in HTML only
./build.sh --dev --book mybook
```

#### Production Mode (Complete)

```bash
# Build all books in all formats
./build.sh

# Build specific book in all formats
./build.sh --book mybook
```

#### Help

```bash
./build.sh --help
```

### Smart Cleaning System

The build system intelligently cleans based on your needs:

| Mode     | Scope         | Cleans                  | Preserves                |
| -------- | ------------- | ----------------------- | ------------------------ |
| **Dev**  | Specific Book | Only that book's HTML   | Other books, all formats |
| **Dev**  | All Books     | All HTML files          | PDF/EPUB/MOBI files      |
| **Prod** | All Books     | Entire public directory | Nothing (fresh start)    |
| **Prod** | Specific Book | Book folder + CSS files | Other books              |

## 🎨 Customization

### Add New Book

```bash
./scripts/new-book.sh my-new-book
```

### Create New Template

```bash
./scripts/new-template.sh my-template
```

### Modify Styling

Edit the CSS files in `templates/`:

- `afrinenglish.css` - For language learning books
- `backendchallenges.css` - For technical content

Both templates support dark/light themes automatically.

### Dark/Light Theme Support

The system automatically detects user's theme preference:

- **Light Theme**: Clean, readable design
- **Dark Theme**: Easy on the eyes, perfect for night reading
- **Automatic Switching**: Based on system preferences
- **E-reader Compatible**: Works with EPUB and MOBI formats

## 📱 Viewing Your Books

- **HTML**: Open in any web browser (supports dark/light themes)
- **PDF**: Use any PDF viewer (Adobe Reader, Preview, etc.)
- **EPUB**: Use any EPUB reader (Apple Books, Calibre, etc.)
- **MOBI**: Transfer to Kindle device or use Kindle app

## 🔧 Advanced Configuration

### Book Configuration

Edit `books/book-config.json` to customize:

- Book titles and authors
- Template selection
- Metadata

Example:

```json
{
  "books": {
    "mybook": {
      "title": "My Amazing Book",
      "author": "Your Name",
      "template": "backendchallenges"
    }
  },
  "templates": {
    "backendchallenges": {
      "css": "backendchallenges.css",
      "html": "backendchallenges.html"
    }
  }
}
```

### Template System

Create custom templates:

1. Add CSS file to `templates/` (include dark theme support)
2. Add HTML template to `templates/`
3. Update `book-config.json`

## 🆘 Troubleshooting

### Common Issues

**Build fails?**

```bash
# Reinstall dependencies
./setup.sh
```

**Missing fonts?**

```bash
# Install system fonts
./scripts/setup-ebook-tools.sh
```

**PDF not generating?**

```bash
# Install WeasyPrint
pip install weasyprint
```

**EPUB/MOBI not generating?**

```bash
# Install Calibre
./scripts/install-calibre.sh
```

### Dependencies

- **Pandoc**: Markdown to HTML conversion
- **WeasyPrint**: HTML to PDF conversion
- **Calibre**: EPUB to MOBI conversion
- **Python packages**: See `requirements.txt`

## 🎯 Supported Formats

| Format | Purpose     | Requirements             | Theme Support |
| ------ | ----------- | ------------------------ | ------------- |
| HTML   | Web viewing | None                     | ✅ Dark/Light |
| PDF    | Printing    | WeasyPrint + mermaid-cli | ✅ Dark/Light |
| EPUB   | E-readers   | Pandoc                   | ✅ Dark/Light |
| MOBI   | Kindle      | Calibre                  | ✅ Dark/Light |

## 🚀 Development Workflow

### Fast Iteration

```bash
# Quick HTML build for development
./build.sh --dev --book mybook

# View in browser and test themes
open public/mybook/mybook.html
```

### Production Release

```bash
# Full build with all formats
./build.sh --book mybook

# All files ready for distribution
ls public/mybook/
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `./build.sh --dev`
5. Submit a pull request

## 📄 License

This project is private and copyrighted to Param Harrison (Secret SaaS OÜ).

## 🙏 Acknowledgments

- **Pandoc** for markdown processing
- **WeasyPrint** for PDF generation
- **Calibre** for EPUB/MOBI conversion
- **Mermaid** for diagram rendering
