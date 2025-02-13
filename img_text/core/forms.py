from django import forms


class AuthForm(forms.Form):
    username = forms.CharField(max_length=254, required=True, help_text='Введите Ваш логин или почту')
    password = forms.CharField(max_length=15, required=True, help_text='Введите Ваш супер-пупер пароль, nagibator3000')