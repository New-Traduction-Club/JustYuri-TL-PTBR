import glob
import re

def contar_traduccion():
    total = 0
    traducidas = 0
    for archivo in glob.glob("files/*.rpy"):
        with open(archivo, 'r', encoding="utf-8") as f:
            lines = f.readlines()
            i = 0
            while i < len(lines):
                line = lines[i].strip()

                # Maneja bloques old/new
                if line.startswith('old "'):
                    total += 1
                    if i + 1 < len(lines) and lines[i+1].strip().startswith('new "') and not lines[i+1].strip().endswith('new ""'):
                        traducidas += 1
                    i += 2  # Saltar la línea 'new'
                    continue

                # Maneja diálogos comentados
                if line.startswith('#'):
                    original_match = re.search(r'#\s*(".*"|\w+\s+".*")', line)
                    if original_match and i + 1 < len(lines):
                        total += 1
                        next_line = lines[i+1].strip()
                        if next_line and not next_line.endswith('""'):
                            traducidas += 1
                i += 1
    return total, traducidas

if __name__ == "__main__":
    total, traducidas = contar_traduccion()
    porcentaje = (traducidas/total*100) if total else 0
    progreso_md = f"# Progreso de traducción\n\n**{traducidas} de {total} líneas traducidas**\n\n**Progreso:** {porcentaje:.2f}%\n"
    with open("TRANSLATION_PROGRESS.md", "w", encoding="utf-8") as f:
        f.write(progreso_md)

    # Actualizar README.md entre los delimitadores
    with open("README.md", "r", encoding="utf-8") as f:
        readme = f.read()
    inicio = readme.find("<!-- PROGRESO_TRADUCCION_START -->")
    fin = readme.find("<!-- PROGRESO_TRADUCCION_END -->")
    if inicio != -1 and fin != -1:
        nuevo_readme = (readme[:inicio] + "<!-- PROGRESO_TRADUCCION_START -->\n" + progreso_md.replace('# Progreso de traducción\n\n', '') + "<!-- PROGRESO_TRADUCCION_END -->" + readme[fin+len("<!-- PROGRESO_TRADUCCION_END -->"):])
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(nuevo_readme)
