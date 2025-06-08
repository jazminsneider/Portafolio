# Generación de Música con Autoencoder y VAE

---

## Objetivo

El objetivo de este trabajo fue **explorar la compresión y generación de audio** utilizando autoencoders y modelos generativos, aplicando técnicas de reducción de dimensión y posterior manipulación del espacio latente para la creación de nuevos sonidos.

---

## Etapa 1: Autoencoder

- Se diseñó un **autoencoder** para trabajar con archivos de audio.
- El modelo fue entrenado para **comprimir** los audios y luego **reconstruirlos** a partir del espacio latente.
- Se logró llegar a un **espacio latente muy pequeño**, manteniendo una **pérdida de calidad mínima** respecto a los audios originales.
- El resultado fue un modelo capaz de representar audios de manera compacta sin sacrificar su contenido perceptual.

---

## Etapa 2: Manipulación del Espacio Latente

- Una vez obtenido el espacio latente, se exploraron distintas formas de **generar música**:
  - Se introdujo **ruido aleatorio** al espacio latente.
  - Se **mezclaron espacios latentes** de distintos audios para obtener resultados híbridos.
- Esto permitió **modificar y generar nuevas representaciones latentes**, que luego eran decodificadas para producir nuevos sonidos.

---

## Etapa 3: VAE (Variational Autoencoder)

- Finalmente se implementó un **VAE** (Variational Autoencoder) entrenado sobre un dataset de audios.
- Este modelo no solo comprime la información, sino que también genera una distribución continua y manipulable en el espacio latente.
- El objetivo fue que el modelo pudiera **reproducir sonidos nuevos** al muestrear directamente del espacio latente aprendido.

---

## Tecnologías utilizadas

- Lenguaje: **Python**
- Librerías: `TensorFlow` / `PyTorch`, `librosa` (para manejo de audio), `numpy`, `matplotlib` (para visualización)

---

## Conclusiones

- Se logró **reducir de forma efectiva** audios a un espacio latente pequeño con mínima pérdida.
- La manipulación del espacio latente permitió **crear variaciones musicales interesantes**.
- El uso de VAE facilitó una generación más estructurada y coherente de nuevos sonidos.

---

## Próximos pasos

- Entrenar con **datasets más variados o específicos por género musical**.
- Incorporar técnicas de **music style transfer** o **control de parámetros musicales** desde el espacio latente.
