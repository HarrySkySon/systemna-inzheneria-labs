#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для генерації PNG діаграми з PlantUML файлу
"""

import os
from plantuml import PlantUML

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

    # Використовуємо PlantUML веб-сервіс для генерації діаграми
    plantuml = PlantUML(url='http://www.plantuml.com/plantuml/img/')

    print("[*] Генерація діаграми...")

    # Генруємо та зберігаємо PNG
    plantuml.processes_file(puml_file, outfile=output_file)

    print(f"[OK] Діаграма успішно згенерована: {output_file}")
    print(f"[INFO] Розмір файлу: {os.path.getsize(output_file)} bytes")

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
