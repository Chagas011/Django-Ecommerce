from django.views import View

from django.shortcuts import render, redirect


class Finalizar(View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')
        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho'],
        }
        return render(self.request, 'produto/finalizar.html', contexto)
