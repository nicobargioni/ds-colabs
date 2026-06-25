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
from style import EDU_CSS  # noqa: E402

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


def _marco(s: dict) -> str:
    metrica = s["ficha"].get("Métrica", s.get("metrica", ""))
    return f"""<div class="edu edu-sheet">
  <span class="edu-eyebrow">Marco del trabajo</span>
  <h2>1 · Objetivo</h2><p>{_esc(s["objetivo"])}</p>
  <h2 class="alt">2 · Hipótesis</h2>
  <div class="edu-note">{_esc(s["hipotesis"])}</div>
  <h2>3 · Datos</h2><p>{_esc(s["datos_desc"])}</p>
  <h2 class="alt">4 · Metodología</h2><p>{_esc(s["metodologia"])}</p>
  <h2>5 · Métrica de evaluación</h2>
  <div class="edu-ok">{_esc(metrica)}</div>
  <div class="edu-foot">Notebook ejecutable top-down · <code>random_state=42</code> · preprocesamiento sin data leakage.</div>
</div>"""


def _concl(s: dict) -> str:
    items = "".join(f"<li>{x}</li>" for x in s["conclusiones"])
    return f"""<div class="edu edu-sheet">
  <span class="edu-eyebrow">Conclusiones</span>
  <h2>Hallazgos y próximos pasos</h2>
  <ul>{items}</ul>
  <div class="edu-foot">Nicolás Bargioni · Data Scientist · nicolasbargioni.com</div>
</div>"""


def _html_cell(title: str, inner_html: str, with_css: bool, seed: str) -> str:
    body = (EDU_CSS if with_css else "") + _wrap(inner_html, seed)
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

    c.append(new_markdown_cell("## 0 · Setup"))
    c.append(new_code_cell(_SETUP))
    c.append(new_markdown_cell("## 1 · Carga de datos"))
    c.append(new_code_cell(spec["loader_code"]))
    c.append(new_code_cell(_LOAD_CHECK))
    c.append(new_markdown_cell(
        "## 2 · Análisis exploratorio (EDA)\nForma, tipos, faltantes, distribuciones, "
        "cardinalidad, correlaciones, outliers y relación con el target."))
    for cell in (_EDA_OVERVIEW, _EDA_MISSING,
                 _EDA_TARGET.replace("__TARGET__", T).replace("__P__", P),
                 _EDA_NUMERIC, _EDA_CATEGORICAL, _EDA_CORR, _EDA_OUTLIERS):
        c.append(new_code_cell(cell))
    c.append(new_markdown_cell(
        "## 3 · Preprocesamiento\nSplit antes de transformar; imputación + escalado + "
        "encoding dentro de `Pipeline` (se ajustan solo con train → sin leakage)."))
    c.append(new_code_cell(_SPLIT.replace("__TARGET__", T).replace("__P__", P)))
    c.append(new_code_cell(_PREPROCESS))
    c.append(new_markdown_cell("## 4 · Modelado"))
    c.append(new_code_cell(_MODEL.get(P, _MODEL["clasificacion"])))
    c.append(new_markdown_cell("## 5 · Evaluación"))
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
for _p in ['datasets', 'seaborn']:
    if importlib.util.find_spec(_p) is None:
        subprocess.run([sys.executable, '-m', 'pip', '-q', 'install', _p])

# 0.2 Imports
import warnings; warnings.filterwarnings('ignore')
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold, KFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

# 0.3 Configuración global (reproducibilidad + estética)
SEED = 42
np.random.seed(SEED)
pd.set_option('display.max_columns', 60)
sns.set_theme(style='whitegrid'); plt.rcParams['figure.dpi'] = 110
PRIMARY, ACCENT = '#0891b2', '#f0521f'
print('Setup OK · numpy', np.__version__, '· pandas', pd.__version__)"""

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
na = df.isna().sum(); na = na[na > 0].sort_values(ascending=False)
if len(na):
    display(pd.DataFrame({'faltantes': na, '%': (na/len(df)*100).round(2)}))
    plt.figure(figsize=(7, max(2, 0.4*len(na))))
    sns.barplot(x=na.values, y=na.index, color=PRIMARY)
    plt.title('Faltantes por columna'); plt.xlabel('cantidad'); plt.tight_layout(); plt.show()
else:
    print('Sin valores faltantes.')"""

_EDA_TARGET = """# 2.3 Variable objetivo
TARGET = "__TARGET__"
if TARGET and TARGET in df.columns:
    if "__P__" == 'regresion':
        display(df[TARGET].describe().to_frame())
        plt.figure(figsize=(6,3)); sns.histplot(df[TARGET], kde=True, color=PRIMARY)
        plt.title(f'Distribución de {TARGET}'); plt.tight_layout(); plt.show()
    else:
        vc = df[TARGET].value_counts(dropna=False)
        display(pd.DataFrame({'n': vc, '%': (vc/len(df)*100).round(2)}))
        plt.figure(figsize=(5,3)); sns.barplot(x=vc.index.astype(str), y=vc.values, color=PRIMARY)
        plt.title(f'Balance — {TARGET}'); plt.ylabel('n'); plt.tight_layout(); plt.show()
        imb = vc.min()/vc.max()
        print(f'Ratio min/max de clases: {imb:.2f}' + ('  ⚠️ desbalanceado' if imb < 0.4 else ''))
else:
    print('Sin target supervisado en esta etapa.')"""

_EDA_NUMERIC = """# 2.4 Distribuciones de variables numéricas
num_cols = df.select_dtypes(include='number').columns.tolist()
if num_cols:
    display(df[num_cols].describe().T)
    cols = num_cols[:9]; rows = (len(cols)+2)//3
    fig, axes = plt.subplots(rows, 3, figsize=(13, 3*rows))
    for ax, col in zip(np.ravel(axes), cols):
        sns.histplot(df[col].dropna(), kde=True, ax=ax, color=PRIMARY); ax.set_title(col, fontsize=10)
    for ax in np.ravel(axes)[len(cols):]: ax.axis('off')
    plt.tight_layout(); plt.show()
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
    corr = df[num_cols].corr(numeric_only=True)
    plt.figure(figsize=(min(1+0.7*len(num_cols),12), min(1+0.6*len(num_cols),10)))
    sns.heatmap(corr, annot=len(num_cols)<=12, fmt='.2f', cmap='coolwarm', center=0, square=True)
    plt.title('Correlaciones'); plt.tight_layout(); plt.show()
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
from sklearn.metrics import (classification_report, confusion_matrix,
    ConfusionMatrixDisplay, RocCurveDisplay)
y_pred = best.predict(X_test)
print(classification_report(y_test, y_pred))
binary = y.nunique() == 2
fig, ax = plt.subplots(1, 2 if binary else 1, figsize=(11,4) if binary else (5,4))
ax0 = ax[0] if binary else ax
ConfusionMatrixDisplay(confusion_matrix(y_test, y_pred),
    display_labels=sorted(map(str, y.unique()))).plot(ax=ax0, cmap='Blues', colorbar=False)
ax0.set_title('Matriz de confusión')
if binary:
    RocCurveDisplay.from_estimator(best, X_test, y_test, ax=ax[1], color=ACCENT); ax[1].set_title('Curva ROC')
plt.tight_layout(); plt.show()""",
"regresion": """# 5 · Evaluación en test (datos nunca vistos)
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
y_pred = best.predict(X_test)
print(f'R2  : {r2_score(y_test, y_pred):.4f}')
print(f'MAE : {mean_absolute_error(y_test, y_pred):.4f}')
print(f'RMSE: {mean_squared_error(y_test, y_pred)**0.5:.4f}')
plt.figure(figsize=(5,5)); plt.scatter(y_test, y_pred, alpha=.4, color=PRIMARY)
lims = [min(y_test.min(), y_pred.min()), max(y_test.max(), y_pred.max())]
plt.plot(lims, lims, '--', color=ACCENT); plt.xlabel('real'); plt.ylabel('predicho')
plt.title('Predicho vs. real'); plt.tight_layout(); plt.show()""",
}
