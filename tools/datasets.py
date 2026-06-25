"""
Pool de datasets confiables (cargan sin auth en Colab). Mezcla de clásicos de
Kaggle/UCI espejados en GitHub y datasets de scikit-learn. Cada entrada trae el
código de carga que deja un DataFrame `df`, el target y el tipo de problema base.

Para usar un dataset puntual de Kaggle/Hugging Face: reemplazar `loader` por la
celda de descarga correspondiente (kaggle API con kaggle.json, o datasets.load_dataset).
"""

_SNS = "https://raw.githubusercontent.com/mwaskom/seaborn-data/master"
_JB = "https://raw.githubusercontent.com/jbrownlee/Datasets/master"

POOL = {
    "titanic": dict(
        name="Titanic", source="Kaggle (mirror)", problema="clasificacion", target="Survived",
        desc="891 pasajeros; numéricas (Age, Fare) y categóricas (Sex, Embarked, Pclass), con faltantes.",
        loader=("import pandas as pd, numpy as np\n"
                "df = pd.read_csv('https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv')\n"
                "df = df.drop(columns=['PassengerId','Name','Ticket','Cabin'])  # IDs/texto libre\n"
                "print('Columnas:', list(df.columns))")),
    "penguins": dict(
        name="Palmer Penguins", source="GitHub (palmerpenguins)", problema="clasificacion", target="species",
        desc="344 pingüinos; medidas morfológicas + isla y sexo; faltantes leves.",
        loader=(f"import pandas as pd\ndf = pd.read_csv('{_SNS}/penguins.csv')\n"
                "df = df.dropna(subset=['species'])\nprint('Columnas:', list(df.columns))")),
    "iris": dict(
        name="Iris", source="UCI (mirror)", problema="clasificacion", target="species",
        desc="150 flores, 4 medidas; 3 especies balanceadas.",
        loader=(f"import pandas as pd\ndf = pd.read_csv('{_SNS}/iris.csv')\nprint(df.shape)")),
    "diamonds": dict(
        name="Diamonds", source="GitHub (seaborn-data)", problema="regresion", target="price",
        desc="~54k diamantes; quilates, corte, color, claridad → precio.",
        loader=(f"import pandas as pd\ndf = pd.read_csv('{_SNS}/diamonds.csv').sample(8000, random_state=42)\nprint(df.shape)")),
    "tips": dict(
        name="Restaurant Tips", source="GitHub (seaborn-data)", problema="regresion", target="tip",
        desc="244 tickets; cuenta total, día, turno, tamaño de mesa → propina.",
        loader=(f"import pandas as pd\ndf = pd.read_csv('{_SNS}/tips.csv')\nprint(df.shape)")),
    "mpg": dict(
        name="Auto MPG", source="UCI (mirror)", problema="regresion", target="mpg",
        desc="398 autos; cilindros, potencia, peso, año → consumo (mpg).",
        loader=(f"import pandas as pd\ndf = pd.read_csv('{_SNS}/mpg.csv').drop(columns=['name'])\nprint(df.shape)")),
    "diabetes": dict(
        name="Pima Diabetes", source="Kaggle/UCI (mirror)", problema="clasificacion", target="target",
        desc="768 pacientes; 8 indicadores clínicos → diabetes (sí/no).",
        loader=(f"import pandas as pd\ncols=['preg','gluc','bp','skin','insulin','bmi','dpf','age','target']\n"
                f"df = pd.read_csv('{_JB}/pima-indians-diabetes.data.csv', header=None, names=cols)\nprint(df.shape)")),
    "wine": dict(
        name="Wine (UCI)", source="scikit-learn", problema="clasificacion", target="target",
        desc="178 vinos; 13 features químicas → 3 cultivares.",
        loader=("from sklearn.datasets import load_wine\nd=load_wine(as_frame=True); df=d.frame\nprint(df.shape)")),
    "cancer": dict(
        name="Breast Cancer", source="scikit-learn", problema="clasificacion", target="target",
        desc="569 muestras; 30 features de imágenes → benigno/maligno.",
        loader=("from sklearn.datasets import load_breast_cancer\nd=load_breast_cancer(as_frame=True); df=d.frame\nprint(df.shape)")),
    "california": dict(
        name="California Housing", source="scikit-learn", problema="regresion", target="MedHouseVal",
        desc="20640 bloques censales; ingreso, ocupación, ubicación → valor medio de vivienda.",
        loader=("from sklearn.datasets import fetch_california_housing\n"
                "d=fetch_california_housing(as_frame=True); df=d.frame.sample(6000, random_state=42)\nprint(df.shape)")),
    "digits": dict(
        name="Digits (8×8)", source="scikit-learn", problema="clasificacion", target="target",
        desc="1797 dígitos manuscritos; 64 píxeles → 0-9.",
        loader=("from sklearn.datasets import load_digits\nd=load_digits(as_frame=True); df=d.frame\nprint(df.shape)")),
    "car_crashes": dict(
        name="Car Crashes (US)", source="GitHub (seaborn-data)", problema="regresion", target="total",
        desc="51 estados; factores de riesgo de manejo → accidentes totales.",
        loader=(f"import pandas as pd\ndf = pd.read_csv('{_SNS}/car_crashes.csv').drop(columns=['abbrev'])\nprint(df.shape)")),
}

# datasets aptos para no supervisado (sacando el target → solo features)
def unsup_loader(key: str) -> str:
    d = POOL[key]
    drop = f"\ndf = df.drop(columns=['{d['target']}'])  # no supervisado: solo features" if d.get("target") else ""
    return d["loader"] + drop

# ── Datasets de texto (NLP) — cargan sin HF (sklearn / CSV público) ───────
def _news(cats):
    return ("from sklearn.datasets import fetch_20newsgroups\nimport pandas as pd\n"
            f"cats={cats}\n"
            "d=fetch_20newsgroups(subset='train', categories=cats, remove=('headers','footers','quotes'))\n"
            "df=pd.DataFrame({'text':d.data,'label':[d.target_names[t] for t in d.target]})\n"
            "df=df[df['text'].str.strip().str.len()>0].reset_index(drop=True)\nprint(df.shape)")

POOL.update({
    "news_tech": dict(name="20 Newsgroups · Tech", source="scikit-learn", problema="nlp", target="label",
        desc="Posts de foros; clasificación de tópico técnico (hardware, ventanas, gráficos, cripto).",
        loader=_news(['comp.sys.mac.hardware','comp.windows.x','comp.graphics','sci.crypt'])),
    "news_sci": dict(name="20 Newsgroups · Ciencia", source="scikit-learn", problema="nlp", target="label",
        desc="Posts de foros de ciencia: espacio, medicina, electrónica, cripto.",
        loader=_news(['sci.space','sci.med','sci.electronics','sci.crypt'])),
    "news_rec": dict(name="20 Newsgroups · Recreación", source="scikit-learn", problema="nlp", target="label",
        desc="Posts sobre autos, motos, béisbol y hockey.",
        loader=_news(['rec.autos','rec.motorcycles','rec.sport.baseball','rec.sport.hockey'])),
    "news_talk": dict(name="20 Newsgroups · Debate", source="scikit-learn", problema="nlp", target="label",
        desc="Posts de debate: política (armas, medio oriente), religión, ateísmo.",
        loader=_news(['talk.politics.guns','talk.politics.mideast','talk.religion.misc','alt.atheism'])),
    "sms": dict(name="SMS Spam", source="UCI (mirror)", problema="nlp", target="label",
        desc="5572 SMS etiquetados ham/spam; texto corto, clases desbalanceadas.",
        loader=("import pandas as pd\n"
                "df=pd.read_csv('https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv',"
                " sep='\\t', header=None, names=['label','text'])\nprint(df.shape)")),
})
