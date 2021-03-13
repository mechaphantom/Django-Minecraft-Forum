from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from article.models import Profile

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola",widget= forms.PasswordInput)
    
class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(label="Parolayı Doğrula", widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor!")

        values = {
            "username" : username,
            "password" : password,
        }
        
        return values

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = {
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
        }

class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "profile_pic"]