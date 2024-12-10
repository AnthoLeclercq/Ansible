import logging
from base_module import BaseModule


class SysctlModule(BaseModule):
    name = "sysctl"

    def process(self, ssh_client):
        username = ssh_client.get_transport().get_username()
        logger = logging.getLogger(username)

        params = self.params

        for key, value in params.items():
            stdin, stdout, stderr = ssh_client.exec_command(
                f"sysctl {key}={value}")
            if stderr.read():
                logger.error(f"Failed to set sysctl parameter: {key}={value}")
                self.status = 'FAILED'
            else:
                logger.info(
                    f"Successfully set sysctl parameter: {key}={value}")
                logger.info(f"Output : {stdout}")
                self.status = 'OK'
        return self.status
