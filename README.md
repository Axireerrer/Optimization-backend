# Subscription API Project

## Описание

### Этот проект представляет собой API для управления подписками на сервисы пользователями. API поддерживает операции CRUD (создание, чтение, обновление, удаление) для подписок. В проекте реализованы следующие ключевые особенности:

- Оптимизация SQL запросов для устранения проблемы n+1 запросов.
- Использование Redis для кэширования.
- Асинхронные задачи с помощью Celery для автоматического формирования цены подписки.
- Проект полностью контейнеризирован с использованием Docker и Docker Compose.

## Стек технологий

### Django Rest Framework, PostgreSQL, Redis, Celery, Docker, Docker-compose.

## Установка и запуск

### Шаги установки
#### Клонируйте репозиторий:

- git clone https://github.com/Axireerrer/Optimization-backend.git
  
#### Заполните необходимые переменные окружения в docker-compose.yml.
#### Поднимите контейнеры с помощью Docker Compose:

- docker-compose build
- docker-compose up
  
#### Выполните миграции базы данных:

- docker-compose run --rm django sh -c "cd service && python manage.py migrate"

#### Создайте суперпользователя для доступа к административной панели:

- docker-compose run --rm django sh -c "cd service && python manage.py createsuperuser"

#### Теперь API доступен по адресу http://localhost:8000.
