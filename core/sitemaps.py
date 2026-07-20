from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Artigo


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'weekly'

    def items(self):
        return ['home', 'blog:lista']

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        ultimo = Artigo.objects.filter(publicado=True).order_by('-atualizado_em').first()
        return ultimo.atualizado_em if ultimo else None


class ArtigoSitemap(Sitemap):
    priority = 0.7
    changefreq = 'monthly'

    def items(self):
        return Artigo.objects.filter(publicado=True)

    def lastmod(self, obj):
        return obj.atualizado_em

    def location(self, obj):
        return reverse('blog:detalhe', args=[obj.slug])
