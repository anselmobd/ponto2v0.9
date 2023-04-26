from django.contrib import admin

from .models import *


# @admin.register(Empresa)
# class EmpresaAdmin(admin.ModelAdmin):
#     search_fields = ['nome']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['cnpj', 'nome']
    list_display_links = ['cnpj']
    search_fields = ['cnpj', 'nome']


@admin.register(DificuldadeBordado)
class DificuldadeBordadoAdmin(admin.ModelAdmin):
    list_display = ['ordem', 'descricao']
    list_display_links = ['descricao']
    search_fields = ['ordem', 'descricao']


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
