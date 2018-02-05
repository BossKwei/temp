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

matches_naive = skimage.feature.match_descriptors(descriptors_1, descriptors_2, cross_check=True)

src = keypoints_1[matches_naive[:,0]]
dst = keypoints_2[matches_naive[:,1]]

print(time.time())
model, matches = skimage.measure.ransac((src, dst), skimage.transform.AffineTransform, min_samples=3, max_trials=30, residual_threshold=2.0)
print(time.time())

fig, ax = plt.subplots()
plt.gray()
matches = np.nonzero(matches)[0]
skimage.feature.plot_matches(ax, img_1, img_2, src, dst, np.column_stack((matches, matches)), matches_color='b')
plt.show()

time.sleep(1)
