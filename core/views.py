from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, ProfileForm, SignupForm

DEMO_USER = {
    "username": "alex", "nickname": "Алексей", "email": "alex@example.com",
    "avatar": "core/img/avatar-1.svg",
}
DEMO_MESSAGE = "Форма проверена. В ДЗ2 данные пока не сохраняются."


def render_form_page(request, template, form_class, *, initial=None, demo_profile=False):
    form = form_class(
        request.POST if request.method == "POST" else None,
        request.FILES if request.method == "POST" else None,
        initial=initial,
    )
    valid = request.method == "POST" and form.is_valid()
    return render(request, template, {
        "form": form,
        "form_action": reverse(request.resolver_match.view_name),
        "demo_message": DEMO_MESSAGE if valid else "",
        "demo_profile": demo_profile,
        "demo_user": DEMO_USER,
    })


@require_http_methods(["GET", "POST"])
def login(request):
    return render_form_page(request, "core/login.html", LoginForm)


@require_http_methods(["GET", "POST"])
def signup(request):
    return render_form_page(request, "core/signup.html", SignupForm)


@require_http_methods(["GET", "POST"])
def profile(request):
    return render_form_page(request, "core/profile.html", ProfileForm,
                            initial={name: DEMO_USER[name] for name in ("username", "email", "nickname")},
                            demo_profile=True)
