# coding=utf-8
"""Satellite imagery downloader module."""

import time
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

LOC_FILE_PATH = 'locations.json'
EXPLORER_URL = 'https://earthexplorer.usgs.gov/'
SCREEN_DIR = 'screens'
SCREEN_STEPS = 9
X_SCREENS = 3
Y_SCREENS = 3
X_SCREENS_OFFSET = 1
Y_SCREENS_OFFSET = 1


def get_instructions(x_screens, y_screens, x_offset, y_offset, steps):
    """Get instructions for screen scheduler.

    Args:
        x_screens: how many screens horizontally.
        y_screens: how many screens vertically.
        x_offset: how many screens of horizontal offset.
        y_offset: how many screens of vertical offset.
        steps: arrow key presses to pass screen.

    Returns:
        list of instructions for screens executor.
    """
    # Move to starting position
    result = [Keys.ARROW_UP] * x_offset * steps + [Keys.ARROW_LEFT] * y_offset * steps

    # First row
    result += ["screen_0_0"]
    for x in range(x_screens - 1):
        result += [Keys.ARROW_RIGHT] * steps + [f"screen_{x + 1}_0"]
    for row in range(y_screens - 1):
        result += [Keys.ARROW_DOWN] * steps + [f"screen_{0 if row % 2 else x_screens - 1}_{row + 1}"]
        for x in range(x_screens - 1):
            result += [Keys.ARROW_RIGHT if row % 2 else Keys.ARROW_LEFT] * steps + \
                      [f"screen_{x if row % 2 else x_screens - x}_{row + 1}"]
    return result


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
        instructions = get_instructions(X_SCREENS, Y_SCREENS, X_SCREENS_OFFSET, Y_SCREENS_OFFSET, SCREEN_STEPS)
        elem = driver.find_element_by_id('map')
        for ins in instructions:
            if 'screen' in ins:
                driver.save_screenshot(SCREEN_DIR + '/' + loc['name'] + '_' + ins + '.jpg')
            else:
                elem.send_keys(ins)
            time.sleep(1)
        driver.close()
