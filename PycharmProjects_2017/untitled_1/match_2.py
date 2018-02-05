import time
import numpy as np
import matplotlib.pyplot as plt
import skimage.io, skimage.feature, skimage.transform, skimage.measure


img_1 = skimage.io.imread('1.jpg', as_grey=True)
img_2 = skimage.io.imread('2.jpg', as_grey=True)

descriptor_extractor = skimage.feature.ORB(n_keypoints=200)

descriptor_extractor.detect_and_extract(img_1)
keypoints_1 = descriptor_extractor.keypoints
descriptors_1 = descriptor_extractor.descriptors

descriptor_extractor.detect_and_extract(img_2)
keypoints_2 = descriptor_extractor.keypoints
descriptors_2 = descriptor_extractor.descriptors

matches12 = skimage.feature.match_descriptors(descriptors_1, descriptors_2, cross_check=True)

src = []
dst = []
for i, j in matches12:
    kp_1 = keypoints_1[i]
    kp_2 = keypoints_2[j]
    #
    error = np.sqrt(np.power(kp_1[0] - kp_2[0], 2) + np.power(kp_1[1] - kp_2[1], 2))
    if error <= 20:
        src.append(kp_1)
        dst.append(kp_2)
src = np.array(src)
dst = np.array(dst)

model = skimage.transform.AffineTransform()
model.estimate(src, dst)
print(model.params)

fig, ax = plt.subplots()
plt.gray()
match = np.array([(i, i) for i in range(dst.shape[0])])
skimage.feature.plot_matches(ax, img_1, img_2, src, dst, match, matches_color='b')
plt.show()

time.sleep(1)
