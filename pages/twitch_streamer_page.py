from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from utils.waits import wait_visible
from utils.popup import close_popups_best_effort


class TwitchStreamerPage(BasePage):
    def wait_until_loaded(self):
        close_popups_best_effort(self.driver)

        candidates = [
            # 追隨 / 訂閱 buttons
            (By.XPATH, '//*[normalize-space()="追隨" or normalize-space()="Follow"]'),
            (By.XPATH, '//*[normalize-space()="訂閱" or normalize-space()="Subscribe"]'),

            # 可能出現的tab
            (By.XPATH, '//*[normalize-space()="創作者基地" or normalize-space()="Home"]'),
            (By.XPATH, '//*[normalize-space()="關於" or normalize-space()="About"]'),
            (By.XPATH, '//*[normalize-space()="時間表" or normalize-space()="Schedule"]'),
            (By.XPATH, '//*[normalize-space()="影片" or normalize-space()="Videos"]'),

            # 過去的實況
            (By.XPATH, '//*[contains(text(),"過去的實況") or contains(text(),"Past broadcasts")]'),
        ]

        last_error = None
        for by, sel in candidates:
            try:
                wait_visible(self.driver, by, sel, timeout=20)
                return
            except Exception as e:
                #保留最後一次失敗的 exception
                last_error = e

        raise RuntimeError(f"[WAP] Streamer page not loaded (no stable element found). Last error: {last_error}")
