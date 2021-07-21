# import the necessary packages
import argparse
import cv2
import imutils
from imutils import paths
import time

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--images", type=str, required=True,
                help="path to input directory of images to stitch")
ap.add_argument("-o", "--output", type=str, required=True,
                help="path to the output image")
args = vars(ap.parse_args())

# grab the paths to the input images and initialize our images list
print("[INFO] 加载图片中...")
imagePaths = sorted(list(paths.list_images(args["images"])))
images = []

# loop over the image paths, load each one, and add them to our images to stitch list
for imagePath in imagePaths:
    image = cv2.imread(imagePath)
    image = cv2.resize(image, (512, 512))  # 缩放到合适大小
    images.append(image)

# initialize OpenCV's image stitchery object and then perform the image stitching
print("[INFO] 正在拼接...")
stitcher = cv2.createStitcher() if imutils.is_cv3() else cv2.Stitcher_create()
(status, stitched) = stitcher.stitch(images)

# if the status is '0', then OpenCV successfully performed image stitching
if status == 0:
    # write the output stitched image to disk
    print("[INFO] 拼接完成")
    time.sleep(1)
    cv2.imwrite(args["output"], stitched)

    # display the output stitched image to our screen
    cv2.imshow("Stitched", stitched)
    cv2.waitKey(0)

# otherwise the stitching failed, likely due to not enough points) being detected
else:
    print("[INFO] 图片拼接失败 ({})".format(status))
