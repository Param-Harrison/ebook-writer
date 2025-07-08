# Ebook Format Generation Guide

This guide explains how to generate your books in multiple formats: HTML, EPUB, PDF, and MOBI.

## Quick Start

### 1. Setup (One-time)

```bash
# Complete setup - installs everything automatically
./setup.sh
```

### 2. Generate All Formats

```bash
# Build all books in all formats
./scripts/build-all-formats.sh

# Build specific book in all formats
./scripts/build-all-formats.sh <book-name>
```

## Supported Formats

### HTML (Always Available)

- **Purpose**: Web viewing, sharing, and preview
- **Requirements**: None (built-in)
- **Output**: `public/<book-name>/<book-name>.html`
- **Features**: Full styling, interactive elements, responsive design

### EPUB (E-book Format)

- **Purpose**: E-readers, tablets, mobile devices
- **Requirements**: Pandoc
- **Output**: `public/<book-name>/<book-name>.epub`
- **Features**: Reflowable text, embedded fonts, table of contents

### PDF (Print-Ready)

- **Purpose**: Printing, archiving, professional distribution
- **Requirements**: WeasyPrint
- **Output**: `public/<book-name>/<book-name>.pdf`
- **Features**: Fixed layout, preserved styling, high quality

### MOBI (Kindle Format)

- **Purpose**: Amazon Kindle devices
- **Requirements**: Calibre
- **Output**: `public/<book-name>/<book-name>.mobi`
- **Features**: Kindle-optimized, DRM-free

## Individual Format Generation

### HTML Only

```bash
./scripts/build-html.sh                    # All books
./scripts/build-html.sh <book-name>       # Specific book
```

### EPUB Only

```bash
python3 scripts/build-epub.py <book-name>
```

### PDF Only

```bash
python3 scripts/build-pdf.py <html-file> <pdf-file> [css-file]
```

### MOBI Only

```bash
# First generate EPUB, then convert to MOBI
python3 scripts/build-epub.py <book-name>
ebook-convert public/<book-name>/<book-name>.epub public/<book-name>/<book-name>.mobi
```

## Format-Specific Features

### HTML Format

- ✅ Full CSS styling
- ✅ Interactive elements (Mermaid diagrams, code highlighting)
- ✅ Responsive design
- ✅ Custom templates
- ✅ Table of contents

### EPUB Format

- ✅ Embedded CSS styling
- ✅ Reflowable text
- ✅ Table of contents
- ✅ Metadata (title, author, description)
- ✅ Cross-platform compatibility

### PDF Format

- ✅ Preserved styling
- ✅ Fixed layout
- ✅ Print-optimized
- ✅ High quality output
- ✅ Page breaks and margins

### MOBI Format

- ✅ Kindle compatibility
- ✅ Reflowable text
- ✅ Embedded fonts
- ✅ DRM-free
- ✅ Cross-device sync

## Installation Requirements

### Required Tools

- **Python 3**: The entire system
- **Homebrew** (macOS) or **apt** (Linux): For system tools

### Automatically Installed Tools

- **Pandoc**: Markdown to HTML/EPUB conversion
- **jq**: JSON configuration parsing
- **WeasyPrint**: PDF generation
- **Calibre**: EPUB/MOBI conversion

### Installation Commands

#### Quick Setup (Recommended)

```bash
# Complete setup - installs everything automatically
./setup.sh
```

#### Manual Setup (Alternative)

If you prefer manual installation:

##### macOS

```bash
# Install required tools
brew install pandoc jq

# Install optional tools
brew install --cask calibre
pip install weasyprint
```

##### Ubuntu/Debian

```bash
# Install required tools
sudo apt-get install pandoc jq

# Install optional tools
sudo apt-get install calibre
pip install weasyprint
```

##### Windows

- Download Pandoc from https://pandoc.org/installing.html
- Download jq from https://jqlang.github.io/jq/download/
- Download Calibre from https://calibre-ebook.com/download
- Install WeasyPrint: `pip install weasyprint`

## Troubleshooting

### PDF Generation Issues

```bash
# Check WeasyPrint installation
python3 -c "import weasyprint; print('OK')"

# Install system dependencies (macOS)
brew install cairo pango gdk-pixbuf libffi

# Install system dependencies (Ubuntu)
sudo apt-get install libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev
```

### EPUB Generation Issues

```bash
# Check pandoc installation
pandoc --version

# Check if mermaid filter is available
pandoc-mermaid-filter --help
```

### MOBI Generation Issues

```bash
# Check Calibre installation
ebook-convert --version

# Install Calibre
./scripts/install-calibre.sh
```

## Output Structure

After running the build scripts, your output will be organized as follows:

```
public/
├── afrinenglish-sample/
│   ├── afrinenglish-sample.html
│   ├── afrinenglish-sample.epub
│   ├── afrinenglish-sample.pdf
│   ├── afrinenglish-sample.mobi
│   └── afrinenglish-sample-epub.css
├── backendchallenges-sample/
│   ├── backendchallenges-sample.html
│   ├── backendchallenges-sample.epub
│   ├── backendchallenges-sample.pdf
│   ├── backendchallenges-sample.mobi
│   └── backendchallenges-sample-epub.css
└── *.css (template CSS files)
```

## Advanced Configuration

### Custom PDF Settings

Edit `scripts/build-pdf.py` to modify:

- Page margins
- Font sizes
- Page breaks
- Image handling

### Custom EPUB Settings

Edit `scripts/build-epub.py` to modify:

- CSS adjustments
- Metadata
- Table of contents

### Custom MOBI Settings

Use Calibre's command-line options:

```bash
ebook-convert input.epub output.mobi \
  --title "Book Title" \
  --authors "Author Name" \
  --language en \
  --no-chapters-in-toc
```

## Performance Tips

1. **Parallel Processing**: Generate multiple books simultaneously
2. **Caching**: Reuse generated HTML for PDF conversion
3. **Optimization**: Compress images for faster processing
4. **Cleanup**: Remove temporary files after generation

## Quality Assurance

### Before Distribution

- [ ] Test HTML in multiple browsers
- [ ] Validate EPUB with epubcheck
- [ ] Preview PDF for layout issues
- [ ] Test MOBI on Kindle device/simulator
- [ ] Check metadata accuracy
- [ ] Verify table of contents
- [ ] Test responsive design (HTML)
- [ ] Validate accessibility features
