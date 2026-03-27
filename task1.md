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

-R: Cómo transformaciones válidas considero que rotaciones leves de +-5 grados, cambios de brillo/contraste y algún zoom in ayudarían bastante. Las rotaciones dan un escenario real, ya que aunque siempre hay que seguir una cierta postura para tomar la radiografía, probablemente se de el caso donde sea necesario que el paciente se acomode de cierta forma para poder tomar una mejor muestra. Los cambios de brillo o contraste pueden ayudar para aquellas máquinas de rayos X que produzcan imagenes más claras/oscuras, o si se utiliza en alguna radiografía algo vieja que tenga cambios en la intensidad pero que sirva por el historial médico, el sistema aun pueda hacer uso de la radiografía. El zoom puede ayudar por si se busca en un lugar en específico. 

Para un ejemplo no válido podría ser una distorsión por que cambia las dimensiones del cuerpo y de esa forma no le estamos enseñando correctamente la anatomía del cuerpo humano. 

3. ¿Es el Data Augmentation suficiente por sí solo para garantizar que el modelo generalice bien? Argumente su posición considerando otras variables del proceso de entrenamiento 

-R: No como lo vimos en clase, por eso lo acompañamos de otras técnicas, como por ejemplo la de early stopping que ayuda bastante para ahorrar recursos ya que se pone a monitorear el modelo mientras entrena y se detiene si detecta que el modelo deja de aprender reglas generales. También el transfer learning, que podemos tomar un modelo preentrenado y luego lo afinamos para que entienda en este caso las radiografías. Además también está el dropout que también sirve bastante, funciona apagando algunas conexiones de la red neuronal durante el entrenamiento y con eso forzamos a que el modelo no dependa de un solo detalle para dar un diagnóstico. 

4. Identifique a partir de qué época aproximada comienza el sobreajuste (overfitting) y describa cómo se evidencia en los números de la tabla.

-R: El sobreajuste comienza a notarse alrededor de la época 15. Esto se evidencia porque, hasta la época 10, ambas métricas, la pérdida de entrenamiento y la de validación, van disminuyendo juntas. Pero, en la época 15 la pérdida de entrenamiento sigue bajando (a 0.18), pero la de validación empieza a subir (a 0.42). Para la época 25, esta brecha es enorme (0.04 vs 0.89) y esto puede significar que el modelo memorizó a la perfección los datos de entrenamiento, pero perdió totalmente su capacidad de generalizar y predecir correctamente con datos nuevos.

5. Proponga dos estrategias de regularización concretas (por ejemplo, Dropout o L2) que podría haber implementado para prevenir este comportamiento. Para cada una, explique intuitivamente qué fenómeno matemático está mitigando y qué impacto esperaría ver en las curvas de la tabla.

-R: Una estrategia sería usar Dropout, que mencioné en respuestas anteriores. Pues, al apagar neuronas al azar durante el entrenamiento, estamos mitigando el fenómeno matemático de la co-adaptación, forzando a que la red no dependa de un solo detalle o patrón específico para dar su diagnóstico. El impacto en la tabla sería que la pérdida de entrenamiento no bajaría tan rápido a 0.04, pero la pérdida de validación se mantendría mucho más baja y estable, siguiendo de cerca a la de entrenamiento.

Otra estrategia sería usar la regularización L2. Por que matemáticamente, esto penaliza que los pesos o parámetros del modelo crezcan demasiado. Esto evita que el modelo cree una función matemática excesivamente compleja o con muchos picos para ajustarse exactamente a cada variación de los datos de entrenamiento. En las curvas, esperaríamos ver que ambas pérdidas bajen de forma más gradual y paralela, evitando que la de validación se dispare a 0.89 en las últimas épocas.

6. Desde una perspectiva médica, ¿por qué es especialmente peligroso desplegar en producción un modelo que exhibe este patrón de sobreajuste para el diagnóstico de radiografías? Argumente más allá de los números.

-R: Es sumamente peligroso porque un modelo sobreajustado no aprendió a detectar la enfermedad real, sino que memorizó detalles irrelevantes de las radiografías específicas con las que se entrenó, como marcas de la máquina de rayos X, artefactos de iluminación o las posturas exactas de esos pacientes. Al desplegarlo en producción, el modelo se topará con radiografías de máquinas distintas o variaciones normales del día a día, y va a fallar. Esto se traduce en diagnósticos erróneos, donde podríamos mandar a casa a un paciente grave diciéndole que está sano solo porque su radiografía tenía un nivel de brillo distinto al que el modelo memorizó.

7. Calcule cuál sería el accuracy de un modelo naive que simplemente predice siempre 'Normal' para todas las imágenes. ¿Qué revela ese cálculo sobre el 94% reportado?

-R: Si sumamos las imágenes, tenemos un total de 850 radiografías, 700 normales + 150 con neumonía. Si un modelo naive predice siempre Normal, acertaría 700 de las 850 veces. El cálculo sería 700 / 850 = 0.8235, es decir, un 82.35% de accuracy.
Esto nos dice que el 94% reportado, aunque suena bastante bien, en realidad es algo engañoso y nos demuestra que el punto de partida ya era altísimo sin que el modelo tuviera que pensar ni detectar nada. El margen real de lo que el modelo aprendió a diagnosticar es mucho menor de lo que aparenta ese porcentaje.

8. Explique por qué, en problemas médicos con clases desbalanceadas, métricas como el F1-Score o la Sensibilidad (Recall) para la clase minoritaria son más informativas que el accuracy. No se limite a definirlas; argumente su relevancia clínica.

-R: El accuracy se deja inflar fácilmente por la clase mayoritaria, en este caso los sanos, ocultando los errores en la clase que realmente nos importa diagnosticar. El recall en cambio nos dice específicamente que, de todos los pacientes que realmente tienen neumonía, ¿cuántos logramos detectar correctamente? 
La relevancia clínica de esto es muy importante ya que en la práctica médica equivocarse diciendo que alguien está Normal cuando en realidad está enfermo, un Falso Negativo, puede costar una vida al retrasar el tratamiento adecuado. Generalmente es preferible tener algunos Falsos Positivos (alertas de neumonía que luego el médico descarta) a que se escape un paciente grave. El F1-Score es útil aquí porque nos da un equilibrio entre qué tan precisos somos y cuántos casos reales estamos logrando abarcar, dándonos una visión honesta de si el modelo es seguro para usar en la vida real.

9. Como director técnico, ¿cómo le respondería al inversionista de forma honesta y profesional? Redacte una respuesta breve (3 a 5 oraciones) que sea técnicamente sólida pero comprensible para un no-especialista.

-R: Ese 94% de precisión general suena excelente, pero en nuestro caso puede ser engañoso porque la gran mayoría de las radiografías que recibimos son de pacientes sanos; de hecho, si el sistema adivinara sano a ciegas para todas las imágenes, ya tendría más de un 82% de acierto automático. Para garantizar que nuestro producto es verdaderamente seguro y confiable para los médicos, no podemos basarnos solo en el promedio general. Necesitamos evaluar el sistema utilizando métricas clínicas especializadas que nos demuestren específicamente su capacidad para no dejar escapar ningún caso real de neumonía, priorizando la seguridad del paciente por encima de un porcentaje general que se vea bien en el reporte.
