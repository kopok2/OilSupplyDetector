# coding=utf-8
"""Satellite imagery downloader module."""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOC_FILE_PATH = 'locations.json'
EXPLORER_URL = 'https://earthexplorer.usgs.gov/'
SCREEN_DIR = 'screens'

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
        elem = driver.find_element_by_class_name('leaflet-control-zoom-in')
        for _ in range(num_zoom):
            elem.click()
            time.sleep(1)

        # hide map overlaying elements
        elems = driver.find_elements_by_class_name('leaflet-top')
        for el in elems:
            driver.execute_script("arguments[0].setAttribute('style','visibility: hidden')", el)
        elems = driver.find_elements_by_class_name('leaflet-bottom')
        for el in elems:
            driver.execute_script("arguments[0].setAttribute('style','visibility: hidden')", el)
        elem = driver.find_element_by_id("mapOverlays")
        driver.execute_script("arguments[0].setAttribute('style','visibility: hidden')", elem)

        instructions = ['screen_cc'] + [Keys.ARROW_DOWN] * 9 + ['screen_cb'] + [Keys.ARROW_RIGHT] * 9 + ['screen_rb'] + \
                       [Keys.ARROW_UP] * 9 + ['screen_rc'] + [Keys.ARROW_UP] * 9 + ['screen_ru'] + \
                       [Keys.ARROW_LEFT] * 9 + \
                       ['screen_cu'] + [Keys.ARROW_LEFT] * 9 + ['screen_lu'] + \
                       [Keys.ARROW_DOWN] * 9 + ['screen_lc'] + [Keys.ARROW_DOWN] * 9 + ['screen_lb']
        elem = driver.find_element_by_id('map')
        for ins in instructions:
            if 'screen' in ins:
                driver.save_screenshot(SCREEN_DIR + '/' + loc['name'] + '_' + ins + '.jpg')
            else:
                elem.send_keys(ins)
            time.sleep(1)
        driver.close()
