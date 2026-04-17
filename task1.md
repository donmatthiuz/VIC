1. Calcule manualmente el IoU entre las dos cajas. Muestre paso a paso el cálculo del área de intersección, el área de unión y el valor final. Explique en términos no técnicos qué significa ese número para el cliente de VisorShelf.

- R: Para empezar, tomamos las coordenadas de las dos cajas. La que predijo el sistema es b_pred = (142, 89, 218, 165) y la real o ground truth es b_gt = (138, 84, 222, 170). De ahí buscamos dónde se cruzan. Las coordenadas mínimas de la intersección son la x y la y más altas de las esquinas superiores izquierdas, que serían (142, 89). Las máximas son las más bajas de las esquinas inferiores derechas, o sea (218, 165).

El ancho de esa intersección nos da:
$$218 - 142 = 76$$
Y el alto es:
$$165 - 89 = 76$$
Así que el área donde ambas cajas se cruzan es:
$$76 \times 76 = 5776$$

Luego, se calcula cada caja por su lado.
Para la caja del sistema:
$$(218 - 142) \times (165 - 89) = 76 \times 76 = 5776$$
Para la caja real del anotador: 
$$(222 - 138) \times (170 - 84) = 84 \times 86 = 7224$$
Para sacar la unión, sumamos estas dos áreas y le restamos la intersección para no contar el traslape dos veces:
$$5776 + 7224 - 5776 = 7224$$
Finalmente el IoU es solo dividir la intersección entre la unión:
$$IoU = \frac{5776}{7224} = 0.7995$$

Da aproximadamente 0.80. Esto significa que la caja que pintó el sistema coincide en un 80% con la marca perfecta que hizo el humano. Es un resultado muy bueno, el sistema atrapó la lata casi por completo y solo se le escaparon unos detallitos en los bordes.

2. En la fórmula IoU = |I| / |U|, identifique qué representa cada símbolo (|I|, |U|) y explique por qué el denominador es la unión y no el área del ground truth. ¿Qué problema concreto evita esa decisión de diseño?

- R: En la fórmula:
$$IoU = \frac{|I|}{|U|}$$
El símbolo $I$ es la intersección, el pedazo exacto donde las dos cajas se montan una sobre la otra. Mientras que $U$ es la unión, que representa todo el espacio que ocupan las dos cajas juntas, pero sin contar el traslape dos veces. 

Usamos la unión abajo en la división y no solo el tamaño del producto real para evitar que el modelo nos haga trampa. Ya que si por ejemplo, el sistema dibuja una caja que abarca la mitad de todo el anaquel. Obviamente va a cubrir el producto por completo y si dividiéramos solo por el tamaño del producto real, el resultado nos diría que tuvimos un 100% de éxito, lo cual es falso. Al usar la unión, esa caja gigante hace que el número de abajo crezca muchísimo, hundiendo el resultado del IoU y castigando esa predicción desproporcionada.

3. El equipo de VisorShelf está evaluando dos umbrales de IoU para decidir si una detección es válida: $\theta$ = 0.5 y $\theta$ = 0.75. ¿Cuál recomendaría para el sistema de auditoría de anaqueles y por qué? Considere el impacto operativo de los falsos positivos y falsos negativos en el negocio del cliente.

- R: Para un proyecto como VisorShelf, yo me iría por el umbral de 0.5 a 0.75. Al final del día, lo que le interesa al negocio en una auditoría es saber si el producto está ahí en el anaquel para llevar bien el inventario, no si la caja quedó dibujada al milímetro. 


4. Calcule la Precisión y el Recall para esta prueba. En las fórmulas P = TP / (TP + FP) y R = TP / (TP + FN), explique verbalmente qué mide cada término del denominador y por qué ambas métricas son necesarias para evaluar el sistema.

- R: Calculando, la precisión nos queda así:
$$P = \frac{12}{12 + 6} = \frac{12}{18} = 0.666$$
Lo que se traduce en un 66.6%.

Y para el Recall:
$$R = \frac{12}{12 + 3} = \frac{12}{15} = 0.80$$
Que sería un 80%.

En la precisión, el número de abajo suma absolutamente todo lo que el sistema dijo que era un producto. Nos dice qué tan atinado es el modelo cuando decide hablar.
En el Recall, el número de abajo suma todos los productos que físicamente estaban parados ahí en el estante. Nos dice qué porcentaje de la realidad logró capturar el sistema.

Necesitamos ver ambas porque se complementan. Si un modelo se vuelve loco y dice que todo el estante es producto, va a tener un Recall de 100% pero una Precisión horrible porque va a inventar cosas de la nada. Por el otro lado, si solo marca la lata más obvia de toda la foto, su Precisión será perfecta, pero su Recall será muy malo, porque ignoró todo lo demás. Como siempre, el truco es buscar el equilibrio.

5. El director de operaciones de la tienda le dice: Prefiero que el sistema no se pierda ningún quiebre de stock, aunque a veces nos avise de falsos alarmas. Traduzca esa preferencia a términos de Precisión y Recall. ¿Qué umbral de confianza ajustaría y en qué dirección?

- R: Lo que el director está pidiendo es que le demos prioridad al Recall sobre la Precisión. Él quiere que el sistema encuentre absolutamente todos los productos, reduciendo al mínimo los Falsos Negativos, y no le importa tanto si de repente el sistema se equivoca y le marca una sombra como si fuera producto, lo cual sería un Falso Positivo. 

Para cumplir con lo que pide y lograr esto, lo que tenemos que hacer es bajar el umbral de confianza del detector. Al hacerlo, el modelo se vuelve mucho más sensible y empieza a dejar pasar predicciones de las que no está tan seguro. Lo cual, sí vamos a tener más ruido y falsas alarmas, pero le garantizamos que no se le va a escapar ni un solo producto real del inventario.

6. Explique qué es el mAP (Mean Average Precision) y por qué es más informativo que reportar un único valor de Precisión o Recall. En su explicación, distinga entre mAP@0.5 (protocolo PASCAL VOC) y mAP@0.5:0.95 (protocolo COCO), y argumente cuál protocolo sería más exigente para VisorShelf y por qué.

- R: El mAP es una métrica súper útil porque nos da un resumen general de cómo se porta el modelo. En lugar de ver la Precisión y el Recall en un solo punto, evalúa todo el panorama probando diferentes niveles de confianza y saca un promedio para todos los tipos de productos que buscamos. Dar solo un valor de Precisión o Recall es como tomarle una foto a un carro en movimiento; el mAP te muestra el video completo para ver qué tan estable es el sistema.

Ahora, sobre los protocolos: el mAP@0.5 es un poco más relajado porque solo te pide que el IoU sea de 0.5 para dar por buena la detección. En cambio, el protocolo COCO o mAP@0.5:0.95 sube el umbral poco a poco hasta llegar a 0.95 y promedia todo. 

Definitivamente el protocolo COCO sería muchísimo más pesado y exigente para VisorShelf. Castigaría sin piedad cualquier caja que encierre bien el producto pero que no esté perfilada de forma milimétrica sobre los bordes de la lata. Si usamos COCO, el número final del mAP se vería bastante más bajo, aunque en la práctica el sistema esté haciendo bien su trabajo principal que es contar el inventario.

7. Explique al cliente qué es el Non-Maximum Suppression (NMS) y por qué el detector genera múltiples cajas para el mismo objeto. Describa el algoritmo paso a paso en lenguaje no técnico.

- R: Nuestro detector mira la foto como si fuera una cuadrícula gigante, y desde varias partes al mismo tiempo intenta encontrar productos. A veces, varias de esas miradas detectan la misma botella y cada una lanza su propia caja. Por eso vemos duplicados. El NMS o Supresión de No Máximos es básicamenteun filtro, que nos permite eliminar esos duplicados que se van generando. 

El proceso es más o menos así:
Primero, el sistema junta todas las cajas que encontró y las ordena, poniendo de primeras las que tienen mayor seguridad o confianza de ser un producto real.
Segundo, agarra la caja más segura de todas, la marca como la buena y la usa como molde.
Luego, revisa todas las demás cajas que cayeron cerca. Si ve que alguna está muy encimada sobre la principal, supone que están viendo lo mismo, y la borra 
Por último, toma la siguiente caja con mayor confianza que haya sobrevivido a la limpieza y repite la estrategia, hasta que deja todo el anaquel limpio de duplicados.

8. El parámetro $\theta$_NMS controla qué tan agresivo es el NMS al suprimir cajas. En un anaquel densamente poblado donde los productos están uno junto al otro casi sin espacio, ¿qué valor de $\theta$_NMS recomendaría (alto o bajo) y por qué? Argumente el riesgo en cada dirección.

- R: En el caso de un anaquel donde todo está amontonado, yo recomendaría usar un valor de NMS más alto, o sea, que sea menos agresivo al limpiar.

El problema de usar un NMS bajo en esta situación es que el sistema se pondría a borrar cajas a lo loco. Al ver dos latas reales que están súper pegadas, el filtro pensaría que es un error del sistema viendo doble, borraría una de las cajas y nos generaría un Falso Negativo. Perderíamos productos que sí están ahí. En cambio, si nos vamos por un NMS alto corremos el riesgo de que el filtro se quede corto y nos deje algunas cajas duplicadas para un mismo producto, creando Falsos Positivos. Pero honestamente, considero que en anaqueles densos es mucho mejor lidiar con un par de duplicados que perderle la pista a la mercadería real.

9. ¿En qué orden se deben aplicar el umbral de confianza $t$ y el NMS? Justifique la respuesta y explique qué sucedería computacionalmente si se invierte ese orden en un sistema que procesa 30 imágenes por minuto.

- R: El orden indiscutible aquí es aplicar primero el umbral de confianza y después pasar la escoba con el NMS. Y la razón es puramente para no quemar los servidores.

El primer filtro por confianza nos ayuda a descartar de golpe miles de cajas basura que el modelo tiró con niveles bajísimos de seguridad, dejando vivas solo unas cuantas docenas que valen la pena. Una vez que tenemos ese grupo pequeño, ya le podemos pasar el NMS.

El NMS es un proceso matemáticamente pesado porque tiene que comparar el traslape de cada caja contra todas las demás. Si lo hiciéramos al revés y estuviéramos procesando 30 fotos por minuto, el hardware colapsaría . Poner a la tarjeta gráfica a cruzar las áreas de miles y miles de cajas crudas antes de filtrarlas consumiría toda la memoria en segundos. Sería imposible que VisorShelf corriera en tiempo real de esa manera.
