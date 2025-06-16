## ДЛЯ РЕВЬЮЕРА
Добрый день! 
Все замечания исправила.
У нас сегодня последний день сдачи принятых работ преподавателю в университете, в связи с чем очень прошу Вас поскорее проверить работу. 
Завтра с утра у нас экзамен, это очень важно.
Надеюсь на Ваше понимание! Спасибо!



## Foodgram

## Технологии
- Python 3.9
- Django 3.2
- Django REST framework
- PostgreSQL
- Docker
- Nginx
- GitHub Actions



## Запуск проекта через Docker 

1. Установите Docker и Docker Compose согласно официальной документации

2. Клонируйте репозиторий и перейдите в него:

3. Создайте файл .env в директории infra/:

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



