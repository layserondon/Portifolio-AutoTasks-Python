from pathlib import Path
import shutil
from settings import DESTINO_BASE, CAMINHOS


def desfazer_organizacao():
    for categoria_dir in DESTINO_BASE.iterdir():
        if not categoria_dir.is_dir():
            continue

        for origem_dir in categoria_dir.iterdir():
            if not origem_dir.is_dir():
                continue

            origem_nome = origem_dir.name

            if origem_nome not in CAMINHOS:
                print(f"Ignorando origem desconhecida: {origem_nome}")
                continue

            destino_original = CAMINHOS[origem_nome]

            for tipo_dir in origem_dir.iterdir():
                if not tipo_dir.is_dir():
                    continue

                for arquivo in tipo_dir.iterdir():
                    if arquivo.is_file():
                        destino = destino_original / arquivo.name

                        # evitar sobrescrita
                        contador = 1
                        while destino.exists():
                            destino = destino_original / f"{arquivo.stem}_restaurado_{contador}{arquivo.suffix}"
                            contador += 1

                        shutil.move(str(arquivo), str(destino))
                        print(f"RESTAURADO: {arquivo} -> {destino}")


if __name__ == "__main__":
    desfazer_organizacao()

print(f"[DRY-RUN] {arquivo} -> {destino}")