from django.contrib import admin
from .models import Artigo


@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    list_display  = ('titulo', 'publicado', 'criado_em')
    list_filter   = ('publicado',)
    search_fields = ('titulo', 'resumo', 'conteudo')
    prepopulated_fields = {'slug': ('titulo',)}
    list_editable = ('publicado',)
    fieldsets = (
        ('Conteúdo', {'fields': ('titulo', 'slug', 'resumo', 'conteudo', 'imagem_capa')}),
        ('Publicação', {'fields': ('publicado',)}),
    )
