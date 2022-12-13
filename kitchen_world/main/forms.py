from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import CharField, Textarea, Form, EmailField, ImageField


class RegistrationUserForm(UserCreationForm):
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


class ChangeUserPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.fields.values():
            f.widget.attrs.update({'class': 'login-form__input input'})


class EditProfileForm(Form):
    username = CharField()
    first_name = CharField(required=False)
    last_name = CharField(required=False)
    email = EmailField(required=False)
    description = CharField(widget=Textarea, required=False)
    photo = ImageField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ""
        self.fields['first_name'].widget.attrs.update({'class': 'input', 'placeholder': 'Имя'})

        self.fields['last_name'].label = ""
        self.fields['last_name'].widget.attrs.update({'class': 'input', 'placeholder': 'Фамилия'})

        self.fields['username'].label = ""
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Логин'})

        self.fields['email'].label = ""
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder': 'Почта'})

        self.fields['description'].label = ""
        self.fields['description'].widget.attrs.update({'class': 'input big-input', 'placeholder': 'О себе'})

        self.fields['photo'].label = ""
        self.fields['photo'].widget.attrs.update({'class': 'input'})

    class Meta:
        fields = ('first_name', 'last_name', 'username', 'email', 'description', 'photo')
