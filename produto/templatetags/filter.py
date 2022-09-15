from django.template import Library

register = Library()


@register.filter
def formata_preco(valor):
    return f'R$ {valor:.2f}'.replace('.', ',')


@register.filter
def cart_total_qtd(carrinho):
    return sum([i['quantidade'] for i in carrinho.values()])


@register.filter
def cart_total(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional')
            else item.get('preco_quantitativo')
            for
            item in carrinho.values()
        ]
    )
