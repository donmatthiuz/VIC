# VIC
## Resumen del Proyecto

Este repositorio contiene la resolución de la **Hoja de Trabajo 1 – Visión por Computadora**, que incluye análisis teórico, implementación práctica y preguntas conceptuales.

### Task 1 – Análisis Teórico
- Un frame crudo 4K (3840×2160) a 12 bits por píxel ocupa aproximadamente **11.86 MB**.  
- El ancho de banda requerido para 8 cámaras a 60 FPS sin compresión es de alrededor de **47.8 Gbps**.  
- Con un buffer de **16 GB de RAM** solo se pueden almacenar cerca de **2.9 segundos** de video.  
- No es viable enviar datos crudos a la nube usando 5G, ya que la velocidad real de subida (100–500 Mbps, picos de 1–2 Gbps) es muy inferior a lo requerido; se necesita compresión o procesamiento local.

En la mejora de imagen:
- Se aplicó corrección gamma (γ = 0.5) y ajuste lineal (α = 1.2, β = −10).
- El valor final correcto del píxel fue **125**, sin saturación.
- Trabajar directamente en uint8 produce un resultado de **0**, con un error absoluto de **125**, demostrando la importancia de usar flotantes normalizados.

En la clasificación de colores:
- La distancia en RGB entre un rojo iluminado y uno en sombra es alta (**205**) por la influencia de la iluminación.
- En HSV ambos colores comparten el mismo **H** y **S**, y solo difieren en **V**, por lo que HSV es más adecuado para clustering por color real.

---

### Task 2 – Práctica
Se implementó un pipeline manual con NumPy:
- Ajuste de contraste y brillo vectorizado.
- Corrección gamma manual.
- Segmentación cromática en HSV, aislando el color blanco mediante rangos definidos de H, S y V.

---

### Task 3 – Post-Práctica
- Las operaciones vectorizadas en NumPy son mucho más rápidas que los bucles `for` porque usan paralelización tipo **SIMD**.
- Si no se convierte de BGR a RGB al usar OpenCV con matplotlib, los colores aparecen invertidos en la visualización.
