from datetime import datetime
from settings import LIMITE_RECENTES


def obter_dados_arquivo(arquivo):
    stat = arquivo.stat()
    return {
        "modificado": datetime.fromtimestamp(stat.st_mtime)
    }


def classificar_arquivo(dados):
    agora = datetime.now()
    diferenca = (agora - dados["modificado"]).days

    if diferenca <= LIMITE_RECENTES:
        return "Recentes"
    elif diferenca <= 30:
        return "Arquivados"
    else:
        return "Antigos"
