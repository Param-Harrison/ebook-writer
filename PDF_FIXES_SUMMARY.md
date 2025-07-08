# PDF Generation Fixes

## Issues Fixed

### 1. Syntax Highlighting (Prism.js) in PDF

**Problem:** Code blocks in PDF had black overlays and unreadable text, while HTML version worked perfectly.

**Root Cause:**

- Prism.js is a JavaScript library that doesn't run in static HTML-to-PDF conversion (WeasyPrint)
- Conflicting CSS styles from Prism CDN were causing dark overlays
- PDF was trying to use Prism CSS but without the JavaScript to apply proper highlighting

**Solution:**

- Created `scripts/fix-pdf-code-blocks.py` that:
  - Removes Prism CSS and JS links from HTML for PDF processing
  - Adds PDF-specific CSS overrides with `!important` declarations
  - Ensures light background (`#f6f8fa`) and dark text (`#24292e`) for all code blocks
  - Maintains syntax highlighting colors for tokens
  - Prevents any dark overlays or backgrounds

### 2. Mermaid Diagrams in PDF

**Problem:** Mermaid diagrams rendered perfectly in HTML but showed only code text in PDF.

**Root Cause:**

- Mermaid diagrams use JavaScript to render, which doesn't work in static PDF generation
- The fallback was just showing the raw mermaid code as text

**Solution:**

- Created `scripts/render-mermaid-for-pdf.py` that:
  - Uses `mermaid-cli` (mmdc) to pre-render mermaid diagrams as SVG
  - Converts SVG to base64 data URLs for embedding in HTML
  - Replaces `<div class="mermaid">...</div>` with `<img src="data:image/svg+xml;base64,...">`
  - Maintains high-quality SVG rendering for print

## New Scripts Created

### 1. `scripts/render-mermaid-for-pdf.py`

- Renders mermaid diagrams as SVG using mermaid-cli
- Embeds SVGs as data URLs in HTML
- Replaces mermaid divs with img tags for PDF compatibility
- Creates `mermaid-images/` directory to store SVG files

### 2. `scripts/fix-pdf-code-blocks.py`

- Removes Prism CSS/JS links that cause conflicts
- Adds PDF-specific code block styles with `!important` overrides
- Ensures readable light background and dark text
- Maintains syntax highlighting colors

### 3. `scripts/install-mermaid-cli.sh`

- Installs mermaid-cli globally via npm
- Checks for existing installation
- Provides clear installation instructions

## Updated Build Process

### Modified `scripts/build-all-formats.sh`

- Creates a separate HTML copy for PDF processing (`book-name-pdf.html`)
- Runs mermaid rendering and code block fixes on PDF-specific HTML
- Preserves original HTML for web viewing
- Uses processed HTML for PDF generation

## Installation Requirements

### For Mermaid Rendering:

```bash
# Install mermaid-cli
./scripts/install-mermaid-cli.sh

# Or manually:
npm install -g @mermaid-js/mermaid-cli
```

### For PDF Generation:

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Build all formats (including PDF with fixes)
./scripts/build-all-formats.sh <book-name>
```

## How It Works

1. **HTML Build:** Normal HTML generation with Prism.js and Mermaid.js
2. **PDF Processing:**

   - Copy HTML to `book-name-pdf.html`
   - Render mermaid diagrams as SVG images
   - Remove Prism CSS/JS and add PDF-specific styles
   - Generate PDF from processed HTML

3. **Result:**
   - HTML: Interactive with Prism.js and Mermaid.js
   - PDF: Static with rendered SVG diagrams and readable code blocks

## Benefits

- ✅ **HTML version unchanged:** Still uses Prism.js and Mermaid.js perfectly
- ✅ **PDF code blocks readable:** Light background, dark text, no overlays
- ✅ **PDF mermaid diagrams rendered:** High-quality SVG images
- ✅ **Separate processing:** PDF fixes don't affect HTML workflow
- ✅ **Uses existing tools:** Leverages mermaid-cli and WeasyPrint
- ✅ **Virtual environment:** Uses `.venv` as requested

## Testing

Both sample books (`backendchallenges-sample` and `afrinenglish-sample`) were successfully built with:

- 11 mermaid diagrams rendered as SVG for backendchallenges
- 10 mermaid diagrams rendered as SVG for afrinenglish
- Code blocks properly styled for PDF
- HTML versions remain unchanged and working perfectly
