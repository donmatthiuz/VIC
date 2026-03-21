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
