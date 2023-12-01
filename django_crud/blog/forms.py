from django import forms
from .models import Post


class useBlogForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={"class": "form-control"}))
    description = forms.CharField(widget=forms.Textarea(
        attrs={"class": "form-control", "rows": "3"}))

    class Meta:
        model = Post
        fields = ["title", "description"]
