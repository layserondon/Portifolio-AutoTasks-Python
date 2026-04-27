import argparse
import time

from logger_config import logger, relatorio

from core.classifier import classificar_arquivo, obter_dados_arquivo
from core.file_ops import listar_arquivos, mover_arquivo, validar_caminhos

from settings import CAMINHOS, DESTINO_BASE


def executar_uma_rodada(dry_run=False):
    relatorio.resetar()
    inicio = time.perf_counter()

    total = 0

    for origem, arquivo in listar_arquivos(CAMINHOS):
        try:
            # evitar reprocessar destino
            if DESTINO_BASE in arquivo.parents:
                continue

            dados = obter_dados_arquivo(arquivo)
            categoria = classificar_arquivo(dados)

            mover_arquivo(origem, arquivo, categoria, dry_run=dry_run)

            total += 1

        except Exception as e:
            logger.error(f"ERRO_PROCESSAMENTO | {arquivo} | {e}")
            relatorio.registrar_erro(f"{arquivo.name}: {e}")

    fim = time.perf_counter()

    print(f"Arquivos processados: {total}")
    print(f"Tempo total: {fim - inicio:.2f}s")
    print(relatorio.resumo())


def criar_parser():
    parser = argparse.ArgumentParser(
        description="Organizador de arquivos por categoria e extensão."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a execução sem mover arquivos.",
    )
    parser.add_argument(
        "--interval-minutes",
        type=int,
        default=0,
        help="Executa continuamente em ciclos com esse intervalo em minutos.",
    )
    return parser


def main():
    args = criar_parser().parse_args()

    validar_caminhos(CAMINHOS)

    if args.interval_minutes <= 0:
        executar_uma_rodada(dry_run=args.dry_run)
        return

    logger.info(f"MODO_AUTOMATICO | intervalo={args.interval_minutes} min")
    print(
        f"Modo automatico ativo: executando a cada {args.interval_minutes} minuto(s). "
        "Pressione Ctrl+C para encerrar."
    )

    intervalo_segundos = args.interval_minutes * 60

    try:
        while True:
            executar_uma_rodada(dry_run=args.dry_run)
            time.sleep(intervalo_segundos)
    except KeyboardInterrupt:
        print("\nExecucao automatica encerrada pelo usuario.")


if __name__ == "__main__":
    main()