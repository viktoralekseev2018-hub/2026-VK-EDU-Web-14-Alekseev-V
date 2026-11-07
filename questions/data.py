"""Детерминированные данные-заглушки. В дальнейшем заменяются ORM."""
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

MEMBERS = [
    {"name": "Алексей", "score": 120, "avatar": "core/img/avatar-1.svg"},
    {"name": "Мария", "score": 95, "avatar": "core/img/avatar-2.svg"},
    {"name": "Иван", "score": 80, "avatar": "core/img/avatar-3.svg"},
]
TAGS = ["python", "django", "javascript", "html", "css", "git"]
EXAMPLES = [
    ("Как организовать структуру Django-проекта?",
     "Начинаю изучать Django. Где хранить общие шаблоны и статические файлы? Как лучше разделить проект на приложения?", ["python", "django"]),
    ("Как выровнять элементы с помощью Flexbox?",
     "Нужно расположить элементы по центру контейнера и сохранить отступы между ними. Какие свойства для этого использовать?", ["html", "css"]),
    ("Почему не работает обработчик события click?",
     "Добавил кнопку и обработчик в JavaScript, но при нажатии ничего не происходит. Как проверить, что элемент найден правильно?", ["javascript", "html"]),
    ("Как передать список из view в шаблон?",
     "Хочу вывести список записей в шаблоне Django. Как передать данные через контекст и использовать цикл for?", ["python", "django"]),
    ("Как сделать адаптивные колонки в Bootstrap?",
     "На компьютере нужны две колонки, а на телефоне — одна. Как использовать классы сетки Bootstrap?", ["html", "css"]),
    ("Как создать новую ветку в Git?",
     "Работаю над учебным проектом. Подскажите, как создать отдельную ветку и переключиться на неё.", ["git"]),
]

QUESTIONS = []
for number, (title, text, tags) in enumerate(EXAMPLES, start=1):
    question_id = 35 if number == 5 else number
    QUESTIONS.append({
        "id": question_id,
        "title": title,
        "text": text,
        "tags": tags,
        "author": MEMBERS[(number - 1) % len(MEMBERS)],
        "rating": (number * 7) % 41 - 3,
        "vote_state": {0: -1, 1: 1, 2: 0}[number % 3],
        "created_at": datetime(2026, 11, 6, 10, tzinfo=ZoneInfo("Europe/Moscow")) + timedelta(minutes=number * 20),
        "answers_count": 5 if question_id in {1, 35} else number % 3,
    })


def get_question(question_id):
    return next((item for item in QUESTIONS if item["id"] == question_id), None)


def get_answers(question):
    texts = [
        "Начните с простого примера из документации. Разделите задачу на небольшие шаги и проверьте каждый из них отдельно.",
        "Проверьте имена файлов, пути и настройки. Если возникает ошибка, полезно привести её полный текст и минимальный пример кода.",
        "Похожую задачу можно решить стандартными средствами. Сначала добейтесь рабочего результата, затем выносите общую логику в отдельные функции.",
    ]
    if "django" in question["tags"]:
        texts[0] = "Создавайте приложения по смыслу: questions для вопросов и core для пользовательских страниц. Общий base.html можно хранить в core/templates/core/, статику — в static/<имя приложения>/."
    elif "css" in question["tags"]:
        texts[0] = "Используйте сетку Bootstrap: container, row и col-lg-*. На узких экранах колонки займут всю доступную ширину и встанут друг под другом."
    return [
        {
            "id": f"{question['id']}-{number}",
            "text": texts[(number - 1) % len(texts)],
            "author": MEMBERS[number % len(MEMBERS)],
            "rating": max(0, 12 - number),
            "vote_state": 0,
            "is_correct": number == 1,
            "created_at": question["created_at"] + timedelta(minutes=number * 5),
        }
        for number in range(1, question["answers_count"] + 1)
    ]
