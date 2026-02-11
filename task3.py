import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
import time


def simulate_drone_A(img):
    img = cv.resize(img, None, fx=0.25, fy=0.25, interpolation=cv.INTER_AREA)
    img = cv.GaussianBlur(img, (9, 9), 0)
    return img




def simulate_drone_B(img):
    img = cv.resize(img, None, fx=2.0, fy=2.0, interpolation=cv.INTER_CUBIC)
    return img





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

    return matched_img, (t_detect + t_match) * 1000, len(kp1), len(kp2), len(good)


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

    return matched_img, (t_detect + t_match) * 1000, len(kp1), len(kp2), len(good)


def main():
    img1 = cv.imread('./data/close2.jpeg', cv.IMREAD_GRAYSCALE)
    img2 = cv.imread('./data/far2.jpeg', cv.IMREAD_GRAYSCALE)

    img1_A = simulate_drone_A(img1)

    img2_A = simulate_drone_A(img2)

    img1_B = simulate_drone_B(img1)
    img2_B = simulate_drone_B(img2)



    N = 10

    res = {
        "A_SIFT": [],
        "A_ORB": [],
        "B_SIFT": [],


        "B_ORB": []
    }

    for _ in range(N):
        sift_A, t, k1, k2, g = SIFT_pipeline(img1_A, img2_A)
        res["A_SIFT"].append((t, k1, k2, g))

        orb_A, t, k1, k2, g = ORB_pipeline(img1_A, img2_A)
        res["A_ORB"].append((t, k1, k2, g))


        sift_B, t, k1, k2, g = SIFT_pipeline(img1_B, img2_B)
        
        res["B_SIFT"].append((t, k1, k2, g))

        orb_B, t, k1, k2, g = ORB_pipeline(img1_B, img2_B)
        res["B_ORB"].append((t, k1, k2, g))

    def avg(data):
        return np.mean(data, axis=0)

    A_SIFT = avg(res["A_SIFT"])
    A_ORB  = avg(res["A_ORB"])
    B_SIFT = avg(res["B_SIFT"])


    B_ORB  = avg(res["B_ORB"])

    print("\n=== RESULTADOS PROMEDIO (N = 10) ===")
    print("Escenario | Algoritmo | Tiempo (ms) | KP Img A | KP Img B | Matches")
    print(f"A (Blur)  | SIFT      | {A_SIFT[0]:9.2f} | {int(A_SIFT[1]):8} | {int(A_SIFT[2]):8} | {int(A_SIFT[3])}")
    
    print(f"A (Blur)  | ORB       | {A_ORB[0]:9.2f} | {int(A_ORB[1]):8} | {int(A_ORB[2]):8} | {int(A_ORB[3])}")
    print(f"B (4K)    | SIFT      | {B_SIFT[0]:9.2f} | {int(B_SIFT[1]):8} | {int(B_SIFT[2]):8} | {int(B_SIFT[3])}")
    print(f"B (4K)    | ORB       | {B_ORB[0]:9.2f} | {int(B_ORB[1]):8} | {int(B_ORB[2]):8} | {int(B_ORB[3])}")

    plt.figure(figsize=(14, 10))

    plt.subplot(2, 2, 1)
    plt.imshow(sift_A)
    
    
    plt.title("Producto A (Blur) – SIFT")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.imshow(orb_A)
    plt.title("Producto A (Blur) – ORB")
    plt.axis('off')

    plt.subplot(2, 2, 3)
    plt.imshow(sift_B)
    plt.title("Producto B (Alta Resolución) – SIFT")
    
    plt.axis('off')

    
    plt.subplot(2, 2, 4)
    plt.imshow(orb_B)
    plt.title("Producto B (Alta Resolución) – ORB")
    plt.axis('off')

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
