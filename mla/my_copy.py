import os
import shutil
from base_module import BaseModule
import logging


class CopyModule(BaseModule):
    name = "copy"

    def process(self, ssh_client):
        src = self.params['src']
        dest = self.params['dest']
        backup = self.params.get('backup', False)

        username = ssh_client.get_transport().get_username()
        logger = logging.getLogger(username)

        try:
            if backup and os.path.exists(dest):
                ssh_client.run(f"cp -r {dest} {dest}.bak")
            shutil.copytree(src, dest)
            logger.info(f"Copy {src} to {dest} done.")
            self.status = 'OK'
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            self.status = 'FAILED'
        return self.status
