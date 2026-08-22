from pathlib import Path
import shutil
from logger_config import logger, relatorio
from settings import DESTINO_BASE, EXTENSOES_MAP, ORIGEM_POR_TIPO


def validar_caminhos(caminhos):
    for nome, caminho in caminhos.items():
        if not caminho.exists():
            raise FileNotFoundError(f"{nome}: {caminho} não existe")
        if not caminho.is_dir():
            raise NotADirectoryError(f"{nome}: {caminho} não é diretório")


def listar_arquivos(caminhos):
    for origem, caminho in caminhos.items():
        for arquivo in caminho.rglob("*"):
            if arquivo.is_file():
                yield origem, arquivo


def criar_pasta(categoria, origem):
    pasta = DESTINO_BASE / categoria / origem
    pasta.mkdir(parents=True, exist_ok=True)
    return pasta


def obter_tipo(arquivo):
    ext = arquivo.suffix.lower()
    return EXTENSOES_MAP.get(ext)


def criar_subpasta_tipo(base_dir, tipo):
    subpasta = base_dir / tipo
    subpasta.mkdir(parents=True, exist_ok=True)
    return subpasta


def mover_arquivo(origem, arquivo, categoria, dry_run=False):
    try:
        tipo = obter_tipo(arquivo)

        if tipo is None:
            logger.info(f"IGNORADO | {arquivo.name} | extensão não mapeada")
            relatorio.registrar("ignorado", origem)
            return

        origem_logica = ORIGEM_POR_TIPO.get(tipo, origem)

        base_dir = criar_pasta(categoria, origem_logica)

        destino_dir = criar_subpasta_tipo(base_dir, tipo)

        destino = destino_dir / arquivo.name

        contador = 1
        while destino.exists():
            destino = destino_dir / f"{arquivo.stem}_{contador}{arquivo.suffix}"
            contador += 1

        if dry_run:
            logger.info(f"[DRY-RUN] {arquivo} -> {destino}")
            relatorio.registrar("simulado", origem_logica)
            return

        shutil.move(str(arquivo), str(destino))

        logger.info(f"{arquivo.name} | {origem} -> {origem_logica} | {categoria}/{tipo}")

        relatorio.registrar("movido", origem_logica)

    except Exception as e:
        logger.error(f"ERRO_MOVER | {origem} | {arquivo.name} | {e}")
        relatorio.registrar_erro(f"{arquivo.name}: {e}")
