from django.views.generic import DetailView
from produto.models import Produto


class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/produto.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'
