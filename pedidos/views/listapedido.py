
from django.views.generic import ListView
from ..models import Pedido
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


@method_decorator(
    login_required(
        login_url='perfil:criar', redirect_field_name='next'), name='dispatch')
class ListaPedido(ListView):
    template_name = 'pedidos/listapedido.html'
    model = Pedido
    context_object_name = 'pedidos'
    paginate_by = 5
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(usuario=self.request.user)
        return qs
