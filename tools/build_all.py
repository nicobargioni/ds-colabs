"""Genera una categoría completa de notebooks a partir de las asignaciones de specs."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbgen import write
from specs import make, CAT_DATA_ML, ASSIGN_DATA_ML

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))


def build_category(cat_name, cat_dir, assign):
    n = 0
    for (slug, name), items in assign.items():
        for i, (dskey, problema) in enumerate(items, 1):
            spec = make(cat_name, slug, name, i, dskey, problema)
            path = os.path.join(ROOT, cat_dir, slug, f"{i:02d}-{dskey}-{problema}.ipynb")
            write(spec, path)
            n += 1
            print(f"  ✓ {cat_dir}/{slug}/{os.path.basename(path)}")
    return n


if __name__ == "__main__":
    total = build_category(CAT_DATA_ML, "data-ml", ASSIGN_DATA_ML)
    print(f"\nGenerados {total} notebooks en data-ml/")
