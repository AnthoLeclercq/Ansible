from setuptools import setup

setup(
    name='mla',
    version='1.0',
    py_modules=['mla', 'mla_script', '__init__', 'base_module', 'my_copy',
                'my_apt', 'my_command', 'my_service', 'my_sysctl', 'my_template'],
    package_data={'': ['inventory.yml', 'todos.yml']},
    entry_points={
        'console_scripts': [
            'mla=mla_script:cli_entry_point',
        ],
    },
)
