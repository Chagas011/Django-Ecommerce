from django.views.generic import DetailView
from ..models import Pedido
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(
        login_url='perfil:criar', redirect_field_name='next'), name='dispatch')
class Pagar(DetailView):
    template_name = 'pedidos/pagar.html'
    model = Pedido
    pk_url_kwarg = 'pk'
    context_object_name = 'pedido'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs
