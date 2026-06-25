#!/usr/bin/env python3
"""
nbgen — fábrica de notebooks de Data Science (estética editorial oscura + rigor).

Clona el sistema visual de la entrega del usuario (tools/style.py · EDU_CSS):
portada cinematográfica, secciones de vidrio, KPIs, callouts y tablas. Para que
los notebooks NO sean todos iguales, cada uno aplica un `hue-rotate` propio
(misma estructura, distinta familia de color). Las celdas que solo contienen
HTML/CSS van detrás de `#@title` (Colab oculta el código y muestra el render).

Estructura: Portada → Marco → Setup → Carga → EDA exhaustivo →
Preprocesamiento (sin leakage) → Modelado → Evaluación → Conclusiones.
random_state=42, comentado en español.
"""
from __future__ import annotations
import json
import os
import html as _html
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style import EDU_CSS, BANNER_CSS  # noqa: E402

# Familias de color (hue-rotate en grados, saturación). Variedad entre notebooks.
HUES = [(0, 1.0), (28, 1.05), (62, 1.0), (118, 0.95), (165, 1.0),
        (205, 1.05), (255, 1.0), (300, 1.05), (330, 1.0)]


def _hue(seed: str):
    return HUES[sum(map(ord, seed)) % len(HUES)]


def _wrap(inner: str, seed: str) -> str:
    deg, sat = _hue(seed)
    return f'<div style="filter:hue-rotate({deg}deg) saturate({sat});">{inner}</div>'


def _esc(s) -> str:
    return _html.escape(str(s))


# ── Portada cinematográfica ────────────────────────────────────────────────
def _portada(s: dict) -> str:
    cat = s["categoria"]
    vlabels = s.get("vlabels") or list(s["ficha"].values())[:3]
    vl = "".join(f"<span>{_esc(x)}</span>" for x in vlabels[:3])
    hi = s.get("highlights") or [
        ("Objetivo", s["objetivo"], "Meta"),
        ("Hipótesis", s["hipotesis"], "A validar"),
        ("Datos", s["datos_desc"], s["ficha"].get("Dataset", "Dataset")),
    ]
    cards = "".join(
        f'<article class="edu-glass"><h4>{_esc(h)}</h4><p>{_esc(p)}</p>'
        f'<div class="edu-glass-foot"><span class="edu-metric">{_esc(m)}</span>'
        f'<a>Ver análisis &rarr;</a></div></article>'
        for h, p, m in hi[:3]
    )
    fuentes = s.get("fuentes") or ["Kaggle", "Hugging Face", "scikit-learn", "Google Colab"]
    logos = "".join(f"<span>{_esc(x)}</span>" for x in fuentes)
    meta = {
        "Autor": "Nicolás Bargioni",
        "Rol": "Data Scientist",
        "Categoría": cat,
        "Dataset": s["ficha"].get("Dataset", "—"),
    }
    metas = "".join(
        f'<div><span class="k">{_esc(k)}</span><span class="v">{_esc(v)}</span></div>'
        for k, v in meta.items()
    )
    acento = f'<em>{_esc(s["acento"])}</em>' if s.get("acento") else ""
    return f"""<div class="edu-portada">
  <div class="edu-cine">
     <div class="edu-fog"></div><div class="edu-stars"></div><div class="edu-stars2"></div>
     <span class="edu-comet"></span><span class="edu-comet edu-comet2"></span>
     <svg class="edu-ridge" viewBox="0 0 1200 200" preserveAspectRatio="none" aria-hidden="true">
        <defs><linearGradient id="eduRg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#0d2034"/><stop offset="1" stop-color="#050b14"/></linearGradient></defs>
        <path d="M0,200 L0,118 L130,72 L250,112 L380,52 L520,118 L660,58 L800,116 L940,46 L1070,104 L1200,64 L1200,200 Z" fill="url(#eduRg)"/>
     </svg>
     <div class="edu-grain"></div>
     <header class="edu-nav"><div class="edu-logo">ds-colabs<span>· {_esc(cat)}</span></div></header>
     <div class="edu-vlabels">{vl}</div>
     <div class="edu-cine-grid"><div class="edu-cine-main">
        <span class="edu-kicker">{_esc(cat)} · {_esc(s["subtema"])}</span>
        <h1 class="edu-mega">{_esc(s["titulo"])}{acento}</h1>
        <p class="edu-lede">{_esc(s["subtitulo"])}</p>
        <a class="edu-cta" href="#">Explorar el análisis <span>&rarr;</span></a>
     </div>
     <aside class="edu-floats">{cards}</aside></div>
     <div class="edu-logos"><span class="edu-logos-label">Fuentes</span>{logos}</div>
  </div>
  <div class="edu-metastrip"><div class="edu-meta">{metas}</div></div>
</div>"""


def _md_inline(x: str) -> str:
    """Convierte <b>…</b> de los specs a **…** para celdas Markdown."""
    return (str(x).replace("<b>", "**").replace("</b>", "**")
            .replace("<i>", "_").replace("</i>", "_"))


def _marco_md(s: dict) -> str:
    metrica = s["ficha"].get("Métrica", s.get("metrica", ""))
    return (
        "## 🧭 Marco del trabajo\n\n"
        "| | |\n|---|---|\n"
        f"| **Objetivo** | {_md_inline(s['objetivo'])} |\n"
        f"| **Hipótesis** | {_md_inline(s['hipotesis'])} |\n"
        f"| **Datos** | {_md_inline(s['datos_desc'])} |\n"
        f"| **Metodología** | {_md_inline(s['metodologia'])} |\n"
        f"| **Métrica** | {_md_inline(metrica)} |\n\n"
        "> Ejecutable top-down · `random_state=42` · preprocesamiento **sin data leakage**."
    )


def _concl_md(s: dict) -> str:
    items = "\n".join(f"- {_md_inline(x)}" for x in s["conclusiones"])
    return (f"## ✅ Conclusiones\n\n{items}\n\n"
            "---\n*Nicolás Bargioni · Data Scientist · [nicolasbargioni.com](https://nicolasbargioni.com)*")


def _html_cell(title: str, inner_html: str, with_css: bool, seed: str) -> str:
    body = ((EDU_CSS + BANNER_CSS) if with_css else "") + _wrap(inner_html, seed)
    return (f"#@title {title}\nfrom IPython.display import HTML, display\n"
            f"display(HTML(r'''{body}'''))")


# ── Builder principal ──────────────────────────────────────────────────────
def build(spec: dict) -> nbformat.NotebookNode:
    nb = new_notebook()
    c = nb.cells
    P = spec["problema"]
    seed = spec.get("titulo", "x")
    T = spec.get("target", "")

    c.append(new_markdown_cell(
        f"# {spec['titulo']}\n*{spec['subtema']} · {spec['categoria']}*"))
    # Portada hero (HTML autocontenido detrás de #@title — único bloque HTML)
    c.append(new_code_cell(_html_cell("📌 Portada", _portada(spec), True, seed)))
    # El resto en Markdown bien formateado (confiable en Colab + alimenta el índice)
    c.append(new_markdown_cell(_marco_md(spec)))

    def section(n, emoji, title, lede):
        c.append(new_markdown_cell(f"## {emoji} {n} · {title}\n\n{lede}"))

    section(0, "🛠", "Setup", "Dependencias, imports y configuración global (reproducibilidad).")
    c.append(new_code_cell(_SETUP))
    section(1, "📥", "Carga de datos", "Lectura del dataset y vista inicial de la tabla.")
    c.append(new_code_cell(spec["loader_code"]))
    c.append(new_code_cell(_LOAD_CHECK))
    if P == "nlp":
        section(2, "🔍", "Análisis exploratorio (EDA de texto)",
                "Balance de clases, longitud de los textos y vocabulario más frecuente.")
        c.append(new_code_cell(_NLP_EDA))
        c.append(new_markdown_cell(_EXPL_EDA_NLP))
        section(3, "🧪", "Representación del texto",
                "TF-IDF dentro del `Pipeline` (el IDF se ajusta solo con train → sin leakage).")
        c.append(new_markdown_cell(_EXPL_MODEL["nlp"]))
        c.append(new_code_cell(_NLP_PREP))
        section(4, "🧠", "Modelado", "TF-IDF + modelos lineales (LogReg vs LinearSVC) con validación cruzada.")
        c.append(new_code_cell(_NLP_MODEL))
        section(5, "📊", "Evaluación", "Desempeño sobre textos no vistos (set de test).")
        c.append(new_code_cell(_NLP_EVAL))
        c.append(new_markdown_cell(_EXPL_EVAL["nlp"]))
        c.append(new_markdown_cell(_concl_md(spec)))
        nb["metadata"] = {"colab": {"provenance": [], "toc_visible": True},
                          "kernelspec": {"name": "python3", "display_name": "Python 3"},
                          "language_info": {"name": "python"}}
        return nb

    section(2, "🔍", "Análisis exploratorio (EDA)",
            "Forma, tipos, faltantes, distribuciones, cardinalidad, correlaciones, outliers y relación con el target.")
    for cell in (_EDA_OVERVIEW, _EDA_MISSING,
                 _EDA_TARGET.replace("__TARGET__", T).replace("__P__", P),
                 _EDA_NUMERIC, _EDA_CATEGORICAL, _EDA_CORR, _EDA_OUTLIERS):
        c.append(new_code_cell(cell))
    c.append(new_markdown_cell(_EXPL_EDA))  # interpretación del EDA

    if P in ("clustering", "anomalia"):
        section(3, "🧪", "Preprocesamiento",
                "Escalado y encoding sobre todo el conjunto (problema no supervisado, sin target).")
        c.append(new_markdown_cell(_EXPL_PREP_UNSUP))
        c.append(new_code_cell(_UNSUP_PREP))
        section(4, "🧠", "Modelado",
                "K-Means con selección de k (codo + silueta)." if P == "clustering"
                else "Isolation Forest para señalar observaciones atípicas.")
        c.append(new_markdown_cell(_EXPL_MODEL[P]))
        c.append(new_code_cell(_MODEL[P]))
        section(5, "📊", "Evaluación", "Interpretación de los grupos / anomalías (proyección PCA 2D).")
        c.append(new_code_cell(_EVAL[P]))
        c.append(new_markdown_cell(_EXPL_EVAL[P]))
    else:
        section(3, "🧪", "Preprocesamiento",
                "Split antes de transformar; imputación, escalado y encoding dentro de un `Pipeline` (ajustado solo con train → sin leakage).")
        c.append(new_markdown_cell(_EXPL_PREP))
        c.append(new_code_cell(_SPLIT.replace("__TARGET__", T).replace("__P__", P)))
        c.append(new_code_cell(_PREPROCESS))
        section(4, "🧠", "Modelado", "Baseline interpretable vs. ensemble, comparados con validación cruzada.")
        c.append(new_markdown_cell(_EXPL_MODEL.get(P, _EXPL_MODEL["clasificacion"])))
        c.append(new_code_cell(_MODEL.get(P, _MODEL["clasificacion"])))
        section(5, "📊", "Evaluación", "Desempeño sobre datos nunca vistos (set de test).")
        c.append(new_code_cell(_EVAL.get(P, _EVAL["clasificacion"])))
        c.append(new_markdown_cell(_EXPL_EVAL.get(P, _EXPL_EVAL["clasificacion"])))
    c.append(new_markdown_cell(_concl_md(spec)))

    nb["metadata"] = {
        "colab": {"provenance": [], "toc_visible": True},
        "kernelspec": {"name": "python3", "display_name": "Python 3"},
        "language_info": {"name": "python"},
    }
    return nb


def write(spec: dict, path: str) -> str:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    nbformat.write(build(spec), path)
    return path


# ── Plantillas de celdas de código (rigurosas, data-agnósticas) ───────────
_SETUP = """# 0.1 Dependencias (Colab ya trae casi todo; instala solo lo que falte)
import importlib, sys, subprocess
for _p in ['datasets', 'plotly']:
    if importlib.util.find_spec(_p) is None:
        subprocess.run([sys.executable, '-m', 'pip', '-q', 'install', _p])

# 0.2 Imports
import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
import plotly.subplots as sp
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# 0.3 Configuración global (reproducibilidad + estética de los gráficos)
SEED = 42
np.random.seed(SEED)
pd.set_option('display.max_columns', 60)
PRIMARY, ACCENT, TEAL = '#7fd4ff', '#ff9f5c', '#43c4b0'
COLORWAY = ['#7fd4ff', '#ff9f5c', '#43c4b0', '#bfe6ff', '#ffd9b8', '#5ce0b5']
pio.templates.default = 'plotly_dark'   # coherente con la estética oscura del notebook
px.defaults.color_discrete_sequence = COLORWAY
px.defaults.template = 'plotly_dark'
print('Setup OK · pandas', pd.__version__, '· plotly listo (gráficos interactivos)')"""

_LOAD_CHECK = """# Vista rápida (el loader debe dejar un DataFrame `df`)
assert 'df' in globals(), 'El loader debe definir un DataFrame llamado df'
df = df.copy()
print('Filas × columnas:', df.shape)
df.head()"""

_EDA_OVERVIEW = """# 2.1 Forma, tipos y memoria
print('Dimensiones:', df.shape)
num_cols = df.select_dtypes(include='number').columns.tolist()
cat_cols = df.select_dtypes(exclude='number').columns.tolist()
print(f'{len(num_cols)} numéricas · {len(cat_cols)} categóricas')
display(df.dtypes.value_counts().rename('columnas').to_frame())
df.info()"""

_EDA_MISSING = """# 2.2 Valores faltantes
na = df.isna().sum(); na = na[na > 0].sort_values()
if len(na):
    display(pd.DataFrame({'faltantes': na[::-1], '%': (na[::-1]/len(df)*100).round(2)}))
    fig = px.bar(x=na.values, y=na.index, orientation='h',
                 labels={'x': 'cantidad', 'y': ''}, title='Valores faltantes por columna')
    fig.update_traces(marker_color=PRIMARY); fig.update_layout(height=80+34*len(na)); fig.show()
else:
    print('Sin valores faltantes.')"""

_EDA_TARGET = """# 2.3 Variable objetivo
TARGET = "__TARGET__"
if TARGET and TARGET in df.columns:
    if "__P__" == 'regresion':
        display(df[TARGET].describe().to_frame())
        px.histogram(df, x=TARGET, nbins=40, title=f'Distribución de {TARGET}').show()
    else:
        vc = df[TARGET].value_counts(dropna=False)
        display(pd.DataFrame({'n': vc, '%': (vc/len(df)*100).round(2)}))
        px.bar(x=vc.index.astype(str), y=vc.values, labels={'x': TARGET, 'y': 'n'},
               title=f'Balance de clases — {TARGET}').show()
        imb = vc.min()/vc.max()
        print(f'Ratio min/max de clases: {imb:.2f}' + ('  ⚠️ desbalanceado' if imb < 0.4 else ''))
else:
    print('Sin target supervisado en esta etapa.')"""

_EDA_NUMERIC = """# 2.4 Distribuciones de variables numéricas
num_cols = df.select_dtypes(include='number').columns.tolist()
if num_cols:
    display(df[num_cols].describe().T)
    cols = num_cols[:9]; rows = (len(cols)+2)//3
    fig = sp.make_subplots(rows=rows, cols=3, subplot_titles=cols)
    for i, col in enumerate(cols):
        fig.add_trace(go.Histogram(x=df[col].dropna(), marker_color=PRIMARY, name=col),
                      row=i//3+1, col=i%3+1)
    fig.update_layout(height=300*rows, showlegend=False, title_text='Distribuciones numéricas',
                      template='plotly_dark'); fig.show()
else:
    print('Sin columnas numéricas.')"""

_EDA_CATEGORICAL = """# 2.5 Categóricas: cardinalidad y valores frecuentes
cat_cols = df.select_dtypes(exclude='number').columns.tolist()
if cat_cols:
    card = df[cat_cols].nunique().sort_values(ascending=False)
    display(card.rename('valores únicos').to_frame())
    for col in card.index[:4]:
        print(f'\\n{col} — top 6:'); print(df[col].value_counts(dropna=False).head(6))
else:
    print('Sin columnas categóricas.')"""

_EDA_CORR = """# 2.6 Matriz de correlación (numéricas)
num_cols = df.select_dtypes(include='number').columns.tolist()
if len(num_cols) >= 2:
    corr = df[num_cols].corr(numeric_only=True).round(2)
    fig = px.imshow(corr, color_continuous_scale='RdBu_r', zmin=-1, zmax=1, aspect='auto',
                    text_auto=(len(num_cols) <= 12), title='Matriz de correlación')
    fig.show()
else:
    print('Pocas numéricas para correlación.')"""

_EDA_OUTLIERS = """# 2.7 Outliers por regla IQR
num_cols = df.select_dtypes(include='number').columns.tolist()
rows = []
for col in num_cols:
    q1, q3 = df[col].quantile([.25, .75]); iqr = q3 - q1
    n = int(((df[col] < q1-1.5*iqr) | (df[col] > q3+1.5*iqr)).sum())
    rows.append((col, n, round(n/len(df)*100, 2)))
if rows:
    display(pd.DataFrame(rows, columns=['columna','outliers','%']).sort_values('outliers', ascending=False))
else:
    print('Sin numéricas para evaluar outliers.')"""

_SPLIT = """# 3.1 X / y y split train/test (estratificado si es clasificación)
TARGET = "__TARGET__"
assert TARGET in df.columns, f'Target no encontrado: {TARGET}'
X = df.drop(columns=[TARGET]); y = df[TARGET]
strat = y if "__P__" == 'clasificacion' else None
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=SEED, stratify=strat)
print('train:', X_train.shape, '· test:', X_test.shape)"""

_PREPROCESS = """# 3.2 Preprocesador (se ajusta SOLO con train dentro del Pipeline → sin leakage)
num_feats = X_train.select_dtypes(include='number').columns.tolist()
cat_feats = X_train.select_dtypes(exclude='number').columns.tolist()
numeric = Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())])
categ = Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                  ('oh', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])
preprocess = ColumnTransformer([('num', numeric, num_feats), ('cat', categ, cat_feats)])
print(f'{len(num_feats)} numéricas + {len(cat_feats)} categóricas → preprocesador listo')"""

_MODEL = {
"clasificacion": """# 4 · Candidatos (baseline + ensemble) con validación cruzada
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
scoring = 'roc_auc' if y.nunique()==2 else 'f1_macro'
cands = {'LogReg (baseline)': LogisticRegression(max_iter=1000, random_state=SEED),
         'RandomForest': RandomForestClassifier(n_estimators=300, random_state=SEED, n_jobs=-1)}
results = {}
for name, clf in cands.items():
    pipe = Pipeline([('prep', preprocess), ('clf', clf)])
    sc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)
    results[name] = sc; print(f'{name:22s} {scoring}: {sc.mean():.4f} ± {sc.std():.4f}')
best_name = max(results, key=lambda k: results[k].mean()); _b = next(k for k in results if 'baseline' in k.lower())
print(f'\\nMejor modelo: {best_name} = {results[best_name].mean():.3f} · baseline {results[_b].mean():.3f} (Δ {results[best_name].mean()-results[_b].mean():+.3f})')
best = Pipeline([('prep', preprocess), ('clf', cands[best_name])]).fit(X_train, y_train)""",
"regresion": """# 4 · Candidatos (baseline + ensemble) con validación cruzada
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
cv = KFold(n_splits=5, shuffle=True, random_state=SEED)
cands = {'LinReg (baseline)': LinearRegression(),
         'RandomForest': RandomForestRegressor(n_estimators=300, random_state=SEED, n_jobs=-1)}
results = {}
for name, reg in cands.items():
    pipe = Pipeline([('prep', preprocess), ('reg', reg)])
    sc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='r2', n_jobs=-1)
    results[name] = sc; print(f'{name:22s} R2: {sc.mean():.4f} ± {sc.std():.4f}')
best_name = max(results, key=lambda k: results[k].mean()); _b = next(k for k in results if 'baseline' in k.lower())
print(f'\\nMejor modelo: {best_name} = {results[best_name].mean():.3f} · baseline {results[_b].mean():.3f} (Δ {results[best_name].mean()-results[_b].mean():+.3f})')
best = Pipeline([('prep', preprocess), ('reg', cands[best_name])]).fit(X_train, y_train)""",
}

_EVAL = {
"clasificacion": """# 5 · Evaluación en test (datos nunca vistos)
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
y_pred = best.predict(X_test)
print(classification_report(y_test, y_pred))
labels = sorted(map(str, y.unique()))
cm = confusion_matrix(y_test, y_pred)
px.imshow(cm, x=labels, y=labels, text_auto=True, color_continuous_scale='Blues',
          labels=dict(x='predicho', y='real', color='n'), title='Matriz de confusión').show()
if y.nunique() == 2 and hasattr(best, 'predict_proba'):
    pos = sorted(y.unique())[-1]
    proba = best.predict_proba(X_test)[:, list(best.classes_).index(pos)]
    fpr, tpr, _ = roc_curve((y_test == pos).astype(int), proba)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=fpr, y=tpr, mode='lines', line=dict(color=ACCENT, width=3),
                             name=f'AUC = {auc(fpr, tpr):.3f}', fill='tozeroy'))
    fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode='lines',
                             line=dict(dash='dash', color='gray'), showlegend=False))
    fig.update_layout(title='Curva ROC', xaxis_title='FPR', yaxis_title='TPR', template='plotly_dark')
    fig.show()""",
"regresion": """# 5 · Evaluación en test (datos nunca vistos)
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
y_pred = best.predict(X_test)
print(f'R2  : {r2_score(y_test, y_pred):.4f}')
print(f'MAE : {mean_absolute_error(y_test, y_pred):.4f}')
print(f'RMSE: {mean_squared_error(y_test, y_pred)**0.5:.4f}')
lims = [float(min(y_test.min(), y_pred.min())), float(max(y_test.max(), y_pred.max()))]
fig = px.scatter(x=y_test, y=y_pred, opacity=.5, labels={'x': 'real', 'y': 'predicho'},
                 title='Predicho vs. real')
fig.update_traces(marker_color=PRIMARY)
fig.add_trace(go.Scatter(x=lims, y=lims, mode='lines', line=dict(dash='dash', color=ACCENT), showlegend=False))
fig.show()""",
}

# ── Plantillas no supervisadas (clustering / anomalías) ───────────────────
_UNSUP_PREP = """# 3 · Preprocesamiento (no supervisado): escalado + encoding sobre todo X
num_feats = df.select_dtypes(include='number').columns.tolist()
cat_feats = df.select_dtypes(exclude='number').columns.tolist()
numeric = Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())])
categ = Pipeline([('imp', SimpleImputer(strategy='most_frequent')),
                  ('oh', OneHotEncoder(handle_unknown='ignore', sparse_output=False))])
preprocess = ColumnTransformer([('num', numeric, num_feats), ('cat', categ, cat_feats)])
Xp = preprocess.fit_transform(df)
print('Matriz preprocesada:', Xp.shape)"""

_MODEL["clustering"] = """# 4 · K-Means: elegir k con el codo (inercia) y la silueta
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
ks = list(range(2, 9)); inertias = []; sils = []
for k in ks:
    km = KMeans(n_clusters=k, random_state=SEED, n_init=10).fit(Xp)
    inertias.append(km.inertia_); sils.append(silhouette_score(Xp, km.labels_))
fig = sp.make_subplots(rows=1, cols=2, subplot_titles=('Codo (inercia)', 'Silueta'))
fig.add_trace(go.Scatter(x=ks, y=inertias, mode='lines+markers', line=dict(color=PRIMARY)), row=1, col=1)
fig.add_trace(go.Scatter(x=ks, y=sils, mode='lines+markers', line=dict(color=ACCENT)), row=1, col=2)
fig.update_layout(height=360, showlegend=False, template='plotly_dark'); fig.show()
best_k = ks[int(np.argmax(sils))]
print('k elegido por silueta:', best_k)
km = KMeans(n_clusters=best_k, random_state=SEED, n_init=10).fit(Xp)
df['cluster'] = km.labels_"""

_EVAL["clustering"] = """# 5 · Interpretación: clusters proyectados en 2D (PCA)
from sklearn.decomposition import PCA
pca = PCA(n_components=2, random_state=SEED); coords = pca.fit_transform(Xp)
px.scatter(x=coords[:, 0], y=coords[:, 1], color=df['cluster'].astype(str),
           labels={'x': 'PC1', 'y': 'PC2', 'color': 'cluster'},
           title=f'Clusters (PCA 2D) · varianza explicada {pca.explained_variance_ratio_.sum():.0%}').show()
display(df.groupby('cluster').size().rename('n').to_frame())"""

_MODEL["anomalia"] = """# 4 · Detección de anomalías con Isolation Forest
from sklearn.ensemble import IsolationForest
iso = IsolationForest(random_state=SEED, contamination='auto').fit(Xp)
scores = iso.decision_function(Xp); pred = iso.predict(Xp)   # -1 = anómalo
df['anomalia'] = (pred == -1)
print('Anomalías detectadas:', int(df['anomalia'].sum()), f'({df[\"anomalia\"].mean()*100:.1f}%)')"""

_EVAL["anomalia"] = """# 5 · Score de anomalía + proyección 2D (PCA)
px.histogram(x=scores, nbins=50, title='Score de anomalía (menor = más atípico)',
             labels={'x': 'score'}).show()
from sklearn.decomposition import PCA
coords = PCA(n_components=2, random_state=SEED).fit_transform(Xp)
px.scatter(x=coords[:, 0], y=coords[:, 1],
           color=df['anomalia'].map({False: 'normal', True: 'anomalía'}),
           color_discrete_map={'normal': PRIMARY, 'anomalía': ACCENT},
           labels={'x': 'PC1', 'y': 'PC2', 'color': ''}, title='Anomalías (PCA 2D)').show()"""

# Variante "deep": red neuronal (MLP) para clasificación
_MODEL["deep"] = """# 4 · Red neuronal (MLP) vs. baseline lineal — validación cruzada
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
scoring = 'roc_auc' if y.nunique()==2 else 'f1_macro'
cands = {'LogReg (baseline)': LogisticRegression(max_iter=1000, random_state=SEED),
         'MLP (red neuronal)': MLPClassifier(hidden_layer_sizes=(64, 32), max_iter=400,
                                             early_stopping=True, random_state=SEED)}
results = {}
for name, clf in cands.items():
    pipe = Pipeline([('prep', preprocess), ('clf', clf)])
    sc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring=scoring, n_jobs=-1)
    results[name] = sc; print(f'{name:22s} {scoring}: {sc.mean():.4f} ± {sc.std():.4f}')
best_name = max(results, key=lambda k: results[k].mean()); _b = next(k for k in results if 'baseline' in k.lower())
print(f'\\nMejor modelo: {best_name} = {results[best_name].mean():.3f} · baseline {results[_b].mean():.3f} (Δ {results[best_name].mean()-results[_b].mean():+.3f})')
best = Pipeline([('prep', preprocess), ('clf', cands[best_name])]).fit(X_train, y_train)"""
_EVAL["deep"] = _EVAL["clasificacion"]

# ── Bloques explicativos en profundidad (celdas Markdown) ─────────────────
_EXPL_EDA = """### 🔍 Cómo leer este EDA

El EDA no es decorativo: **cada hallazgo condiciona una decisión de modelado**.

- **Faltantes** → definen la estrategia de imputación. Pocos nulos se imputan (mediana en numéricas, moda en categóricas); demasiados pueden justificar descartar la columna.
- **Distribución / balance del target** → si las clases están desbalanceadas, la *accuracy* engaña; por eso más abajo evaluamos con **ROC-AUC / F1-macro**. En regresión, un target muy sesgado puede pedir transformaciones (log).
- **Distribuciones y outliers** → sesgos fuertes y valores extremos favorecen escalado robusto y modelos de árboles (que no asumen normalidad).
- **Correlaciones** → variables muy correlacionadas aportan información redundante (afecta más a modelos lineales que a árboles) y pueden anticipar multicolinealidad.
- **Cardinalidad de categóricas** → una cardinalidad alta hace explotar el *one-hot encoding*; conviene vigilarla antes de preprocesar."""

_EXPL_PREP = """### 🧪 Por qué este preprocesamiento

- **Primero separar, después transformar.** Si imputáramos o escaláramos con todo el dataset, el test "filtraría" información al entrenamiento (*data leakage*) y las métricas saldrían infladas. Por eso el split va **antes** y las transformaciones se ajustan **solo con train**, encapsuladas en un `Pipeline`.
- **Imputación:** mediana en numéricas (robusta a outliers), moda en categóricas.
- **Escalado** (`StandardScaler`): media 0, desvío 1. Crítico para modelos sensibles a la escala (lineales, basados en distancias); los árboles no lo necesitan, pero no se perjudican.
- **Encoding** (`OneHotEncoder`, `handle_unknown='ignore'`): categóricas → columnas binarias, tolerando categorías nuevas en test.
- **Split estratificado** (clasificación): preserva la proporción de clases en train y test."""

_EXPL_PREP_UNSUP = """### 🧪 Por qué este preprocesamiento

En un problema **no supervisado** no hay target ni split: el objetivo es describir la estructura de *todos* los datos.

- **Escalado** (`StandardScaler`): imprescindible acá, porque tanto K-Means como Isolation Forest se basan en **distancias**; sin escalar, las variables de mayor magnitud dominan artificialmente.
- **Encoding** de categóricas a binarias para que entren en el cálculo de distancias.
- Todo se ajusta sobre el conjunto completo (no hay fuga posible porque no hay test que predecir)."""

_EXPL_MODEL = {
"clasificacion": """### 🧠 Qué modelos y por qué

Comparo dos enfoques deliberadamente distintos:

1. **Regresión logística** — *baseline* lineal, interpretable y veloz. Si un modelo simple ya rinde, no hace falta complejidad.
2. **Random Forest** — *ensemble* de árboles: captura no linealidades e interacciones, robusto a outliers y a la escala.

**Hiperparámetros** (defaults sensatos, no un tuning exhaustivo — ese es el paso siguiente): `max_iter=1000` asegura convergencia de la logística; `n_estimators=300` da una estimación estable del bosque (con rendimientos decrecientes); `random_state=42` para reproducibilidad.

**Validación cruzada 5-fold estratificada:** en vez de un único split, promediamos 5 particiones → estimación más confiable y con su desvío. La métrica es **ROC-AUC** (binaria) o **F1-macro** (multiclase), no accuracy, porque toleran el desbalance.""",
"regresion": """### 🧠 Qué modelos y por qué

1. **Regresión lineal** — *baseline* interpretable: asume relación lineal entre features y target.
2. **Random Forest Regressor** — *ensemble* que captura no linealidades e interacciones sin que tengamos que especificarlas.

**Hiperparámetros**: defaults sensatos (`n_estimators=300`, `random_state=42`), sin tuning todavía. **Validación cruzada 5-fold** con **R²** como métrica: una estimación promediada del poder explicativo, más confiable que un único split.""",
"deep": """### 🧠 Por qué una red neuronal acá

1. **Regresión logística** — *baseline* lineal, para tener una vara honesta.
2. **MLP (perceptrón multicapa)** — red neuronal con capas ocultas `(64, 32)`: aprende representaciones no lineales de los datos tabulares.

**Decisiones de la red**: `early_stopping=True` corta el entrenamiento cuando la validación deja de mejorar (evita sobreajuste); `max_iter=400` es el techo de épocas; las capas `(64,32)` son una arquitectura modesta acorde al tamaño del dataset (redes grandes sobreajustan en pocos datos). Se compara contra el baseline con **validación cruzada** — una red solo se justifica si **supera** al modelo simple.""",
"clustering": """### 🧠 Por qué K-Means y cómo elegir *k*

**K-Means** agrupa minimizando la distancia de cada punto a su centroide. Es rápido e interpretable, ideal como primer mapeo de la estructura.

Como *k* (cantidad de grupos) no se conoce de antemano, lo elegimos con dos criterios:
- **Método del codo (inercia)**: se busca el quiebre donde sumar clusters deja de reducir mucho la inercia.
- **Coeficiente de silueta**: mide cohesión vs. separación; elegimos el *k* que lo maximiza.""",
"anomalia": """### 🧠 Por qué Isolation Forest

**Isolation Forest** aísla observaciones particionando al azar: los puntos que quedan aislados con **pocas** particiones son los más atípicos. Escala bien, no asume distribución y funciona en alta dimensión.

`contamination='auto'` deja que el algoritmo estime la proporción de anomalías. Si conocés la tasa real (p. ej. 1% de fraudes), conviene fijarla explícitamente.""",
}

_EXPL_EVAL = {
"clasificacion": """### 📊 Cómo interpretar estas métricas

- **Matriz de confusión**: la diagonal son aciertos; fuera de ella, errores. Importa *qué* clase se confunde con cuál.
- **Precision** (de lo que predije positivo, cuánto acerté) vs **Recall** (de los positivos reales, cuántos capturé): hay *trade-off*. **F1** los combina; **F1-macro** promedia por clase sin que la mayoritaria domine.
- **ROC-AUC** (binaria): probabilidad de rankear un positivo por encima de un negativo. 0.5 = azar, 1.0 = perfecto; robusta al desbalance.

**Qué inferir**: si el modelo supera al baseline y el *recall* de la clase de interés es aceptable, hay señal real. Si baseline ≈ ensemble, el problema es mayormente lineal. **Limitación**: hiperparámetros sin tunear → con `GridSearchCV` y *feature engineering* del dominio se puede mejorar.""",
"regresion": """### 📊 Cómo interpretar estas métricas

- **R²**: proporción de varianza explicada (1 = perfecto; 0 = no mejor que predecir la media; negativo = peor que la media).
- **MAE**: error absoluto medio, en las **unidades del target** (lectura directa).
- **RMSE**: penaliza más los errores grandes; si **RMSE ≫ MAE**, hay outliers con error alto.
- **Predicho vs. real**: los puntos deberían alinearse sobre la diagonal; desvíos sistemáticos = sesgo del modelo.

**Limitación**: sin tuning; probar regularización (Ridge/Lasso) y *feature engineering*.""",
"clustering": """### 📊 Cómo interpretar el clustering

- **Codo / silueta**: ya guiaron la elección de *k*. Silueta cercana a 1 = grupos compactos y separados; cerca de 0 = solapados.
- **PCA 2D**: es una *proyección* para visualizar, no la separación real en alta dimensión — grupos que se ven solapados pueden estar separados en más dimensiones.
- **Qué inferir**: caracterizá cada cluster mirando las **medias de las variables por grupo** (perfiles).

**Limitación**: K-Means asume grupos esféricos y de tamaño similar; para formas complejas conviene DBSCAN o Gaussian Mixtures.""",
"anomalia": """### 📊 Cómo interpretar las anomalías

- El **score** (`decision_function`) ordena de más a menos atípico; el histograma muestra dónde está la cola de los anómalos.
- Sin *ground truth*, la validación es **cualitativa**: revisá si los puntos marcados tienen sentido de negocio.
- En la **proyección PCA 2D**, las anomalías suelen caer en los bordes de la nube de puntos.

**Limitación**: `contamination='auto'` estima la proporción; con conocimiento del dominio conviene fijar la tasa esperada.""",
}
_EXPL_EVAL["deep"] = _EXPL_EVAL["clasificacion"]

# ── Plantillas NLP (clasificación de texto) ───────────────────────────────
_NLP_EDA = """# 2 · EDA de texto
print('Documentos:', len(df))
display(df['label'].value_counts().rename('n').to_frame())
df['_len'] = df['text'].astype(str).str.len()
display(df['_len'].describe().to_frame().T)
px.histogram(df, x='_len', nbins=50, color='label',
             title='Longitud de los textos (caracteres) por clase', labels={'_len':'caracteres'}).show()
from sklearn.feature_extraction.text import CountVectorizer
cvz = CountVectorizer(max_features=20, stop_words='english')
m = cvz.fit_transform(df['text'].astype(str))
freq = pd.Series(m.sum(axis=0).A1, index=cvz.get_feature_names_out()).sort_values()
px.bar(x=freq.values, y=freq.index, orientation='h',
       title='Tokens más frecuentes (sin stopwords)').show()"""

_NLP_PREP = """# 3 · Representación del texto
# El texto se vectoriza con TF-IDF DENTRO del Pipeline del modelo, así el
# vocabulario y los pesos IDF se ajustan solo con train (sin data leakage).
print('Listo: la vectorización TF-IDF se hace dentro del Pipeline (sección 4).')"""

_NLP_MODEL = """# 4 · TF-IDF + modelos lineales con validación cruzada
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
X = df['text'].astype(str); y = df['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=SEED, stratify=y)
def mk(clf):
    return Pipeline([('tfidf', TfidfVectorizer(max_features=20000, ngram_range=(1,2),
                      stop_words='english', sublinear_tf=True)), ('clf', clf)])
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
cands = {'LogReg (baseline)': mk(LogisticRegression(max_iter=1000, random_state=SEED)),
         'LinearSVC': mk(LinearSVC(random_state=SEED))}
results = {}
for name, pipe in cands.items():
    sc = cross_val_score(pipe, X_train, y_train, cv=cv, scoring='f1_macro', n_jobs=-1)
    results[name] = sc; print(f'{name:20s} F1-macro: {sc.mean():.4f} ± {sc.std():.4f}')
best_name = max(results, key=lambda k: results[k].mean()); _b = next(k for k in results if 'baseline' in k.lower())
print(f'\\nMejor modelo: {best_name} = {results[best_name].mean():.3f} · baseline {results[_b].mean():.3f} (Δ {results[best_name].mean()-results[_b].mean():+.3f})')
best = cands[best_name].fit(X_train, y_train)"""

_NLP_EVAL = """# 5 · Evaluación en test
from sklearn.metrics import classification_report, confusion_matrix
y_pred = best.predict(X_test)
print(classification_report(y_test, y_pred))
labels = sorted(map(str, y.unique()))
cm = confusion_matrix(y_test, y_pred)
px.imshow(cm, x=labels, y=labels, text_auto=True, color_continuous_scale='Blues',
          labels=dict(x='predicho', y='real', color='n'), title='Matriz de confusión').show()"""

_EXPL_EDA_NLP = """### 🔍 Cómo leer este EDA de texto

- **Balance de clases**: si una clase domina (p. ej. ham ≫ spam), la *accuracy* engaña → evaluamos con **F1-macro**.
- **Longitud de los textos**: distribuciones muy distintas por clase ya son señal (los spam suelen ser más cortos/largos según el caso).
- **Tokens frecuentes**: dan intuición del vocabulario; las *stopwords* se quitan para que no tapen las palabras informativas.
- Esto guía la vectorización: **TF-IDF** pondera términos frecuentes en un documento pero raros en el corpus (los más discriminativos)."""

_EXPL_MODEL["nlp"] = """### 🧠 Por qué TF-IDF + modelos lineales

Para texto, **TF-IDF + un modelo lineal** es un baseline fortísimo y rápido (a menudo difícil de superar sin transformers):

1. **TF-IDF** (`ngram_range=(1,2)`, `sublinear_tf`, `stop_words='english'`): representa cada documento por la importancia de sus términos y bigramas.
2. **Regresión logística** vs **LinearSVC**: ambos lineales sobre el espacio TF-IDF; SVM lineal suele rendir muy bien en texto disperso de alta dimensión.

El vectorizador va **dentro del `Pipeline`** → el IDF se ajusta solo con train (sin leakage). Validación cruzada 5-fold con **F1-macro** (tolera desbalance)."""

_EXPL_EVAL["nlp"] = """### 📊 Cómo interpretar estas métricas

- **F1-macro**: promedia el F1 por clase sin que la mayoritaria domine — la métrica honesta cuando hay desbalance.
- **Matriz de confusión**: revelá qué temas/clases se confunden entre sí (suelen ser los semánticamente cercanos).
- **Precision vs Recall por clase**: en spam, un *recall* alto en la clase "spam" importa más que la accuracy global.

**Limitación**: TF-IDF ignora el orden y el contexto; para problemas donde la semántica fina importa, el paso siguiente son **embeddings** (sentence-transformers) o *fine-tuning* de un transformer."""
