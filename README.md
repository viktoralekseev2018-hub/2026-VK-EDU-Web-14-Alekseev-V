# AskSpace — ДЗ2

Сайт вопросов и ответов на Django 5.2 и Bootstrap 5.3. Все стили, скрипты и изображения хранятся локально.

## Локальный запуск

Выполняйте команды в папке с `manage.py`.

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
.\.venv\Scripts\python.exe manage.py migrate
.\.venv\Scripts\python.exe manage.py runserver
```

Linux / macOS:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
cp .env.example .env
.venv/bin/python manage.py migrate
.venv/bin/python manage.py runserver
```

Откройте <http://127.0.0.1:8000/>. Для остановки нажмите Ctrl+C.

В `.env.example` перечислены настройки: `DJANGO_SECRET_KEY`, `DJANGO_DEBUG`, `DJANGO_ALLOWED_HOSTS`.

## Запуск через Docker Compose

Установите и запустите Docker, затем выполните из корня проекта:

```sh
docker compose up --build
```

Откройте <http://localhost:8000/>. Для остановки:

```sh
docker compose down
```

При необходимости стандартные миграции можно применить в работающем контейнере:

```sh
docker compose exec web python manage.py migrate
```

Сервис `web` использует порт 8000. Код подключён через volume `.:/app`, а для `media/` выделен отдельный volume `media_data`. Если `.env` отсутствует, используются настройки локальной разработки по умолчанию.

## Страницы

| Адрес | Назначение |
| --- | --- |
| `/` | Новые вопросы |
| `/hot/` | Популярные вопросы |
| `/tag/python/` | Вопросы по тегу |
| `/question/35/` | Вопрос с ответами |
| `/ask/` | Создание вопроса |
| `/login/` | Вход |
| `/signup/` | Регистрация |
| `/profile/` | Настройки профиля |

Тег и номер вопроса меняются в адресе. Несуществующий вопрос возвращает 404, неизвестный тег — пустой список.

## Устройство проекта

- `application/` — настройки Django и корневой `urls.py`.
- `core/` — вход, регистрация, профиль, общий шаблон и функция пагинации.
- `questions/` — вопросы, ответы, данные-заглушки и соответствующие страницы.
- `core/static/` и `questions/static/` — исходная статика приложений.
- `static/` в корне — результат команды `collectstatic`, исключён из Git.
- `media/` — каталог для будущих пользовательских загрузок, исключён из Git.

Шаблоны используют `extends` и `include`. Маршруты именованные; ссылки формируются через `url` и `reverse()`, пути к ресурсам — через `static`.

## Данные и пагинация

В `questions/data.py` находятся 6 разных вопросов. У вопросов 1 и 35 — по 5 ответов. В списках выводится по 3 записи на страницу.

Примеры: `/?page=2` и `/question/35/?page=2#answers`. Общая функция `paginate(objects_list, request, per_page=10)` находится в `core/pagination.py`; views передают ей размер страницы 3. Некорректные номера страниц заменяются первой страницей с обработкой `PageNotAnInteger` и `EmptyPage`.

Данные без сохранения в БД. Формы проверяют введённые значения, но не создают аккаунты, вопросы или ответы и не выполняют настоящий вход. Аватары не сохраняются. Состояния голосования и правильного ответа сбрасываются после перезагрузки.

Версии зависимостей закреплены в `requirements.txt`.