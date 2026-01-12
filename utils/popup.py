from __future__ import annotations
import time
from typing import Iterable, Tuple
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

Selector = Tuple[str, str]  # (By.*, selector)


def _safe_click(driver: WebDriver, by: str, sel: str) -> bool:
    try:
        #找所有可能的元素
        els = driver.find_elements(by, sel)
        for el in els:
            if el.is_displayed() and el.is_enabled():
                try:
                    el.click()
                    return True
                except Exception:
                    # 有時候被遮住，改用 JS click
                    driver.execute_script("arguments[0].click();", el)
                    return True
        return False
    except Exception:
        return False


def close_popups_best_effort(driver: WebDriver, loops: int = 3, pause_sec: float = 0.4) -> None:
    # 常見：cookie/consent "Accept", "I Agree", "同意", "接受"
    accept_candidates: Iterable[Selector] = [
        (By.CSS_SELECTOR, 'button[data-a-target*="consent"]'),
        (By.CSS_SELECTOR, 'button[aria-label*="Accept"]'),
        (By.CSS_SELECTOR, 'button[aria-label*="同意"]'),
        (By.CSS_SELECTOR, 'button[aria-label*="接受"]'),
        (By.XPATH, '//button[contains(., "Accept")]'),
        (By.XPATH, '//button[contains(., "I Agree")]'),
        (By.XPATH, '//button[contains(., "同意")]'),
        (By.XPATH, '//button[contains(., "接受")]'),
        (By.XPATH, '//button[contains(., "我同意")]'),
    ]

    # 常見：右上角 X / Close / 關閉
    close_candidates: Iterable[Selector] = [
        (By.CSS_SELECTOR, 'button[aria-label*="Close"]'),
        (By.CSS_SELECTOR, 'button[aria-label*="關閉"]'),
        (By.CSS_SELECTOR, 'button[aria-label="Dismiss"]'),
        (By.XPATH, '//button[contains(., "Close")]'),
        (By.XPATH, '//button[contains(., "關閉")]'),
    ]

    for _ in range(loops):
        clicked = False

        for by, sel in accept_candidates:
            if _safe_click(driver, by, sel):
                clicked = True
                time.sleep(pause_sec)
                break

        if not clicked:
            for by, sel in close_candidates:
                if _safe_click(driver, by, sel):
                    clicked = True
                    time.sleep(pause_sec)
                    break

        if not clicked:
            # 沒有任何 popup 可關就結束
            return
