from django.db import models


class ConfigMapa(models.Model):
    restricao_norte = models.FloatField('Limite Norte', default=-22.5)
    restricao_sul   = models.FloatField('Limite Sul',   default=-33.8)
    restricao_leste = models.FloatField('Limite Leste', default=-48.0)
    restricao_oeste = models.FloatField('Limite Oeste', default=-57.7)
    centro_lat   = models.FloatField('Centro Lat',    default=-27.0)
    centro_lng   = models.FloatField('Centro Lng',    default=-52.0)
    zoom_inicial = models.IntegerField('Zoom inicial', default=7)
    zoom_minimo  = models.IntegerField('Zoom mínimo',  default=6)
    poligono     = models.JSONField('Polígono da região', default=list)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuração do Mapa'

    def __str__(self):
        return 'Configuração do mapa'

    @classmethod
    def get_config(cls):
        from .polygon import FRONTEIRA_SUL_POLYGON
        config, _ = cls.objects.get_or_create(
            pk=1,
            defaults={
                'poligono': [{'lat': p[0], 'lng': p[1]} for p in FRONTEIRA_SUL_POLYGON],
            },
        )
        return config

    def as_dict(self):
        return {
            'restricao': {
                'norte': self.restricao_norte,
                'sul':   self.restricao_sul,
                'leste': self.restricao_leste,
                'oeste': self.restricao_oeste,
            },
            'centro': {'lat': self.centro_lat, 'lng': self.centro_lng},
            'zoom_inicial': self.zoom_inicial,
            'zoom_minimo':  self.zoom_minimo,
            'poligono': self.poligono,
        }


class Local(models.Model):
    CATEGORIAS = [
        ('forte', 'Forte'),
        ('ruina', 'Ruína'),
        ('museu', 'Museu'),
        ('igreja', 'Igreja'),
        ('marco', 'Marco histórico'),
        ('casarao', 'Casarão'),
    ]

    nome = models.CharField('Nome', max_length=200)
    categoria = models.CharField('Categoria', max_length=50, choices=CATEGORIAS)
    lat = models.FloatField('Latitude')
    lng = models.FloatField('Longitude')
    cidade = models.CharField('Cidade', max_length=100)
    uf = models.CharField('UF', max_length=2)
    resumo = models.TextField('Resumo')
    descricao = models.TextField('Descrição')
    endereco = models.CharField('Endereço', max_length=300)
    periodo = models.CharField('Período histórico', max_length=100)
    imagens = models.JSONField('Imagens (cores)', default=list, blank=True)
    ativo = models.BooleanField('Ativo', default=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nome']
        verbose_name = 'Local'
        verbose_name_plural = 'Locais'

    def __str__(self):
        return f"{self.nome} ({self.cidade}/{self.uf})"
