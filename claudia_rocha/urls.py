from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views

urlpatterns = [
    path('blog/', include('blog.urls')),

    # Autenticação do painel
    path('painel/login/',  core_views.painel_login,  name='painel_login'),
    path('painel/logout/', core_views.painel_logout, name='painel_logout'),

    # Painel customizado
    path('painel/',                              core_views.painel_dashboard,       name='painel_dashboard'),
    path('painel/artigos/',                      core_views.painel_artigos,         name='painel_artigos'),
    path('painel/artigos/novo/',                 core_views.painel_artigo_novo,     name='painel_artigo_novo'),
    path('painel/artigos/<int:pk>/editar/',      core_views.painel_artigo_editar,   name='painel_artigo_editar'),
    path('painel/artigos/<int:pk>/publicar/',    core_views.painel_artigo_publicar, name='painel_artigo_publicar'),
    path('painel/artigos/<int:pk>/deletar/',     core_views.painel_artigo_deletar,  name='painel_artigo_deletar'),

    path('', core_views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
