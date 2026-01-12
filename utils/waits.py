from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def wait_visible(driver: WebDriver, by: By, value: str, timeout: int = 15):
    return WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((by, value))
    )

def wait_clickable(driver: WebDriver, by: By, value: str, timeout: int = 15):
    return WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )

def wait_first_visible(driver: WebDriver, by: By, value: str, timeout: int = 15):
    
    #等到「任一個」符合 locator 的 element 變成可見，並回傳第一個可見的那個。
   
    def _pick_first_visible(_driver: WebDriver):
        els = _driver.find_elements(by, value)
        for el in els:
            try:
                if el.is_displayed() and el.is_enabled():
                    return el
            except Exception:
                continue
        return False

    return WebDriverWait(driver, timeout).until(_pick_first_visible)

