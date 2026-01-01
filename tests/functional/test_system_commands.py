from rubix_cli.core import commands
from tests import utils


def test_uname_command(capfd, commander):
    cmd = commands.UnameCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 2
    assert output[0].endswith("uname")


def test_get_rtc_command(capfd, commander):
    cmd = commands.GetRtcCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 9


def test_set_rtc_command(capfd, commander):
    cmd = commands.SetRtcCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 1
    assert output[0].endswith("setting rtc")
