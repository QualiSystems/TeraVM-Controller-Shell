from traffic.teravm.controller.cli.ctrl_handler import TeraVMControllerCliHandler
from traffic.teravm.controller.flows.load_configuration_file_flow import TeraVMLoadConfigurationFlow


class TeraVMLoadConfigurationRunner(object):
    def __init__(self, cli, cs_api, resource_config, logger):
        """

        :param cli: CLI object
        :param cs_api: cloudshell api object
        :param logging.Logger logger:
        :return:
        """
        self._cli = cli
        self._cs_api = cs_api
        self._resource_config = resource_config
        self._logger = logger

    @property
    def cli_handler(self):
        return TeraVMControllerCliHandler(self._cli,
                                          self._resource_config,
                                          self._logger,
                                          self._cs_api)

    @property
    def load_configuration_flow(self):
        return TeraVMLoadConfigurationFlow(cli_handler=self.cli_handler,
                                           resource_config=self._resource_config,
                                           logger=self._logger)

    def load_configuration(self, test_file_path):
        """

        :param test_file_path:
        :return:
        """
        return self.load_configuration_flow.execute_flow(test_file_path)
