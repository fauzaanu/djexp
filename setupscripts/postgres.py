# this script will setup postgresql database

import os
import subprocess
import sys

def setup_postgres():
    # read the .env file to get the database settings from one directory above
    os.system("cd ..")
    db_name = ""
    db_user = ""
    db_password = ""
    db_host = ""
    db_port = ""
    with open(".env", "r") as file:
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
    
                

    os.system("sudo apt-get install postgresql postgresql-contrib")
    print("Postgresql installed successfully!")


    database_name = db_name
    new_user = db_user
    
    os.system("""
            sudo -u postgres createdb {}
            """.format(database_name))
    
    os.system("""
              sudo -u postgres createuser --superuser {}
              """.format(new_user))
    
    print("User and database created successfully!")
    db_password = db_password
    os.system(f"""
              sudo -u postgres psql -c 'CREATE USER {db_user} WITH SUPERUSER PASSWORD '{db_password}';
              """)

    print("Please update the database settings in Project/settings.py file and run 'python manage.py migrate' to create the tables in the database.")

    # recommendation by Django 
    # ALTER ROLE dbadmin SET client_encoding TO 'utf8';
    # ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';
    # ALTER ROLE dbadmin SET timezone TO 'UTC';
    os.system("""
              sudo -u postgres psql -c 'ALTER ROLE {} SET client_encoding TO 'utf8';
              """.format(new_user))
    
    os.system("""
              sudo -u postgres psql -c 'ALTER ROLE {} SET default_transaction_isolation TO 'read committed';
              """.format(new_user))
    
    os.system("""
              sudo -u postgres psql -c 'ALTER ROLE {} SET timezone TO 'UTC';
              """.format(new_user))
    
    
    os.system("""
              sudo -u postgres psql -c 'GRANT ALL PRIVILEGES ON DATABASE {} TO {};
              """.format(database_name, new_user))
    
if __name__ == "__main__":
    setup_postgres()