from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.alert import Alert
from logging import Logger
from typing import Tuple
from selenium import webdriver
import time


class UILib:
    def __init__(self, driver: webdriver, logger: Logger):
        self.driver = driver
        self.logger = logger

    def get_url(self, url: str):
        self.driver.get(url)

    def wait_ele_visible(self, locator: Tuple[str, str], timeout: int = 10):
        self.logger.debug(f"wait_ele_visible: {locator}, timeout:{timeout}")
        ele = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator))
        return ele

    def wait_ele_clickable(self, locator: Tuple[str, str], timeout: int = 10):
        self.logger.debug(f"wait_ele_clickable: {locator}, timeout:{timeout}")
        ele = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator))
        return ele

    def click(self, locator: Tuple[str, str], timeout: int = 10):
        self.logger.debug(f"click element: {locator}, timeout:{timeout}")
        ele = self.wait_ele_clickable(locator, timeout=timeout)
        ele.click()

    def send_keys(self, locator: Tuple[str, str], msg: str, timeout: int = 10, need_check: bool = True):
        print(f"send_keys: {locator}, timeout:{timeout}")
        self.logger.debug(f"send_keys: {locator}, timeout:{timeout}")
        ele = self.wait_ele_clickable(locator, timeout=timeout)
        ele.clear()
        ele.send_keys(msg)
        if need_check:
            ele_value = self.get_value(locator, timeout=timeout)
            if str(msg) != str(ele_value):
                self.logger.debug(f"input: {msg}, element value:{ele_value}")
                raise f"[ERROR]\ninput: {msg} not equal to\nelement value:{ele_value}"

    def get_text(self, locator, timeout: int = 10):
        self.logger.debug(f"get_text: {locator}, timeout:{timeout}")
        ele = self.wait_ele_visible(locator, timeout=timeout)
        return ele.text

    def get_value(self, locator, timeout: int = 10):
        self.logger.debug(f"get_value: {locator}, timeout:{timeout}")
        ele = self.wait_ele_visible(locator, timeout=timeout)
        return ele.get_attribute("value")

    def get_alert(self, timeout: int = 10):
        self.logger.debug(f"get_alert, timeout:{timeout}")
        alert = Alert(self.driver)

    def scroll_down(self, movepixels: int = 1000, wait_time: int = 2):
        self.logger.debug(
            f"scroll_down {movepixels} pixels, wait_time={wait_time}")
        self.driver.execute_script(f"window.scrollBy(0, {movepixels});")
        time.sleep(wait_time)

    def take_screenshot(self, filename: str):
        self.logger.debug(f"take screenshot :{filename}")
        self.driver.save_screenshot(filename)
