# coding=utf-8
"""Satellite imagery downloader module."""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOC_FILE_PATH = 'locations.json'
EXPLORER_URL = 'https://earthexplorer.usgs.gov/'


if __name__ == '__main__':
    # Load location list
    locations = json.loads(open(LOC_FILE_PATH).read())['locations']

    for loc in locations:

        driver = webdriver.Firefox()
        driver.fullscreen_window()
        driver.get(EXPLORER_URL)
        driver.execute_script("window.scrollTo(0,165)")

        elem = driver.find_element_by_id('googleAddress')
        elem.clear()
        elem.send_keys(loc['address'])
        elem.send_keys(Keys.RETURN)

        time.sleep(3)
        elem = driver.find_element_by_class_name('address')
        elem.click()
        time.sleep(2)

        # zoom in
        num_zoom = 11
        for _ in range(num_zoom):
            elem = driver.find_element_by_class_name('leaflet-control-zoom-in')
            elem.click()
            time.sleep(1)
        while True:
            pass
        driver.close()