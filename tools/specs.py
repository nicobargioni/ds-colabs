"""
Specs auto-generados: para cada (subtema, dataset, problema) arma el dict que
consume nbgen, con copy coherente por tipo de problema. La variedad entre los 5
notebooks de un subtema viene de usar datasets distintos.
"""
from datasets import POOL, unsup_loader

HUE_FUENTES = ["Kaggle", "Hugging Face", "scikit-learn", "Google Colab"]

_P = {
    "clasificacion": dict(tec="LogReg vs. RandomForest", met="ROC-AUC / F1-macro",
        obj="predecir {tgt} a partir de los atributos, con foco en un EDA y un preprocesamiento rigurosos",
        hip="unas pocas variables concentran la mayor parte de la señal predictiva",
        sub="Clasificación supervisada con foco en EDA exhaustivo y preprocesamiento sin fugas."),
    "regresion": dict(tec="LinearReg vs. RandomForest", met="R² / RMSE",
        obj="estimar {tgt} (variable continua) a partir de los atributos",
        hip="existen relaciones no lineales que el ensemble captura mejor que el modelo lineal",
        sub="Regresión supervisada: del EDA al modelo, evaluando el error fuera de muestra."),
    "deep": dict(tec="MLP (red neuronal) vs. baseline lineal", met="ROC-AUC / F1-macro",
        obj="clasificar {tgt} con una red neuronal (MLP) y compararla contra un baseline lineal",
        hip="la red neuronal mejora al baseline cuando hay interacciones no lineales entre features",
        sub="Red neuronal (MLP) sobre datos tabulares, con la misma rigurosidad de EDA y preprocesamiento."),
    "clustering": dict(tec="K-Means (codo + silueta) + PCA", met="Coeficiente de silueta",
        obj="descubrir grupos naturales (no supervisado) y caracterizarlos",
        hip="los datos se organizan en grupos separables que K-Means puede recuperar",
        sub="Segmentación no supervisada: elección de k por silueta e interpretación con PCA."),
    "anomalia": dict(tec="Isolation Forest + PCA", met="Proporción y score de anomalías",
        obj="detectar observaciones atípicas (no supervisado) y visualizarlas",
        hip="una fracción pequeña de registros se aparta del patrón general",
        sub="Detección de anomalías con Isolation Forest y visualización en el espacio PCA."),
    "nlp": dict(tec="TF-IDF + LogReg/LinearSVC", met="F1-macro",
        obj="clasificar el texto en sus categorías ({tgt})",
        hip="un baseline de TF-IDF + modelo lineal alcanza una performance fuerte",
        sub="Clasificación de texto: EDA de texto, TF-IDF y modelos lineales (sin leakage)."),
}

_TIT = {"clasificacion": "Clasificación con {n}", "regresion": "Regresión sobre {n}",
        "deep": "Red neuronal sobre {n}", "clustering": "Segmentación de {n}",
        "anomalia": "Detección de anomalías en {n}", "nlp": "Clasificación de texto · {n}"}


def make(category: str, sub_slug: str, sub_name: str, idx: int, dskey: str, problema: str) -> dict:
    d = POOL[dskey]
    p = _P[problema]
    tgt = d.get("target", "")
    unsup = problema in ("clustering", "anomalia")
    loader = unsup_loader(dskey) if unsup else d["loader"]
    titulo = _TIT[problema].format(n=d["name"])
    return {
        "categoria": category,
        "subtema": sub_name,
        "titulo": titulo,
        "acento": "",
        "subtitulo": p["sub"],
        "vlabels": [d["source"], problema.capitalize(), p["met"].split(" / ")[0]],
        "fuentes": HUE_FUENTES,
        "ficha": {
            "Dataset": d["name"], "Fuente": d["source"],
            "Problema": problema.capitalize(),
            "Target": tgt if not unsup else "— (no supervisado)",
            "Técnica": p["tec"], "Métrica": p["met"],
        },
        "objetivo": p["obj"].format(tgt=f"`{tgt}`") + f" sobre el dataset {d['name']}.",
        "hipotesis": p["hip"].capitalize() + ".",
        "datos_desc": d["desc"],
        "metodologia": ("EDA exhaustivo → preprocesamiento (imputación/escalado/encoding) → "
                        + (p["tec"]) + " → evaluación" + ("" if unsup else " en test (datos no vistos)") + "."),
        "metrica": p["met"] + ".",
        "problema": problema if problema != "deep" else "deep",
        "target": "" if unsup else tgt,
        "highlights": [
            ("Datos", d["desc"], d["source"]),
            ("Enfoque", p["sub"], p["tec"]),
            ("Métrica", f"Se evalúa con {p['met']}.", "Rigor"),
        ],
        "conclusiones": [
            f"El EDA mapea calidad, faltantes y relaciones antes de modelar sobre <b>{d['name']}</b>.",
            "El preprocesamiento vive dentro de un <b>Pipeline</b> → sin data leakage.",
            f"Técnica aplicada: <b>{p['tec']}</b>, evaluada con <b>{p['met']}</b>.",
            "Próximos pasos: feature engineering específico del dominio y ajuste de hiperparámetros.",
        ],
        "loader_code": loader,
    }


# ── Asignación Data & ML (subtemas que mapean al factory tabular) ──────────
CAT_DATA_ML = "Data & Machine Learning"
ASSIGN_DATA_ML = {
    ("eda", "Análisis exploratorio (EDA)"): [
        ("titanic", "clasificacion"), ("penguins", "clasificacion"), ("tips", "regresion"),
        ("mpg", "regresion"), ("diabetes", "clasificacion")],
    ("estadistica", "Estadística & probabilidad"): [
        ("wine", "clasificacion"), ("cancer", "clasificacion"), ("california", "regresion"),
        ("car_crashes", "regresion"), ("iris", "clasificacion")],
    ("clustering-pca", "Clustering & PCA"): [
        ("penguins", "clustering"), ("iris", "clustering"), ("wine", "clustering"),
        ("diabetes", "clustering"), ("mpg", "clustering")],
    ("deteccion-anomalias", "Detección de anomalías"): [
        ("cancer", "anomalia"), ("diabetes", "anomalia"), ("california", "anomalia"),
        ("car_crashes", "anomalia"), ("wine", "anomalia")],
    ("mineria-de-datos", "Minería de datos"): [
        ("diabetes", "clasificacion"), ("titanic", "clasificacion"), ("cancer", "clasificacion"),
        ("penguins", "clasificacion"), ("wine", "clasificacion")],
    ("deep-learning", "Deep Learning (CNNs)"): [
        ("digits", "deep"), ("cancer", "deep"), ("diabetes", "deep"),
        ("wine", "deep"), ("penguins", "deep")],
}

# ── IA & Agentes (subtemas NLP que mapean a clasificación de texto) ────────
CAT_IA = "IA aplicada & Agentes"
_NLP5 = lambda: [("news_tech", "nlp"), ("news_sci", "nlp"), ("news_rec", "nlp"),
                 ("news_talk", "nlp"), ("sms", "nlp")]
ASSIGN_IA = {
    ("llms-prompting", "LLMs & Prompt Engineering"): _NLP5(),
    ("rag-embeddings", "RAG & embeddings"): _NLP5(),
    ("agentes", "Agentes de IA"): _NLP5(),
    ("procesamiento-habla", "Procesamiento del habla"): _NLP5(),
}

# ── Hiperautomatización (repurposado a DS/ML/NLP) ──────────────────────────
CAT_HIPER = "Hiperautomatización"
ASSIGN_HIPER = {
    ("rpa", "RPA (UiPath)"): [("titanic","clasificacion"),("diabetes","clasificacion"),
        ("mpg","regresion"),("penguins","clustering"),("cancer","anomalia")],
    ("n8n-make", "n8n & Make"): [("wine","clasificacion"),("california","regresion"),
        ("iris","clustering"),("tips","regresion"),("diabetes","anomalia")],
    ("agentes-conversacionales", "Agentes conversacionales"): [("sms","nlp"),("news_tech","nlp"),
        ("titanic","clasificacion"),("cancer","clasificacion"),("penguins","clasificacion")],
    ("bpmn", "BPMN & process mining"): [("car_crashes","regresion"),("mpg","regresion"),
        ("diabetes","clasificacion"),("wine","clustering"),("california","anomalia")],
    ("idp", "Documentos inteligentes (IDP)"): [("news_sci","nlp"),("sms","nlp"),
        ("titanic","clasificacion"),("diabetes","clasificacion"),("cancer","anomalia")],
}

# ── Cloud & Deploy (repurposado a DS/ML/NLP) ───────────────────────────────
CAT_CLOUD = "Cloud & Deploy"
ASSIGN_CLOUD = {
    ("gcp", "Google Cloud (Vertex AI)"): [("diamonds","regresion"),("cancer","clasificacion"),
        ("penguins","clustering"),("california","regresion"),("wine","clasificacion")],
    ("cloud-run", "Cloud Run & Functions"): [("titanic","clasificacion"),("diabetes","clasificacion"),
        ("mpg","regresion"),("iris","clasificacion"),("car_crashes","regresion")],
    ("bigquery", "BigQuery"): [("california","regresion"),("diamonds","regresion"),
        ("wine","clasificacion"),("penguins","clasificacion"),("tips","regresion")],
    ("docker", "Docker & contenedores"): [("cancer","clasificacion"),("diabetes","anomalia"),
        ("iris","clustering"),("mpg","regresion"),("titanic","clasificacion")],
    ("serverless", "Arquitectura serverless"): [("penguins","clasificacion"),("wine","clustering"),
        ("california","anomalia"),("tips","regresion"),("diabetes","clasificacion")],
    ("cicd", "CI/CD & despliegue"): [("titanic","clasificacion"),("cancer","clasificacion"),
        ("mpg","regresion"),("iris","clasificacion"),("wine","clasificacion")],
}
