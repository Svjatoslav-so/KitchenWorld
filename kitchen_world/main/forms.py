from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class RegistrationUserForm(UserCreationForm):
    # username = forms.CharField()
    # email
    # password1
    # password2
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'login-form__input input'})
        self.fields['username'].label = "Логин"
        self.fields['email'].label = "Эл-почта"
        self.fields['password1'].label = "Пароль"
        self.fields['password2'].label = "Подтвердите пароль"

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'login-form__input input'})
        self.fields['username'].label = "Логин"
        self.fields['password'].label = "Пароль"


