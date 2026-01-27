import numpy as np
import matplotlib.pyplot as plt
import cv2

# ============================================
# Ejercicio 1: Convolución 2D Genérica
# ============================================
def mi_convolucion(imagen, kernel, padding_type='reflect'):
    """
    Implementación de convolución 2D con diferentes tipos de padding.
    
    Parameters:
    -----------
    imagen : numpy.ndarray
        Imagen en escala de grises (2D array)
    kernel : numpy.ndarray
        Kernel de convolución (2D array, preferiblemente impar x impar)
    padding_type : str
        Tipo de padding: 'reflect', 'constant', 'edge'
    
    Returns:
    --------
    output : numpy.ndarray
        Imagen resultante de la convolución
    """
    # Obtener dimensiones
    img_h, img_w = imagen.shape
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    
    # 1. Flip del kernel (necesario para convolución matemática)
    kernel_flipped = np.flipud(np.fliplr(kernel))
    
    # 2. Aplicar padding
    if padding_type == 'reflect':
        imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    elif padding_type == 'constant':
        imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    elif padding_type == 'edge':
        imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    else:
        raise ValueError(f"Tipo de padding no soportado: {padding_type}")
    
    # 3. Inicializar matriz de salida
    output = np.zeros((img_h, img_w))
    
    # 4. Convolución vectorizada (2 bucles en lugar de 4)
    for i in range(img_h):
        for j in range(img_w):
            # Extraer región de interés usando slicing
            region = imagen_padded[i:i + k_h, j:j + k_w]
            # Multiplicación elemento a elemento y suma
            output[i, j] = np.sum(region * kernel_flipped)
    
    return output

# Versión optimizada con más vectorización (opcional)
def mi_convolucion_optimizada(imagen, kernel, padding_type='reflect'):
    """
    Versión optimizada usando broadcasting de NumPy.
    """
    img_h, img_w = imagen.shape
    k_h, k_w = kernel.shape
    pad_h, pad_w = k_h // 2, k_w // 2
    
    # Flip del kernel
    kernel_flipped = np.flipud(np.fliplr(kernel))
    
    # Aplicar padding
    if padding_type == 'reflect':
        imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
    elif padding_type == 'constant':
        imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    elif padding_type == 'edge':
        imagen_padded = np.pad(imagen, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
    
    # Preparar arrays para broadcasting
    output = np.zeros((img_h, img_w))
    
    # Usar ventanas deslizantes con as_strided para mayor velocidad
    from numpy.lib.stride_tricks import as_strided
    
    # Crear vista de ventanas deslizantes
    shape = (img_h, img_w, k_h, k_w)
    strides = (imagen_padded.strides[0], imagen_padded.strides[1], 
               imagen_padded.strides[0], imagen_padded.strides[1])
    
    windows = as_strided(imagen_padded, shape=shape, strides=strides)
    
    # Realizar convolución vectorizada
    output = np.einsum('ijkl,kl->ij', windows, kernel_flipped)
    
    return output

# ============================================
# Ejercicio 2: Generador de Gaussianos
# ============================================
def generar_gaussiano(tamano, sigma):
    """
    Genera un kernel gaussiano 2D normalizado.
    
    Parameters:
    -----------
    tamano : int
        Tamaño del kernel (debe ser impar)
    sigma : float
        Desviación estándar de la distribución gaussiana
    
    Returns:
    --------
    kernel : numpy.ndarray
        Kernel gaussiano normalizado (suma = 1.0)
    """
    # Asegurar que el tamaño sea impar
    if tamano % 2 == 0:
        tamano += 1
        print(f"Advertencia: Tamaño ajustado a {tamano} (debe ser impar)")
    
    # Crear coordenadas centradas
    medio = tamano // 2
    x = np.arange(-medio, medio + 1)
    y = np.arange(-medio, medio + 1)
    
    # Crear malla 2D
    xx, yy = np.meshgrid(x, y)
    
    # Calcular la distribución gaussiana 2D
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    
    # Normalizar para que la suma sea 1.0
    kernel = kernel / np.sum(kernel)
    
    return kernel

# ============================================
# Ejercicio 3: Pipeline de Detección de Bordes (Sobel)
# ============================================
def detectar_bordes_sobel(imagen):
    """
    Detecta bordes usando los operadores de Sobel.
    
    Parameters:
    -----------
    imagen : numpy.ndarray
        Imagen en escala de grises
    
    Returns:
    --------
    magnitud : numpy.ndarray
        Magnitud del gradiente (0-255)
    direccion : numpy.ndarray
        Dirección del gradiente en radianes
    """
    # 1. Definir kernels de Sobel
    sobel_x = np.array([[-1, 0, 1],
                        [-2, 0, 2],
                        [-1, 0, 1]])
    
    sobel_y = np.array([[-1, -2, -1],
                        [0, 0, 0],
                        [1, 2, 1]])
    
    # 2. Aplicar convolución
    G_x = mi_convolucion(imagen, sobel_x, padding_type='reflect')
    G_y = mi_convolucion(imagen, sobel_y, padding_type='reflect')
    
    # 3. Calcular magnitud del gradiente
    magnitud = np.sqrt(G_x**2 + G_y**2)
    
    # Normalizar a 0-255 para visualización
    magnitud_normalizada = np.clip(magnitud, 0, 255)
    if magnitud.max() > 0:
        magnitud_normalizada = (magnitud_normalizada / magnitud_normalizada.max()) * 255
    
    # 4. Calcular dirección del gradiente
    # Usamos np.arctan2 para manejar todos los cuadrantes correctamente
    # Evitamos división por cero
    with np.errstate(divide='ignore', invalid='ignore'):
        direccion = np.arctan2(G_y, G_x)
    
    # Reemplazar NaN por 0 (donde G_x = 0)
    direccion = np.nan_to_num(direccion)
    
    return magnitud_normalizada.astype(np.uint8), direccion

# ============================================
# Funciones de prueba y visualización
# ============================================
def probar_convolucion():
    """Función para probar la convolución con diferentes kernels."""
    
    # Crear una imagen de prueba simple
    imagen_prueba = np.array([[1, 2, 3, 4, 5],
                              [6, 7, 8, 9, 10],
                              [11, 12, 13, 14, 15],
                              [16, 17, 18, 19, 20],
                              [21, 22, 23, 24, 25]], dtype=np.float32)
    
    # Kernel de prueba
    kernel_prueba = np.array([[1, 0, -1],
                              [1, 0, -1],
                              [1, 0, -1]])
    
    print("Imagen original:")
    print(imagen_prueba)
    print("\nKernel:")
    print(kernel_prueba)
    
    # Aplicar convolución
    resultado = mi_convolucion(imagen_prueba, kernel_prueba, padding_type='reflect')
    
    print("\nResultado de la convolución:")
    print(resultado)

def probar_gaussiano():
    """Función para probar el generador gaussiano."""
    
    print("=== Prueba del generador gaussiano ===")
    
    # Generar kernel gaussiano
    tamano = 5
    sigma = 1.0
    gauss = generar_gaussiano(tamano, sigma)
    
    print(f"\nKernel Gaussiano ({tamano}x{tamano}, sigma={sigma}):")
    print(gauss)
    print(f"\nSuma de todos los elementos: {gauss.sum():.6f}")
    print("(Debe ser muy cercano a 1.0)")
    
    # Visualizar el kernel
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.imshow(gauss, cmap='hot')
    plt.colorbar()
    plt.title(f'Kernel Gaussiano {tamano}x{tamano}')
    
    plt.subplot(1, 2, 2)
    plt.plot(gauss[tamano//2, :], 'b-o', label='Perfil central')
    plt.grid(True)
    plt.title('Perfil central del kernel')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

def probar_deteccion_bordes(ruta_imagen=None):
    """Función para probar la detección de bordes."""
    
    if ruta_imagen is None:
        # Crear imagen sintética de prueba
        imagen = np.zeros((100, 100))
        imagen[30:70, 30:70] = 255  # Cuadrado blanco
        imagen[40:60, 40:60] = 0    # Agujero negro
    else:
        # Cargar imagen real
        imagen_color = cv2.imread(ruta_imagen)
        imagen = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY)
        imagen = imagen.astype(np.float32)
    
    # Detectar bordes
    magnitud, direccion = detectar_bordes_sobel(imagen)
    
    # Visualizar resultados
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    axes[0, 0].imshow(imagen, cmap='gray')
    axes[0, 0].set_title('Imagen Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(magnitud, cmap='gray')
    axes[0, 1].set_title('Magnitud del Gradiente')
    axes[0, 1].axis('off')
    
    # Visualizar dirección como imagen de colores
    direccion_color = direccion.copy()
    direccion_color = (direccion_color + np.pi) / (2 * np.pi)  # Normalizar a [0, 1]
    axes[0, 2].imshow(direccion_color, cmap='hsv')
    axes[0, 2].set_title('Dirección del Gradiente (HSV)')
    axes[0, 2].axis('off')
    
    # Histograma de magnitud
    axes[1, 0].hist(magnitud.flatten(), bins=50, color='blue', alpha=0.7)
    axes[1, 0].set_title('Histograma de Magnitud')
    axes[1, 0].set_xlabel('Intensidad')
    axes[1, 0].set_ylabel('Frecuencia')
    axes[1, 0].grid(True)
    
    # Histograma de dirección
    axes[1, 1].hist(direccion.flatten(), bins=50, color='red', alpha=0.7)
    axes[1, 1].set_title('Histograma de Dirección')
    axes[1, 1].set_xlabel('Ángulo (radianes)')
    axes[1, 1].set_ylabel('Frecuencia')
    axes[1, 1].grid(True)
    
    # Mostrar el kernel de Sobel
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    axes[1, 2].text(0.1, 0.5, 
                   f"Sobel X:\n{sobel_x}\n\nSobel Y:\n{sobel_y}", 
                   fontsize=12, 
                   verticalalignment='center')
    axes[1, 2].set_title('Kernels de Sobel')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return magnitud, direccion

def pipeline_completa(ruta_imagen):
    """
    Ejecuta todo el pipeline: suavizado gaussiano + detección de bordes.
    """
    # 1. Cargar imagen
    imagen_color = cv2.imread(ruta_imagen)
    imagen_gris = cv2.cvtColor(imagen_color, cv2.COLOR_BGR2GRAY).astype(np.float32)
    
    # 2. Crear kernel gaussiano y suavizar
    print("Aplicando suavizado gaussiano...")
    gauss_kernel = generar_gaussiano(7, 1.5)
    imagen_suavizada = mi_convolucion(imagen_gris, gauss_kernel, padding_type='reflect')
    
    # 3. Detectar bordes
    print("Detectando bordes con Sobel...")
    magnitud, direccion = detectar_bordes_sobel(imagen_suavizada)
    
    # 4. Mostrar resultados
    fig, axes = plt.subplots(2, 3, figsize=(15, 8))
    
    axes[0, 0].imshow(imagen_gris, cmap='gray')
    axes[0, 0].set_title('Original')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(imagen_suavizada, cmap='gray')
    axes[0, 1].set_title('Suavizada (Gaussiano)')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(magnitud, cmap='gray')
    axes[0, 2].set_title('Bordes detectados')
    axes[0, 2].axis('off')
    
    # Mostrar kernels
    axes[1, 0].imshow(gauss_kernel, cmap='hot')
    axes[1, 0].set_title('Kernel Gaussiano')
    axes[1, 0].axis('off')
    
    sobel_x = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    sobel_y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
    
    axes[1, 1].imshow(sobel_x, cmap='gray')
    axes[1, 1].set_title('Sobel X')
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(sobel_y, cmap='gray')
    axes[1, 2].set_title('Sobel Y')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.show()
    
    return magnitud, direccion

# ============================================
# Ejecutar pruebas
# ============================================
if __name__ == "__main__":
    print("=== Práctica de Procesamiento de Imágenes ===\n")
    
    # Prueba 1: Convolución básica
    print("1. Probando función de convolución...")
    probar_convolucion()
    
    # Prueba 2: Generador gaussiano
    print("\n" + "="*50)
    print("2. Probando generador gaussiano...")
    probar_gaussiano()
    
    # Prueba 3: Detección de bordes
    print("\n" + "="*50)
    print("3. Probando detección de bordes...")
    print("   Usando imagen sintética...")
    magnitud, direccion = probar_deteccion_bordes()
