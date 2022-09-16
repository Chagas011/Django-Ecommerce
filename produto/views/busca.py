
from django.views.generic import ListView
from django.db.models import Q

from ..models import Produto


class Busca(ListView):
    template_name = 'produto/busca.html'
    paginate_by = 3
    context_object_name = 'produtos'
    model = Produto
    ordering = ['-id']

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        termo = self.request.GET.get('termo') or self.request.session['termo']
        if not termo:
            return qs
        self.request.session['termo'] = termo

        qs = qs.filter(

            Q(nome__icontains=termo) |
            Q(descricao_curta__icontains=termo) |
            Q(descricao_longa__icontains=termo)
        )
        self.request.session.save()
        return qs
