
from django.db import models
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
# Create your models here.


class Produto(models.Model):
    nome = models.CharField(max_length=75)
    descricao_curta = models.TextField(
        verbose_name='Descricao Curta', max_length=150)
    descricao_longa = models.TextField(verbose_name='Descricao Longa')
    image = models.ImageField(
        upload_to='produto_img/%Y,%m/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    preco_marketing = models.FloatField(verbose_name='Preço')
    preco_marketing_promocional = models.FloatField(
        default=0, verbose_name='Preço promo')
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variavel'),
            ('S', 'Simples'),
        )
    )

    def preco(self):
        return f'R$ {self.preco_marketing:.2f}'.replace('.', ',')

    def preco_promo(self):
        return f'R$ {self.preco_marketing_promocional:.2f}'.replace('.', ',')

    def resize_image(self, img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_heigth = img_pil.size

        if original_width >= new_width:
            new_heigth = round((new_width * original_heigth) / original_width)
            new_img = img_pil.resize((new_width, new_heigth), Image.LANCZOS)
            new_img.save(
                img_full_path,
                optimize=True,
                quality=50
            )
            return new_img
        else:
            return img_pil.close()

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.nome)}'
            self.slug = slug

        super().save(*args, **kwargs)
        max_img_size = 800
        if self.image:
            self.resize_image(self.image, max_img_size)

    def __str__(self) -> str:
        return self.nome


class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(max_length=75, blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.IntegerField(default=1)

    def __str__(self) -> str:
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
