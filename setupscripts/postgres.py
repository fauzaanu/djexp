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
    
    # grant permission to current user to edit the file
    os.system(f"sudo chown {os.getlogin()} /etc/postgresql/{postgres_version}/main/pg_hba.conf")
    
    original_lines = []
    with open(f"/etc/postgresql/{postgres_version}/main/pg_hba.conf", "w") as file:
        for line in lines:
            original_lines.append(line)
            if "local" in line and "all" in line and "peer" in line:
                file.write(line.replace("peer", "trust"))
            else:
                file.write(line)
            
            
    
    
    
    # restart postgresql
    os.system(f"sudo systemctl restart postgresql@{postgres_version}-main")
    
    
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
        for line in original_lines:
            file.write(line)



if __name__ == "__main__":
    setup_postgres()
