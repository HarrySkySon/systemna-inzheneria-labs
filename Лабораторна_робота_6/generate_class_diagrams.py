#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import requests
import zlib
import base64
import string

def plantuml_encode(plantuml_text):
    """Encode PlantUML text for use in PlantUML server URL"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]

    plantuml_alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase + '-_'
    base64_string = base64.b64encode(compressed_string).decode('utf-8')

    encoded = ''
    for i in range(0, len(base64_string), 3):
        if i + 2 < len(base64_string):
            b1 = base64_string[i]
            b2 = base64_string[i + 1]
            b3 = base64_string[i + 2]

            c1 = ord(b1) >> 2
            c2 = ((ord(b1) & 0x3) << 4) | (ord(b2) >> 4)
            c3 = ((ord(b2) & 0xF) << 2) | (ord(b3) >> 6)
            c4 = ord(b3) & 0x3F

            encoded += plantuml_alphabet[c1]
            encoded += plantuml_alphabet[c2]
            encoded += plantuml_alphabet[c3]
            encoded += plantuml_alphabet[c4]

    return encoded

def generate_diagram_from_file(puml_file):
    """Generate PNG diagram from PlantUML file using PlantUML server"""

    if not os.path.exists(puml_file):
        print(f"File not found: {puml_file}", file=sys.stderr)
        return False

    # Read PlantUML file
    with open(puml_file, 'r', encoding='utf-8') as f:
        plantuml_text = f.read()

    # Encode for PlantUML server
    encoded = plantuml_encode(plantuml_text)

    # Generate PNG using PlantUML server
    server_url = f"http://www.plantuml.com/plantuml/png/{encoded}"

    print(f"Generating diagram for: {puml_file}")
    print(f"Server URL: {server_url[:80]}...")

    try:
        response = requests.get(server_url, timeout=60)
        response.raise_for_status()

        # Save PNG file
        png_file = puml_file.replace('.puml', '.png')
        with open(png_file, 'wb') as f:
            f.write(response.content)

        print(f"Successfully generated: {png_file}")
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
