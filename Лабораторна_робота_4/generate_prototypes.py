#!/usr/bin/env python3
"""
Generate PNG images from PlantUML files using correct PlantUML encoding
"""

import os
import sys
import requests
import zlib
from pathlib import Path

def plantuml_encode(plantuml_text):
    """
    Encode PlantUML text using PlantUML's special base64 encoding
    Based on: https://plantuml.com/text-encoding
    """
    # PlantUML uses a special base64 alphabet
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'

    def encode6bit(b):
        if b < 10:
            return chr(48 + b)  # 0-9
        b -= 10
        if b < 26:
            return chr(65 + b)  # A-Z
        b -= 26
        if b < 26:
            return chr(97 + b)  # a-z
        b -= 26
        if b == 0:
            return '-'
        if b == 1:
            return '_'
        return '?'

    def append3bytes(b1, b2, b3):
        c1 = b1 >> 2
        c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
        c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
        c4 = b3 & 0x3F
        return encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) + encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)

    # Compress with zlib
    compressed = zlib.compress(plantuml_text.encode('utf-8'))
    # Remove zlib header and checksum (first 2 bytes and last 4 bytes)
    compressed = compressed[2:-4]

    # Encode to PlantUML format
    result = []
    for i in range(0, len(compressed), 3):
        if i + 2 < len(compressed):
            result.append(append3bytes(compressed[i], compressed[i + 1], compressed[i + 2]))
        elif i + 1 < len(compressed):
            result.append(append3bytes(compressed[i], compressed[i + 1], 0))
        else:
            result.append(append3bytes(compressed[i], 0, 0))

    return ''.join(result)

def generate_image(puml_file, output_dir):
    """Generate PNG image from PlantUML file"""
    # Read PlantUML file
    with open(puml_file, 'r', encoding='utf-8') as f:
        puml_content = f.read()

    # Encode content with correct PlantUML encoding
    encoded = plantuml_encode(puml_content)

    # PlantUML server URL
    url = f'http://www.plantuml.com/plantuml/png/{encoded}'

    # Download image
    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 200:
            # Check if response is actually an image (not error text)
            content_type = response.headers.get('Content-Type', '')
            if 'image' in content_type or response.content[:4] == b'\x89PNG':
                # Save image
                output_filename = puml_file.stem + '.png'
                output_path = output_dir / output_filename

                with open(output_path, 'wb') as f:
                    f.write(response.content)

                print(f"OK: {puml_file.name} -> {output_filename}")
                return True
            else:
                print(f"ERROR: {puml_file.name} - Server returned text instead of image")
                # Save error for debugging
                error_file = output_dir / f"{puml_file.stem}_error.txt"
                with open(error_file, 'wb') as f:
                    f.write(response.content)
                return False
        else:
            print(f"ERROR: {puml_file.name} - HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: {puml_file.name} - {str(e)}")
        return False

# Main
prototypes_dir = Path("Лабораторна_робота_4/3-RequirementsValidation/3.3-Prototypes")
images_dir = prototypes_dir / "images"

# Create images directory
images_dir.mkdir(exist_ok=True)

# Find all .puml files
puml_files = sorted(prototypes_dir.glob("*.puml"))

print(f"Found {len(puml_files)} .puml files")
print("-" * 60)

success_count = 0
for puml_file in puml_files:
    if generate_image(puml_file, images_dir):
        success_count += 1

print("-" * 60)
print(f"Generated {success_count}/{len(puml_files)} images successfully")

if success_count == len(puml_files):
    print("All images generated successfully!")
else:
    print(f"Failed: {len(puml_files) - success_count} images")
