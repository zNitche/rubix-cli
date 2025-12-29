from rubix_cli.core.commands import CommandBase


class RebootCommand(CommandBase):
    def exec(self):
        self._commander.soft_reboot()
