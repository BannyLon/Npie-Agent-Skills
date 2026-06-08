#!/bin/bash
# deploy-vercel.sh — Deploy an HTML slides file to Vercel
# Usage: bash deploy-vercel.sh <file.html> [project-name]

set -e

HTML_FILE="${1:-slides.html}"
PROJECT_NAME="${2:-html-slides}"

if [ ! -f "$HTML_FILE" ]; then
    echo "Error: File not found: $HTML_FILE"
    exit 1
fi

# Check for vercel CLI
if ! command -v vercel &> /dev/null; then
    echo "Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Create temp directory for deployment
DEPLOY_DIR=$(mktemp -d)
cp "$HTML_FILE" "$DEPLOY_DIR/index.html"

echo "Deploying $HTML_FILE to Vercel as project '$PROJECT_NAME'..."
cd "$DEPLOY_DIR"

# Deploy
vercel --prod --name "$PROJECT_NAME" --confirm

# Cleanup
rm -rf "$DEPLOY_DIR"

echo ""
echo "Done! Your slides are live on Vercel."
echo "Share the URL above with your audience."
