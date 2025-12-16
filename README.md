# Київський національний університет будівництва і архітектури

## Кафедра: "Інформаційних технологій"

**Дисципліна:** "Системна інженерія програмного забезпечення"

**Студент:** Постановський Ігор
**Група:** ІПЗм(д)-25

---

## Проект: SafeHeight Monitor

**Повна назва:** Веб-додаток моніторингу будівельних майданчиків з AI для запобігання падінням з висоти

**Варіант:** 7 - Виявляти і інформувати про ризик для працівників на майданчику через падіння з висоти

### Опис проекту

IoT-система для моніторингу безпеки будівельних робіт на висоті з використанням штучного інтелекту для виявлення та попередження ризиків падіння працівників. Система аналізує дані з IoT-пристроїв в режимі реального часу та надає попередження про потенційні небезпеки.

---

## Структура репозиторію

```
.
├── README.md                                           # Опис проекту (цей файл)
├── Інформація про виконані лабораторні роботи.md      # Детальна інформація про всі роботи
│
├── Лабораторна_робота_1/                              # Lab 1: Концепція проекту
│   └── 0-BusinessGoalAnalysis/                         # Аналіз бізнес-цілей
│       ├── concept_document.md                         # Положення про концепцію
│       ├── business_goals_diagram.puml                 # Діаграма бізнес-цілей
│       ├── business_goals_diagram.png
│       ├── stakeholders.md                             # Зацікавлені сторони
│       └── raci_matrix.md                              # RACI матриця
│
├── Лабораторна_робота_2/                              # Lab 2: Вимоги користувача
│   └── 1-Requirements/                                 # Use Cases
│       ├── use_cases_detailed.md                       # Детальний опис Use Cases
│       ├── use_case_diagram.puml                       # UML діаграма Use Cases
│       └── use_case_diagram.png
│
├── Лабораторна_робота_3/                              # Lab 3: Функціональні вимоги
│   └── 2-FuncNoFuncRequirements/                       # Функціональні та нефункціональні вимоги
│       ├── functional_requirements.md                  # 12 груп функціональних вимог
│       └── non_functional_requirements.md              # 16 груп нефункціональних вимог
│
├── Лабораторна_робота_4/                              # Lab 4: Валідація вимог
│   └── 3-RequirementsValidation/                       # User Stories & Prototypes
│       ├── user_stories.md                             # 15 User Stories, 23 Gherkin сценарії
│       ├── traceability_matrix.md                      # Матриці трасування
│       ├── prototypes.puml                             # UI прототипи (PlantUML @salt)
│       └── prototypes_*.png                            # 5 прототипів екранів
│
├── Лабораторна_робота_5/                              # Lab 5: UI/UX Design
│   └── 4-UserInterface/                                # Wireframes & Mockups
│       ├── wireframes.puml                             # 5 Wireframes (PlantUML @salt)
│       ├── wireframes_*.png
│       ├── mockups.md                                  # 5 High-fidelity Mockups
│       └── mockups_*.png
│
├── Лабораторна_робота_6/                              # Lab 6: Архітектурне проектування
│   └── 2-Design/
│       └── 2.1-Design/                                 # UML Class Diagrams
│           ├── class_design.md                         # Опис архітектури
│           ├── solid_principles.md                     # Дотримання SOLID
│           ├── class_diagram_main.puml                 # Доменні сутності
│           ├── class_diagram_services.puml             # Service Layer
│           ├── class_diagram_controllers.puml          # Presentation Layer
│           └── *.png                                   # Згенеровані діаграми
│
└── Курсова_робота/                                    # Курсова робота
    └── (у розробці)
```

---

## Лабораторні роботи

### Лабораторна робота №1: Концепція проекту
- **Тема:** Створення документу про концепцію проекту
- **Виконано:** Аналіз зацікавлених сторін, RACI матриця, діаграма бізнес-цілей, положення про концепцію
- **Директорія:** `Лабораторна_робота_1/0-BusinessGoalAnalysis/`

### Лабораторна робота №2: Вимоги користувача
- **Тема:** Виявлення вимог до програмного продукту через Use Cases
- **Виконано:** 5 типів користувачів, 11 детальних Use Cases, UML діаграма
- **Директорія:** `Лабораторна_робота_2/1-Requirements/`

### Лабораторна робота №3: Функціональні вимоги
- **Тема:** Збір та документування функціональних та нефункціональних вимог
- **Виконано:** 12 груп функціональних вимог (58 підвимог), 16 груп нефункціональних вимог (67 підвимог)
- **Стандарт:** ISO/IEC/IEEE 29148:2011
- **Директорія:** `Лабораторна_робота_3/2-FuncNoFuncRequirements/`

### Лабораторна робота №4: Валідація вимог
- **Тема:** Розробка критеріїв приймального тестування та прототипів
- **Виконано:** 9 епіків, 15 User Stories, 23 Gherkin сценарії, 2 матриці трасування, 5 UI прототипів
- **Директорія:** `Лабораторна_робота_4/3-RequirementsValidation/`

### Лабораторна робота №5: UI/UX Design
- **Тема:** Проектування каркасу (wireframe) та макету (mockup) інтерфейсу користувача
- **Виконано:** 5 wireframes, 5 high-fidelity mockups, документація принципів дизайну
- **Директорія:** `Лабораторна_робота_5/4-UserInterface/`

### Лабораторна робота №6: Архітектурне проектування
- **Тема:** Створення класового дизайну з UML діаграм класів
- **Виконано:** 3 UML діаграми класів (60+ класів), доведення відповідності SOLID
- **Директорія:** `Лабораторна_робота_6/2-Design/2.1-Design/`

**Детальна інформація:** Див. файл [`Інформація про виконані лабораторні роботи.md`](./Інформація%20про%20виконані%20лабораторні%20роботи.md)

---

## Технологічний стек

### Backend & Cloud
- Azure App Service, Azure Functions
- Azure SQL Database, Azure Redis Cache
- .NET Core / Java Spring Boot

### IoT Infrastructure
- Azure IoT Hub
- Azure IoT Device Provisioning Service
- Azure Stream Analytics

### AI/ML
- Azure Machine Learning
- Python, TensorFlow/PyTorch
- Azure ML Pipelines

### Frontend
- React.js / Angular
- Material-UI
- Redux / MobX, Chart.js, D3.js

### Security
- Azure Active Directory
- Azure Key Vault
- Azure Virtual Network

---

## Контакти та посилання

**GitHub Repository:** [systemna-inzheneria-labs](https://github.com/HarrySkySon/systemna-inzheneria-labs)

**Університет:** Київський національний університет будівництва і архітектури
**Кафедра:** Інформаційних технологій
**Рік:** 2025

---

*Останнє оновлення: 16 грудня 2025*
