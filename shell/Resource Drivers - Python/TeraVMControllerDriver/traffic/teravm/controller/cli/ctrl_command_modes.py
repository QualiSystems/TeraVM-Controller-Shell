from collections import OrderedDict

from cloudshell.cli.command_mode import CommandMode


class DefaultCommandMode(CommandMode):
    PROMPT = r':~\$'
    ENTER_COMMAND = ''
    EXIT_COMMAND = ''

    def __init__(self):
        super(DefaultCommandMode, self).__init__(DefaultCommandMode.PROMPT,
                                                 DefaultCommandMode.ENTER_COMMAND,
                                                 DefaultCommandMode.EXIT_COMMAND)


class CliCommandMode(CommandMode):
    PROMPT = r'cli>'
    ENTER_COMMAND = 'cli'
    EXIT_COMMAND = 'exit'

    def __init__(self):
        super(CliCommandMode, self).__init__(
            CliCommandMode.PROMPT,
            CliCommandMode.ENTER_COMMAND,
            CliCommandMode.EXIT_COMMAND,
            enter_action_map=self.enter_action_map(),
            exit_action_map=self.exit_action_map(),
            enter_error_map=self.enter_error_map(),
            exit_error_map=self.exit_error_map())

    def enter_actions(self, cli_operations):
        pass

    def enter_action_map(self):
        return OrderedDict()

    def enter_error_map(self):
        return OrderedDict()

    def exit_action_map(self):
        return OrderedDict()

    def exit_error_map(self):
        return OrderedDict()


CommandMode.RELATIONS_DICT = {
    DefaultCommandMode: {
        CliCommandMode: {}
    }
}


# ERROR_MAP = OrderedDict({r'Could not check out the required':
#                              'Failed to acquire teravm license',
#                          r'command not found': 'command not found',
#                          r'NullPointerException': 'NullPointerException',
#                          r'DiversifEyeException': 'DiversifEyeException'})