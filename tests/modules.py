from tests import utils
from rubix_cli.core import Commander, commands


def assert_no_files(commander: Commander, capfd):
    cmd = commands.LsCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 2
    assert output[0].endswith("ls at '/'")
    assert output[1].endswith("No files at /")
