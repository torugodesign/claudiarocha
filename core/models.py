from django.db import models


class ConteudoSite(models.Model):
    """Textos e imagens editáveis pelo painel — sem precisar mexer no código."""
    SECAO_CHOICES = [
        ('hero',          'Hero'),
        ('sobre',         'Sobre'),
        ('atuacao',       'Atuação'),
        ('diferenciais',  'Diferenciais'),
        ('contato',       'Contato'),
    ]
    secao   = models.CharField('Seção', max_length=20, choices=SECAO_CHOICES)
    chave   = models.CharField('Chave', max_length=100, unique=True,
                               help_text='Identificador interno (ex: hero_titulo)')
    titulo  = models.CharField('Título / texto curto', max_length=500, blank=True)
    texto   = models.TextField('Texto longo', blank=True)
    imagem  = models.ImageField('Imagem', upload_to='site/', blank=True)

    class Meta:
        verbose_name = 'Conteúdo do Site'
        verbose_name_plural = 'Conteúdos do Site'
        ordering = ['secao', 'chave']

    def __str__(self):
        return f'{self.get_secao_display()} — {self.chave}'
