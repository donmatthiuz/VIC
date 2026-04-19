Task 2  
Pregunta 2.1  
1. El principal cuello de botella de R-CNN radica en que procesa cada propuesta 
de región de forma independiente a través de la red convolucional, en un 
escenario típico, el algoritmo genera aproximadamente 2000 regiones 
candidatas por imagen, y cada una de estas regiones es recortada, 
redimensionada y pasada individualmente por la CNN.  
Esto implica que la parte más costosa del modelo, que son las operaciones 
convolucionales, se ejecuta miles de veces por imagen, internamente, cada 
pasada involucra múltiples capas de convolución, funciones de activación y 
operaciones de pooling.  
Lo cual genera una enorme redundancia, ya que muchas de estas regiones se 
traslapan y contienen información visual similar. Como resultado, el tiempo de 
procesamiento se vuelve extremadamente alto, alcanzando valores como 45 
segundos por imagen. 
2. Fast R-CNN introduce dos mejoras clave para resolver este problema: el uso 
de un feature map compartido y la operación de RoI Pooling, el feature map 
compartido elimina la necesidad de ejecutar la CNN múltiples veces, ya que la 
imagen completa se procesa una sola vez para generar un mapa de 
características global.  
Luego, las regiones de interés se proyectan sobre este mapa, reutilizando la 
información ya calculada, esto reduce significativamente el costo 
computacional por otro lado, el RoI Pooling resuelve el problema de que las 
regiones tienen tamaños variables.  
Esta operación divide cada región en una cuadrícula fija, por ejemplo de 7 por 
7, y aplica max pooling en cada celda para obtener un tensor de tamaño fijo, 
de esta forma, todas las regiones pueden ser procesadas por las capas fully 
connected de la red sin importar su tamaño original. 
3. A pesar de estas mejoras, Fast R-CNN introduce un nuevo cuello de botella: el 
algoritmo Selective Search, que sigue siendo necesario para generar las 
propuestas de región.  
Este método toma aproximadamente 2 segundos por imagen y representa un 
problema más profundo que simplemente ser lento, selective Search es un 
algoritmo externo al modelo, no es aprendible y no está optimizado para 
ejecutarse en GPU.  
Esto rompe el flujo end-to-end del sistema, ya que la red no puede aprender a 
generar sus propias regiones de interés ni optimizar este proceso durante el 
entrenamiento. 
Pregunta 2.2  
4. La Region Proposal Network (RPN) se introduce para reemplazar métodos 
tradicionales como el sliding window, un sliding window clásico recorre la 
imagen con ventanas de tamaño fijo en múltiples posiciones, sin ningún tipo 
de aprendizaje, lo que genera una gran cantidad de regiones irrelevantes y un 
alto costo computacional.  
En contraste, la RPN aprende a generar propuestas de regiones directamente a 
partir del feature map del backbone, esto significa que no solo es más 
eficiente, sino también más inteligente desde el punto de vista semántico, ya 
que identifica patrones visuales relevantes como bordes, formas y estructuras 
que corresponden a objetos reales. 
5. Las anchor boxes son cajas predefinidas que se colocan en cada posición del 
feature map con diferentes escalas y relaciones de aspecto por ejemplo, se 
pueden utilizar nueve anchors por posición combinando tres tamaños y tres 
proporciones.  
En lugar de predecir coordenadas absolutas desde cero, la red aprende a 
ajustar estas cajas base mediante deltas, que representan desplazamientos y 
escalas relativos.  
Específicamente, predice valores como Δx, Δy, Δw y Δh. Este enfoque facilita el 
aprendizaje, ya que la red solo necesita refinar una aproximación inicial en 
lugar de generar una caja completamente nueva. 
En la ecuación de decodificación 𝑤 = 𝑤𝑎 ⋅ 𝑒Δ𝑤, 𝑤𝑎representa el ancho del 
anchor, Δ𝑤es el valor aprendido por la red, y 𝑤es el ancho final de la caja 
predicha.  
El uso de la función exponencial permite modelar cambios multiplicativos y 
asegura que las dimensiones finales sean siempre positivas, lo cual es 
fundamental en el contexto de tamaños de objetos. 
6. Considerando la restricción de VisorShelf de procesar imágenes en menos de 
500 milisegundos en hardware sin GPU, no recomendaría el uso de Faster R
CNN para producción en CPU.  
Aunque este modelo ofrece alta precisión, especialmente en la detección de 
objetos pequeños y densos, su latencia en CPU es demasiado alta para 
cumplir con los requerimientos operativos.  
Además, su arquitectura de dos etapas es más compleja, lo que dificulta su 
optimización y mantenimiento en entornos con recursos limitados por lo 
tanto, a pesar de su ventaja en precisión, no es una solución viable en este 
contexto. 
Pregunta 2.3  
7. Tomando en cuenta las restricciones operativas del sistema, especialmente la 
ausencia de GPU y el requisito de procesar imágenes en menos de 500 
milisegundos, recomendaría utilizar YOLOv8n como modelo de producción.  
Aunque Faster R-CNN ofrece mejor precisión, especialmente en escenarios 
con objetos pequeños y densos, su rendimiento en CPU es insuficiente para 
cumplir con la latencia requerida.  
YOLOv8n, al ser un modelo de una sola etapa, es significativamente más 
rápido y eficiente, alcanzando aproximadamente 15 FPS en CPU, lo que lo 
hace adecuado para un sistema en tiempo real, aunque presenta una menor 
precisión relativa, este compromiso es aceptable en un entorno donde la 
velocidad es un requisito crítico. 
8. Si el sistema se actualiza con una GPU de gama media como una RTX 3060, la 
recomendación cambiaría. En este caso, Faster R-CNN se vuelve una opción 
viable, ya que su rendimiento mejora considerablemente, alcanzando entre 8 y 
12 FPS.  
Esto permite aprovechar su mayor precisión, especialmente en la detección 
de objetos pequeños en anaqueles densos, sin comprometer el tiempo de 
respuesta, además, el uso de Feature Pyramid Networks mejora la capacidad 
del modelo para detectar objetos a múltiples escalas, lo cual es altamente 
relevante en este tipo de aplicación. 
9. Un riesgo técnico importante al realizar fine-tuning de Faster R-CNN sin aplicar 
un learning rate diferenciado entre el backbone y las capas nuevas es el 
fenómeno conocido como olvido catastrófico.  
Esto ocurre cuando los pesos preentrenados del backbone, que contienen 
información valiosa aprendida en datasets como COCO o ImageNet, se 
modifican demasiado rápido y pierden su capacidad de generalización, como 
resultado, el modelo puede adaptarse excesivamente al nuevo dataset, 
reduciendo su desempeño en escenarios distintos.  
Para mitigar este problema, se recomienda utilizar un learning rate más bajo 
para el backbone y uno más alto para las capas nuevas, congelar inicialmente 
las capas base y aplicar un proceso de fine-tuning progresivo, descongelando 
gradualmente el modelo. 