import logging
from base_module import BaseModule


class ServiceModule(BaseModule):
    name = "service"

    def process(self, ssh_client):
        name = self.params['name']
        state = self.params['state']

        username = ssh_client.get_transport().get_username()
        logger = logging.getLogger(username)

        if state == 'started':
            command = f"systemctl start {name}"
        elif state == 'stopped':
            command = f"systemctl stop {name}"
        elif state == 'restarted':
            command = f"systemctl restart {name}"
        elif state == 'reloaded':
            command = f"systemctl reload {name}"

        stdout, stderr = ssh_client.exec_command(command)

        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logger.info(f"Command executed successfully: {command}")
            logger.info(f"Output : {stdout}")
            self.status = 'OK'
        else:
            logger.error(f"Command failed: {command}")
            logger.error(f"Error message: {stderr.read().decode()}")
            self.status = 'FAILED'
        return self.status
