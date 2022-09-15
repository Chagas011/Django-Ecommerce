from django.views.generic.list import ListView
from produto.models import Produto


class ListaProduto(ListView):
    template_name = 'produto/produtos.html'
    paginate_by = 3
    context_object_name = 'produtos'
    model = Produto
    ordering = ['-id']
