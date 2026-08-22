from pathlib import Path
import os
import platform


def _is_wsl():
    return "microsoft" in platform.uname().release.lower()


def _windows_path_to_wsl(path_str):
    drive, rest = os.path.splitdrive(path_str)
    if not drive:
        return Path(path_str)
    drive_letter = drive[0].lower()
    normalized = rest.replace("\\", "/").lstrip("/")
    return Path(f"/mnt/{drive_letter}/{normalized}")


def _resolve_base_dir():
    userprofile = os.getenv("USERPROFILE")

    if _is_wsl():
        if userprofile:
            return _windows_path_to_wsl(userprofile)
        username = os.getenv("USERNAME") or os.getenv("USER") or "layse"
        return Path("/mnt/c/Users") / username

    if userprofile:
        return Path(userprofile)
    return Path.home()


def _primeiro_existente(base_dir, nomes):
    for nome in nomes:
        candidato = base_dir / nome
        if candidato.exists():
            return candidato
    return base_dir / nomes[0]


BASE_DIR = _resolve_base_dir()

DOWNLOADS_DIR = _primeiro_existente(BASE_DIR, ["Downloads"])
DOCUMENTOS_DIR = _primeiro_existente(BASE_DIR, ["Documents", "Documentos"])
DESKTOP_DIR = _primeiro_existente(BASE_DIR, ["Desktop", "Area-de-Trabalho"])

CAMINHOS = {
    "downloads": DOWNLOADS_DIR,
    "documentos": DOCUMENTOS_DIR,
}

DESTINO_BASE = DESKTOP_DIR / "Organizados"

CATEGORIAS = ["Recentes", "Arquivados", "Antigos"]

EXTENSOES_MAP = {
    ".pdf": "PDF",
    ".docx": "DOCX",
    ".xlsx": "XLSX",
    ".txt": "TXT",
    ".png": "IMAGENS",
    ".jpg": "IMAGENS",
    ".jpeg": "IMAGENS",
    ".mp4": "VIDEOS",
    ".mov": "VIDEOS",
    ".exe": "EXE",
}

ORIGEM_POR_TIPO = {
    "PDF": "documentos",
    "DOCX": "documentos",
    "TXT": "documentos",

    "IMAGENS": "downloads",
    "VIDEOS": "downloads",
    "EXE": "downloads",
}

LIMITE_RECENTES = 7