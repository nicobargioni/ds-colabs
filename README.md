# ds-colabs

Serie de notebooks de **Data Science** rigurosos, ejecutables top-down en Google Colab.
Cada notebook abre con una portada HTML y sigue una estructura fija:

> **Setup → Carga → EDA exhaustivo → Preprocesamiento (sin leakage) → Modelado → Evaluación → Conclusiones**

Comentado en español, `random_state=42`, todo el preprocesamiento dentro de `Pipeline`/`ColumnTransformer`
(se ajusta **solo con train**). Datasets de Kaggle y Hugging Face.

## Organización

Por categoría de [nicolasbargioni.com](https://nicolasbargioni.com) y subtema:

```
data-ml/            # estadística, EDA, clustering/PCA, deep learning, RL, anomalías, minería
ia-agentes/         # LLMs, RAG/embeddings, agentes, visión, habla, búsqueda
hiperautomatizacion/# (DS/ML/NLP aplicado a pipelines y procesos)
cloud/              # (DS/ML/NLP a escala / datos en la nube)
tools/              # nbgen.py — generador de notebooks
```

## La fábrica (`tools/nbgen.py`)

Los notebooks se generan desde un `spec` para garantizar consistencia y rigor:
EDA y preprocesamiento son **data-agnósticos** (se adaptan a las columnas del dataset),
y el modelado/evaluación se elige por tipo de problema (clasificación / regresión / …).

```python
from tools.nbgen import write
write(spec, "data-ml/eda/01-....ipynb")
```

## Cómo correr en Colab

1. Abrí el `.ipynb` en Colab.
2. Ejecutá top-down (Runtime → Run all).
3. Para datasets de Kaggle: subí tu `kaggle.json` cuando la celda lo pida.

---

**Nicolás Bargioni** · Data Scientist · [nicolasbargioni.com](https://nicolasbargioni.com)
