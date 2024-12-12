# File: connect.py
import psycopg2
from sshtunnel import SSHTunnelForwarder

# SSH configuration
SSH_CONFIG = {
    "ssh_host": "103.253.20.13",      # SSH server address
    "ssh_port": 22,                   # SSH port
    "ssh_user": "ubuntu",             # SSH username
    "ssh_private_key": "C:/Users/User/.ssh/id_rsa"  # Path to SSH private key
}

# PostgreSQL configuration
DB_CONFIG = {
    "db_host": "localhost",           # PostgreSQL host (usually localhost via SSH tunnel)
    "db_port": 5434,                  # PostgreSQL port
    "db_name": "dify",                # Database name
    "db_user": "postgres",            # PostgreSQL username
    "db_password": "difyai123456"     # PostgreSQL password
}

def connect_to_database():
    """
    Connect to PostgreSQL database via SSH Tunnel.
    """
    try:
        tunnel = SSHTunnelForwarder(
            (SSH_CONFIG["ssh_host"], SSH_CONFIG["ssh_port"]),
            ssh_username=SSH_CONFIG["ssh_user"],
            ssh_private_key=SSH_CONFIG["ssh_private_key"],
            remote_bind_address=(DB_CONFIG["db_host"], DB_CONFIG["db_port"])
        )
        tunnel.start()
        print("SSH Tunnel connected!")

        connection = psycopg2.connect(
            dbname=DB_CONFIG["db_name"],
            user=DB_CONFIG["db_user"],
            password=DB_CONFIG["db_password"],
            host="127.0.0.1",  # Localhost via SSH Tunnel
            port=tunnel.local_bind_port
        )
        print("PostgreSQL connection successful!")
        return tunnel, connection

    except Exception as e:
        print("An error occurred while connecting:", e)
        raise
    

if __name__ == "__main__":
    connect_to_database()