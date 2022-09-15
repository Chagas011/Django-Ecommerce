from django.views import View
from django.shortcuts import redirect
from django.contrib import messages
from produto.models import Variacao
from utils.cart_total import cart_total_qtd, cart_total_carrinho
from ..models import Pedido, ItemPedido
from django.urls import reverse


class FecharPedido(View):
    template_name = 'pedidos/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Faça login para realizar o pagamento')
            return redirect('perfil:criar')
        if not self.request.session.get('carrinho'):
            messages.warning(
                self.request,
                'Carrinho Vazio'
            )
            return redirect('produto:lista')
        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_id = [v for v in carrinho]
        variacoes_produto = list(
            Variacao.objects.select_related('produto')
            .filter(id__in=carrinho_variacao_id)
        )

        for variacao in variacoes_produto:
            vid = str(variacao.id)
            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade']
            preco_unt = carrinho[vid]['preco_unitario']
            preco_unt_promo = carrinho[vid]['preco_unitario_promocional']

            error_msg_estoque = ''

            if estoque < qtd_carrinho:
                carrinho[vid]['quantidade'] = estoque
                carrinho[vid]['preco_quantitativo'] = estoque * preco_unt
                carrinho[vid]['preco_unitario_promocional'] = estoque * preco_unt_promo  # noqa
                error_msg_estoque = 'Alguns produtos do seu carrinho não estão mais disponivel'  # noqa

            if error_msg_estoque:
                messages.warning(
                    self.request,
                    error_msg_estoque
                )
                self.request.session.save()
                return redirect('produto:carrinho')

        qtd_total_carrinho = cart_total_qtd(carrinho)
        valor_total_carrinho = cart_total_carrinho(carrinho)

        pedido = Pedido(
            usuario=self.request.user,
            total=valor_total_carrinho,
            qtd_total=qtd_total_carrinho,
            status='C',
        )
        pedido.save()
        ItemPedido.objects.bulk_create(
            [ItemPedido(
                pedido=pedido,
                produtos=v['produto_nome'],
                produto_id=v['produto_id'],
                variacao=v['variacao_nome'],
                variacao_id=v['variacao_id'],
                preco=v['preco_quantitativo'],
                preco_promocional=v['preco_quantitativo_promocional'],
                quantidade=v['quantidade'],
                imagem=v['imagem'],
            ) for v in carrinho.values()
            ]
        )
        del self.request.session['carrinho']

        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'pk': pedido.pk
                }
            )
        )
