# Task 1

Usted deberá demostrar comprensión teórica del criterio de Harris sin usar librerías. Para ello considere lo siguiente.

Se te da la siguiente Matriz del Segundo Momento (Tensor de Estructura) M calculada en un píxel específico (u,v) de una imagen:

$$M = \begin{pmatrix} 120 & 5 \\ 5 & 115 \end{pmatrix}$$

Y una segunda matriz M' para otro píxel diferente:

$$M' = \begin{pmatrix} 200 & 10 \\ 10 & 1 \end{pmatrix}$$

Con esta información haga lo siguiente:

1. Calcule manualmente (muestra tu procedimiento) los Eigenvalores (λ₁, λ₂) para ambas matrices.
2. Calcule la Respuesta de Harris (R) para ambas matrices usando la fórmula vista en clase. Asuma k = 0.04
3. Basado en tus resultados numéricos, clasifica qué representa cada píxel geométricamente: ¿Es una Esquina, un Borde o una Región Plana? Justifica tu respuesta usando las definiciones de eigenvalores vistas en clase


## Cálculo de Eigenvalores y Respuesta de Harris

### Eigenvalores

Para una matriz $M = \begin{pmatrix} a & b \\ b & c \end{pmatrix}$, los eigenvalores se obtienen resolviendo:

$$\det(M - \lambda I) = 0 \implies (a - \lambda)(c - \lambda) - b^2 = 0$$

#### Para $M = \begin{pmatrix} 120 & 5 \\ 5 & 115 \end{pmatrix}$:

$$(120 - \lambda)(115 - \lambda) - 25 = 0$$

$$\lambda^2 - 235\lambda + 13800 - 25 = 0$$

$$\lambda^2 - 235\lambda + 13775 = 0$$

$$\lambda = \frac{235 \pm \sqrt{235^2 - 4 \cdot 13775}}{2}$$

$$\lambda = \frac{235 \pm \sqrt{55225 - 55100}}{2}$$

$$\lambda = \frac{235 \pm \sqrt{125}}{2} = \frac{235 \pm 5\sqrt{5}}{2}$$

$$\boxed{\lambda_1 = \frac{235 + 5\sqrt{5}}{2} \approx 123.09}$$

$$\boxed{\lambda_2 = \frac{235 - 5\sqrt{5}}{2} \approx 111.91}$$


#### Para $M' = \begin{pmatrix} 200 & 10 \\ 10 & 1 \end{pmatrix}$:

$$(200 - \lambda)(1 - \lambda) - 100 = 0$$

$$\lambda^2 - 201\lambda + 200 - 100 = 0$$

$$\lambda^2 - 201\lambda + 100 = 0$$

$$\lambda = \frac{201 \pm \sqrt{201^2 - 4 \cdot 100}}{2}$$

$$\lambda = \frac{201 \pm \sqrt{40401 - 400}}{2}$$

$$\lambda = \frac{201 \pm \sqrt{40001}}{2} \approx \frac{201 \pm 200.00125}{2}$$

$$\boxed{\lambda_1 \approx 200.50}$$

$$\boxed{\lambda_2 \approx 0.50}$$


### Harris (R)

#### Para $M$:

$$\det(M) = 120 \cdot 115 - 5 \cdot 5 = 13775$$

$$\text{tr}(M) = 120 + 115 = 235$$

$$R = 13775 - 0.04 \cdot (235)^2 = 13775 - 2209 = \boxed{11566}$$

#### Para $M'$:

$$\det(M') = 200 \cdot 1 - 10 \cdot 10 = 100$$

$$\text{tr}(M') = 200 + 1 = 201$$

$$R' = 100 - 0.04 \cdot (201)^2 = 100 - 1616.04 = \boxed{-1516.04}$$

