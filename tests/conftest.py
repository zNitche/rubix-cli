import time
import pytest
from rubix_cli.core import Commander
from rubix_cli.core.commands import PurgeCommand


def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="example, /dev/tty1")


def pytest_sessionstart(session):
    device_path = session.config.getoption("--device")
    commander = Commander(interface=device_path)

    cmd = PurgeCommand(commander=commander)
    cmd.exec()
    time.sleep(0.2)

    commander.soft_reboot()

    time.sleep(0.2)


@pytest.fixture(scope="session")
def commander(request):
    device_path = request.config.getoption("--device")

    return Commander(interface=device_path)
