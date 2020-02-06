# coding=utf-8
"""Crop collected screens."""

import os
from PIL import Image

CROP_AREA = (449, 31, 1329, 750)
IMG_WIDTH = CROP_AREA[2] - CROP_AREA[0] - 160
IMG_HEIGHT = CROP_AREA[3] - CROP_AREA[1]
SCREENS_DIR = "screens"
CROPPED_DIR = "cropped"
MERGED_DIR = "merged"
X_SCREENS = 7
Y_SCREENS = 7


def merge_images(dir_path):
    """Merge images into bigger parts."""
    new_im = Image.new('RGB', (X_SCREENS * IMG_WIDTH, Y_SCREENS * IMG_HEIGHT))

    for dir_name in os.listdir(dir_path):
        images = [(Image.open(dir_path + "/" + dir_name + "/" + img_f), img_f) for img_f in
                  os.listdir(dir_path + "/" + dir_name)]
        ends = [end + ".jpg" for end in [f"{x}_{y}" for x in range(X_SCREENS) for y in range(Y_SCREENS)]]
        img_paste = {}
        for end in ends:
            for image in images:
                if end in image[1]:
                    img_paste[end[:-4]] = image[0]

        # Create merged image
        for x in range(X_SCREENS):
            for y in range(Y_SCREENS):
                new_im.paste(img_paste[f"{x}_{y}"], (x * IMG_WIDTH, y * IMG_HEIGHT))

        new_im.save(MERGED_DIR + "/" + dir_name + "_merged.jpg")


def crop(image):
    """Crop image."""
    cropped_img = image.crop(CROP_AREA)
    cropped_img.show()
    return cropped_img


if __name__ == '__main__':
    for file in os.listdir(SCREENS_DIR):
        img = Image.open(SCREENS_DIR + "/" + file)
        crop_img = crop(img)
        rgb_im = crop_img.convert('RGB')
        file_short = file[:-7]
        try:
            os.mkdir(CROPPED_DIR + "/" + file_short + "/")
        except FileExistsError:
            pass
        rgb_im.save(CROPPED_DIR + "/" + file_short + "/cropped_" + file, "JPEG")
    merge_images(CROPPED_DIR)
