import json

from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from django.core.cache import cache
from django.test import Client, RequestFactory, TestCase
from django.urls import reverse

from core.models import ConfigMapa, Local
from core.views import MAX_TENTATIVAS, _chave_cache_ip, _imagens_padrao


# ────────────────────────────────────────────────────────────────
# Helpers internos
# ────────────────────────────────────────────────────────────────

class ChaveCacheIPTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()

    def test_usa_x_forwarded_for(self):
        req = self.rf.get('/')
        req.META['HTTP_X_FORWARDED_FOR'] = '1.2.3.4, 5.6.7.8'
        self.assertEqual(_chave_cache_ip(req), 'login_falhas_1.2.3.4')

    def test_usa_apenas_primeiro_ip_do_x_forwarded_for(self):
        req = self.rf.get('/')
        req.META['HTTP_X_FORWARDED_FOR'] = '10.0.0.1, 10.0.0.2, 10.0.0.3'
        self.assertEqual(_chave_cache_ip(req), 'login_falhas_10.0.0.1')

    def test_usa_remote_addr_quando_sem_forwarded(self):
        req = self.rf.get('/')
        req.META.pop('HTTP_X_FORWARDED_FOR', None)
        req.META['REMOTE_ADDR'] = '9.8.7.6'
        self.assertEqual(_chave_cache_ip(req), 'login_falhas_9.8.7.6')

    def test_prefixo_da_chave(self):
        req = self.rf.get('/')
        req.META['REMOTE_ADDR'] = '1.1.1.1'
        self.assertTrue(_chave_cache_ip(req).startswith('login_falhas_'))


class ImagensPadraoTests(TestCase):
    def test_retorna_lista(self):
        self.assertIsInstance(_imagens_padrao('forte'), list)

    def test_lista_nao_vazia(self):
        self.assertGreater(len(_imagens_padrao('forte')), 0)

    def test_todas_categorias_conhecidas(self):
        for cat in ('forte', 'ruina', 'museu', 'igreja', 'marco', 'casarao'):
            with self.subTest(categoria=cat):
                resultado = _imagens_padrao(cat)
                self.assertIsInstance(resultado, list)
                self.assertGreater(len(resultado), 0)

    def test_categoria_desconhecida_retorna_padrao(self):
        resultado = _imagens_padrao('categoria_inexistente')
        self.assertIsInstance(resultado, list)
        self.assertGreater(len(resultado), 0)


# ────────────────────────────────────────────────────────────────
# APIs públicas
# ────────────────────────────────────────────────────────────────

class ApiLocaisTests(TestCase):
    def setUp(self):
        self.client = Client()
        Local.objects.create(
            nome='Local Ativo', categoria='museu', lat=-27.1, lng=-52.6,
            cidade='Chapecó', uf='SC', resumo='R', descricao='D',
            endereco='E', periodo='P', ativo=True,
        )
        Local.objects.create(
            nome='Local Inativo', categoria='forte', lat=-27.2, lng=-52.7,
            cidade='Chapecó', uf='SC', resumo='R', descricao='D',
            endereco='E', periodo='P', ativo=False,
        )

    def test_status_200(self):
        response = self.client.get(reverse('api_locais'))
        self.assertEqual(response.status_code, 200)

    def test_content_type_json(self):
        response = self.client.get(reverse('api_locais'))
        self.assertIn('application/json', response['Content-Type'])

    def test_retorna_apenas_locais_ativos(self):
        response = self.client.get(reverse('api_locais'))
        dados = json.loads(response.content)
        self.assertEqual(len(dados), 1)
        self.assertEqual(dados[0]['nome'], 'Local Ativo')

    def test_estrutura_do_json(self):
        response = self.client.get(reverse('api_locais'))
        dados = json.loads(response.content)
        campos_esperados = {
            'id', 'nome', 'categoria', 'lat', 'lng',
            'cidade', 'uf', 'resumo', 'descricao',
            'endereco', 'periodo', 'imagens',
        }
        self.assertEqual(set(dados[0].keys()), campos_esperados)

    def test_sem_locais_retorna_lista_vazia(self):
        Local.objects.all().delete()
        response = self.client.get(reverse('api_locais'))
        dados = json.loads(response.content)
        self.assertEqual(dados, [])


class ApiConfigMapaTests(TestCase):
    def test_status_200(self):
        response = self.client.get(reverse('api_config_mapa'))
        self.assertEqual(response.status_code, 200)

    def test_estrutura_da_resposta(self):
        response = self.client.get(reverse('api_config_mapa'))
        dados = json.loads(response.content)
        self.assertIn('restricao', dados)
        self.assertIn('centro', dados)
        self.assertIn('zoom_inicial', dados)
        self.assertIn('zoom_minimo', dados)
        self.assertIn('poligono', dados)

    def test_cria_config_automaticamente(self):
        self.assertEqual(ConfigMapa.objects.count(), 0)
        self.client.get(reverse('api_config_mapa'))
        self.assertEqual(ConfigMapa.objects.count(), 1)


# ────────────────────────────────────────────────────────────────
# Controle de acesso (staff_required)
# ────────────────────────────────────────────────────────────────

class StaffRequiredTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.staff = User.objects.create_user('staff', password='pass', is_staff=True)
        self.comum = User.objects.create_user('comum', password='pass', is_staff=False)

    def test_anonimo_e_redirecionado(self):
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_usuario_sem_staff_e_redirecionado(self):
        self.client.login(username='comum', password='pass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_staff_acessa_dashboard(self):
        self.client.login(username='staff', password='pass')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)


# ────────────────────────────────────────────────────────────────
# Login e rate limiting
# ────────────────────────────────────────────────────────────────

class AdminLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        User.objects.create_user('admin', password='senha123', is_staff=True)
        cache.clear()

    def tearDown(self):
        cache.clear()

    def test_get_retorna_formulario(self):
        response = self.client.get(reverse('admin_login'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('form', response.context)

    def test_login_valido_redireciona(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin', 'password': 'senha123',
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('admin_dashboard'))

    def test_login_invalido_nao_redireciona(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin', 'password': 'errada',
        })
        self.assertEqual(response.status_code, 200)

    def test_login_invalido_exibe_mensagem_de_erro(self):
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin', 'password': 'errada',
        })
        msgs = [str(m) for m in get_messages(response.wsgi_request)]
        self.assertTrue(any('incorretos' in m for m in msgs))

    def test_tentativas_invalidas_acumulam(self):
        for _ in range(3):
            self.client.post(reverse('admin_login'), {
                'username': 'admin', 'password': 'errada',
            })
        # A próxima tentativa válida ainda deve funcionar (não bloqueado ainda)
        response = self.client.post(reverse('admin_login'), {
            'username': 'admin', 'password': 'senha123',
        })
        self.assertEqual(response.status_code, 302)

    def test_bloqueio_apos_max_tentativas(self):
        for _ in range(MAX_TENTATIVAS):
            self.client.post(reverse('admin_login'), {
                'username': 'admin', 'password': 'errada',
            })
        response = self.client.get(reverse('admin_login'))
        self.assertTrue(response.context['bloqueado'])

    def test_login_valido_limpa_contador_de_tentativas(self):
        # Faz algumas tentativas inválidas
        for _ in range(MAX_TENTATIVAS - 1):
            self.client.post(reverse('admin_login'), {
                'username': 'admin', 'password': 'errada',
            })
        # Login válido
        self.client.post(reverse('admin_login'), {
            'username': 'admin', 'password': 'senha123',
        })
        self.client.logout()
        # Após o logout, a conta não deve estar bloqueada
        response = self.client.get(reverse('admin_login'))
        self.assertFalse(response.context['bloqueado'])

    def test_staff_ja_autenticado_vai_ao_dashboard(self):
        self.client.login(username='admin', password='senha123')
        response = self.client.get(reverse('admin_login'))
        self.assertRedirects(response, reverse('admin_dashboard'))
