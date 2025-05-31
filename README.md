Foodgram - это веб-приложение, в котором пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Содержание
- [Технологии](#технологии)
- [Подготовка к работе (Windows)](#подготовка-к-работе-windows)
- [Запуск проекта через виртуальное окружение (для разработки)](#запуск-проекта-через-виртуальное-окружение-для-разработки)
- [Запуск проекта через Docker (для деплоя)](#запуск-проекта-через-docker-для-деплоя)
- [Создание суперпользователя](#создание-суперпользователя)
- [API документация](#api-документация)

## Технологии
- Python 3.9
- Django 3.2
- Django REST framework
- PostgreSQL
- Docker
- Nginx
- GitHub Actions

## Подготовка к работе (Windows)

1. Настройте Git для корректной работы с переносами строк:
```bash
# Глобально для всех репозиториев
git config --global core.autocrlf input
# Или локально для этого репозитория
git config core.autocrlf input
```

## Запуск проекта через виртуальное окружение (для разработки)

Важно: этот способ подходит только для локальной разработки, так как использует локальную базу данных SQLite.

1. Проверьте установлен ли у вас Python версии 3.9:
```bash
python --version
# Должно вывести Python 3.9.x
```

2. Клонируйте репозиторий и перейдите в него:
```bash
git clone git@github.com:ваш-аккаунт/foodgram-project-react.git
cd foodgram-project-react
```

3. Создайте и активируйте виртуальное окружение:
```bash
# Создание виртуального окружения
python -m venv venv

# Активация в Windows
source venv/Scripts/activate
# Активация в Linux/Mac
source venv/bin/activate

# Убедитесь, что pip установлен
python -m pip install --upgrade pip
```

4. Установите зависимости:
```bash
cd backend
pip install -r requirements.txt
```

5. Примените миграции:
```bash
python manage.py migrate
```

6. Загрузите тестовые данные (ингредиенты):
```bash
python manage.py load_ingredients
```

7. Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта через Docker 

1. Установите Docker и Docker Compose согласно официальной документации

2. Клонируйте репозиторий и перейдите в него:
```bash
git clone git@github.com:ваш-аккаунт/foodgram-project-react.git
cd foodgram-project-react
```

3. Создайте файл .env в директории infra/:
```bash
touch infra/.env
```
Добавьте в него переменные окружения:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=your-secret-key
```

4. Запустите контейнеры:
```bash
docker-compose up -d --build
```

5. Выполните миграции:
```bash
docker-compose exec backend python manage.py migrate
```

6. Загрузите ингредиенты:
```bash
docker-compose exec backend python manage.py load_ingredients
```

## Создание суперпользователя

### В Docker:
```bash
docker-compose exec backend python manage.py createsuperuser
```

Введите данные для создания суперпользователя

## API документация

[API документация](https://api.foodgram.com/docs/)

