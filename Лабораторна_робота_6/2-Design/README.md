# Проектування програмного продукту

## Зміст

- [Огляд проекту](#огляд-проекту)
- [Архітектурний підхід](#архітектурний-підхід)
- [Структура документації](#структура-документації)

## Огляд проекту

**SafeHeight Monitor** - це IoT-система для моніторингу безпеки будівельних робіт на висоті з використанням машинного навчання для виявлення ризиків.

### Основні компоненти системи:

1. **IoT пристрої** - носимі датчики для працівників (браслети, сенсори на касках)
2. **Backend система** - обробка даних, аналіз ризиків, управління
3. **ML модель** - визначення потенційних ризиків падіння з висоти
4. **Система сповіщень** - негайне оповіщення про критичні ситуації
5. **Dashboard** - моніторинг та аналітика для менеджерів

## Архітектурний підхід

Система спроектована з використанням **багаторівневої архітектури** (Layered Architecture):

```
┌────────────────────────────────────┐
│   Presentation Layer (Controllers) │  ← REST API, WebSockets
├────────────────────────────────────┤
│   Service Layer (Business Logic)   │  ← Use Cases, бізнес-правила
├────────────────────────────────────┤
│   Repository Layer (Data Access)   │  ← Абстракції даних
├────────────────────────────────────┤
│   Domain Layer (Entities)          │  ← Доменні моделі
└────────────────────────────────────┘
```

### Ключові принципи:

- **SOLID Principles** - дотримання всіх п'яти принципів об'єктно-орієнтованого програмування
- **Dependency Injection** - інверсія залежностей для тестованості та гнучкості
- **Repository Pattern** - абстракція доступу до даних
- **DTO Pattern** - розділення доменних моделей та API контрактів
- **Interface Segregation** - вузькі інтерфейси для різних клієнтів

## Структура документації

### [2.1-Design](./2.1-Design/) - UML Діаграми класів

Повна класова модель системи, що включає:
- Domain Entities (Worker, IoTDevice, SensorReading, Alert, Zone)
- Service Interfaces та реалізації
- Repository Interfaces
- API Controllers та DTOs
- Middleware компоненти

### Файли в директорії 2.1-Design:

1. **class_diagram_main.puml** / **class_diagram_main.png**
   - Доменні сутності (Entities)
   - Value Objects
   - Enumerations
   - Зв'язки між сутностями

2. **class_diagram_services.puml** / **class_diagram_services.png**
   - Service інтерфейси та реалізації
   - Repository інтерфейси
   - External service abstractions
   - Dependency Injection

3. **class_diagram_controllers.puml**
   - API Controllers
   - DTOs (Data Transfer Objects)
   - Middleware (Authentication, Logging, etc.)
   - Request/Response моделі

4. **SOLID_PRINCIPLES.md**
   - Детальне доведення відповідності принципам SOLID
   - Практичні приклади з кодової бази
   - Переваги архітектури

## Технології та інструменти

- **UML Modeling**: PlantUML
- **Programming Paradigm**: Object-Oriented Programming (OOP)
- **Design Principles**: SOLID, DRY, KISS
- **Patterns**: Repository, Dependency Injection, DTO, Strategy

## Автор

**Постановський Ігор**
Група: ІПЗм(д)-25
Дата: 16 грудня 2025

---

**Примітка:** Повний опис класів та методів доступний в PlantUML діаграмах в директорії `2.1-Design/`.
