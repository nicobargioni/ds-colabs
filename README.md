# ds-colabs

Serie de notebooks de **Data Science** rigurosos, ejecutables top-down en Google Colab.
Cada notebook abre con una portada HTML y sigue una estructura fija:

> **Setup → Carga → EDA exhaustivo → Preprocesamiento (sin leakage) → Modelado → Evaluación → Conclusiones**

Comentado en español, `random_state=42`, todo el preprocesamiento dentro de `Pipeline`/`ColumnTransformer`
(se ajusta **solo con train**). Datasets de Kaggle y Hugging Face.

## Organización

Organizado por **técnica** (carpeta = contenido real, sin etiquetas que no correspondan):

```
data-ml/            # por subtema didáctico: EDA, estadística, clustering/PCA,
                    #   anomalías, minería de datos, deep learning (MLP)
ml-aplicado/        # por técnica: clasificacion, regresion, clustering,
                    #   anomalias, nlp-texto (casos aplicados, datasets variados)
ia-agentes/         # (bespoke) RAG+embeddings, agentes, habla, visión, búsqueda
tools/              # nbgen.py — generador · style.py · datasets.py · specs.py
```

> Nota: las carpetas que antes nombraban temas de Cloud/Hiperautomatización se
> consolidaron en `ml-aplicado/` por técnica — el contenido es Data Science aplicada,
> así que el nombre lo refleja.

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
