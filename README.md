# Laboratorio 6


[Link al Repositorio](https://github.com/donmatthiuz/VIC/tree/lab6)




## Task 1

Como Ingeniero Principal (Lead AI Engineer) del proyecto AgriTech, usted debe justificar las decisiones
arquitectónicas ante su equipo y sus clientes. Responda a los siguientes escenarios en su reporte (máximo
1 página por respuesta), combinando la teoría matemática con el pragmatismo laboral.

### 1

#### Escenario 1
Un desarrollador junior de su equipo sugiere: "Para detectar con mayor precisión las texturas de las
hojas enfermas, deberíamos construir una red secuencial clásica (tipo VGG) pero de 150 capas. Más
profundo siempre es mejor". Como líder técnico, explíquele argumentativamente por qué esta red
fracasará estrepitosamente en el entrenamiento (mencionando el fenómeno de degradación y el
desvanecimiento del gradiente). Luego, justifique cómo la adición estructural de las conexiones
residuales (𝐹(𝑥) + 𝑥) de ResNet rescata el proyecto, haciendo viable entrenar redes ultra-profundas
sin colapsar.


#### Respuesta

Esta red VGG no mejora nada con respecto al entrenamiento, esto se debe al efecto de desvanecimiento del gradiente. Ya que la retropropagación aplica la regla de la cadena pura: para llegar al gradiente de una capa temprana, multiplicas los gradientes de todas las capas siguientes.

$$H(x) = F(x)$$

Dado como se ve en la formula seria la salida de cada bloque de cada capa, y entonces la retropropagacion de esa capa seria lo siguiente

$$
\frac{\partial L}{\partial x} =
\frac{\partial L}{\partial H}
\left(
\frac{\partial F}{\partial x} 
\right)
$$

Si $\frac{\partial F}{\partial x}$ tiende a 0 entonces $\frac{\partial L}{\partial x}$ tambien lo hace.

Esto provoca que al red no aprenda y entonces muera. Aunque le agreguemos mas capas esto solo empeorara la misma.

En cambio otras arquitecturas como ResNet agrega un bloque residual como se ve aqui $F(x) = H(x)-x$, esto hace que la salida sea:
$H(x) = F(x)+x$

Si calculamos la retropropagacion de esto nos quedaria lo siguiente

$$
\frac{\partial L}{\partial x} =
\frac{\partial L}{\partial H}
\left(
\frac{\partial F}{\partial x} +1
\right) 
$$

Como se ve aqui si $\frac{\partial F}{\partial x}$ tiende a 0  osea que la derivada parcial de la funcion  no hara que la red muera porque al haber un 1 , siempre obtendra almenos un valor.

