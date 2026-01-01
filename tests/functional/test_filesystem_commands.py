import os
from rubix_cli.core import commands
from tests.modules import assert_no_files
from tests import utils


def test_ls_command_for_empty(capfd, commander):
    assert_no_files(commander, capfd)


def test_upload_file_command(capfd, commander):
    cmd = commands.UploadFileCommand(commander=commander)

    source_path = os.path.join("tests", "mocks", "uname_mock.mp-py")
    cmd.exec(source_path=source_path, target_path="uname_mock.py")

    output = utils.get_stderr(capfd)

    assert len(output) == 1
    assert output[0].endswith("tests/mocks/uname_mock.mp-py -> uname_mock.py")


def test_ls_command(capfd, commander):
    cmd = commands.LsCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 4
    assert output[0].endswith("ls at '/'")
    assert output[3].endswith("uname_mock.py")


def test_cat_command(capfd, commander):
    cmd = commands.CatCommand(commander=commander)
    cmd.exec(path="/uname_mock.py")

    output = utils.get_stderr(capfd)

    assert len(output) == 4


def test_rm_command(capfd, commander):
    cmd = commands.RmCommand(commander=commander)
    cmd.exec(path="/uname_mock.py")

    output = utils.get_stderr(capfd)

    assert len(output) == 1
    assert output[0].endswith("rm '/uname_mock.py'")


def test_mkdir_command(capfd, commander):
    cmd = commands.MkDirCommand(commander=commander)
    cmd.exec(path="/test_dir")

    output = utils.get_stderr(capfd)

    assert len(output) == 1
    assert output[0].endswith("mkdir '/test_dir'")

    cmd = commands.LsCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 4
    assert output[0].endswith("ls at '/'")
    assert output[3].endswith("[directory] test_dir")


def test_rmdir_command(capfd, commander):
    cmd = commands.RmDirCommand(commander=commander)
    cmd.exec(path="/test_dir")

    output = utils.get_stderr(capfd)

    assert len(output) == 2
    assert output[0].endswith("rmdir '/test_dir'")
    assert output[1].endswith("removed /test_dir")

    assert_no_files(commander, capfd)


def test_flash_command(capfd, commander):
    source_path = os.path.join("tests", "mocks", "flash_mocks")

    cmd = commands.FlashCommand(commander=commander)
    cmd.exec(root_path=source_path)

    output = utils.get_stderr(capfd)

    assert len(output) == 7

    assert output[0].endswith("flashing 'tests/mocks/flash_mocks'")
    assert output[4].endswith(".flashignore has been loaded, found 1 rules")

    cmd = commands.LsCommand(commander=commander)
    cmd.exec()

    output = utils.get_stderr(capfd)

    assert len(output) == 4

    assert output[0].endswith("ls at '/'")
    assert output[3].endswith("main.py")
