import ansible_runner
import json


config_file = 'ansible_vault_config.json'

with open(config_file, 'r') as f:
    conf = json.load(f)
    ansible_vault_password = conf.get('ansible_vault_password')

runner = ansible_runner.run.AsyncRunner(vault_password=ansible_vault_password)

