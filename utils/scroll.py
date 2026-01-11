import time
from selenium.webdriver.remote.webdriver import WebDriver

def scroll_down(driver: WebDriver, times: int = 1, pause_sec: float = 0.6):
    for _ in range(times):
        driver.execute_script("window.scrollBy(0, Math.floor(window.innerHeight * 0.8));")
        time.sleep(pause_sec)
