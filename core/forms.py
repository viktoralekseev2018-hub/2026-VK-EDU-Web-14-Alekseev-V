from django import forms
from django.core.validators import FileExtensionValidator


class BootstrapForm(forms.Form):
    """Общее оформление полей для всех форм сайта."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"
            field.widget.attrs["aria-describedby"] = f"id_{name}_help id_{name}_errors"
            if getattr(field, "min_length", None):
                field.widget.attrs["minlength"] = field.min_length
        if self.is_bound:
            for name in self.errors:
                if name in self.fields:
                    self.fields[name].widget.attrs.update({
                        "class": "form-control is-invalid", "aria-invalid": "true"
                    })


class LoginForm(BootstrapForm):
    email = forms.EmailField(label="Email", max_length=254,
                             widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    password = forms.CharField(label="Пароль", min_length=8, max_length=128,
                               help_text="От 8 до 128 символов.",
                               widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}))


class SignupForm(BootstrapForm):
    username = forms.CharField(label="Логин", min_length=3, max_length=30,
                               help_text="От 3 до 30 символов.",
                               widget=forms.TextInput(attrs={"autocomplete": "username"}))
    email = forms.EmailField(label="Email", max_length=254,
                             widget=forms.EmailInput(attrs={"autocomplete": "email"}))
    nickname = forms.CharField(label="Отображаемое имя", max_length=50,
                               widget=forms.TextInput(attrs={"autocomplete": "nickname"}))
    password = forms.CharField(label="Пароль", min_length=8, max_length=128,
                               help_text="От 8 до 128 символов.",
                               widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    password_repeat = forms.CharField(label="Повторите пароль", min_length=8, max_length=128,
                                      widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}))
    avatar = forms.FileField(label="Аватар", required=False,
                             help_text="Необязательно. JPG или PNG, до 2 МБ.",
                             validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
                             widget=forms.FileInput(attrs={"accept": "image/png,image/jpeg"}))

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") and cleaned.get("password_repeat"):
            if cleaned["password"] != cleaned["password_repeat"]:
                self.add_error("password_repeat", "Пароли не совпадают.")
        return cleaned

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Файл должен быть не больше 2 МБ.")
        return avatar


class ProfileForm(BootstrapForm):
    username = forms.CharField(label="Логин", min_length=3, max_length=30,
                               help_text="От 3 до 30 символов.")
    email = forms.EmailField(label="Email", max_length=254)
    nickname = forms.CharField(label="Отображаемое имя", max_length=50)
    avatar = forms.FileField(label="Изменить аватар", required=False,
                             help_text="JPG или PNG, до 2 МБ. Пустое поле сохраняет текущий аватар.",
                             validators=[FileExtensionValidator(["jpg", "jpeg", "png"])],
                             widget=forms.FileInput(attrs={"accept": "image/png,image/jpeg"}))

    def clean_avatar(self):
        avatar = self.cleaned_data.get("avatar")
        if avatar and avatar.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Файл должен быть не больше 2 МБ.")
        return avatar
