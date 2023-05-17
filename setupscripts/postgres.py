import os
import subprocess
import sys
import psycopg2

def setup_postgres():
    
    # edit the pg_hba.conf file to allow without password
    
    # get the postgres version
    postgres_version = subprocess.check_output("psql --version", shell=True).decode("utf-8").split(" ")[2].split(".")[0]
    print(f"Postgres version: {postgres_version}")
    
    # postgres_version maybe a decimal number, so we need to convert it to an integer
    postgres_version = int(postgres_version)
    
    
    without_password_settings = """
  # TYPE  DATABASE        USER            ADDRESS                 METHOD
  local   all             all                                     trust
  host    all             all             127.0.0.1/32            trust
  host    all             all             ::1/128                 trust
    """

    
    # create a new pg_hba.conf file allowing without password
    with open(f"/etc/postgresql/{postgres_version}/main/pg_hba.conf", "w") as file:
        file.write(without_password_settings)
        
    # restart postgresql
    os.system(f"sudo systemctl restart postgresql")
    
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


    # Connect to the PostgreSQL server we dont have a user or database yet
    conn = psycopg2.connect(host=db_host, port=db_port, user=db_user,)

        

    # Create a cursor object
    cur = conn.cursor()

    # Execute SQL statements to create the database and user
    cur.execute(f"CREATE DATABASE {db_name};")
    cur.execute(f"CREATE USER {db_user} WITH ENCRYPTED PASSWORD '{db_password}';")
    cur.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {db_user};")
    
    conn.commit()
    cur.close()
    conn.close()
    
    # create the pg_hba.conf file allowing with password for the new user only
    with_password_settings = f"""
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             all                                     md5
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
"""
    
    # create a new pg_hba.conf file allowing with password for the new user only
    with open(f"/etc/postgresql/{postgres_version}/main/pg_hba.conf", "w") as file:
        file.write(with_password_settings)
        
    # restart postgresql
   
    os.system(f"sudo systemctl restart postgresql")
    
    # Connect to the PostgreSQL server again with the new user and database
    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    
    # Create a cursor object
    cur = conn.cursor()

    # Execute SQL statements to set the default encoding and timezone
    cur.execute(f"ALTER ROLE {db_user} SET client_encoding TO 'utf8';")
    cur.execute(f"ALTER ROLE {db_user} SET default_transaction_isolation TO 'read committed';")
    cur.execute(f"ALTER ROLE {db_user} SET timezone TO 'UTC';")
    
    

    # Commit the changes to the database
    conn.commit()

    # Close the cursor and the connection
    cur.close()
    conn.close()
    
    # edit the pg_hba.conf file to allow with password
    with open(f"/etc/postgresql/{postgres_version}/main/pg_hba.conf", "w") as file:
        for line in lines:
            print("Writing original line: "+line)
            file.write(line)



if __name__ == "__main__":
    setup_postgres()
