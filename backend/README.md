# Find Job Tech

API em Python para analisar currículos em PDF, extrair informações estruturadas e sugerir vagas remotas compatíveis com o perfil do candidato.

## Objetivo

Automatizar parte da busca por emprego na área de tecnologia: o usuário envia o currículo em PDF, o sistema lê o documento, identifica habilidades, experiência, formação, cursos e idiomas, e cruza esses dados com vagas remotas publicadas no [Remotive](https://remotive.com/), retornando uma lista ordenada por **score de compatibilidade** (%).

## Público-alvo

- Profissionais de **tecnologia** em busca de vagas **remotas**
- Desenvolvedores, analistas, designers e perfis afins que querem comparar o currículo com oportunidades reais
- Estudantes e pessoas em transição de carreira que desejam entender quais vagas fazem mais sentido para o perfil atual

## Funcionalidades

| Funcionalidade | Descrição |
|----------------|-----------|
| Upload de PDF | Recebe currículo em PDF e extrai texto com PyMuPDF |
| Parser de seções | Separa o conteúdo em habilidades, experiência, formação, cursos e idiomas |
| Busca de vagas | Consulta a API pública do Remotive com base nas palavras-chave do currículo |
| Score de compatibilidade | Calcula % de match entre currículo e cada vaga (título, tags, descrição) |
| Filtro por score | Parâmetro `score_minimo` (10–100%); vagas abaixo de 10% não são exibidas |
| Ordenação | Vagas ordenadas da **menor** para a **maior** compatibilidade |

### Endpoints da API

| Método | Rota | Função |
|--------|------|--------|
| `GET` | `/health` | Verifica se a API está no ar |
| `POST` | `/api/upload` | Envia PDF e recebe seções parseadas do currículo |
| `POST` | `/api/jobs` | Busca vagas no Remotive a partir das seções do currículo |
| `POST` | `/api/matching` | Mesmo fluxo de vagas + filtro por `score_minimo` no body |

Documentação interativa: http://127.0.0.1:8000/docs (com a API rodando).

## Como executar

```bash
cd backend
python -m venv .venv

# Windows
.\.venv\Scripts\Activate.ps1

# Linux / WSL
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

## Estrutura do projeto

```
find-job-tech/
├── README.md
├── .gitignore
└── backend/
    ├── requirements.txt      # Dependências Python
    ├── .env.example          # Modelo de variáveis de ambiente
    ├── pyrightconfig.json    # Configuração do analisador de tipos (Pyright)
    └── app/
        ├── main.py           # Entrada da API FastAPI e registro das rotas
        ├── routes/           # Endpoints HTTP
        ├── services/         # Regras de negócio
        ├── models/           # Schemas Pydantic (request/response)
        ├── database/         # Conexão SQLAlchemy (preparado para persistência)
        └── utils/            # Funções auxiliares
```

## O que cada arquivo faz

### Raiz

| Arquivo | Função |
|---------|--------|
| `README.md` | Documentação do projeto |
| `.gitignore` | Arquivos ignorados pelo Git (`.venv`, `.env`, cache, etc.) |

### `backend/`

| Arquivo | Função |
|---------|--------|
| `requirements.txt` | Lista de pacotes: FastAPI, Uvicorn, PyMuPDF, SQLAlchemy, etc. |
| `.env.example` | Exemplo de `DATABASE_URL` para configuração local |
| `pyrightconfig.json` | Aponta o Pyright para o ambiente virtual do backend |

### `backend/app/`

| Arquivo | Função |
|---------|--------|
| `main.py` | Cria a aplicação FastAPI, inclui rotas (`upload`, `jobs`, `matching`) e endpoint `/health` |
| `__init__.py` | Marca `app` como pacote Python |

### `backend/app/routes/`

| Arquivo | Função |
|---------|--------|
| `upload.py` | `POST /api/upload` — recebe PDF, chama parser e devolve seções do currículo |
| `jobs.py` | `POST /api/jobs` — recebe seções do currículo e retorna vagas filtradas por score |
| `matching.py` | `POST /api/matching` — mesmo fluxo de vagas com `score_minimo` no corpo da requisição |
| `__init__.py` | Pacote de rotas |

### `backend/app/services/`

| Arquivo | Função |
|---------|--------|
| `pdf_service.py` | Extrai texto bruto do PDF usando **PyMuPDF** (`fitz`) |
| `parser_service.py` | Divide o texto em seções (habilidades, experiência, formação, cursos, idiomas) |
| `jobs_service.py` | Busca vagas na API do Remotive e calcula o % de compatibilidade de cada vaga |
| `matching_service.py` | Filtra vagas pelo `score_minimo`, remove matches &lt; 10% e ordena do menor ao maior score |
| `__init__.py` | Pacote de serviços |

### `backend/app/models/`

| Arquivo | Função |
|---------|--------|
| `schemas.py` | Modelos Pydantic: `ResumeSectionsResponse`, `MatchRequest`, `JobListingResponse`, etc. |
| `__init__.py` | Pacote de modelos |

### `backend/app/database/`

| Arquivo | Função |
|---------|--------|
| `database.py` | Configura engine SQLAlchemy, sessão e `get_db()` (base para salvar dados no futuro) |
| `__init__.py` | Pacote de banco de dados |

### `backend/app/utils/`

| Arquivo | Função |
|---------|--------|
| `helpers.py` | Utilitários de texto (ex.: normalização) |
| `__init__.py` | Pacote de utilitários |

## Fluxo de uso recomendado

1. **Upload** — `POST /api/upload` com o PDF do currículo  
2. **Matching** — `POST /api/matching` com o JSON retornado + `score_minimo` (ex.: `30` para ver só vagas com ≥ 30% de match)

Exemplo de corpo para matching:

```json
{
  "habilidades": "Python, FastAPI, React, AWS",
  "experiencia": "Desenvolvedor backend sênior...",
  "formacao": "Ciência da Computação",
  "cursos": "AWS Certified",
  "idiomas": "Português nativo, Inglês fluente",
  "score_minimo": 10
}
```

## Observações

- As vagas vêm da [API pública do Remotive](https://remotive.com/api/remote-jobs). Ao republicar resultados, cite o Remotive e link para a vaga original, conforme os termos deles.
- O parser depende de **títulos de seção** no PDF (ex.: `HABILIDADES`, `EXPERIÊNCIA`). Currículos sem essa estrutura podem ter parsing incompleto.
- O banco SQLite (`database.py`) está preparado, mas ainda não é usado pelos endpoints atuais.

## Stack

- **FastAPI** — API REST  
- **PyMuPDF** — leitura de PDF  
- **Pydantic** — validação de dados  
- **SQLAlchemy** — ORM (futuro)  
- **Remotive API** — fonte de vagas remotas  
