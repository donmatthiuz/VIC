import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_img(img, title="Imagen", cmap=None):
    plt.figure(figsize=(6, 6))
    plt.title(title)
    # TODO: Matplotlib espera RGB, OpenCV carga BGR.
    # Verifica si la imagen tiene 3 canales y conviértela para visualización correcta.
    if len(img.shape) == 3 and cmap is None:
        img_show = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    else:
        img_show = img
    
    plt.imshow(img_show, cmap=cmap)
    plt.axis('off')
    plt.show()
    


def mi_convolucion(imagen, kernel, padding_type='reflect'):
 
    if len(imagen.shape) == 3:
        imagen = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)

    imagen = imagen.astype(np.float32)

   
    kernel = np.flipud(np.fliplr(kernel))

    k_h, k_w = kernel.shape
    pad_h = k_h // 2
    pad_w = k_w // 2


    imagen_pad = np.pad(
        imagen,
        ((pad_h, pad_h), (pad_w, pad_w)),
        mode=padding_type
    )

   
    salida = np.zeros_like(imagen, dtype=np.float32)

    
    for i in range(imagen.shape[0]):
        for j in range(imagen.shape[1]):
            region = imagen_pad[i:i+k_h, j:j+k_w]
            salida[i, j] = np.sum(region * kernel)

    return salida


def main():
    img = cv2.imread('sample.jpg')

    if img is None:
        print("Error: No se encontró la imagen.")
        return

    kernel = np.array([
        [1, 0, -1],
        [1, 0, -1],
        [1, 0, -1]
    ], dtype=np.float32)

    resultado = mi_convolucion(img, kernel)

    show_img(img, "Imagen original")
    show_img(resultado, "Convolución", cmap='gray')
        
    
    
if __name__ == "__main__":
    main()