import pytest
from utils.driver_factory import create_mobile_emulation_driver

@pytest.fixture(scope="function")
def driver():
    driver = create_mobile_emulation_driver()
    yield driver
    driver.quit()
