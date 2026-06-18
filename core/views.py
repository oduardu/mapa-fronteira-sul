import json
from functools import wraps

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from .forms import LoginForm, LocalForm
from .models import Local
from .polygon import FRONTEIRA_SUL_POLYGON


# ────────────────────────────────────────────────────────────────
# Helpers de autenticação
# ────────────────────────────────────────────────────────────────

MAX_TENTATIVAS = 5
BLOQUEIO_SEGUNDOS = 300  # 5 minutos


def _chave_cache_ip(request):
    ip = (
        request.META.get('HTTP_X_FORWARDED_FOR', '')
        .split(',')[0]
        .strip()
        or request.META.get('REMOTE_ADDR', 'unknown')
    )
    return f'login_falhas_{ip}'


def staff_required(view_func):
    """Acesso restrito a usuários com is_staff=True."""
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(f'/admin/login/?next={request.path}')
        if not request.user.is_staff:
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ────────────────────────────────────────────────────────────────
# Views públicas
# ────────────────────────────────────────────────────────────────

def index(request):
    return render(request, 'core/index.html', {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })


def api_locais(request):
    locais = list(
        Local.objects.filter(ativo=True).values(
            'id', 'nome', 'categoria', 'lat', 'lng',
            'cidade', 'uf', 'resumo', 'descricao',
            'endereco', 'periodo', 'imagens',
        )
    )
    return JsonResponse(locais, safe=False)


def api_config_mapa(request):
    from .models import ConfigMapa
    return JsonResponse(ConfigMapa.get_config().as_dict())


# ────────────────────────────────────────────────────────────────
# Views de autenticação
# ────────────────────────────────────────────────────────────────

@require_http_methods(['GET', 'POST'])
def admin_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin_dashboard')

    chave = _chave_cache_ip(request)
    tentativas = cache.get(chave, 0)

    if tentativas >= MAX_TENTATIVAS:
        return render(request, 'core/login.html', {
            'form': LoginForm(),
            'bloqueado': True,
            'minutos': BLOQUEIO_SEGUNDOS // 60,
        })

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            cache.delete(chave)
            login(request, form.get_user())
            return redirect(request.GET.get('next') or 'admin_dashboard')
        cache.set(chave, tentativas + 1, BLOQUEIO_SEGUNDOS)
        messages.error(request, 'Usuário ou senha incorretos.')
    else:
        form = LoginForm()

    return render(request, 'core/login.html', {'form': form, 'bloqueado': False})


@require_http_methods(['POST'])
def admin_logout(request):
    logout(request)
    return redirect('admin_login')


# ────────────────────────────────────────────────────────────────
# Views administrativas (staff only)
# ────────────────────────────────────────────────────────────────

@staff_required
def admin_dashboard(request):
    locais = Local.objects.all().order_by('nome')
    return render(request, 'core/admin_dashboard.html', {'locais': locais})


def _ctx_mapa(form):
    from .models import ConfigMapa
    config = ConfigMapa.get_config()
    return {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'poligono_json': json.dumps(config.poligono),
    }


@staff_required
def admin_local_novo(request):
    if request.method == 'POST':
        form = LocalForm(request.POST)
        if form.is_valid():
            local = form.save(commit=False)
            if not local.imagens:
                local.imagens = _imagens_padrao(local.categoria)
            local.save()
            messages.success(request, f'Local "{local.nome}" criado com sucesso.')
            return redirect('admin_dashboard')
    else:
        form = LocalForm()

    return render(request, 'core/admin_local_form.html', {
        'form': form,
        'titulo': 'Novo local',
        **_ctx_mapa(form),
    })


@staff_required
def admin_local_editar(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == 'POST':
        form = LocalForm(request.POST, instance=local)
        if form.is_valid():
            obj = form.save(commit=False)
            if not obj.imagens:
                obj.imagens = _imagens_padrao(obj.categoria)
            obj.save()
            messages.success(request, f'Local "{obj.nome}" atualizado.')
            return redirect('admin_dashboard')
    else:
        form = LocalForm(instance=local)

    return render(request, 'core/admin_local_form.html', {
        'form': form,
        'local': local,
        'titulo': f'Editar — {local.nome}',
        **_ctx_mapa(form),
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def admin_config_mapa(request):
    from .models import ConfigMapa
    config = ConfigMapa.get_config()

    if request.method == 'POST':
        try:
            config.restricao_norte = float(request.POST['restricao_norte'])
            config.restricao_sul   = float(request.POST['restricao_sul'])
            config.restricao_leste = float(request.POST['restricao_leste'])
            config.restricao_oeste = float(request.POST['restricao_oeste'])
            config.centro_lat   = float(request.POST['centro_lat'])
            config.centro_lng   = float(request.POST['centro_lng'])
            config.zoom_inicial = int(request.POST['zoom_inicial'])
            config.zoom_minimo  = int(request.POST['zoom_minimo'])
            poligono_raw = request.POST.get('poligono', '')
            if poligono_raw:
                config.poligono = json.loads(poligono_raw)
            config.save()
            messages.success(request, 'Configuração do mapa salva.')
        except (KeyError, ValueError, json.JSONDecodeError) as e:
            messages.error(request, f'Erro ao salvar: {e}')
        return redirect('admin_config_mapa')

    return render(request, 'core/admin_config_mapa.html', {
        'config': config,
        'config_json': json.dumps(config.as_dict()),
        'poligono_json': json.dumps(config.poligono),
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
    })


@staff_required
@require_http_methods(['GET', 'POST'])
def admin_local_excluir(request, pk):
    local = get_object_or_404(Local, pk=pk)
    if request.method == 'POST':
        nome = local.nome
        local.delete()
        messages.success(request, f'Local "{nome}" excluído.')
        return redirect('admin_dashboard')
    return render(request, 'core/admin_confirmar_exclusao.html', {'local': local})


# ────────────────────────────────────────────────────────────────
# Páginas de erro
# ────────────────────────────────────────────────────────────────

def simular_erro_500(request):
    """Renderiza a página de 500 diretamente para facilitar testes visuais."""
    return render(request, '500.html', status=500)


# ────────────────────────────────────────────────────────────────
# Utilitário interno
# ────────────────────────────────────────────────────────────────

def _imagens_padrao(categoria):
    paletas = {
        'forte':   [["#1f3a5f", "#0b2545"], ["#2c4a6e", "#143872"], ["#3d5a7d", "#1f4a8f"]],
        'ruina':   [["#7a3520", "#3a1a0e"], ["#9a5034", "#5a2a18"], ["#b06a4a", "#7a3520"]],
        'museu':   [["#3a4a3c", "#1a2a1e"], ["#5a6a5c", "#3a4a3c"], ["#7a8a7c", "#5a6a5c"]],
        'igreja':  [["#5a4a3a", "#2a1a0e"], ["#7a6a5a", "#4a3a2a"], ["#9a8a7a", "#6a5a4a"]],
        'marco':   [["#2d6a4f", "#0f3825"], ["#52b788", "#2d6a4f"], ["#74c69d", "#52b788"]],
        'casarao': [["#8a4a2a", "#4a2a1a"], ["#a06a4a", "#6a3a2a"], ["#c08a6a", "#8a5a3a"]],
    }
    return paletas.get(categoria, [["#1a2040", "#2d3a6e"], ["#243044", "#1f4060"]])
