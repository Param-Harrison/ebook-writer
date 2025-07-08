# Ebook Writer

A beautiful, automated ebook generator that creates professional books in multiple formats with full styling preserved.

## ✨ Features

- **Multiple Formats**: HTML, PDF, and MOBI
- **Beautiful Design**: Responsive layouts with embedded CSS
- **Mermaid Diagrams**: Interactive charts and flowcharts (rendered as SVG in PDF)
- **Syntax Highlighting**: Code blocks with proper formatting (Prism.js in HTML, optimized for PDF)
- **Multiple Templates**: Different styles for different content types
- **Automated Build**: One command builds everything

## 🚀 Quick Start

```bash
# Setup everything
./setup.sh

# Build all books
./build.sh
```

## 📁 Project Structure

```
ebook-writer/
├── books/                    # Your markdown files
│   ├── afrinenglish-sample.md
│   └── backendchallenges-sample.md
├── templates/                # Design templates
│   ├── afrinenglish.css
│   ├── afrinenglish.html
│   ├── backendchallenges.css
│   └── backendchallenges.html
├── public/                   # Generated output
│   ├── afrinenglish-sample/
│   │   ├── afrinenglish-sample.html
│   │   ├── afrinenglish-sample.pdf
│   │   └── afrinenglish-sample.mobi
│   └── backendchallenges-sample/
│       ├── backendchallenges-sample.html
│       ├── backendchallenges-sample.pdf
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
   - Install all dependencies (pandoc, jq, WeasyPrint)
   - Set up all tools
   - Test the installation

## 📖 Usage

### Build All Books

```bash
./build.sh
```

This generates all books in all formats:

- HTML files for web viewing
- PDF files for printing
- MOBI files for Kindle

### Build Specific Book

```bash
./build.sh afrinenglish-sample
```

### Individual Formats

```bash
# HTML only
./scripts/build-html.sh afrinenglish-sample

# PDF only
python3 scripts/build-pdf.py public/afrinenglish-sample/afrinenglish-sample.html public/afrinenglish-sample/afrinenglish-sample.pdf
```

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

## 📱 Viewing Your Books

- **HTML**: Open in any web browser
- **PDF**: Use any PDF viewer (Adobe Reader, Preview, etc.)
- **MOBI**: Transfer to Kindle device or use Kindle app

## 🔧 Advanced Configuration

### Book Configuration

Edit `books/book-config.json` to customize:

- Book titles and authors
- Template selection
- Metadata

### Template System

Create custom templates:

1. Add CSS file to `templates/`
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

### Dependencies

- **Pandoc**: Markdown to HTML conversion
- **WeasyPrint**: HTML to PDF conversion
- **Python packages**: See `requirements.txt`

## 🎯 Supported Formats

| Format | Purpose     | Requirements             |
| ------ | ----------- | ------------------------ |
| HTML   | Web viewing | None                     |
| PDF    | Printing    | WeasyPrint + mermaid-cli |
| MOBI   | Kindle      | Calibre                  |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with `./build.sh`
5. Submit a pull request

## 📄 License

This project is private and copyrighted to Param Harrison (Secret SaaS OÜ).

## 🙏 Acknowledgments

- **Pandoc** for markdown processing
- **WeasyPrint** for PDF generation
- **Calibre** for MOBI conversion
