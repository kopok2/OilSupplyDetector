# coding=utf-8
"""Crop collected screens."""

import os
from PIL import Image

CROP_AREA = (449, 31, 1329, 750)
SCREENS_DIR = "screens"
CROPPED_DIR = "cropped"


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
        rgb_im.save(CROPPED_DIR + "/cropped_" + file, "JPEG")
