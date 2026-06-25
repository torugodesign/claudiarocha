from django.db import models


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
    imagem = models.ImageField('Imagem', upload_to='site/', blank=True)
    video  = models.FileField('Vídeo', upload_to='site/videos/', blank=True)

    class Meta:
        verbose_name = 'Conteúdo do Site'
        verbose_name_plural = 'Conteúdos do Site'
        ordering = ['secao', 'chave']

    def __str__(self):
        return f'{self.get_secao_display()} — {self.chave}'
