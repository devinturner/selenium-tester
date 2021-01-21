#!/usr/bin/env python3

import os
import time
import multiprocessing

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Request:
    def __init__(self, host, browser):
        self.host = host
        self.browser = browser
        self.destination = "https://www.python.org"

    def send(self):
        total_time = 0
        driver_start_time = time.time()
        driver = webdriver.Remote(
            command_executor=self.host,
            desired_capabilities=self.browser.capabilities)

        driver_boot_time = time.time() - driver_start_time
        print("{}: BOOT DRIVER => {}".format(self.browser, round(driver_boot_time, 4)))
        total_time += driver_boot_time
        try:
            req_start_time = time.time()
            driver.get(self.destination)
            if "Python" in driver.title:
                response_time = time.time() - req_start_time
                print("{}: HTTP RESPONSE => {}".format(self.browser, round(response_time, 4)))
                total_time += response_time
        except:
            print("Error encountered")
            raise
        finally:
            print("{}: TOTAL => {}".format(self.browser, round(total_time, 4)))
            driver.quit()


class Chrome:
    def __init__(self):
        self.capabilities = DesiredCapabilities.CHROME.copy()

    def __str__(self):
        return "CHROME"


class Firefox:
    def __init__(self):
        self.capabilities = DesiredCapabilities.FIREFOX.copy()

    def __str__(self):
        return "FIREFOX"


class IE11:
    def __init__(self):
        self.capabilities = DesiredCapabilities.INTERNETEXPLORER.copy()

    def __str__(self):
        return "IE11"


BROWSERS = [
    Chrome(),
    Firefox(),
    IE11(),
]


def spawn_request(browser):
    Request(os.environ.get("SELENIUM_HOST"), browser).send()


if __name__ == '__main__':
    pool = multiprocessing.Pool(os.cpu_count())
    pool.map(spawn_request, BROWSERS)
