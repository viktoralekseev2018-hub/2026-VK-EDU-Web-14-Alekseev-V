from questions.data import MEMBERS, QUESTIONS, TAGS


def sidebar(request):
    return {
        "popular_tags": [{"name": tag, "count": sum(tag in q["tags"] for q in QUESTIONS)} for tag in TAGS],
        "best_members": MEMBERS,
    }
