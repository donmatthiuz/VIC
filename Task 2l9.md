# Task 2

## 1.

El problema se origina en el funcionamiento del **Non-Maximum Suppression (NMS)**, que utiliza el **IoU (Intersección sobre Unión)** para eliminar cajas redundantes. El IoU entre dos cajas \(A\) y \(B\) se define como:

$$
IoU(A,B) = \frac{|A \cap B|}{|A \cup B|}
$$

Este valor mide qué tanto se traslapan dos cajas. Si el IoU es alto, significa que ocupan casi la misma región de la imagen.

El NMS ordena las cajas por confianza y conserva la de mayor score. Luego elimina todas las demás cajas cuyo IoU con esa caja sea mayor que un umbral. Matemáticamente, si \(IoU > \theta\), la caja se descarta. Este criterio funciona bien cuando las cajas realmente representan el mismo objeto.

Sin embargo, en este caso los clones están muy juntos, superpuestos y parcialmente ocluidos. Esto provoca que las cajas de personas distintas tengan un IoU alto. Por ejemplo, si dos personas están muy cerca, sus cajas pueden tener un IoU de 0.7 u 0.8, aunque sean individuos diferentes.

Por lo tanto, el NMS interpreta erróneamente que son duplicados y elimina una de ellas. Esto genera **falsos negativos**, ya que la red sí detectó a las personas, pero el postprocesamiento las elimina debido al alto traslape.

---

## 2.

Si el umbral de IoU del NMS se ajusta a **0.15**, el criterio de eliminación se vuelve muy estricto. En este caso, cualquier par de cajas con:

$$
IoU > 0.15
$$

será considerado redundante. Esto es problemático porque en una escena con muchas personas juntas, es normal que las cajas tengan ese nivel de traslape. Como resultado, el NMS eliminará muchas detecciones correctas.

En cambio, si el umbral se ajusta a **0.95**, el NMS se vuelve muy permisivo. Solo eliminará cajas que tengan un traslape extremadamente alto, es decir, casi idénticas. Esto permite que varias detecciones de personas cercanas se mantengan, reduciendo los falsos negativos.

Sin embargo, un umbral tan alto también implica que pueden sobrevivir múltiples cajas sobre una misma persona, generando duplicados. Es decir, mejora la detección de personas reales, pero aumenta el ruido en la salida.

Para este problema de alta densidad, es preferible un umbral alto. Entre las opciones dadas, **0.95 es más adecuado que 0.15**, porque evita la eliminación excesiva de detecciones válidas. Aunque no es perfecto, reduce el problema principal que es la desaparición de personas.

---

## 3.

YOLOv10 aborda este problema desde la arquitectura del modelo, reduciendo la dependencia del NMS. Utiliza un enfoque llamado **Dual Label Assignment**, que mejora la forma en que se asignan las predicciones a los objetos reales durante el entrenamiento.

En modelos como YOLOv8, la red genera muchas cajas superpuestas y luego el NMS decide cuáles eliminar. Esto funciona mal en escenas densas, porque el NMS no puede diferenciar entre cajas duplicadas y objetos distintos muy cercanos.

YOLOv10, en cambio, aprende a producir predicciones más precisas desde el inicio. Esto significa que cada objeto tiene una mejor representación individual, incluso cuando hay oclusión o múltiples instancias de la misma clase muy juntas.

Como resultado, el modelo genera menos cajas redundantes y no necesita depender tanto de un NMS agresivo. Esto permite mantener más detecciones correctas en escenas complejas, reduciendo los falsos negativos causados por el traslape entre objetos.