"""
Let's see how some resources are auto handled
and others are not.
"""
import subprocess

# noinspection PyUnresolvedReferences
import chromedriver_binary
import psutil
from selenium import webdriver
from selenium.webdriver import ChromeOptions


def test_selenium_and_webdriver_self_close():
    """
    Even despite the explicit resources close
    webdriver is closed and doesn't hang up
    """
    driver = webdriver.Chrome(options=ChromeOptions())
    driver.get("https://heisenbug.ru")
    raise RuntimeError("☠☠☠")
    driver.close()


def test_process_hangs_up_and_pollutes():
    """
    Unlike web driver, this process will hang up pretty much 4ever
    until it's either killed by the system or closed manually.
    """
    my_proc = subprocess.Popen("notepad.exe")
    raise RuntimeError("☠☠☠")
    psutil.Process(pid=my_proc.pid).kill()
