from django.test import SimpleTestCase, TestCase

from core.polygon import (
    FRONTEIRA_SUL_POLYGON,
    get_poligono_ativo,
    ponto_dentro_fronteira,
)

# Quadrado simples usado para testar o algoritmo de forma isolada,
# sem depender do polígono hardcoded da Fronteira Sul.
# Cobre: lat de -30 a -25, lng de -55 a -50.
_QUADRADO = [(-30, -55), (-30, -50), (-25, -50), (-25, -55)]


class PontoDentroFronteiraTests(SimpleTestCase):
    """Testa o algoritmo ray-casting com um polígono explícito."""

    def test_ponto_claramente_dentro(self):
        self.assertTrue(ponto_dentro_fronteira(-27, -52, polygon=_QUADRADO))

    def test_ponto_claramente_fora(self):
        self.assertFalse(ponto_dentro_fronteira(-20, -45, polygon=_QUADRADO))

    def test_ponto_ao_norte_do_poligono(self):
        self.assertFalse(ponto_dentro_fronteira(-24, -52, polygon=_QUADRADO))

    def test_ponto_ao_sul_do_poligono(self):
        self.assertFalse(ponto_dentro_fronteira(-31, -52, polygon=_QUADRADO))

    def test_ponto_a_leste_do_poligono(self):
        self.assertFalse(ponto_dentro_fronteira(-27, -49, polygon=_QUADRADO))

    def test_ponto_a_oeste_do_poligono(self):
        self.assertFalse(ponto_dentro_fronteira(-27, -56, polygon=_QUADRADO))

    def test_retorna_bool(self):
        resultado = ponto_dentro_fronteira(-27, -52, polygon=_QUADRADO)
        self.assertIsInstance(resultado, bool)

    # Testes com o polígono real da Fronteira Sul
    def test_chapeco_sc_dentro(self):
        """Chapecó (SC) fica dentro da Fronteira Sul."""
        self.assertTrue(ponto_dentro_fronteira(-27.1, -52.6))

    def test_sao_paulo_fora(self):
        """São Paulo está fora da Fronteira Sul."""
        self.assertFalse(ponto_dentro_fronteira(-23.5, -46.6))

    def test_florianopolis_fora(self):
        """Florianópolis está fora da Fronteira Sul (muito a leste)."""
        self.assertFalse(ponto_dentro_fronteira(-27.6, -48.5))


class GetPoligonoAtivoTests(TestCase):
    """Testa a seleção do polígono ativo (banco vs. padrão)."""

    def test_sem_config_retorna_padrao(self):
        resultado = get_poligono_ativo()
        self.assertEqual(resultado, FRONTEIRA_SUL_POLYGON)

    def test_config_com_poligono_vazio_retorna_padrao(self):
        from core.models import ConfigMapa
        ConfigMapa.objects.create(pk=1, poligono=[])
        resultado = get_poligono_ativo()
        self.assertEqual(resultado, FRONTEIRA_SUL_POLYGON)

    def test_config_com_poligono_retorna_do_banco(self):
        from core.models import ConfigMapa
        poli = [{'lat': -27.0, 'lng': -52.0}, {'lat': -28.0, 'lng': -53.0}]
        ConfigMapa.objects.create(pk=1, poligono=poli)
        resultado = get_poligono_ativo()
        self.assertEqual(resultado, [(-27.0, -52.0), (-28.0, -53.0)])
