"""Ensamblador de notebooks BESPOKE (hechos a mano, no factory tabular).

Reusa la estética de nbgen (portada hero detrás de #@title + Markdown) pero deja
que cada notebook defina sus propias celdas de código. Pensado para los temas que
el factory no cubre: RAG, agentes, visión, RL, transfer, habla, búsqueda.

Uso:
    import sys; sys.path.insert(0, "tools")
    from bespoke import assemble, write, lectura_cell

    spec = {...}              # mismas keys que consume nbgen (ver A* / specs.py)
    secciones = [
        dict(emoji="🛠", n=0, title="Setup", lead="Imports.", code=[CODE_SETUP]),
        dict(emoji="📊", n=1, title="Datos", lead="...", code=[CODE_A, CODE_B],
             md_after="Texto explicativo en Markdown después del código."),
        ...
    ]
    nb = assemble(spec, secciones)
    write(nb, "ia-agentes/rag-embeddings/01-....ipynb")

Después: ejecutar con nbconvert, leer outputs y agregar la lectura de resultados
con `lectura_cell(...)` insertada antes de las conclusiones (helper más abajo).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
import nbgen


def assemble(spec: dict, secciones: list) -> "nbformat.NotebookNode":
    """Arma el notebook: título → portada (#@title) → marco → secciones → conclusiones."""
    nb = new_notebook()
    c = nb.cells
    c.append(new_markdown_cell(f"# {spec['titulo']}\n*{spec['subtema']} · {spec['categoria']}*"))
    c.append(new_code_cell(nbgen._html_cell("📌 Portada", nbgen._portada(spec), True, spec["titulo"])))
    c.append(new_markdown_cell(nbgen._marco_md(spec)))
    for s in secciones:
        c.append(new_markdown_cell(f"## {s['emoji']} {s['n']} · {s['title']}\n\n{s['lead']}"))
        for code in s.get("code", []):
            c.append(new_code_cell(code))
        if s.get("md_after"):
            c.append(new_markdown_cell(s["md_after"]))
    c.append(new_markdown_cell(nbgen._concl_md(spec)))
    nb["metadata"] = {"colab": {"provenance": [], "toc_visible": True},
                      "kernelspec": {"name": "python3", "display_name": "Python 3"},
                      "language_info": {"name": "python"}}
    return nb


def write(nb, rel_path: str):
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
    path = os.path.join(root, rel_path)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    nbformat.write(nb, path)
    return path


def lectura_cell(markdown: str):
    """Celda '📌 Lectura de resultados' para insertar antes de las conclusiones.

    Uso típico tras ejecutar:
        nb = nbformat.read(path, as_version=4)
        nb.cells.insert(len(nb.cells)-1, lectura_cell(texto_con_numeros_reales))
        nbformat.write(nb, path)
    """
    return new_markdown_cell("### 📌 Lectura de resultados\n\n" + markdown)
