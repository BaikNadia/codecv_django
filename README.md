# 🚀 CodeCV - Интерактивное резюме для разработчиков
В НАСТОЯЩЕЕ ВРЕМЯ НАХОДИТСЯ В ПРОЦЕССЕ РАЗРАБОТКИ!!!
<div align="center">

![Django](https://img.shields.io/badge/Django-5.0.4-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)
![Docker](https://img.shields.io/badge/Docker-✓-blue.svg)
![Python](https://img.shields.io/badge/Python-3.11+-yellow.svg)
![HTMX](https://img.shields.io/badge/HTMX-1.9.10-orange.svg)

**Современное SPA-резюме для разработчиков с автозаполнением из GitHub и 3D визуализацией**

[Демо](#демо) • [Установка](#установка) • [Функционал](#функционал) • [API](#api) • [Разработка](#разработка)

</div>

## 📋 Оглавление

- [🎯 О проекте](#-о-проекте)
- [✨ Ключевые особенности](#-ключевые-особенности)
- [🏗️ Архитектура](#️-архитектура)
- [🚀 Быстрый старт](#-быстрый-старт)
- [🐳 Запуск с Docker](#-запуск-с-docker)
- [💻 Локальная установка](#-локальная-установка)
- [🔧 Конфигурация](#-конфигурация)
- [📁 Структура проекта](#-структура-проекта)
- [🎨 Функционал](#-функционал)
- [🔌 API Endpoints](#-api-endpoints)
- [🧪 Тестирование](#-тестирование)
- [🚀 Деплой](#-деплой)
- [🤝 Вклад в проект](#-вклад-в-проект)
- [📄 Лицензия](#-лицензия)

## 🎯 О проекте

**CodeCV** — это интерактивная платформа для создания современных резюме для IT-специалистов. Вместо статичных PDF-файлов разработчики получают полноценные веб-приложения с живыми демо, 3D визуализацией стека технологий и интеграцией с GitHub.

### 💡 Проблема, которую мы решаем

Разработчики тратят часы на:
- Обновление резюме при каждом новом проекте
- Создание отдельных демо для работодателей  
- Подтверждение реальных навыков (не просто списки)
- Адаптацию резюме под разные вакансии

### ✅ Наше решение

1. **Автозаполнение из GitHub** — резюме обновляется автоматически
2. **Интерактивные демо** — код можно запустить прямо в резюме
3. **3D визуализация навыков** — наглядное представление стека
4. **Адаптивные шаблоны** — одна копия для всех платформ
5. **Публичная статистика** — кто и когда просматривал резюме

## ✨ Ключевые особенности

### 🎨 **Дизайн и UX**
- **4 темы на выбор**: GitHub Dark, GitHub Light, Dracula, Nord
- **Полная адаптивность** (mobile-first подход)
- **Анимации на Framer Motion** и микроинтеракции
- **Тёмная/светлая тема** с сохранением в localStorage

### 🤖 **Технологический стек**
- **Бэкенд**: Django 5.0 + PostgreSQL
- **Фронтенд**: HTMX, Alpine.js, Tailwind CSS
- **3D графика**: Three.js для интерактивной визуализации
- **API**: Django REST Framework + GitHub API
- **Контейнеризация**: Docker + Docker Compose

### 🔌 **Интеграции**
- **GitHub API**: Автоимпорт репозиториев, активности, языков
- **GitHub Actions**: CI/CD пайплайны
- **Vercel/Netlify**: Автодеплой фронтенда
- **Plausible Analytics**: Приватная аналитика без cookies

## 🏗️ Архитектура

### Структура проекта
```
codecv/
├── backend/                    # Django проект
│   ├── config/                # Настройки Django
│   ├── cvbuilder/            # Основное приложение
│   ├── users/                # Аутентификация
│   ├── api/                  # REST API
│   └── templates/            # HTML шаблоны SSR
├── frontend/                  # Клиентские файлы
│   ├── static/               # CSS, JS, изображения
│   └── templates/            # Базовые шаблоны
├── docker-compose.yml        # Docker конфигурация
├── Dockerfile                # Бэкенд Dockerfile
├── .env.example              # Шаблон переменных окружения
└── requirements.txt          # Python зависимости
```

### База данных (PostgreSQL)
```sql
-- Основные таблицы
cvbuilder_cvprofile         # Профили пользователей
cvbuilder_skill             # Навыки с уровнями
cvbuilder_project           # Проекты из GitHub
cvbuilder_experience        # Опыт работы
django_migrations          # Миграции Django
auth_user                  # Пользователи
```

## 🚀 Быстрый старт

### Предварительные требования
- Python 3.11+
- PostgreSQL 15+ или Docker
- Git

### Вариант 1: Docker (рекомендуется)
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/yourusername/codecv.git
cd codecv

# 2. Настройте переменные окружения
cp .env.example .env
# Отредактируйте .env под свои нужды

# 3. Запустите с Docker Compose
docker-compose up -d

# 4. Примените миграции
docker-compose exec web python manage.py migrate

# 5. Создайте суперпользователя
docker-compose exec web python manage.py createsuperuser

# 6. Откройте в браузере
# http://localhost:8000
```

### Вариант 2: Локальная установка
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/yourusername/codecv.git
cd codecv

# 2. Создайте виртуальное окружение
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Установите зависимости
pip install -r requirements.txt

# 4. Настройте базу данных PostgreSQL
# Создайте базу 'codecv_db'
# Отредактируйте DATABASES в config/settings.py

# 5. Примените миграции
python manage.py migrate

# 6. Создайте суперпользователя
python manage.py createsuperuser

# 7. Соберите статику
python manage.py collectstatic

# 8. Запустите сервер
python manage.py runserver
```

## 🐳 Docker конфигурация

### docker-compose.yml
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: codecv_db
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  web:
    build: .
    command: >
      sh -c "python manage.py migrate &&
             python manage.py collectstatic --noinput &&
             gunicorn config.wsgi:application --bind 0.0.0.0:8000"
    environment:
      DATABASE_URL: postgres://postgres:${DB_PASSWORD}@postgres:5432/codecv_db
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    ports:
      - "8000:8000"
    depends_on:
      - postgres

  nginx:
    image: nginx:1.25
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - static_volume:/app/staticfiles
    ports:
      - "80:80"
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

## 🔧 Конфигурация

### Переменные окружения (.env)
```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

# База данных
DB_ENGINE=django.db.backends.postgresql
DB_NAME=codecv_db
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# GitHub API (для автозаполнения)
GITHUB_API_TOKEN=your_github_token_here
GITHUB_API_URL=https://api.github.com

# Безопасность
CSRF_TRUSTED_ORIGINS=http://localhost:8000,https://yourdomain.com
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Email (опционально)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Настройки Django (config/settings.py)
```python
# Основные настройки
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Сторонние приложения
    'django_htmx',
    'crispy_forms',
    'crispy_tailwind',
    'corsheaders',
    'rest_framework',
    
    # Наши приложения
    'cvbuilder',
    'users',
    'api',
]

# Безопасность
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
```

## 📁 Структура проекта

### Бэкенд (Django)
```
cvbuilder/
├── models.py              # Модели: CVProfile, Skill, Project, Experience
├── views.py               # Представления: cv_detail, dashboard, api
├── forms.py               # Формы для редактирования профиля
├── admin.py               # Админ-панель Django
├── serializers.py         # Сериализаторы для API
├── context_processors.py  # Контекстные процессоры
├── templatetags/          # Пользовательские теги шаблонов
└── templates/cvbuilder/   # Шаблоны приложения
```

### Модели данных
```python
class CVProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    github_username = models.CharField(max_length=100)
    bio = models.TextField()
    headline = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    website = models.URLField()
    theme = models.CharField(max_length=50, choices=THEME_CHOICES)
    github_data = models.JSONField(default=dict)  # Кэш данных GitHub
    is_public = models.BooleanField(default=True)
    views = models.PositiveIntegerField(default=0)

class Skill(models.Model):
    profile = models.ForeignKey(CVProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20)  # frontend/backend/tools
    level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    order = models.IntegerField(default=0)
```

## 🎨 Функционал

### 1. 📊 **Панель управления**
- Редактирование профиля в реальном времени
- Предпросмотр изменений
- Управление видимостью резюме
- Статистика просмотров

### 2. 🔄 **GitHub интеграция**
- Автоимпорт репозиториев
- Анализ используемых языков программирования
- Календарь активности (как на GitHub)
- Топ проекты с описанием

### 3. 🌐 **Публичное резюме**
- Уникальный URL: `/cv/username/`
- Адаптивный дизайн
- Темная/светлая тема
- Оптимизация для SEO
- Open Graph разметка для соцсетей

### 4. 🎯 **Интерактивные элементы**
- **3D Tech Sphere**: Вращающаяся сфера с иконками технологий
- **Skill Metrics**: Интерактивные диаграммы навыков
- **Live Code Editor**: Встроенный редактор для демо
- **Project Previews**: Превью проектов прямо в резюме

### 5. 📱 **Мобильные возможности**
- PWA поддержка (можно установить как приложение)
- Оффлайн-доступ к резюме
- Push-уведомления о просмотрах

### 6. 🔧 **Инструменты разработчика**
- JSON API для всех данных
- Webhook для автоматического обновления
- RSS лента изменений
- Sitemap.xml для поисковиков

## 🔌 API Endpoints

### Основные endpoints
```
GET    /api/profile/{username}/          # Получить профиль
GET    /api/skills/{username}/          # Навыки пользователя
GET    /api/projects/{username}/        # Проекты из GitHub
POST   /api/sync-github/{username}/     # Синхронизация с GitHub
GET    /api/stats/{username}/           # Статистика просмотров
```

### Пример ответа API
```json
{
  "username": "developer",
  "profile": {
    "bio": "Full-stack разработчик",
    "headline": "Senior Developer",
    "github_username": "devuser",
    "location": "Москва, Россия",
    "theme": "github-dark"
  },
  "skills": [
    {"name": "Python", "level": 5, "category": "backend"},
    {"name": "Django", "level": 5, "category": "backend"},
    {"name": "React", "level": 4, "category": "frontend"}
  ],
  "stats": {
    "views": 42,
    "last_viewed": "2024-01-18T14:30:00Z"
  }
}
```

## 🧪 Тестирование

### Запуск тестов
```bash
# Все тесты
python manage.py test

# Конкретное приложение
python manage.py test cvbuilder

# С покрытием кода
coverage run manage.py test
coverage report
coverage html
```

### Типы тестов
- **Unit тесты**: Модели, формы, сериализаторы
- **Интеграционные тесты**: API endpoints
- **Функциональные тесты**: Пользовательские сценарии
- **Нагрузочные тесты**: Locust сценарии

## 🚀 Деплой

### Вариант 1: Vercel + Railway
```bash
# Фронтенд на Vercel
vercel deploy --prod

# Бэкенд на Railway
railway up --service backend
```

### Вариант 2: Heroku
```bash
# Создать приложение
heroku create codecv-app

# Добавить PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Деплой
git push heroku main

# Миграции
heroku run python manage.py migrate
```

### Вариант 3: Собственный сервер (Ubuntu)
```bash
# Установка
sudo apt update
sudo apt install nginx postgresql python3-pip

# Настройка
sudo cp codecv.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/codecv.conf /etc/nginx/sites-enabled/

# Запуск
sudo systemctl restart nginx
gunicorn --workers 3 config.wsgi:application
```

### CI/CD (GitHub Actions)
```yaml
# .github/workflows/deploy.yml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Run tests
        run: |
          python -m pytest
          
  deploy:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to production
        run: |
          # Ваши команды деплоя
```

## 🤝 Вклад в проект

### Как помочь проекту
1. Форкните репозиторий
2. Создайте ветку для фичи (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Запушьте в форк (`git push origin feature/amazing-feature`)
5. Создайте Pull Request

### Требования к коду
- PEP 8 для Python кода
- Комментарии для сложной логики
- Тесты для новой функциональности
- Обновление документации

### Roadmap проекта
- [ ] Мобильное приложение (React Native)
- [ ] Расширенная аналитика
- [ ] Плагины для VS Code/Chrome
- [ ] Интеграция с LinkedIn
- [ ] AI-ассистент для написания резюме

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для подробностей.

### Используемые технологии с лицензиями
- **Django**: BSD лицензия
- **PostgreSQL**: PostgreSQL лицензия
- **Three.js**: MIT лицензия
- **Tailwind CSS**: MIT лицензия
- **HTMX**: BSD лицензия

## 🙏 Благодарности

- **Django Software Foundation** за удивительный фреймворк
- **Команда Three.js** за 3D графику в браузере
- **Сообщество HTMX** за современный подход к веб-разработке
- **Всем контрибьюторам** проекта

## 📞 Контакты и поддержка

### Ссылки
- 🌐 **Демо**: [https://codecv-demo.vercel.app](https://codecv-demo.vercel.app)
- 📖 **Документация**: [https://docs.codecv.dev](https://docs.codecv.dev)
- 💬 **Discord**: [https://discord.gg/codecv](https://discord.gg/codecv)
- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/codecv/issues)
- 💡 **Идеи**: [GitHub Discussions](https://github.com/yourusername/codecv/discussions)

### Авторы
- **Ваше Имя** - Разработчик и автор идеи
- **Сообщество** - Контрибьюторы и тестеры

### Поддержать проект
Если вам нравится проект, вы можете:
- ⭐ Поставить звезду на GitHub
- 🐛 Сообщать о багах
- 💡 Предлагать идеи
- 🔧 Делать Pull Requests
- ☕ [Купить кофе автору](https://buymeacoffee.com/youraccount)

---

<div align="center">

**Сделано с ❤️ для разработчиков по всему миру**

*"Ваш код — ваше лучшее резюме"*

[⬆️ Наверх](#-codecv---интерактивное-резюме-для-разработчиков)

</div>