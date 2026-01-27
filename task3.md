# Task 3 – Evaluación de Ingeniería y Criterio

## Experimento A: El efecto de Sigma (σ)

**Imágenes de referencia:**
[Experimento A](./outputs/experimento_A_sigma.png)

### 1. Generación de versiones (Resultados)
Se generaron las detecciones de bordes variando el suavizado Gaussiano sobre una imagen con ruido tipo "Sal y Pimienta".
* **Imagen Original:** 
[Original](./outputs/A_original.png)
* **Imagen con Ruido:** 
[Ruido](./outputs/A_con_ruido.png)

### 2. Análisis de Resultados

* **¿Qué pasa con los bordes finos cuando σ es muy alto (σ=5)?**
    * Los bordes finos se difuminan excesivamente.
    * La ubicación precisa del borde se vuelve una mancha gruesa, reduciendo la resolución espacial.
    * Como se observa en la imagen las grietas del suelo casi desaparecen, dejando solo sombras vagas.

[Borde sigma5](./outputs/A_bordes_sigma5.png )

* **¿Qué pasa con la textura del suelo cuando no hay suavizado?**
    * El detector de bordes (Sobel) es un filtro de paso alto, por lo que amplifica drásticamente el ruido de alta frecuencia.
    * Como se ve en la imagen cada grano de "sal y pimienta" y la textura rugosa del asfalto se detectan erróneamente como bordes, haciendo la imagen inútil para la navegación.

[Bordes sin suavizado](./outputs/A_bordes_sin_suavizado.png )

* **Selección de Ingeniería (Pallets vs. Grietas):**
    * **Elección:** Elegiría el filtro con **Gaussiano σ = 5** (o incluso mayor).
    * **Justificación:** En una aplicación de robótica industrial, los pallets son objetos grandes con geometría definida, mientras que las grietas del suelo son detalles finos. Al usar un Sigma alto, actuamos como un filtro Low-Pass que elimina el ruido del suelo y las grietas irrelevantes, dejando solo las estructuras grandes para ser procesadas, ahorrando cómputo y evitando falsos positivos.

---

## Experimento B: Histéresis Manual vs. Canny

**Imágenes de referencia:**
[Experimento B](./outputs/experimento_B_histeresis.png)
[Comparación](./outputs/experimento_B_comparacion.png)

### 1. Búsqueda del Umbral Único (T)
* Se intentó aislar los bordes usando umbralización simple.
* **T=30:** Demasiado ruido de fondo.
* **T=50:** Compromiso medio, pero aún ruidoso.
* **T=80 / T=120:** El ruido desaparece, pero se pierden partes importantes de las grietas.

### 2. Observación de Resultados
* **¿Se rompen las líneas de los bordes?**
    * Sí. Al usar un umbral simple (por ejemplo, T=80), si la intensidad de un borde varía levemente a lo largo de la línea (pasando de 81 a 79), el borde se corta abruptamente, generando líneas discontinuas o fragmentadas.

### 3. Pregunta Crítica: Umbral Simple vs. Histéresis

* **Por qué el umbral simple es menos efectivo:**
    * El umbral simple es una decisión binaria local (pixel por pixel) sin contexto. Si un pixel está por debajo de T, se descarta, sin importar si es parte de una línea larga. Esto hace que los bordes débiles desaparezcan.

* **El problema que resuelve la Histéresis (Conectividad) en robótica:**
    * **Contexto:** Un robot en movimiento sufre vibraciones que causan que la luz incida con ángulos ligeramente distintos cuadro a cuadro, haciendo que la intensidad de los bordes fluctúe (ej. un borde oscila entre valores de 40 y 60).
    * **Solución:** La histéresis usa dos umbrales ($T_{alto}$ y $T_{bajo}$).
        1.  Solo inicia un borde si supera $T_{alto}$ (borde fuerte seguro).
        2.  Mantiene el borde conectado incluso si la intensidad cae hasta $T_{bajo}$, siempre y cuando esté tocando a un pixel fuerte.
    * Esto garantiza **continuidad topológica**: aunque el robot vibre y la intensidad del borde baje momentáneamente, la línea no se "rompe" ni parpadea en el mapa de visión del robot, permitiendo una navegación estable.
