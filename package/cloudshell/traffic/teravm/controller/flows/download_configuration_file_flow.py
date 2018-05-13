import urllib
import ftplib
import tempfile

from scp import SCPClient
from cloudshell.traffic.teravm.cli import ctrl_command_templates
from cloudshell.cli.command_template.command_template_executor import CommandTemplateExecutor
from cloudshell.devices.networking_utils import UrlParser
from cloudshell.traffic.teravm import exceptions

from cloudshell.traffic.teravm.controller import constants


class TeraVMDownloadConfigurationFlow(object):
    def __init__(self, logger):
        """

        :param logging.Logger logger:
        """
        self._logger = logger
        self._protocol_handler_map = {
            "http": self._process_http,
            "ftp": self._process_ftp,
            "sftp": self._process_sftp,
            "scp": self._process_scp,
        }

    def _process_http(self, file_path):
        """

        :param file_path:
        :return:
        """
        tmp_file, _ = urllib.urlretrieve(file_path)

        return tmp_file

    def _process_ftp(self, file_path):
        """

        :param file_path:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_path)

        address = full_path_dict.get(UrlParser.HOSTNAME)
        username = full_path_dict.get(UrlParser.USERNAME)
        password = full_path_dict.get(UrlParser.PASSWORD)
        port = full_path_dict.get(UrlParser.PORT)
        path = full_path_dict.get(UrlParser.PATH)
        filename = full_path_dict.get(UrlParser.FILENAME)

        ftp = ftplib.FTP()
        ftp.connect(host=address, port=port)
        ftp.login(user=username, passwd=password)
        ftp.cwd(path)

        tmp_file = tempfile.NamedTemporaryFile(delete=False)

        try:
            ftp.retrbinary("RETR " + filename, tmp_file.write)
        except:
            raise Exception("Unable to download configuration file via FTP")

        return tmp_file.name

    def _process_sftp(self, file_path):
        """

        :param file_path:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_path)

    def _process_scp(self, file_path):
        """

        :param file_path:
        :return:
        """
        full_path_dict = UrlParser().parse_url(file_path)

    def execute_flow(self, file_path):
        """

        :param str file_path: filename or full path to file
        :rtype: str
        """
        full_path_dict = UrlParser().parse_url(file_path)
        self._logger.info("Parsed config file link: {}".format(full_path_dict))

        protocol = full_path_dict.get(UrlParser.SCHEME)
        handler = self._protocol_handler_map.get(protocol)

        if handler is None:
            raise Exception("Unable to download configuration file '{}'. Invalid protocol type '{}'"
                            .format(file_path, protocol))
