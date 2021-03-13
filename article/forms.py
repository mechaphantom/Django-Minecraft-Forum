from django import forms
from .models import Article, Profile

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "content", "header_image"]


class contactformemail(forms.Form):
    frommail = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
