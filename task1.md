1. Calcule manualmente el IoU entre las dos cajas. Muestre paso a paso el cálculo del área de intersección, el área de unión y el valor final. Explique en términos no técnicos qué significa ese número para el cliente de VisorShelf.

- R: Primero sacamos las coordenadas de la intersección entre la caja predicha b_pred = (142, 89, 218, 165) y la caja real b_gt = (138, 84, 222, 170).
y de esas coordenadas, sacamos las x's, y's mínimas, siendo x mínima y, y mínima (142, 89), luego x máxima y, y máxima (218, 165). 

El ancho de la intersección es:
$$218 - 142 = 76$$
El alto de la intersección es:
$$165 - 89 = 76$$
El área de intersección es:
$$76 \times 76 = 5776$$

Luego, le sacamos el área de cada caja por separado.
Área de la caja predicha:
$$(218 - 142) \times (165 - 89) = 76 \times 76 = 5776$$
Área de la caja real: 
$$(222 - 138) \times (170 - 84) = 84 \times 86 = 7224$$
El área de unión es la suma de las dos áreas menos la intersección:
$$5776 + 7224 - 5776 = 7224$$
El IoU se calcula dividiendo la intersección entre la unión:
$$IoU = \frac{5776}{7224} = 0.7995$$
Prácticamente es un IoU de 0.80 aprox. En términos sencillos para el cliente esto significa que la caja que dibujó el sistema coincide en un 80% con la caja perfecta que anotó el radiólogo. Es una detección bastante precisa, el sistema encerró la lata casi a la perfección y solo le faltó cubrir unos bordes.

2. En la fórmula IoU = |I| / |U|, identifique qué representa cada símbolo (|I|, |U|) y explique por qué el denominador es la unión y no el área del ground truth. ¿Qué problema concreto evita esa decisión de diseño?
- R: En la fórmula:
$$IoU = \frac{|I|}{|U|}$$
El símbolo |I| representa el área de intersección, que los píxeles donde ambas cajas se traslapan, y |U| es el área de unión el espacio total que abarcan las dos cajas juntas sin contar doble el traslape. Se usa la unión en el denominador y no el área real del objeto para castigar a las cajas predichas que son muy grandes. 
Si el sistema tira una caja gigante que cubre la mitad del anaquel, la intersección con el ground truth sería completa, y si dividiéramos solo entre el ground truth, el resultado sería 100% de éxito, lo cual es mentira. Usar la unión evita ese problema, ya que una caja gigante hace que el denominador crezca un montón y el IoU se desplome a un número bajo.

3. El equipo de VisorShelf está evaluando dos umbrales de IoU para decidir si una detección es válida: θ = 0.5 y θ = 0.75. ¿Cuál recomendaría para el sistema de auditoría de anaqueles y por qué? Considere el impacto operativo de los falsos positivos y falsos negativos en el negocio del cliente.
- R: Para VisorShelf recomiendo el umbral de 0.5. En una auditoría de anaqueles lo que más importa a nivel de negocio es saber si el producto está presente para hacer el conteo del inventario, no que la caja de detección esté ajustada al milímetro. Si usamos 0.75, es un límite muy exigente; el sistema podría detectar la lata de atún pero si la caja está un poco movida, la va a descartar como inválida. Esto generaría Falsos Negativos (el sistema diría que no hay atún cuando sí hay en físico), lo que se traduce en quiebres de stock fantasma que arruinan la logística del cliente. Es mejor tener un umbral permisivo de 0.5 para asegurar el conteo real.

4. Calcule la Precisión y el Recall para esta prueba. En las fórmulas P = TP / (TP + FP) y R = TP / (TP + FN), explique verbalmente qué mide cada término del denominador y por qué ambas métricas son necesarias para evaluar el sistema.
- R: La Precisión es:
$$P = \frac{TP}{TP + FP} = \frac{12}{12 + 6} = \frac{12}{18} = 0.666$$
o sea 66.6%.
El Recall es:
$$R = \frac{TP}{TP + FN} = \frac{12}{12 + 3} = \frac{12}{15} = 0.80$$
o sea 80%.
En la Precisión, el denominador (TP + FP) representa absolutamente todas las predicciones que hizo el modelo; mide de todo lo que el sistema dijo que era un producto, cuánto era realmente un producto válido.
En el Recall, el denominador (TP + FN) representa todos los productos reales que de verdad estaban físicamente en el anaquel; mide de todo lo que había en la imagen, cuánto logró encontrar el sistema.
Se necesitan ambas métricas porque un modelo que dice que todo el anaquel está lleno de productos tendrá un Recall perfecto pero una Precisión pésima (muchos falsos positivos), y un modelo que solo marca una lata súper obvia tendrá Precisión perfecta pero un Recall terrible (se saltó todo lo demás). Se necesita el balance de las dos.

5. El director de operaciones de la tienda le dice: Prefiero que el sistema no se pierda ningún quiebre de stock, aunque a veces nos avise de falsos alarmas. Traduzca esa preferencia a términos de Precisión y Recall. ¿Qué umbral de confianza ajustaría y en qué dirección?
- R: Esa preferencia significa que al director le interesa maximizar el Recall por encima de la Precisión. Quiere que el sistema detecte absolutamente todos los productos reales (minimizando los Falsos Negativos), y está dispuesto a tolerar detecciones repetidas o de cosas que no son productos (Falsos Positivos). Para lograr esto en el detector, hay que bajar el umbral de confianza. Al hacerlo en esa dirección, el sistema se vuelve más sensible y empieza a dejar pasar más cajas candidatas; van a ocurrir más errores de falsas alarmas, pero nos aseguramos de no dejar ningún producto sin registrar.

6. Explique qué es el mAP (Mean Average Precision) y por qué es más informativo que reportar un único valor de Precisión o Recall. En su explicación, distinga entre mAP@0.5 (protocolo PASCAL VOC) y mAP@0.5:0.95 (protocolo COCO), y argumente cuál protocolo sería más exigente para VisorShelf y por qué.
- R: El mAP es una métrica global que resume el rendimiento del modelo evaluando el área bajo la curva de Precisión y Recall en distintos niveles de confianza, sacando un promedio para todas las clases de productos que detectamos. Es más informativo porque dar solo la Precisión o el Recall es como tomar una foto estática en un umbral específico; el mAP te dice qué tan robusto es el modelo en general a lo largo de diferentes parámetros.
El mAP@0.5 evalúa las detecciones usando un IoU fijo de 0.5 como requisito mínimo para considerar que la caja predicha está bien. El mAP@0.5:0.95 saca un promedio del rendimiento del modelo probando umbrales de IoU cada vez más estrictos (0.50, 0.55, 0.60, hasta 0.95).
Para VisorShelf, el protocolo COCO (0.5:0.95) sería muchísimo más exigente, porque penaliza fuertemente a las cajas que encierran el producto pero no están dibujadas de forma milimétrica sobre los bordes de la lata, haciendo que el número final de mAP caiga bastante.

7. Explique al cliente qué es el Non-Maximum Suppression (NMS) y por qué el detector genera múltiples cajas para el mismo objeto. Describa el algoritmo paso a paso en lenguaje no técnico.
- R: El detector genera múltiples cajas porque al analizar la imagen, mira los productos desde muchas cuadrículas y posiciones al mismo tiempo, y varias de esas miradas logran reconocer el mismo producto lanzando una predicción. El NMS (Supresión de No Máximos) es un filtro de limpieza que usamos para borrar esos duplicados.
Paso a paso funciona así:
Primero, el sistema agarra todas las cajas que encontró y las ordena desde la que tiene mayor seguridad (confianza) de ser un producto, hasta la que tiene menor.
Segundo, toma la caja con la confianza más alta, la guarda como definitiva y la usa como referencia principal.
Tercero, compara esa caja ganadora con todas las demás que están cerca. Si otra caja se encima demasiado sobre la ganadora, el sistema asume que están viendo el mismo objeto y la borra de la lista.
Cuarto, repite el proceso con la siguiente caja de mayor confianza que haya sobrevivido a la limpieza, hasta revisar todo el anaquel.

8. El parámetro θ_NMS controla qué tan agresivo es el NMS al suprimir cajas. En un anaquel densamente poblado donde los productos están uno junto al otro casi sin espacio, ¿qué valor de θ_NMS recomendaría (alto o bajo) y por qué? Argumente el riesgo en cada dirección.
- R: Recomendaría un valor de NMS alto. Si los productos están muy pegados uno a la par del otro en el anaquel, un NMS bajo (que es muy agresivo para limpiar) sería un problema. Al ver dos cajas de productos distintos que se traslapan un poco por lo juntos que están, el filtro borraría una de ellas pensando que es un duplicado, generando Falsos Negativos (productos ignorados). El riesgo de usar un NMS bajo es perder visibilidad del inventario. El riesgo de usar un NMS muy alto es que el filtro no limpie lo suficiente y deje cajas dobles para un solo producto, generando Falsos Positivos, pero en anaqueles densos es preferible lidiar con eso que no registrar la mercadería.

9. ¿En qué orden se deben aplicar el umbral de confianza τ y el NMS? Justifique la respuesta y explique qué sucedería computacionalmente si se invierte ese orden en un sistema que procesa 30 imágenes por minuto.
- R: El orden correcto en la tubería es aplicar primero el umbral de confianza y después el NMS. La razón es puramente por eficiencia computacional. Primero filtras y eliminas todas las cajas basura que tienen una confianza muy baja (las predicciones que la red tiró por si acaso), reduciendo miles de cajas iniciales a solo unas cuantas docenas. Luego le pasas el NMS a esas pocas cajas que quedaron.
El NMS es un algoritmo pesado porque tiene que comparar matemáticamente el traslape de cada caja contra todas las demás. Si invertimos el orden y procesamos 30 imágenes por minuto, el hardware colapsaría. Intentar hacer el cruce de áreas del NMS con las miles de predicciones crudas antes de filtrarlas por confianza consumiría toda la memoria y capacidad de procesamiento de la GPU, haciendo imposible mantener el ritmo de procesamiento en tiempo real para VisorShelf.
