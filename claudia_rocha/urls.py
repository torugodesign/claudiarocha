from django.urls import path, include, reverse_lazy
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from core import views as core_views
from core.sitemaps import StaticViewSitemap, ArtigoSitemap

sitemaps = {
    'estatico': StaticViewSitemap,
    'artigos':  ArtigoSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    path('robots.txt', core_views.robots_txt, name='robots_txt'),

    path('blog/', include('blog.urls')),

    # Autenticação do painel
    path('painel/login/',  core_views.painel_login,  name='painel_login'),
    path('painel/logout/', core_views.painel_logout, name='painel_logout'),

    # Recuperação de senha do painel
    path(
        'painel/senha/recuperar/',
        auth_views.PasswordResetView.as_view(
            template_name='painel/senha_recuperar.html',
            email_template_name='painel/senha_email.txt',
            subject_template_name='painel/senha_email_assunto.txt',
            success_url=reverse_lazy('painel_senha_recuperar_enviado'),
        ),
        name='painel_senha_recuperar',
    ),
    path(
        'painel/senha/recuperar/enviado/',
        auth_views.PasswordResetDoneView.as_view(template_name='painel/senha_enviado.html'),
        name='painel_senha_recuperar_enviado',
    ),
    path(
        'painel/senha/redefinir/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='painel/senha_redefinir.html',
            success_url=reverse_lazy('painel_senha_redefinir_completo'),
        ),
        name='painel_senha_redefinir',
    ),
    path(
        'painel/senha/redefinir/completo/',
        auth_views.PasswordResetCompleteView.as_view(template_name='painel/senha_completo.html'),
        name='painel_senha_redefinir_completo',
    ),

    # Painel customizado
    path('painel/',                              core_views.painel_dashboard,       name='painel_dashboard'),
    path('painel/artigos/',                      core_views.painel_artigos,         name='painel_artigos'),
    path('painel/artigos/novo/',                 core_views.painel_artigo_novo,     name='painel_artigo_novo'),
    path('painel/artigos/<int:pk>/editar/',      core_views.painel_artigo_editar,   name='painel_artigo_editar'),
    path('painel/artigos/<int:pk>/publicar/',    core_views.painel_artigo_publicar, name='painel_artigo_publicar'),
    path('painel/artigos/<int:pk>/deletar/',     core_views.painel_artigo_deletar,  name='painel_artigo_deletar'),

    # Conteúdo do site
    path('painel/conteudo/',           core_views.painel_conteudo,        name='painel_conteudo'),
    path('painel/conteudo/<str:secao>/', core_views.painel_conteudo_secao, name='painel_conteudo_secao'),

    path('', core_views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
