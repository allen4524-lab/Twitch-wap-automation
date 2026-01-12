import time
from urllib.parse import quote
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.waits import wait_visible, wait_first_visible
from utils.scroll import scroll_down
from utils.popup import close_popups_best_effort
from selenium.common.exceptions import ElementClickInterceptedException

class TwitchHomePage(BasePage):
    URL = "https://www.twitch.tv/"

    # 現階段twitch首頁沒有SEARCH INPUT , 但仍保留哪天 /search 的 input 找得到可以用
    SEARCH_INPUT_CANDIDATES = [
        (By.XPATH, '//input[contains(@placeholder, "搜尋")]'),
        (By.XPATH, '//input[contains(@placeholder, "Search")]'),
        (By.CSS_SELECTOR, 'input[type="search"]'),
        (By.CSS_SELECTOR, 'input[name="search"]'),
    ]

    def open(self):
        self.driver.get(self.URL)
        #關popup
        close_popups_best_effort(self.driver)

    def search(self, keyword: str):
        #關popup
        close_popups_best_effort(self.driver)

        term = quote(keyword)
        # 直接到 results + Channels tab
        self.driver.get(f"https://www.twitch.tv/search?term={term}&tab=channels")

        close_popups_best_effort(self.driver)

        # 等待確保 results 有載入
        wait_visible(
            self.driver,
            By.XPATH,
            '//a[starts-with(@href,"/") and not(starts-with(@href,"/search"))]',
            timeout=20
        )

    def scroll_down_times(self, times: int = 2):
        #關popup
        close_popups_best_effort(self.driver)
        scroll_down(self.driver, times=times)

    def select_first_streamer_result(self):
        #關popup
        close_popups_best_effort(self.driver)

        # Step 1: 點「頻道」tab
        tab = wait_visible(self.driver, By.XPATH, '//*[normalize-space()="頻道" or normalize-space()="Channels"]', timeout=15)
        tab.click()
        time.sleep(0.2)
        close_popups_best_effort(self.driver)

        # Step 2: 找第一個 streamer link（排除首頁/分類/影片/剪輯）
        streamer_xpath = (
            '//main//a['
            '('
            'starts-with(@href,"/")'
            ' or starts-with(@href,"https://www.twitch.tv/")'
            ' or starts-with(@href,"https://m.twitch.tv/")'
            ')'
            ' and string-length(@href) > 1'
            ' and not(@href="/")'
            ' and not(contains(@href,"/search"))'
            ' and not(contains(@href,"/directory"))'
            ' and not(contains(@href,"/videos"))'
            ' and not(contains(@href,"/clip"))'
            ']'
        )


        el = wait_first_visible(self.driver, By.XPATH, streamer_xpath, timeout=20)

        # JS click
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center', inline: 'center'});", el
        )
        time.sleep(0.3)

        try:
            el.click()
        except ElementClickInterceptedException:
            # 用 JS click 確保有進入
            self.driver.execute_script("arguments[0].click();", el)

    def go_to_channels_tab(self):
        close_popups_best_effort(self.driver)
        tab = wait_visible(
            self.driver,
            By.XPATH,
            '//*[normalize-space()="頻道" or normalize-space()="Channels"]',
            timeout=15
        )
        tab.click()
