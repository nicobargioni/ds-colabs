#!/usr/bin/env python3
"""
nbgen — fábrica de notebooks de Data Science con estética y rigor estilo TP2.

Genera un .ipynb ejecutable top-down en Google Colab a partir de un `spec`:
portada HTML (IPython.display) + bloque académico + secciones numeradas
(Setup → Carga → EDA exhaustivo → Preprocesamiento → Modelado → Evaluación →
Conclusiones). Comentado en español, random_state=42, sin data leakage.

Estética (firma visual, coherente con nicolasbargioni.com):
  cian #0891b2 + coral #f0521f, Space Grotesk (display) + Inter (texto),
  con una "ficha técnica" en la portada como elemento distintivo.

Uso:
  from nbgen import build, write
  write(spec, "data-ml/eda/01-...ipynb")
"""
from __future__ import annotations
import json
import os
import html as _html
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

# ── Tokens de diseño ──────────────────────────────────────────────────────
CYAN = "#0891b2"
CORAL = "#f0521f"
INK = "#0f172a"
MUTE = "#64748b"
LINE = "#e2e8f0"
FONTS = ("@import url('https://fonts.googleapis.com/css2?"
         "family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500;600&display=swap');")


# ── Portada y bloques HTML (render vía display(HTML(...))) ─────────────────
def _cover_html(s: dict) -> str:
    chips = "".join(
        f'<div style="border:1px solid {LINE};border-radius:10px;padding:12px 14px;">'
        f'<div style="font:600 10px/1 Inter,sans-serif;letter-spacing:.14em;'
        f'text-transform:uppercase;color:{CORAL};margin-bottom:6px;">{_html.escape(k)}</div>'
        f'<div style="font:500 14px/1.3 Inter,sans-serif;color:{INK};">{_html.escape(v)}</div></div>'
        for k, v in s["ficha"].items()
    )
    return f"""<div style="font-family:Inter,system-ui,sans-serif;max-width:860px;margin:0 auto;">
<style>{FONTS}</style>
<div style="border-left:6px solid {CYAN};padding:6px 0 6px 22px;margin-bottom:26px;">
  <div style="font:600 11px/1 Inter,sans-serif;letter-spacing:.22em;text-transform:uppercase;color:{CYAN};margin-bottom:12px;">
    {_html.escape(s['categoria'])} · {_html.escape(s['subtema'])}
  </div>
  <h1 style="font:700 34px/1.12 'Space Grotesk',sans-serif;color:{INK};margin:0 0 10px;">{_html.escape(s['titulo'])}</h1>
  <p style="font:400 16px/1.5 Inter,sans-serif;color:{MUTE};margin:0;max-width:640px;">{_html.escape(s['subtitulo'])}</p>
</div>
<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin-bottom:22px;">{chips}</div>
<div style="display:flex;align-items:center;gap:10px;color:{MUTE};font:500 13px/1 Inter,sans-serif;">
  <span style="color:{INK};font-weight:600;">Nicolás Bargioni</span>
  <span style="width:4px;height:4px;border-radius:50%;background:{CORAL};"></span>
  <span>Data Scientist · nicolasbargioni.com</span>
  <span style="margin-left:auto;font:600 11px/1 'Space Grotesk',monospace;color:{CYAN};">ds-colabs</span>
</div></div>"""


def _block_html(title: str, items: list[tuple[str, str]]) -> str:
    rows = "".join(
        f'<div style="margin-bottom:16px;"><div style="font:600 11px/1 Inter,sans-serif;'
        f'letter-spacing:.12em;text-transform:uppercase;color:{CORAL};margin-bottom:5px;">{_html.escape(h)}</div>'
        f'<div style="font:400 15px/1.55 Inter,sans-serif;color:{INK};">{b}</div></div>'
        for h, b in items
    )
    return f"""<div style="font-family:Inter,system-ui,sans-serif;max-width:860px;margin:0 auto;
border:1px solid {LINE};border-radius:14px;padding:26px 30px;">
<style>{FONTS}</style>
<h2 style="font:700 20px/1.2 'Space Grotesk',sans-serif;color:{INK};margin:0 0 20px;">{_html.escape(title)}</h2>
{rows}</div>"""


def _conclusion_html(items: list[str]) -> str:
    lis = "".join(
        f'<li style="margin-bottom:10px;font:400 15px/1.55 Inter,sans-serif;color:{INK};">{b}</li>'
        for b in items
    )
    return f"""<div style="font-family:Inter,system-ui,sans-serif;max-width:860px;margin:0 auto;
border-left:6px solid {CORAL};padding:4px 0 4px 22px;">
<style>{FONTS}</style>
<div style="font:600 11px/1 Inter,sans-serif;letter-spacing:.2em;text-transform:uppercase;color:{CORAL};margin-bottom:10px;">Conclusiones</div>
<ul style="margin:0;padding-left:18px;">{lis}</ul></div>"""


def _html_cell(builder_call: str) -> str:
    """Genera el código de una celda que importa HTML y lo muestra."""
    return f"from IPython.display import HTML, display\ndisplay(HTML({builder_call}))"


# ── Builder principal ──────────────────────────────────────────────────────
def build(spec: dict) -> nbformat.NotebookNode:
    nb = new_notebook()
    c = nb.cells
    P = spec["problema"]  # 'clasificacion' | 'regresion' | 'clustering'

    # Portada y bloque académico se inyectan como datos serializados (robusto).
    spec_json = json.dumps(spec, ensure_ascii=False)

    c.append(new_markdown_cell(
        f"# {spec['titulo']}\n### {spec['subtitulo']}\n\n"
        f"> **{spec['categoria']} · {spec['subtema']}** — notebook ejecutable top-down en Google Colab.\n"
        f"> Comentado en español · `random_state=42` · sin data leakage (todo el preprocesamiento dentro de `Pipeline`)."
    ))

    # Celda 1: portada HTML
    c.append(new_code_cell(
        "# Portada (IPython.display.HTML)\n"
        "from IPython.display import HTML, display\n"
        f"SPEC = {spec_json}\n"
        f"{_COVER_FN}\n"
        "display(HTML(_cover_html(SPEC)))"
    ))

    # Celda 2: bloque académico
    c.append(new_code_cell(
        f"{_BLOCK_FN}\n"
        "display(HTML(_block_html('Marco del trabajo', [\n"
        f"    ('Objetivo', {json.dumps(spec['objetivo'], ensure_ascii=False)}),\n"
        f"    ('Hipótesis', {json.dumps(spec['hipotesis'], ensure_ascii=False)}),\n"
        f"    ('Datos', {json.dumps(spec['datos_desc'], ensure_ascii=False)}),\n"
        f"    ('Metodología', {json.dumps(spec['metodologia'], ensure_ascii=False)}),\n"
        f"    ('Métrica', {json.dumps(spec['metrica'], ensure_ascii=False)}),\n"
        "])))"
    ))

    c.append(new_markdown_cell("---\n## 0 · Setup — dependencias, imports y configuración global"))
    c.append(new_code_cell(_SETUP))
    c.append(new_markdown_cell("## 1 · Carga de datos"))
    c.append(new_code_cell(spec["loader_code"]))
    c.append(new_code_cell(_LOAD_CHECK))

    c.append(new_markdown_cell(
        "## 2 · Análisis exploratorio (EDA)\n"
        "EDA exhaustivo **antes** de tocar el modelo: forma, tipos, faltantes, "
        "distribuciones, cardinalidad, correlaciones, outliers y relación con el target."
    ))
    c.append(new_code_cell(_EDA_OVERVIEW))
    c.append(new_code_cell(_EDA_MISSING))
    c.append(new_code_cell(_EDA_TARGET.replace("__TARGET__", spec.get("target", "")).replace("__P__", P)))
    c.append(new_code_cell(_EDA_NUMERIC))
    c.append(new_code_cell(_EDA_CATEGORICAL))
    c.append(new_code_cell(_EDA_CORR))
    c.append(new_code_cell(_EDA_OUTLIERS))

    c.append(new_markdown_cell(
        "## 3 · Preprocesamiento\n"
        "Split **antes** de transformar (evita leakage). Imputación + escalado + encoding "
        "encapsulados en `ColumnTransformer`/`Pipeline`, ajustados **solo con train**."
    ))
    c.append(new_code_cell(_SPLIT.replace("__TARGET__", spec.get("target", "")).replace("__P__", P)))
    c.append(new_code_cell(_PREPROCESS))

    c.append(new_markdown_cell("## 4 · Modelado"))
    c.append(new_code_cell(_MODEL.get(P, _MODEL["clasificacion"])))

    c.append(new_markdown_cell("## 5 · Evaluación"))
    c.append(new_code_cell(_EVAL.get(P, _EVAL["clasificacion"])))

    c.append(new_markdown_cell("## 6 · Conclusiones"))
    c.append(new_code_cell(
        f"{_CONCL_FN}\n"
        "display(HTML(_conclusion_html([\n"
        + "".join(f"    {json.dumps(x, ensure_ascii=False)},\n" for x in spec["conclusiones"])
        + "])))"
    ))

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

_LOAD_CHECK = """# Vista rápida de la tabla cargada (el loader debe dejar un DataFrame `df`)
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

# Las funciones HTML se serializan como texto para inyectarlas en el notebook
# (así el notebook es autocontenido y no depende de nbgen en Colab).
import inspect  # noqa: E402
_COVER_FN = inspect.getsource(_cover_html) + f"\nCYAN={CYAN!r};CORAL={CORAL!r};INK={INK!r};MUTE={MUTE!r};LINE={LINE!r};FONTS={FONTS!r}\nimport html as _html"
_BLOCK_FN = inspect.getsource(_block_html)
_CONCL_FN = inspect.getsource(_conclusion_html)
