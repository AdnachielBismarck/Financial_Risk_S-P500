# 🧠 PROJECT CONTINUITY GUIDE  
## Financial Extreme Risk Modeling (Poisson + GARCH + Dash)

---

# 🎯 OBJETIVO DEL PROYECTO

Desarrollar un sistema de análisis de riesgo financiero que modele la ocurrencia de eventos extremos en mercados (caídas severas) usando:

- Proceso de Poisson no homogéneo
- Modelos de volatilidad (GARCH)
- Visualización interactiva (Dash)
- Despliegue en Render

---

# 📊 DEFINICIÓN DEL PROBLEMA

El proyecto NO predice precios.

El objetivo es:

> Modelar la probabilidad de eventos extremos en el tiempo en función de la volatilidad del mercado.

Evento extremo:
- caída significativa del retorno diario
- definido mediante percentil o múltiplos de desviación estándar

---

# 📁 ESTRUCTURA DEL PROYECTO
financial-risk-project/
│
├── data/
│ ├── raw/ # Datos originales (NO modificar)
│ └── processed/ # Datos listos para modelado
│
├── notebooks/
│ ├── 01_data_collection.ipynb
│ ├── 02_feature_engineering.ipynb
│ ├── 03_modeling.ipynb
│
├── src/
│ ├── features.py # Returns, volatilidad, eventos
│ ├── models.py # GARCH, Poisson, baseline
│ └── utils.py # Funciones auxiliares
│
├── app/
│ └── app.py # Dashboard Dash
│
├── reports/
│ └── executive_report.pdf
│
├── requirements.txt
├── render.yaml
└── README.md


---

# 🔄 PIPELINE GENERAL

1. Descarga de datos
2. Limpieza
3. Feature engineering
4. Definición de eventos extremos
5. Modelado:
   - GARCH → volatilidad
   - Poisson → eventos
6. Evaluación
7. Dashboard
8. Reporte

---

# 📊 DATOS

Fuente:
- Yahoo Finance

Ticker principal:
- ^GSPC (S&P 500)

Periodo:
- 2010-01-01 a 2024-12-31

Frecuencia:
- diaria

---

# 🧮 DEFINICIONES MATEMÁTICAS CLAVE

## Log-returns
r_t = log(P_t / P_{t-1})

## Volatilidad
- rolling std o GARCH

## Evento extremo
Y_t = 1 si r_t < umbral
Y_t = 0 en otro caso

Umbral recomendado:
- percentil 5
- o r_t < -2σ

---

# ⚙️ MODELOS

---

## 1. GARCH(1,1)

Objetivo:
- modelar volatilidad dinámica

Salida:
- σ_t (volatilidad)

Parámetros:
- α (constante)
- β (shock reciente)
- γ (persistencia)

Limitaciones:
- simetría
- sensible a outliers

---

## 2. Proceso de Poisson no homogéneo

Objetivo:
- modelar frecuencia de eventos extremos

Modelo:

λ(t) = exp(α + β * σ_t)

Entrada:
- σ_t (de GARCH o rolling)

Salida:
- intensidad de eventos

Interpretación:
- λ(t) alto → mayor riesgo

Limitaciones:
- depende del umbral de eventos
- asume independencia condicional

---

## 3. Modelo baseline

Opcional:
- regresión logística

Objetivo:
- comparación

---

# 📓 NOTEBOOKS (RESPONSABILIDADES)

---

## 01_data_collection.ipynb

Responsabilidades:
- descargar datos
- validar datos
- guardar en data/raw

NO debe:
- transformar datos
- hacer modelos

---

## 02_feature_engineering.ipynb

Responsabilidades:
- calcular log-returns
- calcular volatilidad
- definir eventos extremos
- guardar en data/processed

---

## 03_modeling.ipynb

Responsabilidades:
- entrenar GARCH
- estimar volatilidad
- ajustar modelo Poisson
- comparar modelos
- visualizar resultados

---

# 🧩 SRC (CÓDIGO REUTILIZABLE)

---

## features.py

Funciones esperadas:
- compute_returns()
- compute_volatility()
- define_extreme_events()

---

## models.py

Funciones esperadas:
- fit_garch()
- predict_volatility()
- fit_poisson()
- predict_intensity()

---

## utils.py

Funciones:
- métricas
- helpers

---

# 📊 DASHBOARD (app/app.py)

Debe incluir:

## Vista 1: Overview
- precio
- returns

## Vista 2: Eventos extremos
- marcados en serie

## Vista 3: Volatilidad
- dinámica en el tiempo

## Vista 4: Riesgo
- λ(t)
- probabilidad de evento

---

# 🌐 DESPLIEGUE (RENDER)

Archivo:
- render.yaml

Comando:
- python app/app.py

Requisitos:
- app debe correr sin errores locales
- puerto dinámico (Render lo asigna)

---

# ⚠️ DECISIONES CRÍTICAS

---

## Umbral de evento extremo
- percentil vs desviación estándar

---

## Ventana de volatilidad
- 20 días (recomendado)

---

## Train/Test
- train: 2010–2019
- test: 2020–2024

---

# ❌ ERRORES A EVITAR

- predecir precios directamente
- mezclar notebooks
- no documentar decisiones
- no validar datos
- dashboards sin interpretación

---

# 🚀 ESTADO ACTUAL (ACTUALIZAR MANUALMENTE)

[ ] Data descargada  
[ ] Features creadas  
[ ] Eventos definidos  
[ ] GARCH implementado  
[ ] Poisson implementado  
[ ] Dashboard iniciado  
[ ] Reporte escrito  

---

# 🧠 CONTEXTO PARA FUTURAS IA

Este proyecto busca:

- destacar en roles de Data Science / Risk / Quant
- demostrar uso de modelos estocásticos
- evitar enfoques triviales (predicción de precios)

El enfoque principal es:
👉 modelado de riesgo interpretable

---

# 📌 SIGUIENTE PASO

Implementar:

01_data_collection.ipynb

- descarga
- validación
- guardado en data/raw

---