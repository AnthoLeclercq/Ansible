from base_module import BaseModule
import logging
from jinja2 import Environment, FileSystemLoader


class TemplateModule(BaseModule):
    name = "template"

    def __init__(self, params: dict):
        super().__init__(params)
        self.template_env = Environment(loader=FileSystemLoader('.'))

    def process(self, ssh_client):
        src = self.params['src']
        dest = self.params['dest']
        vars = self.params.get('vars', {})

        username = ssh_client.get_transport().get_username()
        logger = logging.getLogger(username)

        with open(src, 'r') as file:
            content = file.read()

        templated_content = self.render_template(content, vars)

        try:
            with ssh_client.open(dest, 'w') as file:
                file.write(templated_content)
            self.status = 'OK'
        except FileNotFoundError:
            logger.error(f"File {dest} doesn't exist.")
            self.status = 'FAILED'
        except Exception as e:
            logger.error(f"An error occurred, check rights: {e}")
            self.status = 'FAILED'
        return self.status

    def render_template(self, content, vars):
        template = self.template_env.from_string(content)
        return template.render(vars)
