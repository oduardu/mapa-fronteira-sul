from django.test import TestCase

from core.models import ConfigMapa, Local
from core.polygon import FRONTEIRA_SUL_POLYGON


class LocalStrTests(TestCase):
    def test_str_formato(self):
        local = Local(nome='Forte Coimbra', cidade='Corumbá', uf='MS')
        self.assertEqual(str(local), 'Forte Coimbra (Corumbá/MS)')


class ConfigMapaStrTests(TestCase):
    def test_str(self):
        config = ConfigMapa()
        self.assertEqual(str(config), 'Configuração do mapa')


class ConfigMapaGetConfigTests(TestCase):
    def test_cria_registro_se_nao_existir(self):
        self.assertEqual(ConfigMapa.objects.count(), 0)
        ConfigMapa.get_config()
        self.assertEqual(ConfigMapa.objects.count(), 1)

    def test_retorna_pk_1(self):
        config = ConfigMapa.get_config()
        self.assertEqual(config.pk, 1)

    def test_nao_duplica_chamadas_repetidas(self):
        ConfigMapa.get_config()
        ConfigMapa.get_config()
        self.assertEqual(ConfigMapa.objects.count(), 1)

    def test_retorna_instancia_existente(self):
        ConfigMapa.objects.create(pk=1, zoom_inicial=9)
        config = ConfigMapa.get_config()
        self.assertEqual(config.zoom_inicial, 9)

    def test_preenche_poligono_padrao_ao_criar(self):
        config = ConfigMapa.get_config()
        esperado = [{'lat': p[0], 'lng': p[1]} for p in FRONTEIRA_SUL_POLYGON]
        self.assertEqual(config.poligono, esperado)


class ConfigMapaAsDictTests(TestCase):
    def setUp(self):
        self.config = ConfigMapa(
            restricao_norte=-22.5,
            restricao_sul=-33.8,
            restricao_leste=-48.0,
            restricao_oeste=-57.7,
            centro_lat=-27.0,
            centro_lng=-52.0,
            zoom_inicial=7,
            zoom_minimo=6,
            poligono=[],
        )

    def test_chaves_presentes(self):
        d = self.config.as_dict()
        self.assertIn('restricao', d)
        self.assertIn('centro', d)
        self.assertIn('zoom_inicial', d)
        self.assertIn('zoom_minimo', d)
        self.assertIn('poligono', d)

    def test_subchaves_restricao(self):
        restricao = self.config.as_dict()['restricao']
        self.assertIn('norte', restricao)
        self.assertIn('sul', restricao)
        self.assertIn('leste', restricao)
        self.assertIn('oeste', restricao)

    def test_valores_restricao(self):
        restricao = self.config.as_dict()['restricao']
        self.assertEqual(restricao['norte'], -22.5)
        self.assertEqual(restricao['sul'], -33.8)
        self.assertEqual(restricao['leste'], -48.0)
        self.assertEqual(restricao['oeste'], -57.7)

    def test_valores_centro(self):
        centro = self.config.as_dict()['centro']
        self.assertEqual(centro['lat'], -27.0)
        self.assertEqual(centro['lng'], -52.0)

    def test_valores_zoom(self):
        d = self.config.as_dict()
        self.assertEqual(d['zoom_inicial'], 7)
        self.assertEqual(d['zoom_minimo'], 6)
