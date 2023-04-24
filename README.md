# Описание
Проект YaMDb собирает отзывы пользователей на различные произведения. Произведение могут  сгруппированы по жанрам и категориям. Создавать и удалять произведения может только администратор. Любой авторизованный пользователь может прокоментировать отзыв оставленный на сервисе. В случае надобности администрация сервиса может изменять или удалять комментарии оставленные пользователями.

Реализован REST API CRUD для моделей проекта, аунтефикация производится по jwt-токену. В проекте также реализованы пермишены, фильтрации, сортировки и поиск по запросам клиентов, пагинация ответов от API, установлено ограничение количества запросов к API.

# Системные требования
* Python 3.8+
* Works on Linux, Windows, macOS

# Стек технологий:
* Python 3.8
* Django 3.2
* Django Rest Framework
* Simple-JWT

# Как запустить проект:
Клонируем репозиторийи перемещаемся в него используя командую строку:

```
git clone https://github.com/Den-Krutov/api_yamdb
```

```
cd api_yamdb
```

Создаём и активируем виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Обновляем pip и загружаем зависимости из файла requirements:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Проводим миграции:

```
python3 manage.py migrate
```

Запускаем сервер:

```
python3 manage.py runserver
```
# Документация к проекту
Документация для API доступна по ссылке после установки приложения.

# Примеры некоторых полезных API запросов:
### Зарегистрироваться:
POST request:
```
http://127.0.0.1:8000/api/v1/signup/
```
```
{
    "email": "string",
    "username": "string"
}
```
### Получить jwt-токен:
POST request:
```
http://127.0.0.1:8000/api/v1/auth/token/
```
```
{
  "username": "string",
  "confirmation_code": "string"
}
```
# CRUD для отзывов и комментариев пользователей:

GET request(любой, кроме PUT):
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/
```
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 1,
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
GET request(любой, кроме PUT):
```
http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/
```
```
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2019-08-24T14:15:22Z"
    }
  ]
}
```
