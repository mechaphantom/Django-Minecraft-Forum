from django import forms

class contactformemail(forms.Form):
    frommail = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)


