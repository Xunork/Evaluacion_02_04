from django.contrib import admin
from .models import Categoria, Producto, Pedido, DetallePedido


class CategoriaAdmin(admin.ModelAdmin):
    list_display = ("nombre", "descripcion")
    search_fields = ("nombre",)


class DetalleInline(admin.TabularInline):
    model = DetallePedido
    extra = 0
    readonly_fields = ("producto", "nombre_producto", "cantidad", "precio_unitario")


class ProductoAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "stock", "categoria")
    list_editable = ("precio", "stock")
    list_filter = ("categoria",)
    search_fields = ("nombre", "descripcion")
    fields = ("nombre", "precio", "stock", "categoria", "descripcion")
    list_per_page = 20
    save_on_top = True


class PedidoAdmin(admin.ModelAdmin):
    list_display = ("id", "usuario", "fecha", "total")
    inlines = [DetalleInline]


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
