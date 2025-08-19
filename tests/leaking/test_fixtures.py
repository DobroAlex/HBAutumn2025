import subprocess
import time

import psutil
import pytest


@pytest.fixture(scope="session")
def no_teardown_fixture():
    # Let's create some resources or a state without removing
    # ...
    proc = subprocess.Popen("notepad.exe")
    return proc


def test_no_teardown_fixture(no_teardown_fixture):
    # Do something...
    pass
    # Neither the test nor the function are closing the window -> it hangs forever


def test_trying_to_handle_inside_the_test(no_teardown_fixture):
    # Do something
    # Oh no, something unexpected has happened!
    raise RuntimeError("💀☠")

    # noinspection PyUnreachableCode
    psutil.Process(no_teardown_fixture.pid).kill()


@pytest.fixture(scope="session")
def auto_handling_fixture():
    proc = subprocess.Popen("notepad.exe")
    time.sleep(5)
    yield proc
    psutil.Process(proc.pid).kill()


def test_relying_on_auto_handling_fixture(auto_handling_fixture):
    # Do something
    # Oh no, something unexpected has happened!
    raise RuntimeError("💀☠")
