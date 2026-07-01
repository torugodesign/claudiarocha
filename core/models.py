import uuid
import os
from django.db import models


def _upload_imagem(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'site/{uuid.uuid4().hex}{ext}'


def _upload_video(instance, filename):
    ext = os.path.splitext(filename)[1].lower()
    return f'site/videos/{uuid.uuid4().hex}{ext}'


class ConteudoSite(models.Model):
    """Textos, imagens e vídeo editáveis pelo painel."""
    SECAO_CHOICES = [
        ('hero',          'Hero'),
        ('sobre',         'Sobre'),
        ('atuacao',       'Atuação'),
        ('diferenciais',  'Diferenciais'),
        ('contato',       'Contato'),
    ]
    secao  = models.CharField('Seção', max_length=20, choices=SECAO_CHOICES)
    chave  = models.CharField('Chave', max_length=100, unique=True)
    titulo = models.CharField('Texto curto', max_length=500, blank=True)
    texto  = models.TextField('Texto longo', blank=True)
    imagem = models.ImageField('Imagem', upload_to=_upload_imagem, blank=True)
    video  = models.FileField('Vídeo', upload_to=_upload_video, blank=True, max_length=255)

    class Meta:
        verbose_name = 'Conteúdo do Site'
        verbose_name_plural = 'Conteúdos do Site'
        ordering = ['secao', 'chave']

    def __str__(self):
        return f'{self.get_secao_display()} — {self.chave}'
