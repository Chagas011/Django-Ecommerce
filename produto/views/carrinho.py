
from django.views import View

from django.shortcuts import render


class Carrinho(View):

    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho')
        }
        return render(self.request, 'produto/carrinho.html', context=contexto)
