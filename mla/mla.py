import argparse
import logging
import yaml
import paramiko
import os
from my_copy import CopyModule
from my_apt import AptModule
from my_template import TemplateModule
from my_service import ServiceModule
from my_sysctl import SysctlModule
from my_command import CommandModule

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('mla')


def load_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"Tasks file {file_path} doesn't exist.")
    except yaml.YAMLError as e:
        logger.error(f'Error reading YAML file: {e}')
    return None


def initialize_ssh_client(address, port, username, password, key_file):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    if key_file:
        key_file = os.path.expanduser(key_file)
        private_key = paramiko.RSAKey.from_private_key_file(key_file)
        client.connect(address, port=port, username=username,
                       password=password, pkey=private_key)
    else:
        client.connect(address, port=port,
                       username=username, password=password)
    return client


def call_module(client, module_name, module_params):
    modules = {
        'copy': CopyModule,
        'apt': AptModule,
        'template': TemplateModule,
        'service': ServiceModule,
        'sysctl': SysctlModule,
        'command': CommandModule
    }

    if module_name not in modules:
        logger.error(f"Unsupported module: {module_name}")
        return "KO"

    module = modules[module_name](module_params)

    try:
        status = module.process(client)
        return status
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return "FAILED"


def process_tasks(client, tasks):
    stats = {'OK': 0, 'CHANGED': 0, 'FAILED': 0}

    for index, task in enumerate(tasks, start=1):
        module_name = task['module']
        module_params = task['params']

        logger.info(f'[{index}] op={module_name} params={module_params}')

        status = call_module(client, module_name, module_params)
        logger.info(f'Task [{index}] status={status}')

        if status == 'FAILED':
            logger.error(f'Task [{index}] failed.')
            stats['FAILED'] += 1
        elif status == 'CHANGED':
            stats['CHANGED'] += 1
        else:
            stats['OK'] += 1

    return stats


def ssh(inventory, tasks):
    stats = {}

    for host, params in inventory['hosts'].items():
        ssh_address = params['ssh_address']
        ssh_port = params.get('ssh_port', 22)
        ssh_user = params.get('ssh_user')
        ssh_password = params.get('ssh_password')
        ssh_key_file = params.get('ssh_key_file')

        if not ssh_user and not ssh_password:
            logger.error(
                f"Invalid authentication configuration for host {host}.")
            continue

        client = initialize_ssh_client(
            ssh_address, ssh_port, ssh_user, ssh_password, ssh_key_file)
        logger_host = logging.getLogger(ssh_user)

        logger_host.info(f'Connected to host {ssh_address}')

        stats[host] = process_tasks(client, tasks)

        client.close()
        logger_host.info(f'Disconnected from host {ssh_address}')

        host_status = 'OK' if stats[host]['FAILED'] == 0 else 'FAILED'
        logger_host.info(f'host={ssh_address} status={host_status}')

    return stats


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-f', '--todos', help='To-Do Tasks YAML File', required=True)
    parser.add_argument('-i', '--inventory',
                        help='Host Inventory YAML File', required=True)
    args = parser.parse_args()

    todos_file = args.todos
    inventory_file = args.inventory

    todos = load_yaml_file(todos_file)
    inventory = load_yaml_file(inventory_file)

    if todos is None or inventory is None:
        return

    host_ips = [inventory['hosts'][host]['ssh_address']
                for host in inventory['hosts']]
    logger.info(
        f'Processing {len(todos)} tasks on hosts: {", ".join(host_ips)}')

    stats = ssh(inventory, todos)

    logger.info(f'Done processing tasks on hosts: {", ".join(host_ips)}')
    logger.info('Final statistics:')
    for host, values in stats.items():
        logger.info(
            f'host={host} ok={values["OK"]} changed={values["CHANGED"]} fail={values["FAILED"]}')


if __name__ == '__main__':
    main()
