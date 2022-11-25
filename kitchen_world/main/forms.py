from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, Textarea


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


# to do
class MultiEmailField(CharField):
    def validate(self, value):
        # """Check if value consists only of valid emails."""
        # # Use the parent's handling of required fields, etc.
        # super().validate(value)
        # for email in value:
        #     validate_email(email)
        pass


class EditProfileForm(ModelForm):
    description = CharField(widget=Textarea)
    # email = CharField()
    username = MultiEmailField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].label = ""
        self.fields['first_name'].widget.attrs.update({'class': 'input', 'placeholder':'Имя'})

        self.fields['last_name'].label = ""
        self.fields['last_name'].widget.attrs.update({'class': 'input', 'placeholder': 'Фамилия'})

        self.fields['username'].label = ""
        self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder':'Логин'})

        self.fields['email'].label = ""
        self.fields['email'].widget.attrs.update({'class': 'input', 'placeholder':'Почта'})

        self.fields['description'].label = ""
        self.fields['description'].widget.attrs.update({'class': 'input big-input', 'placeholder':'О себе'})


    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'description')
