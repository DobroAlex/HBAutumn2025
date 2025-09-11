import shutil
import subprocess
from pathlib import Path

import psutil
import pytest

from selenium import webdriver
from selenium.webdriver import ChromeOptions
# noinspection PyUnresolvedReferences
import chromedriver_binary

THIS_DIR_CHROME = (Path(__file__).parent / "chrome_profiles/").resolve().absolute()


def test_leaking_file_read():
    connections = []
    for _ in range(0, 1_000_000):
        handle = open(__file__, "r")
        connections.append(handle)
        handle.readlines()


@pytest.fixture(scope="session")
def __setup_and_clean_up_chrome_once():
    shutil.rmtree(THIS_DIR_CHROME, ignore_errors=True)
    THIS_DIR_CHROME.mkdir(exist_ok=False)
    yield
    shutil.rmtree(THIS_DIR_CHROME, ignore_errors=False)


@pytest.mark.parametrize(
    "iteration",
    (
            pytest.param(1, id="iteration №1"),
            pytest.param(2, id="iteration №2"),
    )
)
def test_my_browser_now_has_contaminated_profile(__setup_and_clean_up_chrome_once, iteration):
    options = ChromeOptions()
    options.add_argument(f"--user-data-dir={THIS_DIR_CHROME}")
    options.add_argument("--profile-directory=Default")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(options=options)

    driver.get("https://ya.ru")
    driver.get("https://google.com")

    driver.get_cookies()


def test_we_ve_got_a_zombie_of_sorts():
    my_proc = subprocess.Popen("notepad.exe")

    raise RuntimeError("Something went wrong!")

    # noinspection PyUnreachableCode
    psutil.Process(pid=my_proc.pid).kill()

