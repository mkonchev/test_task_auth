# Система аутентификации и авторизации

Собственная реализация backend-приложения для управления пользователями и разграничения прав доступа

## Оглавление

- [Технологии](#технологии)
- [Архитектура](#архитектура)
- [Система прав доступа](#система-прав-доступа)
- [Запуск проекта](#запуск-проекта)
- [API Endpoints](#api-endpoints)
- [Структура проекта](#структура-проекта)

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** - ORM (асинхронный)
- **PostgreSQL** - база данных
- **JWT** - аутентификация
- **bcrypt** - хеширование паролей
- **Pydantic** - валидация данных
- **Docker** - контейнеризация

## Архитектура

Проект построен на многослойной архитектуре с четким разделением ответственности:

API слой (маршруты)

  ↓

Сервисный слой (бизнес-логика)

  ↓

Репозитории (доступ к данным)

  ↓

База данных


### Слои приложения:

1. **API слой** (`app/api/`) - только обработка HTTP запросов
2. **Сервисный слой** (`app/services/`) - бизнес-логика
3. **Репозитории** (`app/repositories/`) - работа с БД
4. **Модели** (`app/models/`) - SQLAlchemy модели
5. **Схемы** (`app/schemas/`) - Pydantic модели

## Система прав доступа

### Модель данных

```sql
-- Роли пользователей
roles (id, name)

-- Бизнес-элементы (ресурсы)
business_elements (id, name)

-- Правила доступа
access_rules (
    role_id, element_id,
    read_permission, read_all_permission,
    create_permission,
    update_permission, update_all_permission,
    delete_permission, delete_all_permission
)
```
### Права доступа:

1. (`read_permission`) - Чтение своих объектов
2. (`read_all_permission`) - Чтение всех объектов
3. (`create_permission`) - Создание объектов
4. (`update_permission`) - Обновление своих объектов
5. (`update_all_permission`) - Обновление всех объектов
6. (`delete_permission`) - Удаление своих объектов
7. (`delete_all_permission`) - Удаление всех объектов

### Роли:

1. admin - Полный доступ
2. manager - Управление пользователями
3. user - Пользователь
4. guest - Гость


## Запуск проекта

```bash
# Клонировать репозиторий
git clone <repository-url>
cd project

# Запустить контейнеры
docker-compose up --build

# Приложение будет доступно по адресу:
# http://localhost:8000
```

## Первый запуск

При первом запуске автоматически:

Создаются таблицы в БД
Заполняются роли (admin, manager, user, guest)
Создаются бизнес-элементы
Настраиваются правила доступа
Создается тестовый администратор


### Учетные данные

admin - ADMIN_PW(Пароль) и ADMIN_EMAIL(Электронная почта) задаются в .env файле
user - При регистрации


## API Endpoints

/auth
<img width="1635" height="375" alt="image" src="https://github.com/user-attachments/assets/2fbf9923-b3fb-4460-af4d-6063d8be7ed3" />

/admin
<img width="1634" height="370" alt="image" src="https://github.com/user-attachments/assets/2e6ff0b0-929d-405e-8c32-dd97c870f2bc" />

/mock
<img width="1615" height="359" alt="image" src="https://github.com/user-attachments/assets/7324dcc2-b850-4166-9c10-75128f0604ec" />


## Структура проекта

```
app/
├── api/                    # API маршруты
│   ├── auth.py            # Аутентификация
│   ├── admin.py           # Админ панель
│   ├── mock.py            # Mock объекты
│   └── dependencies.py    # Зависимости
├── models/                # SQLAlchemy модели
│   ├── user.py
│   ├── role.py
│   ├── business_element.py
│   └── access_rule.py
├── schemas/               # Pydantic схемы
│   ├── user.py
│   ├── access_rule.py
│   └── ...
├── repositories/          # Репозитории (доступ к БД)
│   ├── base.py
│   ├── user_repository.py
│   ├── role_repository.py
│   └── ...
├── services/              # Бизнес-логика
│   ├── user_service.py
│   ├── permission_service.py
│   ├── access_rule_service.py
│   └── init_service.py
├── security/              # Безопасность
│   ├── auth_handler.py    # JWT
│   └── hash_helper.py     # bcrypt
└── db/                    # Настройки БД
    ├── config.py
    └── database.py
```








