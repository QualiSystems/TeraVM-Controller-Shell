from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_api
from cloudshell.devices.driver_helper import get_cli
from cloudshell.devices.driver_helper import get_logger_with_thread_id
from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from cloudshell.traffic.teravm.controller.configuration_attributes_structure import TrafficGeneratorControllerResource
from cloudshell.traffic.teravm.controller.quali_rest_api_helper import create_quali_api_instance
from cloudshell.traffic.teravm.controller.runners.cleanup_runner import TeraVMCleanupRunner
from cloudshell.traffic.teravm.controller.runners.load_config_runner import TeraVMLoadConfigurationRunner
from cloudshell.traffic.teravm.controller.runners.results_runner import TeraVMResultsRunner
from cloudshell.traffic.teravm.controller.runners.tvm_tests_runner import TeraVMTestsRunner


class TeraVMControllerDriver(ResourceDriverInterface):

    def __init__(self):
        super(TeraVMControllerDriver, self).__init__()
        self._cli = None

    def initialize(self, context):
        """

        :param context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        resource_config = TrafficGeneratorControllerResource.from_context(context)
        session_pool_size = int(resource_config.sessions_concurrency_limit)
        self._cli = get_cli(session_pool_size)

        return 'Finished initializing'

    def get_inventory(self, context):
        """Autoload inventory. Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return AutoLoadDetails([], [])

    def load_config(self, context, config_file_location):
        """Load configuration file and reserve ports

        :param context: 
        :param config_file_location: 
        :return: 
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Load configuration command started')

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            reservation_id = context.reservation.reservation_id
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            load_conf_runner = TeraVMLoadConfigurationRunner(resource_config=resource_config,
                                                             cs_api=cs_api,
                                                             cli=self._cli,
                                                             reservation_id=reservation_id,
                                                             logger=logger)

            response = load_conf_runner.load_configuration(config_file_location)
            logger.info('Load configuration command ended')

            return response

    def start_traffic(self, context):
        """Start traffic

        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Start traffic command started')

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            test_runner = TeraVMTestsRunner(resource_config=resource_config,
                                            cs_api=cs_api,
                                            cli=self._cli,
                                            logger=logger)

            response = test_runner.start_tests()
            logger.info('Start traffic command ended')

            return response

    def stop_traffic(self, context):
        """Stop traffic and unreserve ports

        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Stop traffic command started')

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            test_runner = TeraVMTestsRunner(resource_config=resource_config,
                                            cs_api=cs_api,
                                            cli=self._cli,
                                            logger=logger)

            response = test_runner.stop_tests()
            logger.info('Stop traffic command ended')

            return response

    def get_results(self, context):
        """Attach result file to the reservation

        :param context:
        :return:
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Get results command started')

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            reservation_id = context.reservation.reservation_id
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            quali_api_client = create_quali_api_instance(context, logger)
            quali_api_client.login()

            test_runner = TeraVMResultsRunner(resource_config=resource_config,
                                              cs_api=cs_api,
                                              cli=self._cli,
                                              quali_api_client=quali_api_client,
                                              reservation_id=reservation_id,
                                              logger=logger)

            response = test_runner.get_results()
            logger.info('Get results command ended')

            return response

    def cleanup_reservation(self, context):
        """Stop traffic and delete test group

        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Cleanup reservation command started')

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.create_from_chassis_resource(context=context,
                                                                                              cs_api=cs_api)

            cleanup_runner = TeraVMCleanupRunner(resource_config=resource_config,
                                                 cs_api=cs_api,
                                                 cli=self._cli,
                                                 logger=logger)

            response = cleanup_runner.cleanup_reservation()
            logger.info('Cleanup reservation command ended')

            return response

    def cleanup(self):
        """

        :return: 
        """
        pass


if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    address = '192.168.42.208'

    user = 'cli'
    password = 'diversifEye'
    port = 443
    auth_key = 'h8WRxvHoWkmH8rLQz+Z/pg=='
    api_port = 8029

    context = ResourceCommandContext()
    context.resource = ResourceContextDetails()
    context.resource.name = 'dsada'
    context.resource.fullname = 'TestAireOS'
    context.reservation = ReservationContextDetails()
    context.reservation.reservation_id = 'bea26e1a-9557-4204-8a51-8adf83f3fbd2'
    context.resource.attributes = {}
    context.resource.attributes['User'] = user
    context.resource.attributes['Password'] = password
    context.resource.attributes["CLI TCP Port"] = 22
    context.resource.attributes["CLI Connection Type"] = "ssh"
    context.resource.attributes["Sessions Concurrency Limit"] = 1
    context.resource.attributes["Test Files Location"] = "/home/anthony/Downloads/"
    context.resource.address = address

    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.9"

    dr = TeraVMControllerDriver()
    dr.initialize(context)

    # with mock.patch('__main__.get_api') as get_api:
    #     get_api.return_value = type('api', (object,), {
    #         'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        # out = dr.start_traffic(context)
    #     #
    #     # for xx in out.resources:
    #     #     print xx.__dict__
    #
    #     out = dr.load_config(context, "TestConfig.xml")
    #
    #     print(out)

    # with mock.patch('__main__.get_api') as get_api:
    #     get_api.return_value = type('api', (object,), {
    #         'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        # out = dr.get_inventory(context)
    #
    # for xx in out.resources:
    #     print xx.__dict__

    # out = dr.load_config(context, "CS_TEST.xml")
    out = dr.start_traffic(context)
    # out = dr.stop_traffic(context)
    # out = dr.get_results(context)
    # out = dr.cleanup_reservation(context)

    print(out)
