#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import zlib
import base64
import string

def plantuml_encode(plantuml_text):
    """Encode PlantUML text for use in PlantUML server URL using DEFLATE encoding"""
    # Compress using DEFLATE
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]  # Strip zlib header and checksum

    # PlantUML custom base64 alphabet
    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'

    encoded = ''
    i = 0
    while i < len(compressed_string):
        # Process bytes in groups of 3 to produce 4 characters
        if i + 2 < len(compressed_string):
            # Handle 3 bytes
            b1 = compressed_string[i]
            b2 = compressed_string[i + 1]
            b3 = compressed_string[i + 2]

            # Encode 3 bytes into 4 characters
            c1 = b1 >> 2
            c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
            c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
            c4 = b3 & 0x3F

            encoded += plantuml_alphabet[c1]
            encoded += plantuml_alphabet[c2]
            encoded += plantuml_alphabet[c3]
            encoded += plantuml_alphabet[c4]
            i += 3
        elif i + 1 < len(compressed_string):
            # Handle 2 remaining bytes
            b1 = compressed_string[i]
            b2 = compressed_string[i + 1]

            c1 = b1 >> 2
            c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
            c3 = (b2 & 0xF) << 2

            encoded += plantuml_alphabet[c1]
            encoded += plantuml_alphabet[c2]
            encoded += plantuml_alphabet[c3]
            i += 2
        else:
            # Handle 1 remaining byte
            b1 = compressed_string[i]

            c1 = b1 >> 2
            c2 = (b1 & 0x3) << 4

            encoded += plantuml_alphabet[c1]
            encoded += plantuml_alphabet[c2]
            i += 1

    return encoded

def generate_diagram_from_file(puml_file):
    """Generate PNG diagram from PlantUML file using PlantUML server"""

    if not os.path.exists(puml_file):
        print(f"File not found: {os.path.basename(puml_file)}", file=sys.stderr)
        return False

    # Read PlantUML file
    with open(puml_file, 'r', encoding='utf-8') as f:
        plantuml_text = f.read()

    # Encode for PlantUML server
    encoded = plantuml_encode(plantuml_text)

    # Generate PNG using PlantUML server
    server_url = f"http://www.plantuml.com/plantuml/png/{encoded}"

    print(f"Generating diagram for: {os.path.basename(puml_file)}")
    print(f"Server URL length: {len(server_url)} characters")

    try:
        response = requests.get(server_url, timeout=60)
        response.raise_for_status()

        # Save PNG file
        png_file = puml_file.replace('.puml', '.png')
        with open(png_file, 'wb') as f:
            f.write(response.content)

        print(f"Successfully generated: {os.path.basename(png_file)}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Error generating diagram: {e}", file=sys.stderr)
        return False

def main():
    # Get directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    diagrams_dir = os.path.join(script_dir, '2-Design', '2.1-Design')

    # PlantUML files to process
    puml_files = [
        'class_diagram_main.puml',
        'class_diagram_services.puml',
        'class_diagram_controllers.puml'
    ]

    success_count = 0
    for filename in puml_files:
        puml_path = os.path.join(diagrams_dir, filename)
        if generate_diagram_from_file(puml_path):
            success_count += 1

    print(f"\nGenerated {success_count}/{len(puml_files)} diagrams successfully")

    if success_count == len(puml_files):
        return 0
    else:
        return 1

if __name__ == '__main__':
    sys.exit(main())
