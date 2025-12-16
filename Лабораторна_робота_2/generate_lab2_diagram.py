#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор PNG діаграми для Lab 2 (Use Case Diagram)
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

def generate_diagram():
    """Генерує PNG діаграму з PlantUML файлу для Lab 2"""

    base_path = os.path.dirname(os.path.abspath(__file__))
    puml_file = os.path.join(base_path, "Лабораторна_робота_2", "1-Requirements",
                             "1.2-UseCaseDiagram", "diagram.puml")
    images_dir = os.path.join(base_path, "Лабораторна_робота_2", "1-Requirements",
                              "1.2-UseCaseDiagram", "images")
    output_file = os.path.join(images_dir, "use_case_diagram.png")

    os.makedirs(images_dir, exist_ok=True)

    with open(puml_file, 'r', encoding='utf-8') as f:
        puml_content = f.read()

    print(f"[+] Читання файлу: {puml_file}")
    print(f"[INFO] Розмір вхідного файлу: {len(puml_content)} символів")

    print("[*] Кодування діаграми...")
    encoded = encode_plantuml(puml_content)

    plantuml_url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    print(f"[INFO] URL діаграми (перші 100 символів): {plantuml_url[:100]}...")

    print("[*] Завантаження PNG з PlantUML сервісу...")
    try:
        request = urllib.request.Request(
            plantuml_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(request, timeout=30) as response:
            png_data = response.read()

        if not png_data.startswith(b'\x89PNG'):
            error_text = png_data.decode('utf-8', errors='ignore')
            if 'bad URL' in error_text or 'error' in error_text.lower():
                print(f"[ERROR] PlantUML повернув помилку: {error_text[:200]}")
                raise Exception("PlantUML сервіс повернув помилку замість зображення")

        with open(output_file, 'wb') as f:
            f.write(png_data)

        print(f"[OK] Діаграма успішно згенерована: {output_file}")
        print(f"[INFO] Розмір PNG файлу: {len(png_data)} bytes")

        with open(output_file, 'rb') as f:
            if f.read(8).startswith(b'\x89PNG'):
                print("[OK] Перевірка: файл є валідним PNG")
            else:
                print("[WARNING] Файл може бути пошкоджений")

    except Exception as e:
        print(f"[ERROR] Помилка при завантаженні: {e}")
        print(f"\n[INFO] Спробуйте відкрити URL вручну:")
        print(plantuml_url[:200] + "...")

if __name__ == "__main__":
    try:
        generate_diagram()
    except Exception as e:
        print(f"[ERROR] Помилка при генерації діаграми: {e}")
        print("\n[INFO] Альтернативний метод:")
        print("1. Відкрийте http://www.plantuml.com/plantuml/")
        print("2. Скопіюйте вміст файлу diagram.puml")
        print("3. Вставте в PlantUML редактор")
        print("4. Збережіть згенеровану PNG діаграму в папку images/")
