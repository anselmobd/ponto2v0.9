from django.contrib import admin

from .models import *


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    search_fields = ["nome"]


admin.site.register(Cliente)
