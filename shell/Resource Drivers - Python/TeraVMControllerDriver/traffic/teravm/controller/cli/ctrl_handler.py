from cloudshell.cli.command_mode_helper import CommandModeHelper
from cloudshell.devices.cli_handler_impl import CliHandlerImpl
from traffic.teravm.controller.cli.ctrl_command_modes import DefaultCommandMode
from traffic.teravm.controller.cli.ctrl_command_modes import CliCommandMode


class TeraVMControllerCliHandler(CliHandlerImpl):
    def __init__(self, cli, resource_config, logger, api):
        super(TeraVMControllerCliHandler, self).__init__(cli, resource_config, logger, api)
        self.modes = CommandModeHelper.create_command_mode()

    @property
    def default_mode(self):
        return self.modes[DefaultCommandMode]

    @property
    def cli_mode(self):
        return self.modes[CliCommandMode]

    @property
    def enable_mode(self):
        return self.default_mode

    @property
    def config_mode(self):
        return self.default_mode
