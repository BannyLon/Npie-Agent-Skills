#!/bin/bash
# export-pdf.sh — Export an HTML slides file to PDF
# Usage: bash export-pdf.sh <file.html> [output.pdf]
#
# Requires: chromium or google-chrome (headless)
# If neither is found, prints manual instructions.

set -e

HTML_FILE="${1:-slides.html}"
PDF_OUTPUT="${2:-slides.pdf}"

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: File not found: $HTML_FILE"
    exit 1
fi

# Find a headless browser
BROWSER=""
for cmd in chromium google-chrome google-chrome-stable "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"; do
    if command -v "$cmd" &> /dev/null || [ -x "$cmd" ]; then
        BROWSER="$cmd"
        break
    fi
done

if [ -z "$BROWSER" ]; then
    echo "No headless browser found (chromium/google-chrome)."
    echo ""
    echo "Manual export instructions:"
    echo "  1. Open $HTML_FILE in your browser"
    echo "  2. Press Ctrl+P / Cmd+P"
    echo "  3. Choose 'Save as PDF'"
    echo "  4. Set paper size to custom: 16:9 landscape (e.g., 25.4 x 14.29 cm)"
    echo "  5. Enable 'Background graphics'"
    echo "  6. Save as $PDF_OUTPUT"
    exit 1
fi

# Convert to absolute path
HTML_ABS=$(realpath "$HTML_FILE" 2>/dev/null || echo "$(cd "$(dirname "$HTML_FILE")" && pwd)/$(basename "$HTML_FILE")")
PDF_ABS=$(realpath "$PDF_OUTPUT" 2>/dev/null || echo "$(pwd)/$PDF_OUTPUT")

echo "Exporting $HTML_FILE → $PDF_OUTPUT using $BROWSER..."

"$BROWSER" \
    --headless \
    --disable-gpu \
    --no-sandbox \
    --print-to-pdf="$PDF_ABS" \
    --print-to-pdf-no-header \
    --no-pdf-header-footer \
    "file://$HTML_ABS"

echo ""
echo "PDF exported to: $PDF_OUTPUT"
echo "Note: Each slide will appear as one page in the PDF."
echo "If slides overlap, try opening manually and using browser Print for better results."
