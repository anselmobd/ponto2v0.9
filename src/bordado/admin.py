from django.contrib import admin

from .models import *


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ["nome"]


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ["empresa", "nome"]
    list_display_links = ["nome"]
    search_fields = ["empresa", "nome"]
