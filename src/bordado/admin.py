from ponto2.admin import admin

from .models import *


class CustomModelAdmin(admin.ModelAdmin):
    def get_form(self, request, obj=None, **kwargs):
        form = super(CustomModelAdmin, self).get_form(request, obj, **kwargs)
        if hasattr(self, 'field_style'):
            for field, style in self.field_style.items():
                form.base_fields[field].widget.attrs['style'] = style
        return form

# @admin.register(Empresa)
# class EmpresaAdmin(admin.ModelAdmin):
#     search_fields = ['nome']


@admin.register(Cliente)
class ClienteAdmin(CustomModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']
    field_style = {
        'cnpj9': 'width: 9em;',
        'cnpj4': 'width: 4em;',
        'cnpj2': 'width: 3em;',
        'parcela': 'width: 3em;',
    }


@admin.register(DificuldadeBordado)
class DificuldadeBordadoAdmin(CustomModelAdmin):
    list_display = ['__str__']
    search_fields = ['__str__']
    field_style = {
        'ordem': 'width: 3em;',
    }


@admin.register(Bordado)
class BordadoAdmin(admin.ModelAdmin):
    list_display = [
        'cliente', 'nome', 'pontos', 'cores', 'tamanho_maximo', 'dificuldade'
    ]
    list_display_links = ['nome']
    search_fields = ['cliente', 'nome']
    list_filter = ['cliente']


@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'inserido_em',
        'entrega',
        'cancelado',
    ]
    list_filter = [
        'cliente',
    ]
    fields = [
        'numero',
        'inserido_em',
        'cliente',
        'entrega',
        'cancelado',
    ]
    readonly_fields = [
        'numero',
        'inserido_em',
    ]


@admin.register(PedidoItem)
class PedidoItemAdmin(admin.ModelAdmin):
    list_display = [
        'pedido',
        'ordem',
        'inserido_em',
        'bordado',
        'quantidade',
        'preco',
        'cancelado',
    ]
    list_display_links = [
        'pedido',
        'ordem',
    ]
    list_filter = [
        'pedido__cliente',
    ]
    fields = [
        'pedido',
        'ordem',
        'inserido_em',
        'bordado',
        'quantidade',
        'preco',
        'cancelado',
    ]
    readonly_fields = [
        'ordem',
        'inserido_em',
    ]


@admin.register(OrdemProducao)
class OrdemProducaoAdmin(admin.ModelAdmin):
    list_display = [
        '__str__',
        'quantidade',
        'cancelado',
        'inserido_em',
    ]
    fields = [
        'numero',
        'inserido_em',
        'pedido_item',
        'quantidade',
        'cancelado',
    ]
    readonly_fields = [
        'numero',
        'inserido_em',
    ]


@admin.register(ApontamentoProducao)
class ApontamentoProducaoAdmin(admin.ModelAdmin):
    list_display = [
        'op',
        'qtd_perda',
        'qtd_prod',
        'apontado_em',
        'encerrado',
    ]
