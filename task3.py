import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time


def ORB_pipeline(img1, img2):
    orb = cv.ORB_create(nfeatures=1500)

    t0 = time.perf_counter()
    kp1, des1 = orb.detectAndCompute(img1, None)

    
    kp2, des2 = orb.detectAndCompute(img2, None)
    t_detect = time.perf_counter() - t0

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
    t0 = time.perf_counter()


    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])



    t_match = time.perf_counter() - t0

    matched_img = cv.drawMatchesKnn(
        img1, kp1, img2, kp2, good, None,
        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    return matched_img, t_detect, t_match, len(kp1), len(kp2), len(good)


def SIFT_pipeline(img1, img2):
    sift = cv.SIFT_create()

    t0 = time.perf_counter()
    kp1, des1 = sift.detectAndCompute(img1, None)

    kp2, des2 = sift.detectAndCompute(img2, None)

    t_detect = time.perf_counter() - t0

    bf = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
    t0 = time.perf_counter()
    matches = bf.knnMatch(des1, des2, k=2)

    good = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    t_match = time.perf_counter() - t0

    matched_img = cv.drawMatchesKnn(
        img1, kp1, img2, kp2, good, None,


        flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    return matched_img, t_detect, t_match, len(kp1), len(kp2), len(good)


def main():
    img1 = cv.imread('./data/close2.jpeg', cv.IMREAD_GRAYSCALE)
    img2 = cv.imread('./data/far2.jpeg', cv.IMREAD_GRAYSCALE)

    N = 10

    sift_detect, sift_match = [], []
    orb_detect, orb_match = [], []

    for _ in range(N):
        _, td, tm, kp1_s, kp2_s, gm_s = SIFT_pipeline(img1, img2)
        sift_detect.append(td)
        sift_match.append(tm)

        _, td, tm, kp1_o, kp2_o, gm_o = ORB_pipeline(img1, img2)

        orb_detect.append(td)
        orb_match.append(tm)

    sift_detect_avg = np.mean(sift_detect)
    sift_match_avg = np.mean(sift_match)
    orb_detect_avg = np.mean(orb_detect)

    orb_match_avg = np.mean(orb_match)

    sift_total = (sift_detect_avg + sift_match_avg) * 1000
    orb_total = (orb_detect_avg + orb_match_avg) * 1000

    print("\n=== RESULTADOS PROMEDIO ===")
    print("Algoritmo | Tiempo total (ms) | KP Img A | KP Img B | Matches buenos")
    print(f"SIFT      | {sift_total:.2f}           | {kp1_s}      | {kp2_s}      | {gm_s}")
    print(f"ORB       | {orb_total:.2f}            | {kp1_o}       | {kp2_o}       | {gm_o}")

    sift_img, _, _, _, _, _ = SIFT_pipeline(img1, img2)
    orb_img, _, _, _, _, _ = ORB_pipeline(img1, img2)





    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.imshow(np.hstack((img1, img2)), cmap='gray')
    plt.title('Imágenes Originales')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(sift_img)
    plt.title('SIFT – Matches')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(orb_img)
    plt.title('ORB – Matches')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    labels = ['SIFT', 'ORB']
    tiempos = [sift_total, orb_total]

    plt.figure(figsize=(7, 5))
    plt.bar(labels, tiempos)
    plt.ylabel('Tiempo total promedio (ms)')
    plt.title('Comparación de tiempo total: SIFT vs ORB')
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
