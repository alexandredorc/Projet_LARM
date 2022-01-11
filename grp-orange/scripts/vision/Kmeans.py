from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import cv2
import numpy as np

def centroid_histogram(clt):
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    (hist, _) = np.histogram(clt.labels_, bins=numLabels)

    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    return hist

def plot_colors(hist, centroids):
    bar = np.zeros((50, 300, 3), dtype="uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for (percent, color) in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
                      color.astype("uint8").tolist(), -1)
        startX = endX

    return bar
    
image = cv2.imread('white_WP.jpg')
print(np.vstack((np.array(color),min_color)))

original_shape=image.shape
n_clusters=10
image = image.reshape((image.shape[0] * image.shape[1], 3))
clt = KMeans(n_clusters = n_clusters )
clt.fit(image)
hist = centroid_histogram(clt)
bar = plot_colors(hist, clt.cluster_centers_)
cv2.imshow("test",bar)


new_img = np.zeros((800*1280,3),dtype='uint8')
for ix in range(new_img.shape[0]):
    new_img[ix] = clt.cluster_centers_[clt.labels_[ix]]
    
new_img = new_img.reshape((original_shape))
cv2.imshow("Bam the 25th",new_img)
cv2.waitKey(0)