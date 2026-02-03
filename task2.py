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



def erosion(img, nivel_erosion=3):
    # asegurar tamaño mínimo 
    nivel_erosion = 3 if nivel_erosion < 3 else nivel_erosion
    if nivel_erosion % 2 == 0:
        nivel_erosion += 1

    # kernel 
    kernel = np.ones((nivel_erosion, nivel_erosion), dtype=np.uint8)

    # padding correcto
    pad_width = nivel_erosion // 2
    tamano_origin = img.shape

    pad_imagen = np.pad(img, pad_width=pad_width, mode='constant', constant_values=0)
    pimg_shape = pad_imagen.shape

    flat_submatrices = np.array([
        pad_imagen[i:(i + nivel_erosion), j:(j + nivel_erosion)]
        for i in range(pimg_shape[0] - nivel_erosion + 1)
        for j in range(pimg_shape[1] - nivel_erosion + 1)
    ])

    # erosión son todos blancos
    erosionada = np.array([
        255 if np.all(sub[kernel == 1] == 255) else 0
        for sub in flat_submatrices
    ])

    erosionada = erosionada.reshape(tamano_origin)
    return erosionada

    

def dilatacion(img, nivel_dilatacion=3):
    nivel_dilatacion = 3 if nivel_dilatacion < 3 else nivel_dilatacion

    ## creamos el kernel en base al nivel de dilatacion
    kernel = np.full(shape=(nivel_dilatacion, nivel_dilatacion), fill_value=255)
    
    ## calculamos el padding
    tamano_origin = img.shape
    pad_width = nivel_dilatacion - 2
    
    
    pad_imagen = np.pad(array=img, pad_width=pad_width, mode='constant')
    pimg_shape = pad_imagen.shape
    h_reduce, w_reduce = (pimg_shape[0] - tamano_origin[0]), (pimg_shape[1] - tamano_origin[1])
    
    flat_submatrices = np.array([
        pad_imagen[i:(i + nivel_dilatacion), j:(j + nivel_dilatacion)]
        for i in range(pimg_shape[0] - h_reduce) for j in range(pimg_shape[1] - w_reduce)
    ])
    
    # aqui hacemos el calculo de la dilatacion
    dilatada = np.array([255 if (i == kernel).any() else 0 for i in flat_submatrices])
    
    # convertimos la imagen diltada de nuevo al mismo tamaño de la dilatada
    dilatada = dilatada.reshape(tamano_origin)
    
    return dilatada
    
    


    
def main():
    
    # Carga de imagen a binaria
    img_gray = cv2.imread('fingerprint_noisy.png', cv2.IMREAD_GRAYSCALE)
    _, img_binary = cv2.threshold(
        img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    ## Para este tipo de imagenes lo mejor es la de apertura abre los espacios y quita el ruido salt

    erosionada = erosion(img_binary)
    dilatada = dilatacion(erosionada)

    ## hacemos cierre

    dilatada2 = dilatacion(dilatada)
    erosion2 = erosion(dilatada2)


    plt.figure(figsize=(12,4))
    plt.subplot(131), plt.imshow(img_gray, cmap='gray'), plt.title('Imagen Original')
    plt.subplot(132), plt.imshow(dilatada, cmap='gray'), plt.title('Primera Operacion')
    plt.subplot(133), plt.imshow(erosion2, cmap='gray'), plt.title('Imagen Final')
    plt.show()

    

if __name__ == "__main__":
    main()