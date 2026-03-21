[Repositorio](https://github.com/donmatthiuz/VIC/tree/lab7)
---
# Task 1

## Pregunta 1.1
El médico coordinador del proyecto le presenta la siguiente situación: "Tenemos 800 radiografías etiquetadas por nuestros radiólogos. Un colega me dijo que con tan pocos datos el modelo va a memorizar todo y no va a servir para nada en producción."
Como ingeniero de IA a cargo, usted decide aplicar Data Augmentation como parte de la solución. Sin embargo, el médico le pregunta: "¿No estamos inventando datos falsos que podrían confundir al modelo?"
Con esto en mente, responda las siguientes preguntas en su reporte:

1. Explíquele al médico, en términos que él pueda entender, qué es el Data Augmentation y por qué las imágenes generadas no son datos falsos. Use la analogía que considere más apropiada.

-R: El Data Augmentation consiste en, por ejemplo, tomar radiografías reales que ya existen y aplicarles ligeras variaciones visuales, como girar la imagen un par de grados, hacer un pequeño zoom, o cambiar el brillo y el contraste. La imagen original y la información médica que contiene siguen siendo 100% reales y lo único que cambia es que la estamos presentando bajo diferentes condiciones.

Una analogía podría ser si imagina que le está enseñando a un niño a reconocer un carro usando una sola fotografía tomada de frente y a plena luz del día. Si el niño memoriza solo esa imagen, el día que vea ese mismo carro de lado, de noche, o un poco sucio, no lo va a reconocer.

Y esto lo hacemos, ya que evitamos que el modelo simplemente memorice las imágenes perfectas. Y lo obligamos a que realmente aprenda a identificar el problema médico, preparándolo para el mundo real donde las radiografías muchas veces salen un poco movidas, descentradas o con diferente iluminación dependiendo de la máquina.


2. En el contexto específico de radiografías de tórax, proponga tres transformaciones de Data Augmentation que serían válidas y justifique cada una. Luego, identifique una transformación que no debería aplicarse en este dominio médico y explique por qué podría comprometer la integridad diagnóstica del modelo.

Cómo transformaciones válidas considero que rotaciones leves de +-5 grados, cambios de brillo/contraste y algún zoom in ayudarían bastante. Las rotaciones dan un escenario real, ya que aunque siempre hay que seguir una cierta postura para tomar la radiografía, probablemente se de el caso donde sea necesario que el paciente se acomode de cierta forma para poder tomar una mejor muestra. Los cambios de brillo o contraste pueden ayudar para aquellas máquinas de rayos X que produzcan imagenes más claras/oscuras, o si se utiliza en alguna radiografía algo vieja que tenga cambios en la intensidad pero que sirva por el historial médico, el sistema aun pueda hacer uso de la radiografía. El zoom puede ayudar por si se busca en un lugar en específico. 

Para un ejemplo no válido podría ser una distorsión por que cambia las dimensiones del cuerpo y de esa forma no le estamos enseñando correctamente la anatomía del cuerpo humano. 

3. ¿Es el Data Augmentation suficiente por sí solo para garantizar que el modelo generalice bien? Argumente su posición considerando otras variables del proceso de entrenamiento 

No como lo vimos en clase, por eso lo acompañamos de otras técnicas, como por ejemplo la de early stopping que ayuda bastante para ahorrar recursos ya que se pone a monitorear el modelo mientras entrena y se detiene si detecta que el modelo deja de aprender reglas generales. También el transfer learning, que podemos tomar un modelo preentrenado y luego lo afinamos para que entienda en este caso las radiografías. Además también está el dropout que también sirve bastante, funciona apagando algunas conexiones de la red neuronal durante el entrenamiento y con eso forzamos a que el modelo no dependa de un solo detalle para dar un diagnóstico. 
