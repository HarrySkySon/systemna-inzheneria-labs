# Відповіді на контрольні запитання

**Лабораторна робота №6:** Проектування класів нового програмного продукту

**Студент:** Постановський Ігор
**Група:** ІСП-ХХ
**Дата:** 16 грудня 2025

---

## Питання 1: Які архітектурні типи програмного продукту вам відомі?

**Відповідь:**

Основні архітектурні типи (стилі) програмного забезпечення:

### 1. **Monolithic Architecture (Монолітна архітектура)**
- Всі компоненти системи об'єднані в один виконуваний модуль
- **Переваги:** Простота розробки та deployment, швидкість взаємодії між компонентами
- **Недоліки:** Складність масштабування, тісне зв'язування компонентів
- **Приклад:** Традиційні desktop додатки, малі web-застосунки

### 2. **Layered (N-Tier) Architecture (Багаторівнева архітектура)**
- Система розділена на шари з чіткою ієрархією
- Типові шари: Presentation → Business Logic → Data Access → Database
- **Переваги:** Чіткий поділ відповідальностей, легка заміна шарів
- **Недоліки:** Можливі проблеми з продуктивністю через багато шарів
- **Приклад:** Enterprise додатки, наша система SafeHeight Monitor

### 3. **Microservices Architecture (Мікросервісна архітектура)**
- Система складається з незалежних сервісів
- Кожен сервіс відповідає за певну бізнес-функцію
- **Переваги:** Незалежне масштабування, технологічна гнучкість
- **Недоліки:** Складність інфраструктури, distributed systems challenges
- **Приклад:** Netflix, Amazon, Uber

### 4. **Event-Driven Architecture (Подієво-орієнтована архітектура)**
- Компоненти взаємодіють через події (events)
- **Переваги:** Слабке зв'язування, висока масштабованість
- **Недоліки:** Складність відстеження потоку виконання
- **Приклад:** Real-time системи, IoT платформи

### 5. **Service-Oriented Architecture (SOA) (Сервіс-орієнтована архітектура)**
- Функціональність надається як набір сервісів
- **Переваги:** Повторне використання сервісів, інтероперабельність
- **Недоліки:** Overhead від ESB (Enterprise Service Bus)
- **Приклад:** Корпоративні інтеграційні системи

### 6. **Client-Server Architecture (Клієнт-серверна архітектура)**
- Розділення на клієнтську та серверну частини
- **Типи:** 2-tier, 3-tier, n-tier
- **Переваги:** Централізоване управління даними
- **Недоліки:** Single point of failure на сервері
- **Приклад:** Web-додатки, мобільні застосунки з backend

### 7. **Pipe-and-Filter Architecture**
- Дані проходять через ланцюжок обробників (filters)
- **Переваги:** Модульність, можливість parallel processing
- **Недоліки:** Overhead від передачі даних між фільтрами
- **Приклад:** Unix pipelines, компілятори, ETL системи

### 8. **MVC (Model-View-Controller)**
- Розділення на модель даних, представлення та контролер
- **Варіанти:** MVP (Model-View-Presenter), MVVM (Model-View-ViewModel)
- **Переваги:** Чіткий поділ UI та бізнес-логіки
- **Приклад:** Web frameworks (Django, ASP.NET MVC, Spring MVC)

### 9. **Hexagonal Architecture (Ports and Adapters)**
- Бізнес-логіка в центрі, зовнішні залежності через адаптери
- **Переваги:** Ізоляція бізнес-логіки, легке тестування
- **Приклад:** Clean Architecture, Domain-Driven Design застосунки

### 10. **Serverless Architecture**
- Код виконується у відповідь на події, без управління серверами
- **Переваги:** Автоматичне масштабування, оплата за використання
- **Недоліки:** Cold start, vendor lock-in
- **Приклад:** AWS Lambda, Azure Functions, Google Cloud Functions

**Для SafeHeight Monitor ми обрали Layered Architecture з елементами:**
- Repository Pattern (Data Access)
- Service Layer (Business Logic)
- Controller Layer (Presentation)
- Dependency Injection (для слабкого зв'язування)

---

## Питання 2: Які три рівні представлення визначають при описі архітектури?

**Відповідь:**

При описі архітектури програмного продукту визначають три основні рівні представлення (4+1 View Model by Philippe Kruchten):

### **1. Logical View (Логічне представлення)**

**Призначення:** Описує функціональність системи з точки зору кінцевих користувачів

**Що включає:**
- Об'єктна модель (класи, об'єкти, їх взаємодії)
- Use cases та сценарії використання
- Бізнес-логіка системи

**Діаграми UML:**
- Class Diagrams (діаграми класів)
- Object Diagrams (діаграми об'єктів)
- State Diagrams (діаграми станів)
- Sequence Diagrams (діаграми послідовностей)

**Приклад у SafeHeight Monitor:**
- Класи: Worker, IoTDevice, RiskAssessment, Alert
- Взаємодії: Worker отримує Alert на основі RiskAssessment

**Stakeholders:** Кінцеві користувачі, бізнес-аналітики, розробники

---

### **2. Process View (Процесне представлення / Dynamic View)**

**Призначення:** Описує динамічну поведінку системи під час виконання

**Що включає:**
- Процеси та потоки виконання
- Паралелізм та синхронізація
- Комунікація між процесами
- Продуктивність та масштабованість

**Діаграми UML:**
- Activity Diagrams (діаграми діяльності)
- Sequence Diagrams (діаграми послідовностей для runtime)
- Communication Diagrams (діаграми комунікацій)
- Timing Diagrams (діаграми часу)

**Приклад у SafeHeight Monitor:**
- IoT пристрій → відправляє дані → DataIngestionService → RiskAnalysisService → AlertService → Notification
- Паралельна обробка даних від множини IoT пристроїв
- Асинхронна відправка сповіщень через queue

**Stakeholders:** Системні архітектори, performance engineers, DevOps

---

### **3. Development View (Представлення розробки / Implementation View)**

**Призначення:** Описує організацію коду та компонентів з точки зору розробників

**Що включає:**
- Організація модулів та пакетів
- Структура проекту (directories, namespaces)
- Управління залежностями між компонентами
-Layering та component boundaries

**Діаграми UML:**
- Component Diagrams (діаграми компонентів)
- Package Diagrams (діаграми пакетів)

**Приклад у SafeHeight Monitor:**
```
SafeHeight.Domain/          (Entities, Value Objects)
SafeHeight.Application/     (Services, Interfaces)
SafeHeight.Infrastructure/  (Repositories, External Services)
SafeHeight.API/            (Controllers, DTOs)
```

**Stakeholders:** Розробники, архітектори, менеджери конфігурації

---

### **Додаткові рівні (з моделі 4+1):**

### **4. Physical View (Фізичне представлення / Deployment View)**

**Призначення:** Описує розгортання системи на апаратному забезпеченні

**Що включає:**
- Сервери та мережева топологія
- Deployment на cloud/on-premises
- Load balancing, clustering

**Діаграми UML:**
- Deployment Diagrams (діаграми розгортання)

**Приклад у SafeHeight Monitor:**
- Azure Cloud (VM instances, IoT Hub, Database)
- On-premises IoT devices (gateways, sensors)
- CDN для static content

---

### **5. Scenarios (Use Case View) - Центральний вузол моделі 4+1**

**Призначення:** Об'єднує всі чотири view через use cases

**Що включає:**
- Use case scenarios
- User stories
- Acceptance criteria

**Діаграми UML:**
- Use Case Diagrams

---

### **Три основні рівні (традиційний підхід):**

Якщо говорити про **три традиційні рівні** (не за моделлю 4+1):

1. **Conceptual Level (Концептуальний рівень)**
   - Високорівневий опис системи
   - Business requirements
   - Stakeholder concerns

2. **Logical Level (Логічний рівень)**
   - Детальна архітектура класів та компонентів
   - Design patterns
   - SOLID principles

3. **Physical Level (Фізичний рівень)**
   - Deployment на інфраструктуру
   - Конфігурація серверів
   - Network topology

**Для SafeHeight Monitor ми використовуємо:**
- **Logical View:** UML діаграми класів (Domain, Services, Controllers)
- **Process View:** Описано в архітектурі (async processing, event flow)
- **Development View:** Layered architecture (Presentation → Services → Repositories → Domain)

---

## Питання 3: Які основні принципи декомпозиції вам відомі?

**Відповідь:**

Декомпозиція - це розбиття складної системи на менші, більш керовані частини. Основні принципи декомпозиції:

### **1. Functional Decomposition (Функціональна декомпозиція)**

**Суть:** Розбиття системи за функціональними обов'язками

**Принцип:** "Що робить система?"

**Приклад у SafeHeight Monitor:**
```
SafeHeight Monitor
├── Risk Analysis (аналіз ризиків)
├── Alert Management (управління попередженнями)
├── Device Management (управління пристроями)
├── Zone Monitoring (моніторинг зон)
└── Analytics & Reporting (аналітика)
```

**Переваги:** Зрозуміла для бізнесу, чітко визначені обов'язки
**Недоліки:** Може призвести до дублювання коду

---

### **2. Data-Oriented Decomposition (Декомпозиція за даними)**

**Суть:** Розбиття системи за типами даних, які обробляються

**Принцип:** "З якими даними працює система?"

**Приклад у SafeHeight Monitor:**
```
├── Worker Data Module (дані працівників)
├── IoT Device Data Module (дані пристроїв)
├── Sensor Readings Module (показники сенсорів)
├── Risk Assessment Module (оцінки ризиків)
└── Alert Data Module (дані попереджень)
```

**Переваги:** Чітка Domain Model, легко масштабувати дані
**Недоліки:** Може бути складно координувати між модулями

---

### **3. Object-Oriented Decomposition (Об'єктно-орієнтована декомпозиція)**

**Суть:** Розбиття системи на об'єкти (класи) з інкапсуляцією даних та поведінки

**Принцип:** Об'єднання даних та методів у класи

**Приклад у SafeHeight Monitor:**
```
Worker (дані + методи: assignDevice(), updateStatus())
IoTDevice (дані + методи: sendHeartbeat(), calibrate())
RiskAssessment (дані + методи: isCritical(), getTopRiskFactors())
```

**Переваги:** Інкапсуляція, повторне використання, SOLID principles
**Недоліки:** Можливий overhead від великої кількості класів

---

### **4. Layered Decomposition (Шарова декомпозиція)**

**Суть:** Розбиття системи на горизонтальні шари з різними рівнями абстракції

**Принцип:** Кожен шар надає сервіси шару вище

**Приклад у SafeHeight Monitor:**
```
┌─────────────────────────┐
│ Presentation Layer      │  Controllers, DTOs
├─────────────────────────┤
│ Business Logic Layer    │  Services
├─────────────────────────┤
│ Data Access Layer       │  Repositories
├─────────────────────────┤
│ Domain Layer            │  Entities
└─────────────────────────┘
```

**Переваги:** Чіткий поділ відповідальностей, легка заміна шарів
**Недоліки:** Можливі проблеми з performance (багато шарів)

---

### **5. Service-Oriented Decomposition (Сервіс-орієнтована декомпозиція)**

**Суть:** Розбиття системи на незалежні сервіси

**Принцип:** Кожен сервіс - окрема бізнес-функція з власним API

**Приклад у SafeHeight Monitor:**
```
├── RiskAnalysisService (аналіз ризиків через ML)
├── NotificationService (відправка сповіщень)
├── DeviceManagementService (управління IoT)
├── AnalyticsService (звіти та dashboard)
└── DataIngestionService (прийом даних з IoT)
```

**Переваги:** Слабке зв'язування, незалежне deployment
**Недоліки:** Складність distributed systems

---

### **6. Domain-Driven Decomposition (Декомпозиція за доменами)**

**Суть:** Розбиття системи на bounded contexts за бізнес-доменами

**Принцип:** DDD (Domain-Driven Design)

**Приклад у SafeHeight Monitor:**
```
├── Safety Domain (Worker, RiskAssessment, Alert)
├── IoT Domain (Device, SensorReading, Gateway)
├── Location Domain (Zone, GeoLocation)
└── Analytics Domain (Report, Statistics)
```

**Переваги:** Відповідність бізнес-логіці, зрозуміла модель
**Недоліки:** Потрібна глибока бізнес-експертиза

---

### **7. Component-Based Decomposition (Компонентна декомпозиція)**

**Суть:** Розбиття на незалежні, повторно використовувані компоненти

**Принцип:** Кожен компонент має чіткий інтерфейс

**Приклад у SafeHeight Monitor:**
```
├── AuthenticationComponent (JWT, OAuth)
├── LoggingComponent (structured logging)
├── CachingComponent (Redis cache)
├── NotificationComponent (Email, SMS, Push)
└── MLModelComponent (TensorFlow inference)
```

**Переваги:** Повторне використання, plug-and-play
**Недоліки:** Overhead від абстракцій

---

### **8. Modular Decomposition (Модульна декомпозиція)**

**Суть:** Розбиття на модулі з високою cohesion та низьким coupling

**Принципи:**
- **High Cohesion:** Елементи модуля тісно пов'язані
- **Low Coupling:** Модулі слабко залежать один від одного
- **Information Hiding:** Інкапсуляція деталей реалізації

**Приклад у SafeHeight Monitor:**
Кожен сервіс має свій модуль з чіткими інтерфейсами

---

### **Принципи, які ми застосували у SafeHeight Monitor:**

1. **Layered Decomposition** → Presentation, Services, Repositories, Domain
2. **Object-Oriented Decomposition** → Класи з інкапсуляцією
3. **Service-Oriented Decomposition** → Незалежні сервіси (RiskAnalysis, Alert, Notification)
4. **Component-Based Decomposition** → Повторно використовувані компоненти (Middleware, Providers)
5. **Domain-Driven Decomposition** → Bounded contexts (Safety, IoT, Location)

**Результат:**
- ✅ High Cohesion (кожен модуль має чітку відповідальність)
- ✅ Low Coupling (через інтерфейси та DI)
- ✅ SOLID Principles (SRP, OCP, LSP, ISP, DIP)
- ✅ Легко тестувати (через mocks та stubs)
- ✅ Легко масштабувати (незалежні сервіси)

---

## Питання 4: Що означає, коли програмний модуль має Low Coupling?

**Відповідь:**

**Low Coupling (Слабке зв'язування)** - це ступінь незалежності програмних модулів один від одного.

### **Визначення:**

Модуль має **Low Coupling**, коли він:
- Мінімально залежить від інших модулів
- Може бути змінений без впливу на інші модулі
- Може бути повторно використаний в інших контекстах
- Взаємодіє з іншими модулями через чіткі, стабільні інтерфейси

### **Типи Coupling (від найгіршого до найкращого):**

#### **1. Content Coupling (Найгірший тип) ❌**
- Один модуль безпосередньо модифікує дані іншого модуля
```java
// ПОГАНО: Service напряму змінює internal state Repository
class RiskService {
    void analyze() {
        repository.internalCache.clear(); // Доступ до внутрішніх даних!
    }
}
```

#### **2. Common Coupling ❌**
- Модулі використовують глобальні змінні
```java
// ПОГАНО: Глобальний стан
class GlobalState {
    public static Worker currentWorker; // Shared state
}
```

#### **3. Control Coupling ⚠️**
- Один модуль контролює логіку іншого через параметри
```java
// ПОГАНО: Передача control flags
void processAlert(Alert alert, boolean useSMS, boolean useEmail, boolean usePush) {
    if (useSMS) sendSMS();
    if (useEmail) sendEmail();
    // Caller контролює внутрішню логіку
}
```

#### **4. Stamp Coupling (Data-structure Coupling) ⚠️**
- Модулі обмінюються складними структурами даних, використовуючи лише частину
```java
// ПОГАНО: Передача цілого Worker, коли потрібно лише ID
void sendAlert(Worker worker) {  // Весь об'єкт!
    String workerId = worker.getId(); // Використовується тільки ID
}
```

#### **5. Data Coupling (Найкраще) ✅**
- Модулі обмінюються тільки необхідними примітивними даними
```java
// ДОБРЕ: Передача лише необхідних даних
void sendAlert(String workerId, String message) {
    // Minimal coupling
}
```

#### **6. Message Coupling (Найкраще) ✅**
- Модулі взаємодіють через повідомлення (events, messages)
```java
// ДОБРЕ: Event-driven communication
eventBus.publish(new RiskDetectedEvent(workerId, riskLevel));
```

#### **7. No Coupling (Ідеал) ✅**
- Модулі повністю незалежні

---

### **Як досягти Low Coupling:**

#### **1. Dependency Inversion Principle (DIP)**
```java
// ✅ ДОБРЕ: Залежність від абстракції
class RiskAnalysisService {
    private IMLModelClient mlClient;  // Interface, не concrete class!
    private ISensorReadingRepository sensorRepo;  // Interface!

    constructor(IMLModelClient mlClient, ISensorReadingRepository sensorRepo) {
        this.mlClient = mlClient;
        this.sensorRepo = sensorRepo;
    }
}

// Можна легко замінити реалізацію:
// - TensorFlowMLClient → PyTorchMLClient
// - SqlSensorRepository → MongoSensorRepository
```

#### **2. Interface Segregation**
```java
// ✅ ДОБРЕ: Вузькі інтерфейси
interface INotificationSender {
    boolean send(String recipient, String message);
}

// Замість одного великого інтерфейсу:
// ❌ ПОГАНО:
interface INotificationService {
    sendEmail(), sendSMS(), sendPush(),
    configureSMTP(), configureGateway(),
    retryFailedMessages(), clearQueue() ...  // Занадто багато!
}
```

#### **3. Dependency Injection**
```java
// ✅ ДОБРЕ: Dependencies ін'єктуються ззовні
class AlertService {
    constructor(
        INotificationService notificationService,  // Injected
        IAlertRepository alertRepository           // Injected
    ) { }
}

// DI Container конфігурує dependencies
container.bind<INotificationService>(NotificationService);
container.bind<IAlertRepository>(SqlAlertRepository);
```

#### **4. Event-Driven Architecture**
```java
// ✅ ДОБРЕ: Слабке зв'язування через events
class RiskAnalysisService {
    analyzeReading(reading) {
        RiskAssessment result = mlModel.predict(reading);
        if (result.isCritical()) {
            eventBus.publish(new CriticalRiskDetected(result));
            // Не знає хто обробить event!
        }
    }
}

class AlertService {
    @Subscribe
    onCriticalRisk(CriticalRiskDetected event) {
        createAlert(event.assessment);
        // Не знає хто згенерував event!
    }
}
```

#### **5. Repository Pattern**
```java
// ✅ ДОБРЕ: Абстракція даних
interface IWorkerRepository {
    Worker findById(UUID id);
    List<Worker> findAll();
}

// Service не знає про SQL, MongoDB, REST API
class WorkerService {
    private IWorkerRepository repo;  // Абстракція!

    Worker getWorker(UUID id) {
        return repo.findById(id);  // Не знає про БД!
    }
}
```

---

### **Переваги Low Coupling:**

1. **Легше тестувати**
   ```java
   // Mock dependencies для unit tests
   IMLModelClient mockMLClient = mock(IMLModelClient.class);
   RiskAnalysisService service = new RiskAnalysisService(mockMLClient, ...);
   ```

2. **Легше змінювати**
   - Зміна в одному модулі не впливає на інші
   - Можна замінити реалізацію без зміни клієнтів

3. **Легше повторно використовувати**
   - Модулі можна використовувати в інших проектах
   - Мінімальні залежності

4. **Легше розуміти**
   - Кожен модуль має чіткі межі
   - Зменшена когнітивна складність

5. **Паралельна розробка**
   - Різні команди можуть працювати над різними модулями
   - Мінімальні конфлікти

---

### **Метрики Coupling:**

**Як виміряти coupling:**

1. **Afferent Coupling (Ca)** - скільки класів залежать від цього класу
2. **Efferent Coupling (Ce)** - від скількох класів залежить цей клас
3. **Instability (I) = Ce / (Ca + Ce)**
   - I = 0: Максимально стабільний (тільки інші залежать від нього)
   - I = 1: Максимально нестабільний (залежить від багатьох)

**Ідеал:** Low Ce (мало залежностей), High Ca (багато користувачів)

---

### **Low Coupling у SafeHeight Monitor:**

**Приклади з нашої архітектури:**

1. **Services залежать від Interfaces, не Concrete Classes**
   ```
   RiskAnalysisService → IMLModelClient (не TensorFlowMLClient)
   AlertService → INotificationService (не NotificationService)
   ```

2. **Repository Pattern**
   ```
   WorkerService → IWorkerRepository (не SqlWorkerRepository)
   ```

3. **DTO Pattern**
   ```
   Controllers → DTOs (не Domain Entities)
   ```

4. **Dependency Injection**
   ```
   Всі залежності через constructor injection
   ```

**Результат:**
- ✅ Легко тестувати (mock interfaces)
- ✅ Легко замінити БД (SQL → MongoDB)
- ✅ Легко замінити ML модель (TensorFlow → PyTorch)
- ✅ Легко додати новий notification channel (Telegram, Slack)

---

**Висновок:**

**Low Coupling означає, що модулі:**
- Мінімально залежать один від одного
- Взаємодіють через чіткі інтерфейси
- Можуть бути змінені незалежно
- Легко тестуються та повторно використовуються

**Це досягається через:**
- Dependency Inversion (DIP)
- Interface Segregation (ISP)
- Dependency Injection
- Repository Pattern
- Event-Driven Architecture

---

**Дата:** 16 грудня 2025
**Проект:** SafeHeight Monitor
**Розробник:** Постановський Ігор
