from django.contrib import admin
from .models import ConteudoSite


@admin.register(ConteudoSite)
class ConteudoSiteAdmin(admin.ModelAdmin):
    list_display  = ('secao', 'chave', 'titulo')
    list_filter   = ('secao',)
    search_fields = ('chave', 'titulo', 'texto')
