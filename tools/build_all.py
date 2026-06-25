"""Genera categorías de notebooks a partir de las asignaciones de specs.

NOTA: data-ml ya está generado y ANOTADO; no se regenera para no pisar el trabajo.
Este script genera las categorías nuevas (IA & Agentes, Hiperautomatización, Cloud).
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbgen import write
from specs import (make, CAT_IA, ASSIGN_IA, CAT_HIPER, ASSIGN_HIPER,
                   CAT_CLOUD, ASSIGN_CLOUD)

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def build_category(cat_name, cat_dir, assign):
    n = 0
    for (slug, name), items in assign.items():
        for i, (dskey, problema) in enumerate(items, 1):
            spec = make(cat_name, slug, name, i, dskey, problema)
            path = os.path.join(ROOT, cat_dir, slug, f"{i:02d}-{dskey}-{problema}.ipynb")
            write(spec, path)
            n += 1
    print(f"  {cat_dir}: {n} notebooks")
    return n


if __name__ == "__main__":
    total = 0
    total += build_category(CAT_IA, "ia-agentes", ASSIGN_IA)
    total += build_category(CAT_HIPER, "hiperautomatizacion", ASSIGN_HIPER)
    total += build_category(CAT_CLOUD, "cloud", ASSIGN_CLOUD)
    print(f"\nGenerados {total} notebooks nuevos.")
