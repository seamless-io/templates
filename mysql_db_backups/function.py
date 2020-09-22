import os

import paramiko

SERVER_IP = os.getenv('SERVER_IP')
SSH_PORT = int(os.getenv('SSH_PORT'))
SSH_USER = os.getenv('SSH_USER')
SSH_PASSWORD = os.getenv('SSH_PASSWORD')
DB_BIND_HOST = os.getenv('DB_BIND_HOST')
DB_BIND_PORT = int(os.getenv('DB_BIND_PORT'))
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')


def execute_over_ssh(ssh_client, cmd):
    ssh_stdin, ssh_stdout, ssh_stderr = ssh_client.exec_command(cmd)
    errors = ssh_stderr.read().decode("utf-8")
    if errors:
        if "error" in errors.lower():
            raise Exception(errors)
    return ssh_stdout.read()


if __name__ == "__main__":
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SERVER_IP, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)

    execute_over_ssh(ssh, "mkdir -p ~/db_backups")
    execute_over_ssh(ssh, f"mysqldump -u {DB_USER} -p{DB_PASSWORD} --all-databases "
                          f"--ignore-table=mysql.innodb_index_stats --ignore-table=mysql.innodb_table_stats | "
                          f"gzip > ~/db_backups/`date '+%m-%d-%Y'`.sql.gz")
