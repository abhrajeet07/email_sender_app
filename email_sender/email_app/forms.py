from django import forms

class EmailForm(forms.Form):
    email_file = forms.FileField()
    subject = forms.CharField(max_length=255)
    body = forms.CharField(widget=forms.Textarea)