### Проект short-URL - сервис для создания сокращённой формы передаваемых URL и анализа активности их использования.

### Возможности API:

1. Получить сокращённый вариант переданного URL.

```python
POST /
```

Метод принимает в теле запроса строку URL для сокращения и возвращает ответ с кодом `201`.

2. Вернуть оригинальный URL.

```python
GET /<shorten-url-id>
```

Метод принимает в качестве параметра идентификатор сокращённого URL и возвращает ответ с кодом `307` и оригинальным URL в заголовке `Location`.

3. Вернуть статус использования URL.

```python
GET /<shorten-url-id>/status?[full-info]&[max-result=10]&[offset=0]
```


### Пример наполнения .env-файла:
```
DATABASE_DSN=postgresql+asyncpg://<user>:<password>@localhost:5432/<db_name>
```

### Описание команд для запуска приложения локально:

Клонирование репозитория и переход в него в командной строке:

```
git clone https://git@github.com:mawuta-super-hack/short-URL.git
```

```
cd ./src
```


Установка и активация виртуального окружения:

```
python -m venv env
```

```
source venv/Scripts/activate
```


Установка зависимостей из файла requirements.txt:
```
python -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запуск контейнера с образом базы данных postgres:
```
docker run \
  --rm   \
  --name postgres-fastapi \
  -p 5432:5432 \
  -e POSTGRES_USER=<USER> \
  -e POSTGRES_PASSWORD=<PASSWORD> \
  -e POSTGRES_DB=<NAME_DB> \
  -d postgres:14.5
```

Выполнение миграций:
```
alembic init --t async migrations
```
```
alembic revision --autogenerate -m 01_initial-db
```
```
alembic upgrade head
```

Запуск сервера:
```
uvicorn main:app --host 127.0.0.1 --port 8080 --reload
```

Полный список эндпоинтов описан в документации.
Документация доступна после запуска проекта по [адресу](http://127.0.0.1:8080/api/openapi).

Автор проекта:
<br>
Клименкова Мария [Github](https://github.com/mawuta-super-hack)<br>
