# Ebook Writer

A simple, Pandoc/Markdown/Mermaid-based ebook writer for creating beautifully laid out English books (afrinenglish.com) and coding ebooks (backendchallenges.com).

## Features

- Write books in Markdown
- Render to beautiful HTML with custom templates
- Mermaid diagram support (with live rendering via pandoc-mermaid-filter)
- Scalable system supporting many books of varying sizes (10-120+ pages)
- Configuration-based book management
- Multiple template support

## Project Structure

- `books/` — Markdown source files and book configuration
- `templates/` — Custom HTML/CSS templates for different book types
- `public/` — Output HTML files
- `scripts/` — Automation scripts for book and template management
- `requirements.txt` — Python dependencies for filters

## Quick Start

### Prerequisites

- [Python 3](https://www.python.org/downloads/) - for the entire system
- [Homebrew](https://brew.sh/) (macOS) or [apt](https://ubuntu.com/) (Linux) - for system tools

**Note**: All other tools (pandoc, jq, WeasyPrint, Calibre) are automatically installed by the setup script.

### Quick Setup

Run the complete setup script to install everything automatically:

```bash
./setup.sh
```

This will:

- Create and activate a Python virtual environment
- Install all Python dependencies
- Install system tools (pandoc, jq, WeasyPrint)
- Make all scripts executable
- Test the installation

### Manual Setup (Alternative)

If you prefer manual setup:

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Setup ebook tools (optional, for EPUB/PDF/MOBI):
   ```bash
   ./scripts/setup-ebook-tools.sh
   ```

### List Available Books and Templates

```bash
./scripts/list-books.sh
```

### Create a New Book

```bash
./scripts/new-book.sh <book-name> <template> [title] [author]
```

Example:

```bash
./scripts/new-book.sh my-english-book afrinenglish "My English Book" "John Doe"
```

### Create a New Template

```bash
./scripts/new-template.sh <template-name> <template-title> <description>
```

Example:

```bash
./scripts/new-template.sh modern "Modern Template" "Clean and modern design"
```

### Build Books

#### Quick Build (All Formats)

```bash
# Build all books in all formats (HTML, EPUB, PDF, MOBI)
./build.sh
```

#### Individual Build Commands

```bash
# Build all books in HTML format
./scripts/build-html.sh

# Build specific book in HTML format
./scripts/build-html.sh <book-name>

# Build all books in all formats
./scripts/build-all-formats.sh

# Build specific book in all formats
./scripts/build-all-formats.sh <book-name>
```

### Supported Formats

- **HTML**: Always available, beautiful web-ready output
- **EPUB**: E-book format for most e-readers (requires pandoc)
- **PDF**: Print-ready PDF with preserved styles (requires WeasyPrint)
- **MOBI**: Kindle-compatible format (requires Calibre)

## Book Configuration

Books are configured in `books/book-config.json`:

```json
{
  "books": {
    "book-name": {
      "title": "Book Title",
      "author": "Author Name",
      "template": "template-name",
      "category": "category",
      "description": "Book description"
    }
  }
}
```

## Templates

Each template consists of:

- `templates/template-name.html` - Pandoc HTML template
- `templates/template-name.css` - Custom CSS styling

### Available Templates

- **afrinenglish** - Colorful, elegant layout for English learning books
- **backendchallenges** - Intense, code-focused layout for programming books

## Writing Books

Write your books in Markdown with these features:

### Boxes

```markdown
<div class="box">

Your content in a styled box

</div>
```

### Multi-columns

```markdown
<div class="columns">

- Column 1 content
- Column 2 content

</div>
```

### Mermaid Diagrams

````markdown
```mermaid
graph TD
  A --> B
  B --> C
```
````

````

### Code Blocks
```markdown
```python
def hello():
    return "Hello, World!"
````

## Roadmap

- Add more beautiful templates
- Web-based editor
- Template marketplace

---

## Advanced: Live Mermaid Rendering with Pandoc Filter

To enable live Mermaid diagram rendering in your HTML output:

1. **Activate your virtual environment:**
   ```bash
   source .venv/bin/activate
   ```
2. **Build with the filter:**
   ```bash
   pandoc books/afrinenglish-sample.md -o public/afrinenglish-sample.html --template=templates/afrinenglish.html --standalone --toc --highlight-style=pygments --filter pandoc-mermaid-filter
   ```
3. **Or update your build script to use the filter.**

## Multi-Format Generation

This project now supports generating books in multiple formats while preserving styles:

- **HTML**: Web-ready with full styling
- **EPUB**: E-reader compatible
- **PDF**: Print-ready with preserved layout
- **MOBI**: Kindle compatible

See [FORMATS.md](FORMATS.md) for detailed instructions on generating all formats.

---
