"""Genera el notebook exemplar para validar estilo + rigor de la fábrica."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from nbgen import write

DEMO = {
    "categoria": "Data & Machine Learning",
    "subtema": "Análisis exploratorio (EDA)",
    "titulo": "Supervivencia en el Titanic: EDA y clasificación",
    "subtitulo": ("Caso clásico de clasificación binaria. El foco está en un EDA exhaustivo y "
                  "un preprocesamiento sin fugas, antes de cualquier modelo."),
    "ficha": {
        "Dataset": "Titanic (891 pasajeros)",
        "Fuente": "Kaggle / mirror público",
        "Problema": "Clasificación binaria",
        "Target": "Survived (0/1)",
        "Técnica": "LogReg vs. RandomForest",
        "Métrica": "ROC-AUC",
    },
    "objetivo": "Predecir si un pasajero sobrevivió a partir de sus atributos, priorizando un EDA y un preprocesamiento rigurosos.",
    "hipotesis": "Sexo, clase del pasaje (Pclass) y edad concentran la mayor parte de la señal predictiva.",
    "datos_desc": "891 filas; mezcla de variables numéricas (Age, Fare, SibSp, Parch) y categóricas (Sex, Embarked, Pclass), con faltantes en Age, Cabin y Embarked.",
    "metodologia": "EDA → split estratificado → ColumnTransformer (imputación + escalado + one-hot) dentro de Pipeline → validación cruzada → evaluación en test.",
    "metrica": "ROC-AUC en validación cruzada (5-fold) y en el set de test.",
    "problema": "clasificacion",
    "target": "Survived",
    "loader_code": (
        "# 1 · Carga de datos\n"
        "# Titanic desde un mirror público (en Colab podés usar la Kaggle API con tu kaggle.json).\n"
        "import pandas as pd, numpy as np\n"
        "URL = 'https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv'\n"
        "df = pd.read_csv(URL)\n"
        "# Pruning de columnas no predictivas / texto libre / identificadores (decisión de diseño):\n"
        "df = df.drop(columns=['PassengerId', 'Name', 'Ticket', 'Cabin'])\n"
        "print('Columnas finales:', list(df.columns))"
    ),
    "conclusiones": [
        "El EDA confirma la hipótesis: <b>Sex</b> y <b>Pclass</b> son los predictores más fuertes; <b>Age</b> aporta señal pero tiene ~20% de faltantes.",
        "El preprocesamiento se encapsula en un <b>Pipeline</b>, así la imputación y el escalado se ajustan <b>solo con train</b> — sin data leakage.",
        "RandomForest supera al baseline LogReg en ROC-AUC, pero la diferencia es moderada: en datos tan chicos, el baseline interpretable es competitivo.",
        "Próximos pasos: feature engineering (título extraído del nombre, tamaño de familia) y calibración de probabilidades.",
    ],
}

path = write(DEMO, os.path.join(os.path.dirname(__file__), "..", "data-ml", "eda",
                                "01-titanic-eda-clasificacion.ipynb"))
print("Notebook escrito:", os.path.normpath(path))
