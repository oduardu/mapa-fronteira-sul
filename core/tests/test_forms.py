from django.test import TestCase

from core.forms import LocalForm

_DADOS_VALIDOS = {
    'nome': 'Museu do Contestado',
    'categoria': 'museu',
    'lat': -27.1,
    'lng': -52.6,   # Chapecó, SC — dentro da Fronteira Sul
    'cidade': 'Chapecó',
    'uf': 'SC',
    'resumo': 'Um museu sobre a Guerra do Contestado.',
    'descricao': 'Descrição detalhada do museu.',
    'endereco': 'Av. Getúlio Vargas, 100',
    'periodo': 'Início do século XX',
    'ativo': True,
}


class LocalFormValidacaoGeograficaTests(TestCase):
    def test_coordenadas_dentro_da_regiao_sao_validas(self):
        form = LocalForm(data=_DADOS_VALIDOS)
        self.assertTrue(form.is_valid(), form.errors)

    def test_coordenadas_fora_da_regiao_invalidam_formulario(self):
        dados = {**_DADOS_VALIDOS, 'lat': -23.5, 'lng': -46.6}  # São Paulo
        form = LocalForm(data=dados)
        self.assertFalse(form.is_valid())

    def test_mensagem_de_erro_menciona_fronteira_sul(self):
        dados = {**_DADOS_VALIDOS, 'lat': -23.5, 'lng': -46.6}
        form = LocalForm(data=dados)
        form.is_valid()
        erros_gerais = form.errors.get('__all__', [])
        self.assertTrue(
            any('Fronteira Sul' in e for e in erros_gerais),
            f'Esperava "Fronteira Sul" nos erros, mas obteve: {erros_gerais}',
        )

    def test_sem_lat_lng_nao_levanta_erro_de_poligono(self):
        """Sem coordenadas, o clean() não deve checar o polígono."""
        dados = {k: v for k, v in _DADOS_VALIDOS.items() if k not in ('lat', 'lng')}
        form = LocalForm(data=dados)
        self.assertFalse(form.is_valid())
        # Campos obrigatórios ausentes, mas sem erro de polígono
        self.assertNotIn('__all__', form.errors)
        self.assertIn('lat', form.errors)
        self.assertIn('lng', form.errors)


class LocalFormCamposTests(TestCase):
    def test_campos_do_formulario(self):
        form = LocalForm()
        campos_esperados = {
            'nome', 'categoria', 'lat', 'lng',
            'cidade', 'uf', 'resumo', 'descricao',
            'endereco', 'periodo', 'ativo',
        }
        self.assertEqual(set(form.fields.keys()), campos_esperados)

    def test_imagens_nao_e_campo_do_formulario(self):
        """Imagens são preenchidas automaticamente pela view, não pelo form."""
        form = LocalForm()
        self.assertNotIn('imagens', form.fields)
