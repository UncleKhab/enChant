from django import forms
from django.conf import settings
from .models import Tweet


class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        fields = ['content']

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) > 256:
            raise form.ValidationError("This Tweet is too long!")
        return content