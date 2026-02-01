import numpy as np 
import cv2 
import matplotlib.pyplot as plt 

img = cv2.imread('periodic_noise.jpg', cv2.IMREAD_GRAYSCALE)
f = np.fft.fft2(img)
fshift = np.fft.fftshift(f)
magnitude_spectrum = 20*np.log(np.abs(fshift)+1)

plt.figure(figsize=(12,4))
plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Imagen Original')
plt.subplot(132), plt.imshow(magnitude_spectrum, cmap='gray'), plt.title('Espectro de Magnitud')
plt.subplot(133), plt.imshow(magnitude_spectrum, cmap='gray'), plt.title('Picos de Ruido Identificados')

rows, cols = img.shape
crow, ccol = rows//2, cols//2
mask = np.ones((rows, cols), np.float32)

dist = 10 
peaks = [(crow-dist, ccol-dist), (crow+dist, ccol+dist), 
         (crow-dist, ccol+dist), (crow+dist, ccol-dist)]

for peak in peaks:
    cv2.circle(mask, (peak[1], peak[0]), 5, 0, -1)
    plt.subplot(133).plot(peak[1], peak[0], 'rx', markersize=10)

fshift_filtered = fshift * mask
f_ishift = np.fft.ifftshift(fshift_filtered)
img_filtered = np.abs(np.fft.ifft2(f_ishift))

plt.figure(figsize=(12,4))
plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Imagen Original')
plt.subplot(132), plt.imshow(mask, cmap='gray'), plt.title('Máscara del Filtro Notch')
plt.subplot(133), plt.imshow(img_filtered, cmap='gray'), plt.title('Imagen Restaurada')

img_blur = cv2.blur(img, (5,5))
plt.figure(figsize=(8,4))
plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Imagen Original')
plt.subplot(122), plt.imshow(img_blur, cmap='gray'), plt.title('Filtro Promedio 5x5')

plt.show()
