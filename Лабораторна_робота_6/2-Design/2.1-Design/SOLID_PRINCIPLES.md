# Доведення відповідності принципам SOLID

## Вступ

Система **SafeHeight Monitor** спроектована з дотриманням усіх п'яти принципів SOLID для забезпечення високої якості коду, легкості підтримки та розширюваності.

---

## 1. Single Responsibility Principle (SRP) - Принцип єдиної відповідальності

**Визначення:** Кожен клас повинен мати лише одну причину для зміни, тобто одну відповідальність.

### Приклади застосування в системі:

#### **Worker (Domain Entity)**
```
Відповідальність: Представлення працівника будівельного майданчика
- Зберігає особисту інформацію працівника
- Управляє статусом працівника
- Зберігає контактну інформацію для екстрених випадків

НЕ відповідає за:
- Збереження даних в базу даних (IWorkerRepository)
- Відправку сповіщень (INotificationService)
- Аналіз ризиків (IRiskAnalysisService)
```

#### **RiskAnalysisService**
```
Відповідальність: Аналіз ризиків на основі даних сенсорів
- Обробка показників з IoT пристроїв
- Виклик ML моделі для визначення ризиків
- Розрахунок рівня ризику

НЕ відповідає за:
- Відправку алертів (AlertService)
- Збереження даних (IRiskAssessmentRepository)
- Управління IoT пристроями (DeviceManagementService)
```

#### **NotificationService**
```
Відповідальність: Відправка сповіщень через різні канали
- Email сповіщення
- SMS сповіщення
- Push notifications

НЕ відповідає за:
- Створення алертів (AlertService)
- Визначення кому відправляти (AlertService визначає recipients)
```

#### **WorkerController**
```
Відповідальність: Обробка HTTP запитів для управління працівниками
- Валідація вхідних даних
- Маппінг DTO ↔ Entities
- Формування HTTP відповідей

НЕ відповідає за:
- Бізнес-логіку (делегує в IWorkerService)
- Доступ до даних (використовує IWorkerService → IWorkerRepository)
```

### Висновок SRP:
✅ **Кожен клас має чітко визначену єдину відповідальність**, що робить систему легкою для розуміння та підтримки.

---

## 2. Open/Closed Principle (OCP) - Принцип відкритості/закритості

**Визначення:** Класи повинні бути відкриті для розширення, але закриті для модифікації.

### Приклади застосування в системі:

#### **INotificationService та його реалізації**
```
Інтерфейс INotificationService визначає контракт:
  + sendNotification(recipient, message, channel): boolean
  + sendEmergencyNotification(alert): void

NotificationService реалізує базову функціональність і використовує:
  - IEmailProvider
  - ISMSProvider
  - IPushNotificationProvider

Розширення без модифікації:
  ✅ Додати новий канал (Telegram, Slack) через новий IXXXProvider
  ✅ Замінити email провайдера (SendGrid → Amazon SES)
  ❌ НЕ потрібно змінювати NotificationService
```

#### **IRiskAnalysisService та ML моделі**
```
RiskAnalysisService залежить від IMLModelClient (абстракція)

Можна легко:
  ✅ Замінити TensorFlow модель на PyTorch модель
  ✅ Додати ансамбль моделей
  ✅ Використати хмарний ML сервіс (Azure ML, AWS SageMaker)

Через реалізацію нового IMLModelClient:
  - TensorFlowMLClient
  - PyTorchMLClient
  - AzureMLClient
  - EnsembleMLClient

❌ RiskAnalysisService залишається незмінним
```

#### **Middleware Pipeline**
```
Middleware компоненти додаються без зміни існуючих:
  ✅ AuthenticationMiddleware
  ✅ AuthorizationMiddleware
  ✅ RateLimitingMiddleware
  ✅ RequestLoggingMiddleware
  ✅ ExceptionHandlingMiddleware

Кожен middleware:
  - Має метод invoke(context, next)
  - Може бути доданий/видалений з pipeline
  - НЕ впливає на інші middleware
```

#### **Repository Pattern**
```
Інтерфейси (IWorkerRepository, IAlertRepository, etc.) дозволяють:
  ✅ Змінити SQL → NoSQL без зміни бізнес-логіки
  ✅ Додати кешування (CachedWorkerRepository decorator)
  ✅ Використати різні БД для різних оточень (dev/prod)

Приклад:
  class CachedWorkerRepository implements IWorkerRepository {
      private realRepo: IWorkerRepository;
      private cache: ICache;

      findById(id) {
          if (cache.has(id)) return cache.get(id);
          worker = realRepo.findById(id);
          cache.set(id, worker);
          return worker;
      }
  }
```

### Висновок OCP:
✅ **Система розширюється через додавання нових класів (реалізацій інтерфейсів), а не зміну існуючих**.

---

## 3. Liskov Substitution Principle (LSP) - Принцип підстановки Лісков

**Визначення:** Об'єкти підкласів повинні бути взаємозамінними з об'єктами батьківського класу без порушення коректності програми.

### Приклади застосування в системі:

#### **Всі Repository реалізації**
```
Інтерфейс: IWorkerRepository

Реалізації:
  - SqlWorkerRepository
  - MongoWorkerRepository
  - InMemoryWorkerRepository (для тестів)
  - CachedWorkerRepository

Всі реалізації:
  ✅ Повертають однакові типи даних (Worker, List<Worker>)
  ✅ Викидають однакові exceptions при помилках
  ✅ Дотримуються контракту інтерфейсу
  ✅ Можуть бути замінені одна на одну

Приклад коректної заміни:
  // В production
  IWorkerRepository repo = new SqlWorkerRepository(connectionString);

  // В тестах
  IWorkerRepository repo = new InMemoryWorkerRepository();

  // В обох випадках WorkerService працює однаково
  WorkerService service = new WorkerService(repo);
```

#### **Notification Providers**
```
Всі провайдери (IEmailProvider, ISMSProvider, IPushNotificationProvider):
  - Мають однакову сигнатуру методів
  - Повертають boolean (успіх/невдача)
  - Викидають однакові exceptions

NotificationService може використовувати будь-який провайдер:
  ✅ SendGridEmailProvider
  ✅ AmazonSESEmailProvider
  ✅ TwilioSMSProvider
  ✅ FirebasePushProvider
```

#### **Service Implementations**
```
IRiskAnalysisService може бути реалізований як:
  - RiskAnalysisService (production з ML моделлю)
  - MockRiskAnalysisService (для тестів, завжди повертає LOW risk)
  - SimulatedRiskAnalysisService (для demo з рандомними даними)

AlertService працює з будь-якою реалізацією без змін.
```

#### **Приклад порушення LSP (якого ми уникли)**
```
❌ НЕПРАВИЛЬНО:
  class ReadOnlyWorkerRepository implements IWorkerRepository {
      save(worker) {
          throw new UnsupportedOperationException(); // Порушення LSP!
      }
  }

✅ ПРАВИЛЬНО:
  Створити окремі інтерфейси:
    - IReadOnlyWorkerRepository (findById, findAll)
    - IWorkerRepository extends IReadOnlyWorkerRepository (+ save, update, delete)
```

### Висновок LSP:
✅ **Всі реалізації інтерфейсів можуть бути замінені одна на одну без порушення роботи системи**.

---

## 4. Interface Segregation Principle (ISP) - Принцип розділення інтерфейсів

**Визначення:** Клієнти не повинні залежати від інтерфейсів, які вони не використовують.

### Приклади застосування в системі:

#### **Розділення Repository інтерфейсів**
```
Замість одного великого інтерфейсу:
  ❌ НЕПРАВИЛЬНО:
    interface IRepository {
        findById(id)
        findAll()
        save(entity)
        update(entity)
        delete(id)
        saveBatch(entities)
        executeRawQuery(sql)
        backup()
        restore()
    }

✅ ПРАВИЛЬНО - розділені інтерфейси:
  interface IWorkerRepository {
      findById(id): Worker
      findAll(): List<Worker>
      findByStatus(status): List<Worker>
      save(worker): Worker
      update(worker): Worker
      delete(id): boolean
      findByDeviceId(deviceId): Worker
  }

  interface ISensorReadingRepository {
      findById(id): SensorReading
      findByWorker(workerId, from, to): List<SensorReading>
      save(reading): SensorReading
      saveBatch(readings): int  // Специфічний для сенсорів
      deleteOlderThan(date): int  // Cleanup старих даних
  }

Переваги:
  - WorkerService не бачить методів для сенсорів
  - SensorDataService не бачить методів для працівників
```

#### **Розділення Service інтерфейсів**
```
Замість монолітного IWorkerManagementService:

✅ Окремі інтерфейси:
  interface IWorkerService {
      // Базове CRUD для працівників
      getAllWorkers()
      getWorkerById(id)
      createWorker(request)
      updateWorker(id, worker)
      deleteWorker(id)
  }

  interface IDeviceManagementService {
      // Управління IoT пристроями
      registerDevice(device)
      assignDevice(deviceId, workerId)
      unassignDevice(deviceId)
      updateFirmware(deviceId, version)
      checkDeviceHealth()
  }

  interface IZoneMonitoringService {
      // Моніторинг зон
      checkZoneViolation(workerId, location)
      getWorkersInZone(zoneId)
      updateZoneBoundaries(zoneId, boundaries)
  }

Клієнти використовують тільки потрібний інтерфейс:
  - WorkerController → IWorkerService
  - DeviceController → IDeviceManagementService
  - ZoneController → IZoneMonitoringService
```

#### **Notification Channel Providers**
```
Замість одного INotificationProvider з усіма методами:

✅ Окремі інтерфейси:
  interface IEmailProvider {
      sendEmail(to, subject, body): boolean
      sendBulkEmail(recipients, subject, body): int
  }

  interface ISMSProvider {
      sendSMS(phoneNumber, message): boolean
      sendBulkSMS(phoneNumbers, message): int
  }

  interface IPushNotificationProvider {
      sendPushNotification(deviceToken, title, body): boolean
      sendToTopic(topic, title, body): int
  }

NotificationService композує всі провайдери, але:
  - Email клієнт не знає про SMS
  - SMS клієнт не знає про Push notifications
```

#### **Приклад порушення ISP (якого ми уникли)**
```
❌ НЕПРАВИЛЬНО:
  interface IDataService {
      // Змушує всіх клієнтів реалізувати ВСІ методи
      ingestSensorData()
      analyzeSensorData()
      sendAlerts()
      generateReports()
      manageDevices()
      monitorZones()
      authenticateUsers()
      ... ще 20 методів
  }

✅ ПРАВИЛЬНО:
  Кожен сервіс має свій вузький інтерфейс:
    - IDataIngestionService
    - IRiskAnalysisService
    - IAlertService
    - IAnalyticsService
    - IDeviceManagementService
    - IZoneMonitoringService
    - IAuthService
```

### Висновок ISP:
✅ **Інтерфейси розділені на cohesive групи методів, клієнти залежать лише від потрібних методів**.

---

## 5. Dependency Inversion Principle (DIP) - Принцип інверсії залежностей

**Визначення:**
- Модулі високого рівня не повинні залежати від модулів низького рівня. Обидва повинні залежати від абстракцій.
- Абстракції не повинні залежати від деталей. Деталі повинні залежати від абстракцій.

### Приклади застосування в системі:

#### **Services залежать від Repository Interfaces**
```
✅ ПРАВИЛЬНО (DIP дотримано):

  class RiskAnalysisService implements IRiskAnalysisService {
      private sensorRepository: ISensorReadingRepository;     // Абстракція
      private assessmentRepository: IRiskAssessmentRepository; // Абстракція
      private mlModelClient: IMLModelClient;                  // Абстракція

      constructor(
          sensorRepo: ISensorReadingRepository,
          assessmentRepo: IRiskAssessmentRepository,
          mlClient: IMLModelClient
      ) {
          this.sensorRepository = sensorRepo;
          this.assessmentRepository = assessmentRepo;
          this.mlModelClient = mlClient;
      }
  }

❌ НЕПРАВИЛЬНО (порушення DIP):
  class RiskAnalysisService {
      private sensorRepository: SqlSensorReadingRepository;  // Конкретна реалізація!
      private mlModel: TensorFlowModel;                      // Конкретна реалізація!
  }

Переваги:
  ✅ RiskAnalysisService не знає про SQL, MongoDB, або іншу БД
  ✅ Можна замінити TensorFlow на PyTorch без зміни сервісу
  ✅ Легко тестувати з mock об'єктами
```

#### **Dependency Injection в Controllers**
```
class WorkerController {
    private workerService: IWorkerService;        // Залежить від абстракції
    private mapper: IMapper;                      // Залежить від абстракції
    private logger: ILogger;                      // Залежить від абстракції

    constructor(
        workerService: IWorkerService,
        mapper: IMapper,
        logger: ILogger
    ) {
        // Залежності ін'єктуються ззовні (DI Container)
        this.workerService = workerService;
        this.mapper = mapper;
        this.logger = logger;
    }
}

Налаштування DI Container:
  container.register<IWorkerService>(WorkerService);
  container.register<IMapper>(AutoMapper);
  container.register<ILogger>(Log4jLogger);  // Може бути SerilogLogger, ConsoleLogger, etc.

Переваги:
  ✅ WorkerController не створює залежності сам
  ✅ Залежності можуть бути замінені в конфігурації
  ✅ Легко тестувати з mock'ами
```

#### **NotificationService та провайдери**
```
class NotificationService implements INotificationService {
    private emailProvider: IEmailProvider;              // Абстракція
    private smsProvider: ISMSProvider;                  // Абстракція
    private pushProvider: IPushNotificationProvider;    // Абстракція

    // Залежить від абстракцій, не від SendGrid, Twilio, Firebase
}

Конкретні реалізації:
  - SendGridEmailProvider implements IEmailProvider
  - AmazonSESEmailProvider implements IEmailProvider
  - TwilioSMSProvider implements ISMSProvider
  - FirebasePushProvider implements IPushNotificationProvider

Можна легко замінити:
  Production: SendGridEmailProvider
  Testing:    MockEmailProvider
  Staging:    LoggingEmailProvider (логує замість відправки)
```

#### **Ієрархія залежностей (Dependency Flow)**
```
┌─────────────────────────────┐
│   Controllers (UI Layer)    │
│   - WorkerController        │
│   - AlertController         │
└──────────┬──────────────────┘
           │ залежить від (↓)
           │ інтерфейсів
┌──────────▼──────────────────┐
│   Service Interfaces        │
│   - IWorkerService          │
│   - IAlertService           │
└──────────┬──────────────────┘
           │
           │ реалізовано (↑)
┌──────────▼──────────────────┐
│   Service Implementations   │
│   - WorkerService           │
│   - AlertService            │
└──────────┬──────────────────┘
           │ залежить від (↓)
           │ інтерфейсів
┌──────────▼──────────────────┐
│   Repository Interfaces     │
│   - IWorkerRepository       │
│   - IAlertRepository        │
└──────────┬──────────────────┘
           │
           │ реалізовано (↑)
┌──────────▼──────────────────┐
│   Repository Implementations│
│   - SqlWorkerRepository     │
│   - MongoAlertRepository    │
└─────────────────────────────┘

Важливо:
  → Стрілки "залежить від" завжди вказують на абстракції (інтерфейси)
  → Concrete класи залежать від інтерфейсів, а не навпаки
  → Можна замінити будь-який шар без впливу на інші
```

#### **External Services через абстракції**
```
Всі зовнішні залежності прихован за інтерфейсами:

  IRiskAnalysisService → IMLModelClient
    ↓ реалізації
    - AzureMLClient
    - TensorFlowLocalClient
    - MockMLClient

  INotificationService → IEmailProvider, ISMSProvider
    ↓ реалізації
    - SendGridEmailProvider
    - TwilioSMSProvider

  IDeviceManagementService → IMQTTClient
    ↓ реалізації
    - MosquittoMQTTClient
    - AzureIoTHubMQTTClient

Переваги:
  ✅ Легко змінити провайдера (SendGrid → Amazon SES)
  ✅ Легко тестувати (mock MQTT client)
  ✅ Незалежність від vendor lock-in
```

### Висновок DIP:
✅ **Всі залежності вказують на абстракції (інтерфейси), що забезпечує низьке зв'язування та високу тестованість**.

---

## Загальний висновок

Архітектура системи **SafeHeight Monitor** повністю дотримується всіх п'яти принципів SOLID:

| Принцип | Оцінка | Приклади в системі |
|---------|--------|-------------------|
| **SRP** | ✅ Дотримано | Кожен клас має єдину відповідальність (Worker, RiskAnalysisService, WorkerController) |
| **OCP** | ✅ Дотримано | Розширення через інтерфейси (IMLModelClient, INotificationProvider, Middleware) |
| **LSP** | ✅ Дотримано | Всі реалізації інтерфейсів взаємозамінні (Repository, Services) |
| **ISP** | ✅ Дотримано | Розділені інтерфейси для різних клієнтів (IWorkerService, IDeviceManagementService) |
| **DIP** | ✅ Дотримано | Залежність від абстракцій (інтерфейсів), не від конкретних класів |

### Переваги SOLID архітектури:

1. **Тестованість**: Всі компоненти легко тестуються з mock об'єктами
2. **Підтримуваність**: Зміни в одному компоненті не впливають на інші
3. **Розширюваність**: Нова функціональність додається без зміни існуючого коду
4. **Низьке зв'язування**: Компоненти незалежні один від одного
5. **Висока cohesion**: Кожен компонент має чітко визначену відповідальність

### Практичні приклади переваг:

**Приклад 1: Зміна БД з SQL на MongoDB**
```
Потрібно змінити: Тільки repository реалізації
Залишається незмінним: Services, Controllers, Entities
```

**Приклад 2: Додавання Telegram сповіщень**
```
Потрібно створити: TelegramProvider implements IMessageProvider
Потрібно змінити: Конфігурацію DI контейнера
Залишається незмінним: NotificationService, AlertService, Controllers
```

**Приклад 3: Заміна ML моделі**
```
Потрібно створити: NewMLClient implements IMLModelClient
Потрібно змінити: Конфігурацію DI контейнера
Залишається незмінним: RiskAnalysisService, AlertService, Controllers
```

**Приклад 4: Unit тестування**
```
// Легко створити тести з mock об'єктами
test('RiskAnalysisService analyzes reading correctly') {
    mockSensorRepo = new MockSensorReadingRepository();
    mockAssessmentRepo = new MockRiskAssessmentRepository();
    mockMLClient = new MockMLModelClient();

    service = new RiskAnalysisService(mockSensorRepo, mockAssessmentRepo, mockMLClient);

    result = service.analyzeReading(testReading);

    expect(result.riskLevel).toBe('HIGH');
}
```

---

**Дата розробки:** 16 грудня 2025
**Розробник:** Постановський Ігор
**Проект:** SafeHeight Monitor - Система моніторингу безпеки будівельних робіт
