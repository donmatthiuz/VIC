import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt



    

def ORB_pipeline(frontal, side):
    feat = cv.ORB_create(nfeatures=1500)
    kpnt1, des1 = feat.detectAndCompute(frontal, None)
    kpnt2, des2 = feat.detectAndCompute(side, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
   
    
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    matched_image = cv.drawMatchesKnn(
            frontal,
            kpnt1,
            side,
            kpnt2,
            good,
            None,
            flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
    return matched_image


def SIFT_pipeline(frontal, side):
    sift = cv.SIFT_create()

    kpnt1, des1 = sift.detectAndCompute(frontal, None)
    kpnt2, des2 = sift.detectAndCompute(side, None)

    bf = cv.BFMatcher(cv.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(des1, des2, k=2)
    good = []
   
    
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good.append([m])

    matched_image = cv.drawMatchesKnn(
            frontal,
            kpnt1,
            side,
            kpnt2,
            good,
            None,
            flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
        )
    return matched_image


def main():
    frontal = cv.imread('./data/close1.jpeg', cv.IMREAD_GRAYSCALE)
    side = cv.imread('./data/far1.jpeg', cv.IMREAD_GRAYSCALE)

    matched_sift = SIFT_pipeline(frontal, side)
    matched_orb = ORB_pipeline(frontal, side)

    original_pair = np.hstack((frontal, side))

    plt.figure(figsize=(18, 6))

    # Original (frontal + side)
    plt.subplot(1, 3, 1)
    plt.imshow(original_pair, cmap='gray')
    plt.title('Imagen Original (Frontal + Side)')
    plt.axis('off')

    # SIFT
    plt.subplot(1, 3, 2)
    plt.imshow(matched_sift)
    plt.title('SIFT – Buenos Matches')
    plt.axis('off')

    # ORB (placeholder)
    plt.subplot(1, 3, 3)
    plt.imshow(matched_orb)
    plt.title('ORB – (placeholder)')
    plt.axis('off')

    plt.tight_layout()
    plt.show()



    

if __name__ == "__main__":
    main()
    




