# UML Діаграми класів програмного продукту SafeHeight Monitor

## Зміст

- [Огляд](#огляд)
- [Діаграма 1: Domain Entities](#діаграма-1-domain-entities)
- [Діаграма 2: Services та Repositories](#діаграма-2-services-та-repositories)
- [Діаграма 3: Controllers та API Layer](#діаграма-3-controllers-та-api-layer)
- [SOLID Principles](#solid-principles)
- [Ключові архітектурні рішення](#ключові-архітектурні-рішення)

---

## Огляд

Цей розділ містить повну UML модель класів системи **SafeHeight Monitor**, розділену на три логічні діаграми для кращої читабельності та організації.

### Структура файлів:

| Файл | Опис | Статус |
|------|------|--------|
| `class_diagram_main.puml` | Доменні сутності та їх зв'язки | ✅ PlantUML |
| `class_diagram_main.png` | Візуалізація доменних сутностей | ✅ Згенеровано |
| `class_diagram_services.puml` | Сервісний шар та repositories | ✅ PlantUML |
| `class_diagram_services.png` | Візуалізація сервісів | ✅ Згенеровано |
| `class_diagram_controllers.puml` | API контролери та middleware | ✅ PlantUML |
| `SOLID_PRINCIPLES.md` | Доведення SOLID принципів | ✅ Документація |

---

## Діаграма 1: Domain Entities

**Файл:** `class_diagram_main.puml` / `class_diagram_main.png`

### Призначення
Описує базові доменні сутності (Entity Objects) та їх зв'язки - це ядро бізнес-логіки системи.

### Основні компоненти:

#### **1. Entities (Основні сутності)**

**Worker** - Працівник будівельного майданчика
```
Атрибути:
  - workerId: UUID
  - firstName, lastName: string
  - position: string (посада)
  - department: string (відділ)
  - status: WorkerStatus
  - emergencyContact: EmergencyContact

Методи:
  + getFullName(): string
  + isActive(): boolean
  + updateStatus(status): void
  + assignDevice(device): void

Відповідальність:
  Зберігання інформації про працівника та управління його станом
```

**IoTDevice** - IoT пристрій (браслет, сенсор)
```
Атрибути:
  - deviceId: UUID
  - serialNumber: string
  - deviceType: DeviceType
  - batteryLevel: int
  - status: DeviceStatus
  - assignedWorker: Worker

Методи:
  + isOperational(): boolean
  + updateBatteryLevel(level): void
  + sendHeartbeat(): void
  + calibrate(): void

Відповідальність:
  Управління станом та метриками IoT пристрою
```

**SensorReading** - Показник з датчика
```
Атрибути:
  - readingId: UUID
  - deviceId, workerId: UUID
  - timestamp: DateTime
  - location: GeoLocation
  - altitude, bodyTilt: double
  - heartRate: int
  - accelerometerData, gyroscopeData: Vector3D

Методи:
  + isAnomalous(): boolean
  + validate(): ValidationResult

Відповідальність:
  Зберігання даних з сенсорів у конкретний момент часу
```

**RiskAssessment** - Результат оцінки ризику
```
Атрибути:
  - assessmentId: UUID
  - workerId: UUID
  - timestamp: DateTime
  - riskLevel: RiskLevel (LOW, MEDIUM, HIGH, CRITICAL)
  - riskProbability: double
  - riskFactors: List<RiskFactor>
  - recommendations: List<string>

Методи:
  + isCritical(): boolean
  + requiresImmedateAction(): boolean
  + getTopRiskFactors(count): List<RiskFactor>

Відповідальність:
  Результат аналізу ризиків ML моделлю
```

**Alert** - Попередження/Тривога
```
Атрибути:
  - alertId: UUID
  - workerId, assessmentId: UUID
  - alertType: AlertType
  - severity: AlertSeverity
  - message: string
  - acknowledgedAt: DateTime
  - acknowledgedBy: UUID

Методи:
  + acknowledge(userId): void
  + isAcknowledged(): boolean
  + escalate(): void
  + dismiss(reason): void

Відповідальність:
  Управління попередженнями та їх підтвердженням
```

**Zone** - Зона на будівельному майданчику
```
Атрибути:
  - zoneId: UUID
  - name, description: string
  - boundaries: Polygon
  - maxAltitude: double
  - dangerLevel: DangerLevel
  - restrictions: List<string>

Методи:
  + contains(location): boolean
  + isRestricted(): boolean
  + getAllowedWorkers(): List<Worker>

Відповідальність:
  Визначення меж та обмежень зон
```

#### **2. Value Objects**

- **EmergencyContact** - Контактна особа для екстрених випадків
- **GeoLocation** - Географічні координати (lat, lon, alt)
- **Vector3D** - 3D вектор для акселерометра/гіроскопа
- **RiskFactor** - Фактор ризику з описом та severity

#### **3. Enumerations**

- **WorkerStatus**: ACTIVE, ON_BREAK, OFF_DUTY, IN_DANGER, EMERGENCY, INACTIVE
- **DeviceType**: WRIST_BRACELET, HELMET_SENSOR, HARNESS_MONITOR, GATEWAY
- **DeviceStatus**: ONLINE, OFFLINE, CHARGING, MAINTENANCE, FAULTY
- **RiskLevel**: LOW, MEDIUM, HIGH, CRITICAL
- **AlertType**: FALL_RISK, UNAUTHORIZED_ZONE, HEALTH_ISSUE, DEVICE_MALFUNCTION, EMERGENCY_BUTTON
- **AlertSeverity**: INFO, WARNING, CRITICAL, EMERGENCY
- **DangerLevel**: SAFE, CAUTION, DANGEROUS, RESTRICTED

### Зв'язки між класами:

```
Worker "1" -- "0..1" IoTDevice : assigned to
Worker "1" *-- "1" EmergencyContact : has
Worker "1" -- "0..*" SensorReading : generates
Worker "1" -- "0..*" RiskAssessment : assessed for
Worker "1" -- "0..*" Alert : receives

IoTDevice "1" -- "0..*" SensorReading : produces

SensorReading "1" *-- "1" GeoLocation : recorded at
SensorReading "1" *-- "2" Vector3D : contains

RiskAssessment "1" -- "1" SensorReading : based on
RiskAssessment "1" *-- "1..*" RiskFactor : contains
RiskAssessment "1" -- "0..*" Alert : triggers

Zone "1" -- "0..*" Worker : monitors
Zone "1" -- "0..*" Alert : generates
```

---

## Діаграма 2: Services та Repositories

**Файл:** `class_diagram_services.puml` / `class_diagram_services.png`

### Призначення
Описує сервісний шар (Business Logic) та абстракції доступу до даних (Repositories).

### Основні компоненти:

#### **1. Repository Interfaces**

Абстракції для роботи з даними (Data Access Layer):

- **IWorkerRepository** - CRUD операції для працівників
- **IIoTDeviceRepository** - Управління IoT пристроями
- **ISensorReadingRepository** - Збереження показників сенсорів
- **IRiskAssessmentRepository** - Збереження результатів аналізу ризиків
- **IAlertRepository** - Управління попередженнями
- **IZoneRepository** - Управління зонами

**Приклад:** IWorkerRepository
```java
interface IWorkerRepository {
    + findById(id: UUID): Worker
    + findAll(): List<Worker>
    + findByStatus(status: WorkerStatus): List<Worker>
    + save(worker: Worker): Worker
    + update(worker: Worker): Worker
    + delete(id: UUID): boolean
    + findByDeviceId(deviceId: UUID): Worker
}
```

#### **2. Service Interfaces**

Бізнес-логіка системи:

**IRiskAnalysisService** - Аналіз ризиків
```
+ analyzeReading(reading: SensorReading): RiskAssessment
+ analyzeBatch(readings: List<SensorReading>): List<RiskAssessment>
+ predictRisk(workerId: UUID, horizon: Duration): RiskPrediction
```

**IAlertService** - Управління попередженнями
```
+ createAlert(assessment: RiskAssessment): Alert
+ acknowledgeAlert(alertId: UUID, userId: UUID): void
+ escalateAlert(alertId: UUID): void
+ dismissAlert(alertId: UUID, reason: string): void
+ getActiveAlerts(): List<Alert>
```

**INotificationService** - Відправка сповіщень
```
+ sendNotification(recipient, message, channel): boolean
+ sendBulkNotification(recipients, message): int
+ sendEmergencyNotification(alert: Alert): void
```

**IDeviceManagementService** - Управління IoT пристроями
```
+ registerDevice(device: IoTDevice): IoTDevice
+ assignDevice(deviceId, workerId): void
+ unassignDevice(deviceId): void
+ updateFirmware(deviceId, version): boolean
+ checkDeviceHealth(): List<IoTDevice>
```

**IZoneMonitoringService** - Моніторинг зон
```
+ checkZoneViolation(workerId, location): ZoneViolation
+ getWorkersInZone(zoneId): List<Worker>
+ updateZoneBoundaries(zoneId, boundaries): void
```

**IDataIngestionService** - Прийом даних з IoT
```
+ ingestReading(reading: SensorReading): void
+ ingestBatch(readings: List<SensorReading>): void
+ validateReading(reading: SensorReading): ValidationResult
```

**IAnalyticsService** - Аналітика та звіти
```
+ getWorkerStatistics(workerId, period): WorkerStats
+ getZoneStatistics(zoneId, period): ZoneStats
+ getSystemOverview(period): SystemStats
+ exportReport(criteria): Report
```

#### **3. Service Implementations**

Конкретні реалізації сервісів з dependency injection:

**RiskAnalysisService**
```java
class RiskAnalysisService implements IRiskAnalysisService {
    private mlModelClient: IMLModelClient;           // DIP!
    private sensorRepository: ISensorReadingRepository;  // DIP!
    private assessmentRepository: IRiskAssessmentRepository; // DIP!

    // Constructor injection
    constructor(mlClient, sensorRepo, assessmentRepo) {
        this.mlModelClient = mlClient;
        this.sensorRepository = sensorRepo;
        this.assessmentRepository = assessmentRepo;
    }

    analyzeReading(reading) {
        // Business logic
    }
}
```

#### **4. External Service Interfaces**

Абстракції для зовнішніх залежностей (Dependency Inversion):

- **IMLModelClient** - Абстракція ML моделі
- **IEmailProvider** - Абстракція email сервісу (SendGrid, Amazon SES, etc.)
- **ISMSProvider** - Абстракція SMS сервісу (Twilio, etc.)
- **IPushNotificationProvider** - Абстракція Push сповіщень (Firebase, etc.)
- **IMQTTClient** - Абстракція MQTT broker
- **IMessageQueue** - Абстракція черги повідомлень
- **ICache** - Абстракція кешу (Redis, etc.)
- **IGeoSpatialEngine** - Геопросторові операції

### Dependency Flow (Потік залежностей):

```
Services → Service Interfaces ✓
Services → Repository Interfaces ✓
Services → External Service Interfaces ✓

Services ✗ Concrete Repositories (НЕ напряму!)
Services ✗ Concrete External Services (НЕ напряму!)
```

**Це і є Dependency Inversion Principle (DIP)!**

---

## Діаграма 3: Controllers та API Layer

**Файл:** `class_diagram_controllers.puml`

### Призначення
Описує презентаційний шар (API Controllers, DTOs, Middleware).

### Основні компоненти:

#### **1. DTOs (Data Transfer Objects)**

Об'єкти для передачі даних через API (не є доменними сутностями):

- **WorkerDTO** - Дані працівника для API
- **IoTDeviceDTO** - Дані IoT пристрою для API
- **SensorReadingDTO** - Показник сенсора для API
- **RiskAssessmentDTO** - Результат оцінки ризику для API
- **AlertDTO** - Попередження для API

**Приклад:** WorkerDTO
```java
class WorkerDTO {
    + workerId: UUID
    + firstName, lastName: string
    + position, department: string
    + status: string  // enum → string для JSON
    + deviceId: UUID
    + emergencyContactName, emergencyContactPhone: string

    // Mapping methods
    + static fromEntity(worker: Worker): WorkerDTO
    + toEntity(): Worker
}
```

#### **2. Request Objects**

Спеціальні об'єкти для API запитів:

- **CreateWorkerRequest** - Запит на створення працівника
- **UpdateWorkerStatusRequest** - Оновлення статусу
- **AssignDeviceRequest** - Призначення пристрою
- **AcknowledgeAlertRequest** - Підтвердження попередження

#### **3. Response Wrapper**

**ApiResponse<T>** - Стандартизована відповідь API
```java
class ApiResponse<T> {
    + success: boolean
    + data: T
    + message: string
    + errors: List<string>
    + timestamp: DateTime

    + static success(data: T): ApiResponse<T>
    + static error(message: string): ApiResponse<T>
}
```

#### **4. API Controllers**

REST API endpoints:

**WorkerController**
```
GET    /api/workers              → List<WorkerDTO>
GET    /api/workers/{id}         → WorkerDTO
POST   /api/workers              → WorkerDTO
PUT    /api/workers/{id}         → WorkerDTO
DELETE /api/workers/{id}         → boolean
PUT    /api/workers/{id}/status  → WorkerDTO
GET    /api/workers/{id}/current-risk → RiskAssessmentDTO
```

**DeviceController**
```
GET    /api/devices                    → List<IoTDeviceDTO>
POST   /api/devices/{id}/assign        → IoTDeviceDTO
POST   /api/devices/{id}/unassign      → IoTDeviceDTO
GET    /api/devices/health-check       → List<IoTDeviceDTO>
```

**SensorDataController**
```
POST   /api/sensor-data         → SensorReadingDTO
POST   /api/sensor-data/batch   → BatchResult
GET    /api/sensor-data/worker/{workerId} → List<SensorReadingDTO>
```

**AlertController**
```
GET    /api/alerts              → List<AlertDTO>
GET    /api/alerts/active       → List<AlertDTO>
POST   /api/alerts/{id}/acknowledge → AlertDTO
POST   /api/alerts/{id}/escalate    → AlertDTO
```

**RiskAssessmentController**
```
GET    /api/risk-assessments             → List<RiskAssessmentDTO>
GET    /api/risk-assessments/critical    → List<RiskAssessmentDTO>
POST   /api/risk-assessments/analyze     → RiskAssessmentDTO
```

**AnalyticsController**
```
GET    /api/analytics/worker/{workerId}  → WorkerStats
GET    /api/analytics/system-overview    → SystemStats
GET    /api/analytics/export             → Report
```

**ZoneController**
```
GET    /api/zones                → List<ZoneDTO>
GET    /api/zones/{id}/workers   → List<WorkerDTO>
GET    /api/zones/location       → List<ZoneDTO>
```

#### **5. Middleware Components**

- **AuthenticationMiddleware** - JWT token validation
- **AuthorizationMiddleware** - Permission checking (RBAC)
- **ExceptionHandlingMiddleware** - Global error handling
- **RequestLoggingMiddleware** - Logging requests/responses
- **RateLimitingMiddleware** - API rate limits
- **CorsMiddleware** - CORS policy
- **ValidationFilter** - Model validation

### Controller Pattern:

```java
class WorkerController {
    private workerService: IWorkerService;  // DIP!
    private mapper: IMapper;                // DIP!
    private logger: ILogger;                // DIP!

    constructor(workerService, mapper, logger) {
        // Dependencies injected
    }

    GET_Workers() {
        workers = workerService.getAllWorkers();  // Call service
        dtos = mapper.mapList(workers, WorkerDTO); // Map to DTOs
        return ApiResponse.success(dtos);          // Wrap in response
    }
}
```

**Responsibility:**
- ✓ HTTP concerns (routing, status codes, headers)
- ✓ Input validation
- ✓ DTO mapping
- ✗ Business logic (делегується в Services)
- ✗ Data access (делегується в Repositories через Services)

---

## SOLID Principles

Детальне доведення відповідності принципам SOLID знаходиться в файлі **[SOLID_PRINCIPLES.md](./SOLID_PRINCIPLES.md)**.

### Короткий опис застосування:

| Принцип | Приклад застосування |
|---------|---------------------|
| **SRP** | Кожен клас має єдину відповідальність:<br>- Worker → дані працівника<br>- RiskAnalysisService → аналіз ризиків<br>- WorkerController → HTTP обробка |
| **OCP** | Розширення через інтерфейси:<br>- IMLModelClient дозволяє змінити ML модель<br>- INotificationProvider дозволяє додати Telegram/Slack |
| **LSP** | Всі реалізації інтерфейсів взаємозамінні:<br>- SqlWorkerRepository ↔ MongoWorkerRepository<br>- SendGridEmailProvider ↔ AmazonSESEmailProvider |
| **ISP** | Вузькі інтерфейси:<br>- IWorkerRepository (тільки методи для працівників)<br>- ISensorReadingRepository (окремо для сенсорів) |
| **DIP** | Залежність від абстракцій:<br>- Services → Interfaces (не Concrete Classes)<br>- Controllers → IServices (не Services напряму) |

---

## Ключові архітектурні рішення

### 1. Layered Architecture (Багаторівнева архітектура)

```
Controllers (Presentation)
     ↓ використовують
Services (Business Logic)
     ↓ використовують
Repositories (Data Access)
     ↓ працюють з
Entities (Domain Model)
```

### 2. Dependency Injection

Всі залежності передаються через конструктор (Constructor Injection):

```java
class RiskAnalysisService {
    constructor(
        mlClient: IMLModelClient,
        sensorRepo: ISensorReadingRepository,
        assessmentRepo: IRiskAssessmentRepository
    ) {
        // DI container інжектує залежності
    }
}
```

### 3. Repository Pattern

Абстракція доступу до даних:
- Бізнес-логіка не знає про SQL/NoSQL/REST
- Легко замінити БД (SQL → MongoDB)
- Легко тестувати з In-Memory репозиторіями

### 4. DTO Pattern

Розділення Domain Models та API Contracts:
- Entities для бізнес-логіки
- DTOs для API
- Маппінг між ними

### 5. Interface Segregation

Окремі інтерфейси для різних потреб:
- IWorkerService (базове CRUD)
- IDeviceManagementService (управління пристроями)
- IZoneMonitoringService (моніторинг зон)

### 6. Middleware Pipeline

Модульна обробка HTTP запитів:
```
Request → CORS → Authentication → Authorization → Rate Limiting → Controller → Response
                                                                          ↓
                                                               Exception Handling
                                                                          ↓
                                                                      Logging
```

---

## Метрики якості дизайну

| Метрика | Значення | Оцінка |
|---------|----------|--------|
| **Coupling** | Low (через інтерфейси) | ✅ Відмінно |
| **Cohesion** | High (SRP дотримано) | ✅ Відмінно |
| **Testability** | High (DI + interfaces) | ✅ Відмінно |
| **Extensibility** | High (OCP дотримано) | ✅ Відмінно |
| **Maintainability** | High (чіткий поділ відповідальностей) | ✅ Відмінно |

---

## Інструкції для генерації діаграм

### З PlantUML файлів:

1. **Online PlantUML Server:**
   ```bash
   # Використати онлайн сервіс
   http://www.plantuml.com/plantuml/uml/
   ```

2. **Local PlantUML (якщо встановлено):**
   ```bash
   plantuml -tpng class_diagram_main.puml
   plantuml -tpng class_diagram_services.puml
   plantuml -tpng class_diagram_controllers.puml
   ```

3. **Python скрипт (в репозиторії):**
   ```bash
   cd ../
   python generate_class_diagrams.py
   ```

---

## Автор

**Постановський Ігор**
Група: ІПЗм(д)-25
Дата: 16 грудня 2025
Проект: SafeHeight Monitor - Система моніторингу безпеки будівельних робіт

---

**Примітка:** Для детального аналізу кожного класу та методу, будь ласка, відкрийте PlantUML файли в текстовому редакторі або згенеруйте PNG зображення.
