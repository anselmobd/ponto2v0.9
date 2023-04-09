from django.contrib import admin

from .models import *


# @admin.register(Empresa)
# class EmpresaAdmin(admin.ModelAdmin):
#     search_fields = ['nome']


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nome']
    list_display_links = ['nome']
    search_fields = ['nome']


@admin.register(DificuldadeBordado)
class DificuldadeBordadoAdmin(admin.ModelAdmin):
    list_display = ['ordem', 'descricao']
    list_display_links = ['descricao']
    search_fields = ['ordem', 'descricao']


@admin.register(Bordado)
class BordadoAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'nome']
    list_display_links = ['nome']
    search_fields = ['cliente', 'nome']
