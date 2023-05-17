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

    subprocess.run(["sudo", "apt-get", "install", "postgresql", "postgresql-contrib"])
    print("Postgresql installed successfully!")
    
    # if there are any existing databases, delete them
    subprocess.run(["sudo", "-u", "postgres", "psql", "-c", f'DROP DATABASE IF EXISTS "{db_name}";'])
    
    database_name = db_name
    new_user = db_user
    
    subprocess.run(["sudo", "-u", "postgres", "createdb", database_name])
    
    subprocess.run(["sudo", "-u", "postgres", "createuser", "--superuser", new_user])
    
    db_password = db_password
    subprocess.run(["sudo", "-u", "postgres", "psql", "-c", f"CREATE USER {db_user} WITH SUPERUSER PASSWORD ''{db_password}'';"])
    
    print("User and database created successfully!")
    
    subprocess.run(["sudo", "-u", "postgres", "psql", "-c", f"ALTER ROLE {new_user} SET client_encoding TO 'utf8';"])
    
    subprocess.run(["sudo", "-u", "postgres", "psql", "-c", f"ALTER ROLE {new_user} SET default_transaction_isolation TO 'read committed';"])
    
    subprocess.run(["sudo", "-u", "postgres", "psql", "-c", f"ALTER ROLE {new_user} SET timezone TO 'UTC';"])
    
    subprocess.run(["sudo", "-u", "postgres", "psql", "-c", f"GRANT ALL PRIVILEGES ON DATABASE {database_name} TO {new_user};"])
    
    print("Please update the database settings in Project/settings.py file and run 'python manage.py migrate' to create the tables in the database.")

if __name__ == "__main__":
    setup_postgres()
