
import logging
from base_module import BaseModule


class CommandModule(BaseModule):
    name = "command"

    def process(self, ssh_client):
        username = ssh_client.get_transport().get_username()
        logger = logging.getLogger(username)

        cmd = self.params['cmd']

        _, stdout, stderr = ssh_client.exec_command(cmd)

        output = stdout.read().decode().strip()
        logger.info(f"Output {cmd} : {output}")

        if stderr.channel.recv_exit_status() != 0:
            error = stderr.read().decode().strip()
            logger.error(f"Command failed: {cmd}")
            logger.error(f"Error message: {error}")
            self.status = 'FAILED'
        else:
            logger.info(f"Command executed successfully: {cmd}")
            self.status = 'OK'
        return self.status
