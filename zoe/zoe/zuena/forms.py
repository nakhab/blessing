from django import forms

class EncryptForm(forms.Form):
    file = forms.FileField(required=False)
    text = forms.CharField(widget=forms.Textarea, required=False)
