#!/usr/bin/env python3
"""
extract-pptx.py — Extract text and images from PowerPoint files.

Usage:
    python extract-pptx.py <file.pptx> [--output-dir <dir>] [--format json|markdown]

Output:
    - Extracted text with slide structure (titles, bodies, notes)
    - Images saved to output directory or embedded as base64 data URIs
    - JSON or Markdown output format
"""

import argparse
import base64
import json
import os
import sys
from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET


def extract_text_from_pptx(pptx_path: str) -> list[dict]:
    """Extract text content from a PPTX file by parsing its XML directly."""
    slides = []

    with ZipFile(pptx_path, 'r') as z:
        # Find slide files
        slide_files = sorted(
            [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')],
            key=lambda x: int(''.join(c for c in x if c.isdigit()) or '0')
        )

        # Load shared strings if present
        shared_strings = []
        if 'ppt/sharedStrings.xml' in z.namelist():
            root = ET.fromstring(z.read('ppt/sharedStrings.xml'))
            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}
            for si in root.findall('.//a:si', ns):
                text_parts = []
                for t in si.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                    if t.text:
                        text_parts.append(t.text)
                shared_strings.append(''.join(text_parts))

        # Extract text from each slide
        for slide_file in slide_files:
            root = ET.fromstring(z.read(slide_file))
            ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

            texts = []
            for t in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                if t.text and t.text.strip():
                    texts.append(t.text.strip())

            # Reconstruct paragraphs
            paragraphs = []
            for p in root.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}p'):
                para_texts = []
                for t in p.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t'):
                    if t.text and t.text.strip():
                        para_texts.append(t.text.strip())
                if para_texts:
                    paragraphs.append(''.join(para_texts))

            slides.append({
                'number': len(slides) + 1,
                'paragraphs': paragraphs,
                'all_text': texts
            })

    return slides


def extract_images_from_pptx(pptx_path: str, output_dir: str) -> list[dict]:
    """Extract images from PPTX and save as files, return metadata."""
    images = []
    os.makedirs(output_dir, exist_ok=True)

    with ZipFile(pptx_path, 'r') as z:
        image_extensions = {'.png', '.jpg', '.jpeg', '.gif', '.bmp', '.svg', '.webp'}
        image_files = [f for f in z.namelist()
                       if f.startswith('ppt/media/') and Path(f).suffix.lower() in image_extensions]

        for i, img_file in enumerate(image_files):
            ext = Path(img_file).suffix.lower()
            data = z.read(img_file)
            b64 = base64.b64encode(data).decode('ascii')
            mime_map = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                        '.gif': 'image/gif', '.bmp': 'image/bmp', '.svg': 'image/svg+xml',
                        '.webp': 'image/webp'}

            images.append({
                'index': i,
                'original_path': img_file,
                'extension': ext,
                'mime_type': mime_map.get(ext, 'application/octet-stream'),
                'size_bytes': len(data),
                'base64': b64,
                'data_uri': f'data:{mime_map.get(ext, "application/octet-stream")};base64,{b64}'
            })

            # Also save to file
            out_path = os.path.join(output_dir, f'image_{i:03d}{ext}')
            with open(out_path, 'wb') as f:
                f.write(data)

    return images


def main():
    parser = argparse.ArgumentParser(description='Extract content from PowerPoint files')
    parser.add_argument('pptx', help='Path to .pptx file')
    parser.add_argument('--output-dir', '-o', default='./pptx-extracted',
                        help='Output directory for images (default: ./pptx-extracted)')
    parser.add_argument('--format', '-f', choices=['json', 'markdown'], default='markdown',
                        help='Output format (default: markdown)')
    parser.add_argument('--no-images', action='store_true',
                        help='Skip image extraction')

    args = parser.parse_args()

    if not os.path.exists(args.pptx):
        print(f'Error: File not found: {args.pptx}', file=sys.stderr)
        sys.exit(1)

    print(f'Extracting from: {args.pptx}')

    # Extract text
    slides = extract_text_from_pptx(args.pptx)

    # Extract images
    images = []
    if not args.no_images:
        images = extract_images_from_pptx(args.pptx, args.output_dir)
        print(f'Extracted {len(images)} images to {args.output_dir}/')

    # Output
    if args.format == 'json':
        result = {
            'source': args.pptx,
            'slide_count': len(slides),
            'image_count': len(images),
            'slides': slides,
            'images': [{'index': img['index'], 'data_uri': img['data_uri'],
                        'size_bytes': img['size_bytes']} for img in images]
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        # Markdown output
        print(f'# PPTX Extraction: {os.path.basename(args.pptx)}\n')
        print(f'**Slides**: {len(slides)} | **Images**: {len(images)}\n')

        for slide in slides:
            print(f'## Slide {slide["number"]}\n')
            for para in slide['paragraphs']:
                # Heuristic: short first paragraph = title
                prefix = '### ' if len(para) < 120 and slide['paragraphs'].index(para) == 0 else ''
                print(f'{prefix}{para}\n')

        if images:
            print('## Extracted Images\n')
            for img in images:
                print(f'- Image {img["index"]:03d}: {img["size_bytes"]} bytes '
                      f'({img["original_path"]})')


if __name__ == '__main__':
    main()
