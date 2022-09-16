from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('',
         views.ListaProduto.as_view(),
         name='lista'
         ),
    path('<slug>',
         views.DetalheProduto.as_view(),
         name='detalhe'
         ),
    path('adicionarcarrinho/',
         views.AdicionarCarrinho.as_view(),
         name='adicionarcarrinho'
         ),
    path('removercarrinho/',
         views.RemoverCarrinho.as_view(),
         name='removercarrinho'
         ),
    path('carrinho/',
         views.Carrinho.as_view(),
         name='carrinho'
         ),
    path('finalizar/',
         views.Finalizar.as_view(),
         name='finalizar'
         ),
    path('busca/',
         views.Busca.as_view(),
         name='busca'
         ),
]
