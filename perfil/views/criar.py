
from django.views import View
from ..forms import PerfilForm, UserForm, UserFormLogado
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
import copy
from ..models import Perfil
from django.contrib.auth import authenticate, login
from django.contrib import messages


class BasePerfil(View):
    template_name = 'perfil/create_perfil.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        self.perfil = None
        if self.request.user.is_authenticated:
            self.perfil = Perfil.objects.filter(
                usuario=self.request.user).first()
            self.contexto = {
                'perfilform': PerfilForm(
                    data=self.request.POST or None, instance=self.perfil),
                'userformlogado': UserFormLogado(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                )
            }
            self.perfilform = self.contexto['perfilform']
            self.userformlogado = self.contexto['userformlogado']
        else:
            self.contexto = {
                'perfilform': PerfilForm(data=self.request.POST or None),
                'userform': UserForm(data=self.request.POST or None)
            }
            self.userform = self.contexto['userform']
            self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'

        self.renderizar = render(
            self.request, self.template_name, self.contexto)

    def get(self, *args, **kwargs):
        return self.renderizar


class Criar(BasePerfil):

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            if not self.perfilform.is_valid() or not self.userformlogado.is_valid():  # noqa
                messages.error(self.request, 'Corrija os campos do formulario')
                return self.renderizar
            else:
                username = self.userformlogado.cleaned_data.get('username')
                first_name = self.userformlogado.cleaned_data.get('first_name')
                last_name = self.userformlogado.cleaned_data.get('last_name')
                email = self.userformlogado.cleaned_data.get('email')

                usuario_logado = get_object_or_404(
                    User, username=self.request.user.username)
                usuario_logado.username = username
                usuario_logado.first_name = first_name
                usuario_logado.last_name = last_name
                usuario_logado.email = email
                usuario_logado.save()

                perfil_logado = self.perfilform.save(commit=False)
                perfil_logado.usuario = usuario_logado
                perfil_logado.save()

                if not self.perfil:
                    self.perfilform.cleaned_data['usuario'] = usuario_logado
                    perfil = Perfil(**self.perfilform.cleaned_data)
                    perfil.save()

        else:
            if not self.perfilform.is_valid() or not self.userform.is_valid():
                messages.error(self.request, 'Corrija os campos do formulario')
                return self.renderizar

            else:
                senha = self.userform.cleaned_data.get('password')

                usuario = self.userform.save(commit=False)
                usuario.set_password(senha)
                usuario.save()

                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()

                autentica = authenticate(
                    self.request, username=usuario, password=senha)

                if autentica:
                    login(self.request, user=usuario)

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        if self.request.user.is_authenticated:
            messages.success(
                self.request, 'Seu cadastro foi Atualizado com sucesso')

        messages.success(self.request, 'Seu cadastro foi criado com sucesso')

        return redirect('perfil:criar')
