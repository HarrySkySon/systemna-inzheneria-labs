# Інструкція з публікації на GitHub

## Поточний статус

- **Локальний Git:** ✅ Ініціалізовано, зроблено перший commit (820519d)
- **GitHub CLI:** ✅ Встановлено (v2.76.2)
- **Автентифікація:** ✅ Увійшли як **HarrySkySon**

## Опції публікації

### Варіант 1: Публікація на HarrySkySon (поточний акаунт)

```bash
cd "C:\Users\123_4\Documents\Deutschland\Bewerbung\Вступ до ВУЗ\КНУБА навчання\Системна інженерія програмного забезпечення_Соловей О_ІСП\Лабораторні Курсові_Виконані"

# Створити публічний репозиторій
gh repo create systemna-inzheneria-labs --public --source=. --description="Лабораторні роботи з Системної інженерії програмного забезпечення - КНУБА"

# Запушити код
git push -u origin master
```

### Варіант 2: Публікація на observer_12@protonmail.com

**Спосіб 2A: Перелогінитися в GitHub CLI**

```bash
# Вийти з поточного акаунту
gh auth logout

# Увійти в інший акаунт
gh auth login
# Виберіть: GitHub.com -> HTTPS -> Authenticate with browser
# Введіть дані: observer_12@protonmail.com / A@igorkristina123

# Створити репозиторій
gh repo create systemna-inzheneria-labs --public --source=. --description="Лабораторні роботи з Системної інженерії програмного забезпечення - КНУБА"

# Запушити код
git push -u origin master
```

**Спосіб 2B: Вручну через веб-інтерфейс GitHub**

1. Відкрийте https://github.com/new
2. Увійдіть як observer_12@protonmail.com
3. Назва репозиторію: `systemna-inzheneria-labs`
4. Опис: "Лабораторні роботи з Системної інженерії програмного забезпечення - КНУБА"
5. Public
6. НЕ ініціалізуйте з README
7. Створіть репозиторій

Потім виконайте:

```bash
cd "C:\Users\123_4\Documents\Deutschland\Bewerbung\Вступ до ВУЗ\КНУБА навчання\Системна інженерія програмного забезпечення_Соловей О_ІСП\Лабораторні Курсові_Виконані"

# Додайте remote (замініть USERNAME на ваш GitHub username)
git remote add origin https://github.com/USERNAME/systemna-inzheneria-labs.git

# Запушіть код
git push -u origin master
# Введіть: observer_12@protonmail.com / A@igorkristina123
```

## Структура репозиторію після публікації

```
systemna-inzheneria-labs/
├── README.md                          # Головний README проекту
├── .gitignore                         # Git ignore файл
├── generate_lab1.py                   # Генератор Lab 1
├── generate_diagram_v2.py             # Генератор діаграм
└── Лабораторна_робота_1/
    └── 0-BusinessGoalAnalysis/
        ├── README.md                  # Огляд Lab 1
        ├── 01_StakeholderList/
        ├── 02_StakeholderRACImatrix/
        ├── 03_BusinessGoalDiagram/
        │   ├── diagram.puml
        │   └── images/
        │       └── business_goal_diagram.png
        ├── 04_ProjectConcept/
        └── interview_questions.md
```

## Перевірка після публікації

1. Відкрийте репозиторій на GitHub
2. Перевірте, що всі файли присутні
3. Перевірте, що діаграма відображається в README
4. Переконайтесь, що структура відповідає зразку: https://github.com/olgasolovei/yakusha89-gmail.com

---

**Створено:** 2025-12-14
**Commit:** 820519d - Initial commit: Lab 1 - Business Goal Analysis
