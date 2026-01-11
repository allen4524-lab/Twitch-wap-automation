from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def create_mobile_emulation_driver(device_name: str = "Pixel 2") -> webdriver.Chrome:
    options = Options()
    # test by WAP
    options.add_experimental_option("mobileEmulation", {"deviceName": device_name})
    # 避免瀏覽器自己跳通知 popup
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-infobars")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.set_page_load_timeout(60)
    return driver
