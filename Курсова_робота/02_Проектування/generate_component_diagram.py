#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерації PNG діаграми компонентів для курсової роботи
"""

import os
import zlib
import urllib.request

def encode6bit(b):
    """Кодує 6-бітне значення в PlantUML символ"""
    if b < 10:
        return chr(48 + b)
    b -= 10
    if b < 26:
        return chr(65 + b)
    b -= 26
    if b < 26:
        return chr(97 + b)
    b -= 26
    if b == 0:
        return '-'
    if b == 1:
        return '_'
    return '?'

def append3bytes(b1, b2, b3):
    """Кодує 3 байти в 4 PlantUML символи"""
    c1 = b1 >> 2
    c2 = ((b1 & 0x3) << 4) | (b2 >> 4)
    c3 = ((b2 & 0xF) << 2) | (b3 >> 6)
    c4 = b3 & 0x3F
    return encode6bit(c1 & 0x3F) + encode6bit(c2 & 0x3F) + encode6bit(c3 & 0x3F) + encode6bit(c4 & 0x3F)

def encode_plantuml(plantuml_text):
    """Кодує PlantUML текст для URL"""
    compressed = zlib.compress(plantuml_text.encode('utf-8'))[2:-4]

    encoded = ""
    i = 0
    while i < len(compressed):
        if i + 2 < len(compressed):
            encoded += append3bytes(compressed[i], compressed[i+1], compressed[i+2])
            i += 3
        elif i + 1 < len(compressed):
            encoded += append3bytes(compressed[i], compressed[i+1], 0)
            i += 2
        else:
            encoded += append3bytes(compressed[i], 0, 0)
            i += 1

    return encoded

def generate_diagram(puml_file, output_file):
    """Generates PNG diagram from PlantUML file"""
    print("Reading file...")

    with open(puml_file, 'r', encoding='utf-8') as f:
        plantuml_text = f.read()

    print("Encoding diagram...")
    encoded = encode_plantuml(plantuml_text)

    url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    print(f"Downloading from URL...")

    try:
        urllib.request.urlretrieve(url, output_file)
        print(f"SUCCESS: Diagram saved to {output_file}")
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))

    puml_file = os.path.join(script_dir, "component_diagram.puml")
    output_file = os.path.join(script_dir, "component_diagram.png")

    if not os.path.exists(puml_file):
        print(f"✗ Файл не знайдено: {puml_file}")
        exit(1)

    success = generate_diagram(puml_file, output_file)
    exit(0 if success else 1)
