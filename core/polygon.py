# Contorno aproximado da Mesorregião Grande Fronteira do Mercosul
# Cobre: sudoeste do PR, oeste de SC, noroeste do RS
FRONTEIRA_SUL_POLYGON = [
    (-25.05, -54.60),
    (-25.05, -53.50),
    (-25.10, -52.40),
    (-25.30, -51.50),
    (-25.50, -50.80),
    (-26.00, -50.30),
    (-26.50, -49.80),
    (-27.00, -49.60),
    (-27.50, -49.50),
    (-28.00, -49.70),
    (-28.50, -50.20),
    (-29.00, -50.80),
    (-29.30, -51.20),
    (-29.40, -51.80),
    (-29.30, -52.50),
    (-29.10, -53.30),
    (-28.80, -54.00),
    (-28.70, -54.80),
    (-28.50, -55.40),
    (-28.10, -55.60),
    (-27.60, -55.50),
    (-27.10, -55.30),
    (-26.50, -54.90),
    (-25.80, -54.80),
    (-25.40, -54.70),
    (-25.05, -54.60),
]


def get_poligono_ativo():
    """Retorna o polígono do banco (ConfigMapa) ou o padrão hardcoded."""
    try:
        from core.models import ConfigMapa
        config = ConfigMapa.objects.filter(pk=1).first()
        if config and config.poligono:
            return [(p['lat'], p['lng']) for p in config.poligono]
    except Exception:
        pass
    return FRONTEIRA_SUL_POLYGON


def ponto_dentro_fronteira(lat, lng, polygon=None):
    """Ray casting — retorna True se (lat, lng) está dentro do polígono."""
    if polygon is None:
        polygon = get_poligono_ativo()
    n = len(polygon)
    inside = False
    j = n - 1
    for i in range(n):
        lat_i, lng_i = polygon[i]
        lat_j, lng_j = polygon[j]
        if ((lng_i > lng) != (lng_j > lng)) and \
           (lat < (lat_j - lat_i) * (lng - lng_i) / (lng_j - lng_i) + lat_i):
            inside = not inside
        j = i
    return inside
