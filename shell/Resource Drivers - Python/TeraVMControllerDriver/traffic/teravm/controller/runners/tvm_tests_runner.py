from traffic.teravm.controller.cli.ctrl_handler import TeraVMControllerCliHandler


class TeraVMTestsRunner(object):
    TEST_GROUP_NAME = "CS_TEST_GROUP"

    def __init__(self, cli, cs_api, resource_config, logger):
        """

        :param cli: CLI object
        :param cs_api: cloudshell api object
        :param logging.Logger logger:
        :return:
        """
        self.cli = cli
        self.cs_api = cs_api
        self.logger = logger
        self.resource_config = resource_config

    @property
    def cli_handler(self):
        return TeraVMControllerCliHandler(self.cli, self.resource_config, self.logger, self.cs_api)

    def start_tests_flow(self):
        pass

    def stop_tests_flow(self):
        pass

    def start_tests(self, user):
        # todo: execute in flow
        with self.cli_handler.get_cli_service(self.cli_handler.default_mode) as session:
            response = session.send_command(command="startTestGroup {} -u {}".format(self.TEST_GROUP_NAME, user))
            return response

    def stop_tests(self, user):
        # todo: execute in flow
        with self.cli_handler.get_cli_service(self.cli_handler.default_mode) as session:
            response = session.send_command(command="stopTestGroup {} -u {}".format(self.TEST_GROUP_NAME, user))
            return response
