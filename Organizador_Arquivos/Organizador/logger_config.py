import logging
from pathlib import Path
from collections import defaultdict
from datetime import datetime

LOG_PATH = Path("actions.log")

logging.basicConfig(
    filename=LOG_PATH,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


class RelatorioExecucao:
    def __init__(self):
        self.inicio = datetime.now()
        self.contadores = defaultdict(int)
        self.erros = []

    def resetar(self):
        self.inicio = datetime.now()
        self.contadores.clear()
        self.erros.clear()

    def registrar(self, tipo, origem=None):
        chave = f"{tipo}:{origem}" if origem else tipo
        self.contadores[chave] += 1

    def registrar_erro(self, msg):
        self.contadores["erros"] += 1
        self.erros.append(msg)

    def resumo(self):
        duracao = datetime.now() - self.inicio

        linhas = []
        linhas.append("===== RELATÓRIO =====")
        linhas.append(f"Duração: {duracao}\n")

        for k, v in sorted(self.contadores.items()):
            linhas.append(f"{k}: {v}")

        if self.erros:
            linhas.append("\nErros:")
            for e in self.erros[:10]:
                linhas.append(f"- {e}")

        linhas.append("=====================")
        return "\n".join(linhas)


relatorio = RelatorioExecucao()