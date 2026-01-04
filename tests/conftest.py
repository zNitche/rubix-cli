import time
import pytest
from rubix_cli.core import Commander
from rubix_cli.core.commands import PurgeCommand


def pytest_addoption(parser):
    parser.addoption("--device", action="store", default="example, /dev/tty1")


def pytest_sessionstart(session: pytest.Session):
    device_path = session.config.getoption("--device")
    commander = Commander(interface=device_path)

    setattr(session, "rubix_commander", commander)

    cmd = PurgeCommand(commander=commander)
    cmd.exec()
    time.sleep(0.2)

    commander.soft_reboot()

    time.sleep(0.2)


def pytest_sessionfinish(session: pytest.Session):
    commander = getattr(session, "rubix_commander")

    cmd = PurgeCommand(commander=commander)
    cmd.exec()


@pytest.fixture(scope="session")
def commander(request):
    device_path = request.config.getoption("--device")

    return Commander(interface=device_path)
