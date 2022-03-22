# Foodgram

Учебный проект. Создавался api на DRF для фронтовой части.
На сайте можно создавать записи рецептов, подписываться на пользователей, отмечать рецепты в избранное.

### Установка

  

1. Склонируйте репозиторий

2. Установите на сервер Docker

4. Скопируйте файлы docker-compose.yml и nginx.conf из директории infra на сервер (настройте под свой сервер)

5. Создайте на сервере файл .env:

  

```

DB_ENGINE=

DB_NAME=

DB_USER=

DB_PASSWORD=

DB_HOST=

DB_PORT=

SECRET_KEY=

  

```

  

6. Запустите команду на сервере docker-compose up --build

7. Сделайте миграции и создайте пользователя:

  
  

```

sudo docker-compose exec api python manage.py migrate

sudo docker-compose exec api python manage.py createsuperuser

sudo docker-compose exec api python manage.py collectstatic --no-input

```

  

Ссылка на проект: http://62.84.124.170/

  

Тестовый пользователь:

логин: test@mail.ru

пароль: adminadmin

  

Технологи: Docker django django REST framework djoser nginx

Автор: https://github.com/frollow