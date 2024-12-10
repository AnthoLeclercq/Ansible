import logging
from base_module import BaseModule


class AptModule(BaseModule):
    name = "apt"

    def process(self, ssh_client):
        name = self.params['name']
        state = self.params['state']

        username = ssh_client.get_transport().get_username()
        logger = logging.getLogger(username)

        if state == 'present':
            command = f"apt install {name} -y"
        elif state == 'absent':
            command = f"apt remove {name} -y"

        stdout, stderr = ssh_client.exec_command(command)

        exit_status = stdout.channel.recv_exit_status()
        if exit_status == 0:
            logger.info(f"Command executed successfully: {command}")
            self.status = 'OK'
        else:
            logger.error(f"Command failed: {command}")
            logger.error(f"Error message: {stderr.read().decode()}")
            self.status = 'FAILED'
        return self.status
