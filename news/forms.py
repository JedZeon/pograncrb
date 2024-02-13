from django import forms
from django.core.exceptions import ValidationError


from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'content',
            'author',
            'categories',
        ]

    # дополнительные свои контроли полей формы
    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get("title")
    #     text = cleaned_data.get("text")
    #
    #     if title == text:
    #         raise ValidationError(
    #             "Описание не должно быть идентичным заголовку."
    #         )
    #
    #     return cleaned_data

