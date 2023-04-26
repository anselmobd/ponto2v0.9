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
        'cancelado',
    ]
    list_filter = [
        'cliente',
    ]
    fields = [
        'numero',
        'inserido_em',
        'cliente',
        'cancelado',
    ]
    readonly_fields = [
        'numero',
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
        'cliente',
        'bordado',
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
    ]
