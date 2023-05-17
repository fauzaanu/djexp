import os
import subprocess
import sys

def setup_postgres():
    # read the .env file to get the database settings from one directory above
    db_name = ""
    db_user = ""
    db_password = ""
    db_host = ""
    db_port = ""
    with open("../.env", "r") as file:
        print("Reading the .env file...")
        lines = file.readlines()
        
        for line in lines:
            if "DB_NAME" in line:
                db_name = line.split("=")[1].strip()
            elif "DB_USER" in line:
                db_user = line.split("=")[1].strip()
            elif "DB_PASSWORD" in line:
                db_password = line.split("=")[1].strip()
            elif "DB_HOST" in line:
                db_host = line.split("=")[1].strip()
            elif "DB_PORT" in line:
                db_port = line.split("=")[1].strip()


    print("DB_NAME: ", db_name)
    print("DB_USER: ", db_user)
    print("DB_PASSWORD: ", db_password)
    print("DB_HOST: ", db_host)
    print("DB_PORT: ", db_port)

    # Define your PostgreSQL connection information
    db_name = db_name
    user = db_user
    password = db_password
    host = db_host
    port = db_port

    # Set the necessary environment variables for PostgreSQL authentication
    env = {
        "PGPASSWORD": password,
        **os.environ
    }

    # Execute the createdb command using subprocess
    createdb_command = ["createdb", "-U", user, "-h", host, "-p", port, db_name]
    result = subprocess.run(createdb_command, env=env, capture_output=True, text=True)

    # Check if the command was successful
    if result.returncode == 0:
        print("Database created successfully")
    else:
        print(f"Error creating database: {result.stderr}")

    # Execute the psql commands using subprocess
    psql_commands = [
        f"CREATE USER dbadmin WITH PASSWORD '{password}';",
        f"ALTER ROLE dbadmin SET client_encoding TO 'utf8';",
        f"ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';",
        f"ALTER ROLE dbadmin SET timezone TO 'UTC';",
        f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO dbadmin;"
    ]
    psql_command = f"psql -U {user} -h {host} -p {port} -c "
    for command in psql_commands:
        full_command = psql_command + f"'{command}'"
        result = subprocess.run(full_command, env=env, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Command executed successfully: {command}")
        else:
            print(f"Error executing command: {command}\n{result.stderr}")

    # Check if the commands were successful
    if all(result.returncode == 0 for result in results):
        print("PostgreSQL setup completed successfully")
    else:
        print("PostgreSQL setup completed with errors")


if __name__ == "__main__":
    setup_postgres()
