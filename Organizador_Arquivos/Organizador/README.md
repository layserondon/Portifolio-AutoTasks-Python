# Organizador de Arquivos

## Objetivo do projeto
Este projeto automatiza a organização de arquivos pessoais em pastas por **categoria de tempo** e por **tipo de extensão**.  
Ele varre diretórios de origem (como Downloads e Documents), classifica os arquivos por data de modificação e move cada item para uma estrutura padronizada em `Organizados`.

Organização aplicada:
- Categoria temporal: `Recentes`, `Arquivados` e `Antigos`
- Tipo de arquivo: `PDF`, `DOCX`, `XLSX`, `TXT`, `IMAGENS`, `VIDEOS`, `EXE`
- Origem lógica: mantém separação entre arquivos de `downloads` e `documentos`

## Ferramentas e tecnologias usadas
- **Python 3**
- Bibliotecas padrão:
  - `pathlib` (manipulação de caminhos)
  - `shutil` (movimentação de arquivos)
  - `datetime` e `time` (classificação por data e métricas de execução)
  - `logging` (registro de ações e erros)
  - `collections` (contadores para relatório)
  - `sys`, `os`, `platform` (argumentos e compatibilidade Windows/WSL)

Arquivos principais do projeto:
- `main.py`: fluxo principal de execução
- `core/file_ops.py`: validação, listagem e movimentação dos arquivos
- `core/classifier.py`: classificação temporal dos arquivos
- `settings.py`: configuração de caminhos, extensões e regras
- `logger_config.py`: log e relatório da execução

## Para quem este projeto é útil
- Pessoas que acumulam muitos arquivos em Downloads/Documentos
- Estudantes e profissionais que querem manter o computador organizado automaticamente
- Usuários de Windows e WSL que desejam reaproveitar o mesmo script nos dois ambientes

## Requisitos para rodar o código
- Python **3.9+** instalado
- Permissão de leitura e escrita nas pastas configuradas
- **Importante:** revise o `CAMINHOS` em `settings.py` e ajuste os diretórios que você deseja organizar.
- Pastas de origem existentes no perfil do usuário:
  - `Downloads`
  - `Documents` ou `Documentos`
- Pasta de destino será criada automaticamente em:
  - `Desktop/Organizados` (ou `Area-de-Trabalho/Organizados`, conforme o ambiente)

## Como executar
No diretório do projeto:

```bash
python main.py
```

Para simular sem mover arquivos:

```bash
python main.py --dry-run
```

Para executar automaticamente em ciclos (exemplo: a cada 60 minutos):

```bash
python main.py --interval-minutes 60
```

Para usar automacao + simulacao:

```bash
python main.py --dry-run --interval-minutes 60
```

## Automacao regular (nova funcao)
Use o argumento `--interval-minutes` para manter o organizador rodando continuamente em intervalos fixos.

- Exemplo: `--interval-minutes 60` executa uma rodada por hora
- Para encerrar a automacao, pressione `Ctrl + C`
- Se o intervalo for `0` (padrao), a aplicacao roda apenas uma vez

## Saída e monitoramento
- Logs de execução: `actions.log`
- Resumo ao final da execução no terminal:
  - quantidade de arquivos processados
  - tempo total
  - relatório de contadores e erros
