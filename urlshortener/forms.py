from django import forms
from .models import Shortener,UserAgent

class ShortenerForm(forms.ModelForm):
    long_url = forms.URLField(widget=forms.URLInput(
 attrs={"class": "form-control form-control-lg", "placeholder": "Your URL to shorten"} ))
    class Meta:
        model = Shortener
        fields = ("long_url",)

class UserAgentForm(forms.ModelForm):
    class Meta:
        model = UserAgent
        fields = "__all__"

