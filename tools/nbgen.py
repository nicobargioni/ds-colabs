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


def _banner(n: int, title: str, lede: str) -> str:
    return (f'<div class="edu-banner"><span class="eb">Sección {n:02d}</span>'
            f'<h2>{_esc(title)}</h2><p class="lede">{_esc(lede)}</p>'
            f'<span class="step">{n}</span></div>')


def _row(k: str, v: str, alt: bool = False) -> str:
    return (f'<div class="row{" alt" if alt else ""}"><div class="k">{_esc(k)}</div>'
            f'<div class="v">{_esc(v)}</div></div>')


def _marco(s: dict) -> str:
    metrica = s["ficha"].get("Métrica", s.get("metrica", ""))
    rows = (_row("Objetivo", s["objetivo"]) + _row("Hipótesis", s["hipotesis"], True)
            + _row("Datos", s["datos_desc"]) + _row("Metodología", s["metodologia"], True)
            + _row("Métrica", metrica))
    return (f'<div class="edu-banner"><span class="eb">Marco del trabajo</span>'
            f'<h2>Cómo abordo <em>el problema</em></h2>{rows}'
            f'<div class="foot">Ejecutable top-down · <b>random_state=42</b> · preprocesamiento sin data leakage.</div></div>')


def _concl(s: dict) -> str:
    items = "".join(f"<li>{x}</li>" for x in s["conclusiones"])
    return (f'<div class="edu-banner"><span class="eb">Conclusiones</span>'
            f'<h2>Hallazgos y <em>próximos pasos</em></h2><ul>{items}</ul>'
            f'<div class="foot">Nicolás Bargioni · Data Scientist · nicolasbargioni.com</div></div>')


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
    # Portada (HTML detrás de #@title; inyecta el CSS una vez)
    c.append(new_code_cell(_html_cell("📌 Portada", _portada(spec), True, seed)))
    c.append(new_code_cell(_html_cell("🧭 Marco del trabajo", _marco(spec), False, seed)))

    def banner(n, title, lede, emoji):
        c.append(new_code_cell(_html_cell(f"{emoji} {title}", _banner(n, title, lede), False, seed)))

    banner(0, "Setup", "Dependencias, imports y configuración global (reproducibilidad).", "🛠")
    c.append(new_code_cell(_SETUP))
    banner(1, "Carga de datos", "Lectura del dataset y vista inicial de la tabla.", "📥")
    c.append(new_code_cell(spec["loader_code"]))
    c.append(new_code_cell(_LOAD_CHECK))
    banner(2, "Análisis exploratorio (EDA)",
           "Forma, tipos, faltantes, distribuciones, cardinalidad, correlaciones, outliers y relación con el target.", "🔍")
    for cell in (_EDA_OVERVIEW, _EDA_MISSING,
                 _EDA_TARGET.replace("__TARGET__", T).replace("__P__", P),
                 _EDA_NUMERIC, _EDA_CATEGORICAL, _EDA_CORR, _EDA_OUTLIERS):
        c.append(new_code_cell(cell))
    banner(3, "Preprocesamiento",
           "Split antes de transformar; imputación, escalado y encoding dentro de un Pipeline (ajustado solo con train → sin leakage).", "🧪")
    c.append(new_code_cell(_SPLIT.replace("__TARGET__", T).replace("__P__", P)))
    c.append(new_code_cell(_PREPROCESS))
    banner(4, "Modelado", "Baseline interpretable vs. ensemble, comparados con validación cruzada.", "🧠")
    c.append(new_code_cell(_MODEL.get(P, _MODEL["clasificacion"])))
    banner(5, "Evaluación", "Desempeño sobre datos nunca vistos (set de test).", "📊")
    c.append(new_code_cell(_EVAL.get(P, _EVAL["clasificacion"])))
    # Conclusiones (HTML detrás de #@title)
    c.append(new_code_cell(_html_cell("✅ Conclusiones", _concl(spec), False, seed)))

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
best_name = max(results, key=lambda k: results[k].mean()); print('\\nMejor:', best_name)
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
best_name = max(results, key=lambda k: results[k].mean()); print('\\nMejor:', best_name)
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
