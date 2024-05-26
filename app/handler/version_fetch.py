import os
import json
import paramiko

def update_service_versions(directory, results_file, private_key_path):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    private_key = paramiko.RSAKey(filename=private_key_path)

    files = os.listdir(directory)

    results = {}

    for file in files:
        with open(os.path.join(directory, file), 'r') as f:
            data = json.load(f)

            for host in data['hosts']:
                for service in data['services']:
                    try:
                        ssh.connect(host, username='username', pkey=private_key)

                        sftp = ssh.open_sftp()
                        with sftp.file(f'/opt/{service}/VERSION', 'r') as version_file:
                            version = version_file.read().strip()

                        results.setdefault(host, {})[service] = version

                        sftp.close()
                        ssh.close()
                    except Exception as e:
                        print(f"Failed to get version for {service} on {host}: {e}")

    with open(results_file, 'w') as f:
        json.dump(results, f, indent=4)

