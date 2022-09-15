
from django import forms
from django.contrib.auth.models import User
from .models import Perfil


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = '__all__'
        exclude = ('usuario',)


class UserForm(forms.ModelForm):

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        help_text=('Sua senha precisa ter no minimo 6 Caracter'),
        label='Senha'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirme sua senha',
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email', 'password', 'password2')

    def clean(self, *args, **kwargs):
        data = self.data  # noqa
        cleaned = self.cleaned_data
        validatition_errors_msgs = {}

        usuario_cadastro = cleaned.get('username')
        email_cadastro = cleaned.get('email')
        senha_cadastro = cleaned.get('password')
        senha2_cadastro = cleaned.get('password2')

        user = User.objects.filter(username=usuario_cadastro)
        email = User.objects.filter(email=email_cadastro)

        error_msg_user_exists = 'Usuario ja existe'
        error_msg_email_exists = 'Email ja existe'
        error_msg_psw = 'Senhas divergentes'
        error_msg_psw_short = 'Sua senha precisa ter no minimo 6 Caracteres'
        error_msg_psw_required = 'Este campo é obrigatorio'

        if user:
            validatition_errors_msgs['username'] = error_msg_user_exists
        if email:
            validatition_errors_msgs['email'] = error_msg_email_exists

        if not senha_cadastro:
            validatition_errors_msgs['password'] = error_msg_psw_required
            validatition_errors_msgs['password2'] = error_msg_psw_required

        if senha_cadastro != senha2_cadastro:
            validatition_errors_msgs['password'] = error_msg_psw
            validatition_errors_msgs['password2'] = error_msg_psw
        if len(senha_cadastro) < 6:
            validatition_errors_msgs['password'] = error_msg_psw_short

        if validatition_errors_msgs:
            raise (forms.ValidationError(validatition_errors_msgs))


class UserFormLogado(forms.ModelForm):
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'email')

    def clean(self, *args, **kwargs):
        data = self.data  # noqa
        cleaned = self.cleaned_data
        validatition_errors_msgs = {}

        usuario_cadastro = cleaned.get('username')
        email_cadastro = cleaned.get('email')

        user = User.objects.filter(username=usuario_cadastro).first()
        email = User.objects.filter(email=email_cadastro).first()

        error_msg_user_exists = 'Usuario ja existe'
        error_msg_email_exists = 'Email ja existe'

        if self.usuario:
            if user:
                if usuario_cadastro != user.username:
                    validatition_errors_msgs['username'] = error_msg_user_exists  # noqa
            if email:
                if email_cadastro != email.email:
                    validatition_errors_msgs['email'] = error_msg_email_exists
