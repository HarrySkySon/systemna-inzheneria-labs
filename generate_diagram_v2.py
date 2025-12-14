#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерації PNG діаграми з PlantUML файлу через веб-сервіс
"""

import os
import zlib
import base64
import urllib.request

def plantuml_encode(plantuml_text):
    """Кодує PlantUML текст для URL"""
    zlibbed_str = zlib.compress(plantuml_text.encode('utf-8'))
    compressed_string = zlibbed_str[2:-4]

    plantuml_alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_'
    base64_string = base64.b64encode(compressed_string).decode('utf-8')

    # Конвертуємо base64 в PlantUML формат
    encoded = ''
    for i in range(0, len(base64_string), 3):
        chunk = base64_string[i:i+3]
        b1 = ord(chunk[0]) if len(chunk) > 0 else 0
        b2 = ord(chunk[1]) if len(chunk) > 1 else 0
        b3 = ord(chunk[2]) if len(chunk) > 2 else 0

        encoded += plantuml_alphabet[(b1 >> 2) & 0x3F]
        encoded += plantuml_alphabet[((b1 & 0x3) << 4) | ((b2 >> 4) & 0xF)]
        encoded += plantuml_alphabet[((b2 & 0xF) << 2) | ((b3 >> 6) & 0x3)]
        encoded += plantuml_alphabet[b3 & 0x3F]

    return encoded

def generate_diagram():
    """Генерує PNG діаграму з PlantUML файлу"""

    base_path = os.path.dirname(os.path.abspath(__file__))
    puml_file = os.path.join(base_path, "Лабораторна_робота_1", "0-BusinessGoalAnalysis",
                             "03_BusinessGoalDiagram", "diagram.puml")
    images_dir = os.path.join(base_path, "Лабораторна_робота_1", "0-BusinessGoalAnalysis",
                              "03_BusinessGoalDiagram", "images")
    output_file = os.path.join(images_dir, "business_goal_diagram.png")

    # Створюємо директорію images, якщо не існує
    os.makedirs(images_dir, exist_ok=True)

    # Читаємо PlantUML файл
    with open(puml_file, 'r', encoding='utf-8') as f:
        puml_content = f.read()

    print(f"[+] Читання файлу: {puml_file}")
    print(f"[INFO] Розмір вхідного файлу: {len(puml_content)} символів")

    # Кодуємо PlantUML
    print("[*] Кодування діаграми...")
    encoded = plantuml_encode(puml_content)

    # Генеруємо URL для PlantUML сервісу
    plantuml_url = f"http://www.plantuml.com/plantuml/png/{encoded}"
    print(f"[INFO] URL діаграми: {plantuml_url}")

    # Завантажуємо PNG
    print("[*] Завантаження PNG з PlantUML сервісу...")
    try:
        with urllib.request.urlopen(plantuml_url) as response:
            png_data = response.read()

        # Зберігаємо PNG файл
        with open(output_file, 'wb') as f:
            f.write(png_data)

        print(f"[OK] Діаграма успішно згенерована: {output_file}")
        print(f"[INFO] Розмір PNG файлу: {len(png_data)} bytes")

    except Exception as e:
        print(f"[ERROR] Помилка при завантаженні: {e}")
        print(f"\n[INFO] Відкрийте цей URL в браузері та збережіть PNG вручну:")
        print(plantuml_url)

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
