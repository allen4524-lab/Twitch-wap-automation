import os
import time

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        time.sleep(1)
        self.driver.execute_script(
            "window.scrollBy(0, Math.floor(window.innerHeight * 0.6));"
        )
        time.sleep(0.5)

        self.driver.save_screenshot(path)
