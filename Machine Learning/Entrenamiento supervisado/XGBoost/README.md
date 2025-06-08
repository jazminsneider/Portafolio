# Predicción de Probabilidad de Click con XGBoost

En este proyecto, el objetivo fue **predecir la probabilidad de que un usuario haga click**, trabajando con un conjunto de datos donde la mayoría de las variables no tenían nombre ni descripción clara.

---

## Estructura del Dataset

- La mayoría de las columnas no tenían nombres significativos.
- Les asignamos nombres genéricos como `categórica_1`, `categórica_2`, `numérica_1`, etc.
- A pesar de esta limitación, exploramos posibles relaciones entre variables y **creamos nuevas variables categóricas combinando otras existentes** para capturar posibles patrones ocultos.

---

## Modelo Utilizado: XGBoost

- Usamos la librería **`xgboost`** junto con **`XGBClassifier`** para construir el modelo.
- Dado que el espacio de hiperparámetros es amplio, realizamos una búsqueda aleatoria (**`RandomizedSearchCV`**) para encontrar la mejor combinación de parámetros que maximizara el rendimiento del modelo.

---

## Optimización del Modelo

Algunos de los hiperparámetros que exploramos fueron:

- `n_estimators`: número de árboles.
- `max_depth`: profundidad máxima del árbol.
- `learning_rate`: tasa de aprendizaje.
- `subsample`, `colsample_bytree`: proporciones de muestreo.
- `min_child_weight`, `gamma`: control de complejidad.
- `reg_alpha`, `reg_lambda`: regularización.

Esta optimización fue clave para **mejorar el AUC-ROC del modelo** y evitar problemas como el sobreajuste.

---

## Resultado

> Finalmente, obtuvimos un **AUC-ROC de 0.85**, lo cual indica un buen desempeño en la predicción de la probabilidad de click.

---

## Lecciones Aprendidas

- Aunque las variables no eran interpretables, fue posible **extraer valor mediante ingeniería de características**.
- XGBoost demostró ser una herramienta potente incluso cuando se tiene poca información semántica sobre los datos.

---

## Tecnologías utilizadas

- Lenguaje: **Python**
- Librerías principales: `xgboost`, `scikit-learn`, `pandas`, `numpy`

---

## Conclusión

A pesar de trabajar con un dataset sin descripciones claras, el uso de XGBoost y una buena estrategia de ingeniería de variables y búsqueda de hiperparámetros permitió construir un modelo sólido para predecir la probabilidad de click con buenos resultados de evaluación.
