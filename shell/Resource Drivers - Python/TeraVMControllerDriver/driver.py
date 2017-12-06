from cloudshell.core.context.error_handling_context import ErrorHandlingContext
from cloudshell.devices.driver_helper import get_api
from cloudshell.devices.driver_helper import get_cli
from cloudshell.devices.driver_helper import get_logger_with_thread_id
from cloudshell.shell.core.driver_context import AutoLoadDetails
from cloudshell.shell.core.resource_driver_interface import ResourceDriverInterface

from traffic.teravm.controller.runners.load_config_runner import TeraVMLoadConfigurationRunner
from traffic.teravm.controller.configuration_attributes_structure import TrafficGeneratorControllerResource


class TeraVMControllerDriver(ResourceDriverInterface):

    def initialize(self, context):
        """
        :param context: ResourceCommandContext,ReservationContextDetailsobject with all Resource Attributes inside
        :type context:  context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def get_inventory(self, context):
        """Autoload inventory. Return device structure with all standard attributes

        :type context: cloudshell.shell.core.driver_context.AutoLoadCommandContext
        :rtype: cloudshell.shell.core.driver_context.AutoLoadDetails
        """
        return AutoLoadDetails([], [])

    def load_config(self, context, config_file_location):
        """
        Load configuration file and reserve ports
        :param context: 
        :param config_file_location: 
        :return: 
        """
        logger = get_logger_with_thread_id(context)
        logger.info('Load configuration started')

        with ErrorHandlingContext(logger):
            cs_api = get_api(context)
            resource_config = TrafficGeneratorControllerResource.from_context(context=context)
            session_pool_size = int(resource_config.sessions_concurrency_limit)
            cli = get_cli(session_pool_size)
            # password = cs_api.DecryptPassword(resource_config.password).Value
            #
            load_conf_runner = TeraVMLoadConfigurationRunner(resource_config=resource_config,
                                                             cs_api=cs_api,
                                                             cli=cli,
                                                             logger=logger)

            return load_conf_runner.load_configuration('test_file_location')
            # self.logger.debug('API instance: {}'.format(self.api))
            # reservation_id = self.context.reservation.reservation_id

    def start_traffic(self, context, blocking):
        """Start traffic

        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        :param blocking:
        """
        pass

    def stop_traffic(self, context):
        """Stop traffic and unreserving ports

        :param context: the context the command runs on
        :type context: cloudshell.shell.core.driver_context.ResourceRemoteCommandContext
        """
        pass

    def get_statistics(self, context, view_name, output_type):
        """Get real time statistics

        :param context: 
        :param view_name: 
        :param output_type: 
        :return: 
        """
        pass

    def get_results(self, context):
        """
        Attach result file to the reservation
        :param context: 
        :return: 
        """
        pass

    def get_test_file(self, context, test_name):
        """Download test file configuration and put to the folder defined in Test Files Location attribute

        :param context: 
        :param test_name: Name of the test
        :return: 
        """
        pass

    def cleanup_reservation(self, context):
        """Clear reservation when it ends

        :param context: 
        :return: 
        """
        pass

    def cleanup(self):
        """

        :return: 
        """
        pass

    def keep_alive(self, context, cancellation_context):
        """

        :param context:
        :param cancellation_context:
        :return:
        """
        pass


if __name__ == "__main__":
    import mock
    from cloudshell.shell.core.context import ResourceCommandContext, ResourceContextDetails, ReservationContextDetails

    address = '192.168.42.216'

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
    context.reservation.reservation_id = 'test_id'
    context.resource.attributes = {}
    context.resource.attributes['User'] = user
    context.resource.attributes['Password'] = password
    context.resource.attributes["CLI TCP Port"] = 22
    context.resource.attributes["CLI Connection Type"] = "ssh"
    context.resource.attributes["Sessions Concurrency Limit"] = 1
    context.resource.address = address

    context.connectivity = mock.MagicMock()
    context.connectivity.server_address = "192.168.85.48"

    dr = TeraVMControllerDriver()

    with mock.patch('__main__.get_api') as get_api:
        get_api.return_value = type('api', (object,), {
            'DecryptPassword': lambda self, pw: type('Password', (object,), {'Value': pw})()})()

        # out = dr.get_inventory(context)
        #
        # for xx in out.resources:
        #     print xx.__dict__

        out = dr.load_config(context, "test_conf_location")

        print(out)
