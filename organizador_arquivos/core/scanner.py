from core.classifier import classificar_arquivos
import pathlib
from pypdf import PdfReader
from docx import Document
from openpyxl import load_workbook
from PIL import Image

def obter_dados_arquivo(arquivo):
    dados_arquivos = {
    "nome": arquivo.name,
    "extension": arquivo.suffix,
    "last_access": arquivo.stat().st_atime,
    "last_mod": arquivo.stat().st_mtime
    }
    return dados_arquivo

def scanner_arquivos_analise(arquivo, dias_access):

    leitores = {
        ".txt": open(),
        ".pdf": PdfReader,
        ".docx": Document,
        ".xlsl": load_workbook,
        ".png": Image,
        ".jpg": Image
    }

    if dias_access == "Antigos":

        extensao = arquivo.suffix.lower()

        if extensao in leitores:
            return leitores[extensao]

        relatório = {
            "nome": arquivo.name,
            "extension": arquivo.suffix.lower(),
            "criado": dados["dias"],
            "categoria": dados{"categoria"}
        }

        return relatório