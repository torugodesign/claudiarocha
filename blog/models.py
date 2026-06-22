from django.db import models
from django.utils.text import slugify


class Artigo(models.Model):
    titulo        = models.CharField('Título', max_length=300)
    slug          = models.SlugField(unique=True, blank=True, max_length=320)
    resumo        = models.TextField('Resumo', help_text='Aparece na listagem do blog')
    conteudo      = models.TextField('Conteúdo')
    imagem_capa   = models.ImageField('Imagem de capa', upload_to='blog/', blank=True)
    publicado     = models.BooleanField('Publicado', default=False)
    criado_em     = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Artigo'
        verbose_name_plural = 'Artigos'
        ordering = ['-criado_em']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
