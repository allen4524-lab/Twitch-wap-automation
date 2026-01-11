import os
from pages.twitch_home_page import TwitchHomePage
from pages.twitch_streamer_page import TwitchStreamerPage

def test_twitch_wap_search_and_screenshot(driver):
    os.makedirs("artifacts", exist_ok=True)

    try:
        home = TwitchHomePage(driver)
        home.open()
        home.search("StarCraft II")
        home.scroll_down_times(2)
        home.select_first_streamer_result()

        streamer = TwitchStreamerPage(driver)
        streamer.wait_until_loaded()
        streamer.take_screenshot("artifacts/streamer_page.png")

    except Exception:
        driver.save_screenshot("artifacts/FAILED.png")
        with open("artifacts/url.txt", "w", encoding="utf-8") as f:
            f.write(driver.current_url)
        raise
