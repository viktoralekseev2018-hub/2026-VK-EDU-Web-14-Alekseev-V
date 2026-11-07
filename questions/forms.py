from django import forms

from core.forms import BootstrapForm


class AskForm(BootstrapForm):
    title = forms.CharField(label="Заголовок", min_length=10, max_length=150,
                            help_text="От 10 до 150 символов.")
    text = forms.CharField(label="Текст вопроса", min_length=20, max_length=5000,
                           help_text="От 20 до 5 000 символов. Опишите проблему и что уже пробовали.",
                           widget=forms.Textarea(attrs={"rows": 6}))
    tags = forms.CharField(label="Теги", max_length=80,
                           help_text="До трёх тегов через запятую, не более 80 символов.")

    def clean_tags(self):
        tags = [tag.strip() for tag in self.cleaned_data["tags"].split(",")]
        if not 1 <= len(tags) <= 3 or not all(tags):
            raise forms.ValidationError("Укажите от одного до трёх непустых тегов.")
        return tags


class AnswerForm(BootstrapForm):
    text = forms.CharField(label="Текст ответа", min_length=10, max_length=5000,
                           help_text="От 10 до 5 000 символов.",
                           widget=forms.Textarea(attrs={"rows": 5}))
