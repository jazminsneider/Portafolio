# Predicción de Cancelaciones de Reservas con Árboles de Decisión en R

En este proyecto trabajamos con un conjunto de datos descargado desde **Kaggle** que contiene información sobre reservas de hotel realizadas por distintas personas, incluyendo si cada reserva fue cancelada o no. El objetivo principal fue **predecir la cancelación de una reserva** basándonos en las distintas variables disponibles.

---

## Análisis Exploratorio de Datos

Antes de construir el modelo, realizamos un análisis exploratorio para entender mejor los datos:

- Estudiamos la **correlación entre la variable objetivo (cancelación) y el resto de las variables**.
- Como las reservas incluían fechas, decidimos **agruparlas por mes**, para detectar patrones estacionales en las cancelaciones.
- Convertimos las **variables tipo string a categóricas**, facilitando así su inclusión en el modelo de árbol de decisión.

---

## División del Dataset

Dividimos el conjunto de datos en tres partes:

- **Entrenamiento**: 70%
- **Validación**: 15%
- **Test**: 15%

Esta división nos permitió entrenar el modelo, ajustarlo con validación y finalmente evaluarlo con datos nunca antes vistos.

---

## Modelo: Árbol de Decisión

El modelo central fue un **árbol de decisión** implementado en **R**. Para mejorarlo, trabajamos en la optimización de sus hiperparámetros:

### Hiperparámetros Optimizados

1. **`max_depth`**  
   - Define la **profundidad máxima** del árbol.
   - Rango probado: **1 a 30**.
   - A mayor profundidad, mayor capacidad para capturar complejidad, pero también mayor riesgo de **overfitting**.

2. **`min_split`**  
   - Número mínimo de observaciones necesarias para **dividir un nodo**.
   - Controla el crecimiento del árbol evitando divisiones con pocos datos, lo cual ayuda a **reducir la varianza**.

3. **`min_bucket`**  
   - Tamaño mínimo de los grupos o **“buckets”** en las hojas.
   - Evita la creación de hojas con muy pocas observaciones que puedan generar **predicciones inestables**.

> Dado el amplio rango de valores posibles para `min_split` y `min_bucket`, se probaron múltiples combinaciones buscando un equilibrio entre **rendimiento del modelo** y **tiempo de ejecución razonable**.

---

## Evaluación del Modelo

Durante la optimización, utilizamos la **curva ROC** para analizar el efecto de cada hiperparámetro individualmente sobre el rendimiento. Esto permitió visualizar cómo variaba la capacidad del modelo para clasificar correctamente según cada ajuste.

---

## Experimento Extra

Como prueba de robustez, realizamos un experimento adicional en el que:

- **Reemplazamos aleatoriamente algunos valores por `NA`** en distintas variables de reserva.
- Observamos cómo se comportaba el modelo con **datos incompletos**, evaluando así su tolerancia ante la falta de información.

---

## Tecnologías utilizadas

- Lenguaje: **R**
- Paquetes principales: `rpart`, `rpart.plot`, `pROC`, `dplyr`, `ggplot2`

---

## Conclusión

El uso de árboles de decisión junto con un buen preprocesamiento y selección de hiperparámetros resultó ser una estrategia efectiva para abordar el problema de predicción de cancelaciones. Las curvas ROC ayudaron a interpretar y afinar el modelo, mientras que la introducción de `NA`s permitió poner a prueba su robustez.
