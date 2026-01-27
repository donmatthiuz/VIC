import numpy as np

# (Opcional pero recomendado) para vectorizar sin for usando ventanas deslizantes
try:
    from numpy.lib.stride_tricks import sliding_window_view
except ImportError:
    sliding_window_view = None


def _pad_manual(img, pad_h, pad_w, padding_type='reflect'):
    """Padding manual: reflect, replicate, wrap, zero."""
    if padding_type == 'zero':
        return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)

    if padding_type == 'reflect':
        # reflect: espejo sin repetir el borde
        return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')

    if padding_type == 'replicate':
        # replicate: repetir borde
        return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')

    if padding_type == 'wrap':
        # wrap: enrollar
        return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='wrap')

    raise ValueError("padding_type debe ser: 'reflect', 'replicate', 'wrap' o 'zero'")


def mi_convolucion(imagen, kernel, padding_type='reflect'):
    """
    Convolución 2D (grayscale), con padding manual e inversión del kernel.
    Restricción: imagen 2D (H,W) en escala de grises.
    """
    if imagen.ndim != 2:
        raise ValueError("La imagen debe ser 2D (escala de grises).")

    k = np.asarray(kernel, dtype=np.float64)
    if k.ndim != 2 or (k.shape[0] % 2 == 0) or (k.shape[1] % 2 == 0):
        raise ValueError("El kernel debe ser 2D y de tamaño impar (ej: 3x3, 5x5).")

    img = np.asarray(imagen, dtype=np.float64)

    # Flip del kernel (convolución matemática)
    k_flip = np.flipud(np.fliplr(k))

    kh, kw = k_flip.shape
    pad_h, pad_w = kh // 2, kw // 2

    # Padding manual
    padded = _pad_manual(img, pad_h, pad_w, padding_type=padding_type)

    H, W = img.shape
    out = np.zeros((H, W), dtype=np.float64)

    # ---- Opción A: Vectorizada (sin loops) si sliding_window_view está disponible ----
    if sliding_window_view is not None:
        windows = sliding_window_view(padded, (kh, kw))  # shape: (H, W, kh, kw)
        # Producto punto por pixel (H,W,kh,kw) con (kh,kw)
        out = np.einsum('ijmn,mn->ij', windows, k_flip)
        return out

    # ---- Opción B: 2 bucles (cumple "no 4 for") si no hay sliding_window_view ----
    for i in range(H):
        for j in range(W):
            region = padded[i:i+kh, j:j+kw]
            out[i, j] = np.sum(region * k_flip)

    return out


def generar_gaussiano(tamano, sigma):
    """
    Devuelve kernel Gaussiano 2D centrado de tamaño tamano x tamano.
    Normalizado para que la suma sea 1.0
    """
    if tamano % 2 == 0:
        raise ValueError("tamano debe ser impar (ej: 3,5,7,9).")
    if sigma <= 0:
        raise ValueError("sigma debe ser > 0.")

    r = tamano // 2
    y, x = np.mgrid[-r:r+1, -r:r+1]
    g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
    g /= (2 * np.pi * sigma**2)

    # Normalización (suma = 1)
    g /= np.sum(g)
    return g


def detectar_bordes_sobel(imagen, padding_type='reflect', return_degrees=False):
    """
    Aplica Sobel usando mi_convolucion. Retorna:
    - magnitud normalizada a 0-255 (uint8)
    - direccion (theta) en radianes (o grados si return_degrees=True)
    """
    if imagen.ndim != 2:
        raise ValueError("La imagen debe ser 2D (escala de grises).")

    img = np.asarray(imagen, dtype=np.float64)

    # Kernels Sobel
    Gx_k = np.array([[-1, 0, 1],
                     [-2, 0, 2],
                     [-1, 0, 1]], dtype=np.float64)

    Gy_k = np.array([[-1, -2, -1],
                     [ 0,  0,  0],
                     [ 1,  2,  1]], dtype=np.float64)

    Gx = mi_convolucion(img, Gx_k, padding_type=padding_type)
    Gy = mi_convolucion(img, Gy_k, padding_type=padding_type)

    # Magnitud
    mag = np.sqrt(Gx**2 + Gy**2)

    # Normalizar a 0-255 para visualizar
    mag_norm = mag.copy()
    mmax = mag_norm.max()
    if mmax > 0:
        mag_norm = (mag_norm / mmax) * 255.0
    mag_norm = mag_norm.astype(np.uint8)

    # Dirección (theta)
    theta = np.arctan2(Gy, Gx)  # radianes
    if return_degrees:
        theta = np.degrees(theta)

    return mag_norm, theta


# ---------------- EJEMPLO DE USO (OpenCV SOLO PARA I/O y display) ----------------
if __name__ == "__main__":
    import cv2

    # Leer en gris
    img = cv2.imread("input.png", cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError("No se pudo leer input.png")

    # (Opcional) Suavizado previo con gaussiano hecho por ti
    gk = generar_gaussiano(tamano=7, sigma=1.5)
    img_suave = mi_convolucion(img, gk, padding_type='reflect')

    # Sobel
    mag, theta = detectar_bordes_sobel(img_suave, padding_type='reflect', return_degrees=False)

    # Mostrar
    cv2.imshow("Original", img)
    cv2.imshow("Suavizada (Gauss manual)", np.clip(img_suave, 0, 255).astype(np.uint8))
    cv2.imshow("Sobel Magnitud (0-255)", mag)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Guardar resultados
    cv2.imwrite("suavizada.png", np.clip(img_suave, 0, 255).astype(np.uint8))
    cv2.imwrite("sobel_magnitud.png", mag)
