from django import forms
from .models import ShortenURL,UserAgent

class ShortenURLForm(forms.ModelForm):
    original_url = forms.URLField(widget=forms.URLInput(
 attrs={"class": "form-control form-control-lg", "placeholder": "Your URL to shorten"} ))
    class Meta:
        model = ShortenURL
        fields = ("original_url",)

class UserAgentForm(forms.ModelForm):
    class Meta:
        model = UserAgent
        fields = "__all__"

