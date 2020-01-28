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


def merge_images(dir_path):
    """Merge images into bigger parts."""
    new_im = Image.new('RGB', (3 * IMG_WIDTH, 3 * IMG_HEIGHT))

    new_im.save('test.jpg')
    for dir_name in os.listdir(dir_path):
        images = [(Image.open(dir_path + "/" + dir_name + "/" + img_f), img_f) for img_f in
                  os.listdir(dir_path + "/" + dir_name)]
        ends = [end + ".jpg" for end in ['cb', 'cc', 'cu', 'lb', 'lc', 'lu', 'rb', 'rc', 'ru']]
        img_paste = {}
        for end in ends:
            for image in images:
                if end in image[1]:
                    img_paste[end[:2]] = image[0]

        # Create merged image
        new_im.paste(img_paste['lu'], (0, 0))
        new_im.paste(img_paste['lc'], (0, IMG_HEIGHT))
        new_im.paste(img_paste['lb'], (0, IMG_HEIGHT * 2))
        new_im.paste(img_paste['cu'], (IMG_WIDTH, 0))
        new_im.paste(img_paste['cc'], (IMG_WIDTH, IMG_HEIGHT))
        new_im.paste(img_paste['cb'], (IMG_WIDTH, IMG_HEIGHT * 2))
        new_im.paste(img_paste['ru'], (IMG_WIDTH * 2, 0))
        new_im.paste(img_paste['rc'], (IMG_WIDTH * 2, IMG_HEIGHT))
        new_im.paste(img_paste['rb'], (IMG_WIDTH * 2, IMG_HEIGHT * 2))

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
