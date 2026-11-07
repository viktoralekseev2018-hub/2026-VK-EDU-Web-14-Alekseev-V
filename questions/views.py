from django.http import Http404
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_GET, require_http_methods

from core.pagination import paginate
from core.views import DEMO_MESSAGE, render_form_page
from .data import QUESTIONS, get_answers, get_question
from .forms import AnswerForm, AskForm


def search_questions(request, objects):
    query = request.GET.get("q", "").strip()[:100]
    if query:
        objects = [q for q in objects if query.casefold() in
                   (q["title"] + " " + q["text"] + " " + " ".join(q["tags"])).casefold()]
    return objects, query


@require_GET
def index(request):
    objects, query = search_questions(request, sorted(QUESTIONS, key=lambda q: q["created_at"], reverse=True))
    return render(request, "questions/index.html", {
        "page_obj": paginate(objects, request, per_page=3), "search_query": query, "list_mode": "new",
    })


@require_GET
def hot(request):
    objects, query = search_questions(request, sorted(QUESTIONS, key=lambda q: (-q["rating"], -q["id"])))
    return render(request, "questions/hot.html", {
        "page_obj": paginate(objects, request, per_page=3), "search_query": query, "list_mode": "hot",
    })


@require_GET
def tag(request, tag):
    objects = sorted([q for q in QUESTIONS if tag in q["tags"]], key=lambda q: q["created_at"], reverse=True)
    objects, query = search_questions(request, objects)
    return render(request, "questions/tag.html", {
        "page_obj": paginate(objects, request, per_page=3), "tag_name": tag, "search_query": query,
    })


@require_http_methods(["GET", "POST"])
def question(request, question_id):
    question = get_question(question_id)
    if question is None:
        raise Http404("Вопрос не найден")
    form = AnswerForm(request.POST if request.method == "POST" else None)
    valid = request.method == "POST" and form.is_valid()
    return render(request, "questions/question.html", {
        "question": question,
        "page_obj": paginate(get_answers(question), request, per_page=3),
        "form": form,
        "form_action": reverse("questions:question", args=[question_id]),
        "demo_message": DEMO_MESSAGE if valid else "",
    })


@require_http_methods(["GET", "POST"])
def ask(request):
    return render_form_page(request, "questions/ask.html", AskForm)
