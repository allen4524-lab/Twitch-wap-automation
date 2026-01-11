import os

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def take_screenshot(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.driver.save_screenshot(path)
