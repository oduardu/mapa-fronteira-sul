# Diagrama de Relacionamento — Banco de Dados

```mermaid
erDiagram

    %% ── Tabelas do Django Auth ──────────────────────────────────────────

    auth_user {
        int         id              PK
        varchar     username
        varchar     password
        varchar     email
        varchar     first_name
        varchar     last_name
        boolean     is_staff
        boolean     is_active
        boolean     is_superuser
        datetime    last_login
        datetime    date_joined
    }

    auth_group {
        int     id      PK
        varchar name
    }

    auth_permission {
        int     id          PK
        varchar name
        varchar codename
        int     content_type_id FK
    }

    auth_user_groups {
        int id       PK
        int user_id  FK
        int group_id FK
    }

    auth_user_user_permissions {
        int id            PK
        int user_id       FK
        int permission_id FK
    }

    auth_group_permissions {
        int id            PK
        int group_id      FK
        int permission_id FK
    }

    django_content_type {
        int     id         PK
        varchar app_label
        varchar model
    }

    django_session {
        varchar  session_key  PK
        text     session_data
        datetime expire_date
    }

    %% ── Tabelas da aplicação ────────────────────────────────────────────

    core_local {
        int      id            PK
        varchar  nome
        varchar  categoria     "forte | ruina | museu | igreja | marco | casarao"
        float    lat
        float    lng
        varchar  cidade
        varchar  uf            "2 chars"
        text     resumo
        text     descricao
        varchar  endereco
        varchar  periodo
        json     imagens       "lista de URLs"
        boolean  ativo
        datetime criado_em
        datetime atualizado_em
    }

    core_configmapa {
        int      id               PK "singleton pk=1"
        float    restricao_norte
        float    restricao_sul
        float    restricao_leste
        float    restricao_oeste
        float    centro_lat
        float    centro_lng
        int      zoom_inicial
        int      zoom_minimo
        json     poligono         "lista de {lat, lng}"
        datetime atualizado_em
    }

    %% ── Relacionamentos ─────────────────────────────────────────────────

    auth_user            ||--o{ auth_user_groups           : "pertence a"
    auth_group           ||--o{ auth_user_groups           : "agrupa"
    auth_user            ||--o{ auth_user_user_permissions : "possui"
    auth_permission      ||--o{ auth_user_user_permissions : "concedida a"
    auth_group           ||--o{ auth_group_permissions     : "possui"
    auth_permission      ||--o{ auth_group_permissions     : "concedida a"
    django_content_type  ||--o{ auth_permission            : "referencia"
    auth_user            ||--o{ django_session             : "autenticado em"
```

## Notas

| Tabela | Descrição |
|---|---|
| `core_local` | Pontos do mapa (históricos). Sem FK — autônomo. |
| `core_configmapa` | Singleton (sempre `id = 1`). Guarda os limites do mapa, centro, zoom e polígono da região. |
| `auth_user` | Usuários Django. Apenas usuários com `is_staff = true` acessam a área administrativa. |
| `django_session` | Sessões de login; não há FK explícita, mas o middleware associa sessão ao usuário. |
