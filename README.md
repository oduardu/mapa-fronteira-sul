# Mapa Fronteira Sul em Resenha

Mapa interativo de locais históricos da região da Fronteira Sul (PR/SC/RS). Permite cadastrar, editar e visualizar pontos no mapa com categorias, descrições e imagens.

## Requisitos

- Python 3.9+
- Docker e Docker Compose (para o banco de dados)
- Chave de API do Google Maps

## Chave de API do Google Maps

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um projeto (ou selecione um existente)
3. Vá em **APIs e Serviços → Biblioteca** e ative as seguintes APIs:
   - **Maps JavaScript API**
4. Vá em **APIs e Serviços → Credenciais** e clique em **Criar credenciais → Chave de API**
5. Copie a chave gerada e cole no arquivo `.env` (veja abaixo)

> Recomendado: restrinja a chave por referenciador HTTP (domínio) para evitar uso não autorizado.

## Configuração

### 1. Clone o repositório

```bash
git clone https://github.com/oduardu/mapa-fronteira-sul.git
cd mapa-fronteira-sul
```

### 2. Crie o arquivo `.env`

Copie o exemplo e preencha com seus valores:

```bash
cp .env-example .env
```

Edite o `.env`:

```env
GOOGLE_MAPS_API_KEY=sua_chave_aqui

DB_NAME=mapa_fronteira_sul
DB_USER=mapa
DB_PASSWORD=mapa
DB_HOST=localhost
DB_PORT=5432
```

### 3. Instale as dependências Python

```bash
pip3 install django psycopg2-binary python-dotenv
```

### 4. Suba o banco de dados

```bash
docker compose up -d
```

### 5. Rode as migrações

```bash
python3 manage.py migrate
```

### 6. Crie um usuário admin

```bash
python3 manage.py createsuperuser
```

> O usuário precisa ter `is_staff = True` (o `createsuperuser` já define isso automaticamente).

### 7. Inicie o servidor

```bash
python3 manage.py runserver
```

Acesse em [http://127.0.0.1:8000](http://127.0.0.1:8000).

A área administrativa fica em [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin).

## Estrutura resumida

```
core/
  models.py          # Local e ConfigMapa
  views.py           # Todas as views (portal + admin)
  forms.py           # Formulários com validação de polígono
  polygon.py         # Validação de coordenadas dentro da Fronteira Sul
  templates/core/    # Templates HTML
  static/core/       # CSS e JS estáticos
```
