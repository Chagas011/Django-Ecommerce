
from django.views import View
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib import messages


class RemoverCarrinho(View):
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')
        if not variacao_id:
            # Volta para a pagina anterior com o valor de id ou slug
            return redirect(http_referer)

        if not self.request.session.get('carrinho'):
            return redirect(http_referer)
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)
        carrinho = self.request.session['carrinho'][variacao_id]

        messages.success(
            self.request,
            f'Produto {carrinho["produto_nome"]} Removido com sucesso')
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()

        return redirect(http_referer)
