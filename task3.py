import cv2
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import importlib.util

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    spec = importlib.util.spec_from_file_location("Task2_lab1", "Task2-lab1.py")
    Task2_lab1 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(Task2_lab1)
    
    mi_convolucion = Task2_lab1.mi_convolucion
    generar_gaussiano = Task2_lab1.generar_gaussiano
    detectar_bordes_sobel = Task2_lab1.detectar_bordes_sobel
except:
    try:
        from numpy.lib.stride_tricks import sliding_window_view
    except ImportError:
        sliding_window_view = None

    def _pad_manual(img, pad_h, pad_w, padding_type='reflect'):
        if padding_type == 'zero':
            return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
        if padding_type == 'reflect':
            return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='reflect')
        if padding_type == 'replicate':
            return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='edge')
        if padding_type == 'wrap':
            return np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='wrap')
        raise ValueError("padding_type debe ser: 'reflect', 'replicate', 'wrap' o 'zero'")

    def mi_convolucion(imagen, kernel, padding_type='reflect'):
        if imagen.ndim != 2:
            raise ValueError("La imagen debe ser 2D (escala de grises).")
        k = np.asarray(kernel, dtype=np.float64)
        if k.ndim != 2 or (k.shape[0] % 2 == 0) or (k.shape[1] % 2 == 0):
            raise ValueError("El kernel debe ser 2D y de tamaño impar.")
        img = np.asarray(imagen, dtype=np.float64)
        k_flip = np.flipud(np.fliplr(k))
        kh, kw = k_flip.shape
        pad_h, pad_w = kh // 2, kw // 2
        padded = _pad_manual(img, pad_h, pad_w, padding_type=padding_type)
        H, W = img.shape
        out = np.zeros((H, W), dtype=np.float64)
        
        if sliding_window_view is not None:
            windows = sliding_window_view(padded, (kh, kw))
            out = np.einsum('ijmn,mn->ij', windows, k_flip)
            return out
        
        for i in range(H):
            for j in range(W):
                region = padded[i:i+kh, j:j+kw]
                out[i, j] = np.sum(region * k_flip)
        return out

    def generar_gaussiano(tamano, sigma):
        if tamano % 2 == 0:
            raise ValueError("tamano debe ser impar.")
        if sigma <= 0:
            raise ValueError("sigma debe ser > 0.")
        r = tamano // 2
        y, x = np.mgrid[-r:r+1, -r:r+1]
        g = np.exp(-(x**2 + y**2) / (2 * sigma**2))
        g /= (2 * np.pi * sigma**2)
        g /= np.sum(g)
        return g

    def detectar_bordes_sobel(imagen, padding_type='reflect', return_degrees=False):
        if imagen.ndim != 2:
            raise ValueError("La imagen debe ser 2D.")
        img = np.asarray(imagen, dtype=np.float64)
        Gx_k = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=np.float64)
        Gy_k = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=np.float64)
        Gx = mi_convolucion(img, Gx_k, padding_type=padding_type)
        Gy = mi_convolucion(img, Gy_k, padding_type=padding_type)
        mag = np.sqrt(Gx**2 + Gy**2)
        mag_norm = mag.copy()
        mmax = mag_norm.max()
        if mmax > 0:
            mag_norm = (mag_norm / mmax) * 255.0
        mag_norm = mag_norm.astype(np.uint8)
        theta = np.arctan2(Gy, Gx)
        if return_degrees:
            theta = np.degrees(theta)
        return mag_norm, theta

def agregar_ruido_sal_pimienta(imagen, cantidad=0.02):
    img_ruido = imagen.copy()
    num_sal = int(cantidad * imagen.size * 0.5)
    num_pimienta = int(cantidad * imagen.size * 0.5)
    
    coords_sal = [np.random.randint(0, i, num_sal) for i in imagen.shape]
    img_ruido[coords_sal[0], coords_sal[1]] = 255
    
    coords_pimienta = [np.random.randint(0, i, num_pimienta) for i in imagen.shape]
    img_ruido[coords_pimienta[0], coords_pimienta[1]] = 0
    
    return img_ruido

def agregar_ruido_gaussiano(imagen, media=0, sigma=25):
    ruido = np.random.normal(media, sigma, imagen.shape)
    img_ruido = imagen + ruido
    img_ruido = np.clip(img_ruido, 0, 255)
    return img_ruido.astype(np.uint8)

def umbral_simple(magnitud, T):
    resultado = np.zeros_like(magnitud)
    resultado[magnitud > T] = 255
    return resultado.astype(np.uint8)

def experimento_A(imagen_path):
    img_original = cv2.imread(imagen_path, cv2.IMREAD_GRAYSCALE)
    if img_original is None:
        raise FileNotFoundError(f"No se pudo cargar {imagen_path}")
    
    img_ruido = agregar_ruido_sal_pimienta(img_original, cantidad=0.03)
    
    mag_sin_suavizado, _ = detectar_bordes_sobel(img_ruido, padding_type='reflect')
    
    gauss_1 = generar_gaussiano(tamano=5, sigma=1)
    img_suave_1 = mi_convolucion(img_ruido, gauss_1, padding_type='reflect')
    img_suave_1 = np.clip(img_suave_1, 0, 255).astype(np.uint8)
    mag_sigma_1, _ = detectar_bordes_sobel(img_suave_1, padding_type='reflect')
    
    gauss_5 = generar_gaussiano(tamano=31, sigma=5)
    img_suave_5 = mi_convolucion(img_ruido, gauss_5, padding_type='reflect')
    img_suave_5 = np.clip(img_suave_5, 0, 255).astype(np.uint8)
    mag_sigma_5, _ = detectar_bordes_sobel(img_suave_5, padding_type='reflect')
    
    fig, axes = plt.subplots(2, 4, figsize=(16, 8))
    fig.suptitle('Experimento A: Efecto de Sigma en Detección de Bordes', fontsize=14, fontweight='bold')
    
    axes[0, 0].imshow(img_original, cmap='gray')
    axes[0, 0].set_title('Original Limpia')
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(img_ruido, cmap='gray')
    axes[0, 1].set_title('Con Ruido (Sal y Pimienta)')
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(img_suave_1, cmap='gray')
    axes[0, 2].set_title('Suavizada σ=1')
    axes[0, 2].axis('off')
    
    axes[0, 3].imshow(img_suave_5, cmap='gray')
    axes[0, 3].set_title('Suavizada σ=5')
    axes[0, 3].axis('off')
    
    axes[1, 0].imshow(mag_sin_suavizado, cmap='gray')
    axes[1, 0].set_title('Bordes: SIN suavizado\n(mucho ruido)')
    axes[1, 0].axis('off')
    
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(mag_sigma_1, cmap='gray')
    axes[1, 2].set_title('Bordes: σ=1\n(balance ruido/detalle)')
    axes[1, 2].axis('off')
    
    axes[1, 3].imshow(mag_sigma_5, cmap='gray')
    axes[1, 3].set_title('Bordes: σ=5\n(suave, menos detalle)')
    axes[1, 3].axis('off')
    
    plt.tight_layout()
    plt.savefig('./outputs/experimento_A_sigma.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    cv2.imwrite('./outputs/A_original.png', img_original)
    cv2.imwrite('./outputs/A_con_ruido.png', img_ruido)
    cv2.imwrite('./outputs/A_bordes_sin_suavizado.png', mag_sin_suavizado)
    cv2.imwrite('./outputs/A_bordes_sigma1.png', mag_sigma_1)
    cv2.imwrite('./outputs/A_bordes_sigma5.png', mag_sigma_5)
    
    return img_ruido, mag_sin_suavizado, mag_sigma_1, mag_sigma_5

def experimento_B(imagen_ruido, magnitud_sobel):
    umbrales = [30, 50, 80, 120]
    
    canny_resultado = cv2.Canny(imagen_ruido, threshold1=50, threshold2=150)
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    fig.suptitle('Experimento B: Umbralización Simple vs Histéresis de Canny', fontsize=14, fontweight='bold')
    
    axes[0, 0].imshow(magnitud_sobel, cmap='gray')
    axes[0, 0].set_title('Magnitud Sobel\n(sin umbral)')
    axes[0, 0].axis('off')
    
    for idx, T in enumerate(umbrales[:2]):
        resultado_umbral = umbral_simple(magnitud_sobel, T)
        row = idx // 2
        col = idx % 2 + 1
        axes[row, col].imshow(resultado_umbral, cmap='gray')
        axes[row, col].set_title(f'Umbral Simple T={T}\n(bordes rotos)')
        axes[row, col].axis('off')
    
    for idx, T in enumerate(umbrales[2:]):
        resultado_umbral = umbral_simple(magnitud_sobel, T)
        axes[1, idx].imshow(resultado_umbral, cmap='gray')
        axes[1, idx].set_title(f'Umbral Simple T={T}\n(pierde detalles)' if idx == 1 else f'Umbral Simple T={T}')
        axes[1, idx].axis('off')
    
    axes[1, 2].imshow(canny_resultado, cmap='gray')
    axes[1, 2].set_title('cv2.Canny (Histéresis)\n(bordes conectados)', color='green', fontweight='bold')
    axes[1, 2].axis('off')
    
    plt.tight_layout()
    plt.savefig('./outputs/experimento_B_histeresis.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    fig2, axes2 = plt.subplots(1, 3, figsize=(15, 5))
    fig2.suptitle('Comparación: Mejor Umbral Simple vs Canny', fontsize=14, fontweight='bold')
    
    mejor_umbral = umbral_simple(magnitud_sobel, 50)
    
    axes2[0].imshow(imagen_ruido, cmap='gray')
    axes2[0].set_title('Imagen con Ruido')
    axes2[0].axis('off')
    
    axes2[1].imshow(mejor_umbral, cmap='gray')
    axes2[1].set_title('Umbral Simple T=50\n(bordes fragmentados)')
    axes2[1].axis('off')
    
    axes2[2].imshow(canny_resultado, cmap='gray')
    axes2[2].set_title('Canny (Histéresis)\n(bordes continuos)', color='green', fontweight='bold')
    axes2[2].axis('off')
    
    plt.tight_layout()
    plt.savefig('./outputs/experimento_B_comparacion.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    cv2.imwrite('./outputs/B_umbral_simple_T50.png', mejor_umbral)
    cv2.imwrite('./outputs/B_canny.png', canny_resultado)

def main():
    imagen_path = "sample_task3.jpg"
    
    img_ruido, mag_sin, mag_s1, mag_s5 = experimento_A(imagen_path)
    experimento_B(img_ruido, mag_s1)

main()
