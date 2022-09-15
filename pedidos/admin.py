from django.contrib import admin

# Register your models here.
from .models import Pedido, ItemPedido


class ItemPedidoInLine(admin.TabularInline):
    model = ItemPedido
    extra = 1


class PedidosAdmin(admin.ModelAdmin):
    inlines = [
        ItemPedidoInLine
    ]


admin.site.register(Pedido, PedidosAdmin)
admin.site.register(ItemPedido)
