import matplotlib.pyplot as plt
from PIL import Image, ImageFilter
import numpy as np

# read image into numpy array
img = np.asarray(Image.open('calsls1l.jpg'))
# binarize and coarse-graining
img = (img[::2, ::2, 0] < 128).astype(int)

def make_dots(
    img, # 2d np array of 1s and 0s
    spd=100, # speed up factor
    marg=0.9, # minimum spacing between dots relative to dot size,
    max_ds=27, # maximum dot diameter in pixels
    min_ds=1, # minimum dot diameter in pixels    
):

    # start with blank image
    img2 = np.zeros(img.shape)
    h, w = img.shape

    # keep track of areas occupied by dots
    occ = set()
    
    ofs = int(spd ** 0.5)

    # iterate over dot sizes, decreasing
    for t in np.arange(max_ds, min_ds, -5):
        # iterate over pixels
        for i in range(0, h, ofs):
            for j in range(0, w, ofs):
                d = 0
                # increase dot diameter while 1. within bounds, b. corners of bounding box are black and 3. not already occupied
                while (
                    i + d < h and j + d < w
                ) and all(
                    [img[i + d, j + d], img[i, j + d], img[i + d, j]]
                ) and not any(
                    [(i + d1, j + d2) in occ for d1, d2 in [(0, d), (d, 0), (d, d)]]
                ):
                    d += 1
                # consider dot only if exceeding threshold
                if d > t:
                    m = int(marg * d)
                    ci = i + d // 2
                    cj = j + d // 2
                    d2 = (d//2) ** 2
                    # iterate over pixels in bounding box of dot + margin
                    for a in range(i-m, i+d+m):
                        for b in range(j-m, j+d+m):
                            # mark pixel as occupied by dot
                            occ.add((a, b))
                            # if within radius, draw to image
                            if (ci - a) ** 2 + (cj - b) ** 2 < d2:
                                img2[a, b] = 1
    return img2


plt.imshow(make_dots(img), cmap='gray_r')
plt.axis('off')
plt.savefig('call.jpg')
threshold=30
Image.open('call.jpg').convert('L').filter(ImageFilter.CONTOUR).point(lambda x: 255 if x > threshold else 0, "1").show()
