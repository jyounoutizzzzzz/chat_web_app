from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser
from django import forms


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
    

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if '@' in username:
            raise forms.ValidationError("ユーザー名にEメールアドレスは使用できません")
        return username



class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class LoginForm(AuthenticationForm):
    
    pass