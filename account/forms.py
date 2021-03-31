from django import forms
from django.contrib.auth.models import User

from account.models import Profile


class LoginForm(forms.Form):
    """ Форма входа """
    username = forms.CharField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')


class UserRegistrationForm(forms.ModelForm):
    """ Форма регистрации """
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    repeat_password = forms.CharField(label='Пвторение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_repeat_password(self):
        """ Проверка совпадения повторного введенного пароля"""
        cd = self.cleaned_data
        if cd['password'] != cd['repeat_password']:
            raise forms.ValidationError('Пароли не совпадают!')
        return cd['repeat_password']

    def clean_email(self):
        """ Проверка уникальности email """
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count() > 0:
            raise forms.ValidationError('Пользователь с таким адресом почты уже зарегистрированн!')
        return email


class UserEditForm(forms.ModelForm):
    """ Форма редактирования пользователя """
    email = forms.CharField(
        widget=forms.TextInput(attrs={'readonly': 'readonly'})
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """ Форма редактирования профиля пользователя """
    class Meta:
        model = Profile
        fields = ('budget',)
