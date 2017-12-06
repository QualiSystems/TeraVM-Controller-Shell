import os

from scp import SCPClient
from xml.etree import ElementTree


class TeraVMLoadConfigurationFlow(object):
    TEST_GROUP_NAME = "CS_TEST_GROUP"  # todo: remove duplicate constant !!!

    def __init__(self, cli_handler, resource_config, logger):
        """

        :param cli_handler:
        :param resource_config:
        :param logger:
        """
        self._cli_handler = cli_handler
        self._resource_config = resource_config
        self._logger = logger

    def _replace_test_name(self, test_file_path):
        tree = ElementTree.parse(test_file_path)
        root = tree.getroot()
        name = root.find('./test_group/name')
        name.text = self.TEST_GROUP_NAME

        # with open("filename", "w") as f:
        #     f.write(ET.tostring(tree))
        #
        # temp_file_path = tempfile.mktemp()
        # config.write(temp_file_path)

    def execute_flow(self, file_path):

        # todo step 2: replace test_name (we should import it later)
        # todo step 3: get all interfaces from the file and reserve ports ??? magic happens there

        file_path = self._get_existing_path(file_path)

        test_group_file, user = "/home/cli/rr.xml", "admin"

        with self._cli_handler.get_cli_service(self._cli_handler.default_mode) as session:
            scp = SCPClient(session.session._handler.get_transport())
            scp.put(file_path, "/home/cli/rr.xml")

            # todo: execute this command before importing group "cli -u admin deleteTestGroup 11"

            with session.enter_mode(self._cli_handler.cli_mode) as cli_session:
                response = session.send_command(command="importTestGroup // {} -u {}".format(test_group_file, user))
                print response
                return response

    def _get_existing_path(self, file_path):
        """Looking for existing path

        :rtype: str
        """
        return "/home/anthony/Downloads/TestConfig.xml"

        search_order = [os.pтоath.join(self.context.resource.attributes.get('Test Files Location') or '', file_path),
                        os.path.join(self.context.resource.attributes.get('Test Files Location') or '',
                                     self.context.reservation.reservation_id, file_path), file_path]
        for path in search_order:
            if os.path.exists(path):
                return path

        raise Exception('File {} does not exists or "Test Files Location" '
                        'attribute was not specified'.format(file_path))
