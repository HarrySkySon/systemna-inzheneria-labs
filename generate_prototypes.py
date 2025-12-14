#!/usr/bin/env python3
"""
Generate PNG images from PlantUML files
"""

import os
import sys
import requests
import zlib
import base64
from pathlib import Path

def plantuml_encode(plantuml_text):
    """Encode PlantUML text to URL format"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]
    return base64.urlsafe_b64encode(compressed_string).decode('utf-8')

def generate_image(puml_file, output_dir):
    """Generate PNG image from PlantUML file"""
    # Read PlantUML file
    with open(puml_file, 'r', encoding='utf-8') as f:
        puml_content = f.read()

    # Encode content
    encoded = plantuml_encode(puml_content)

    # PlantUML server URL
    url = f'http://www.plantuml.com/plantuml/png/{encoded}'

    # Download image
    response = requests.get(url)

    if response.status_code == 200:
        # Save image
        output_filename = puml_file.stem + '.png'
        output_path = output_dir / output_filename

        with open(output_path, 'wb') as f:
            f.write(response.content)

        print(f"OK: {puml_file.name} -> {output_filename}")
        return True
    else:
        print(f"ERROR: {puml_file.name} - HTTP {response.status_code}")
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
print(f"Generated {success_count}/{len(puml_files)} images")
print(f"Images saved to: {images_dir}")
