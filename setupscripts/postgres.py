import os
import subprocess
import sys
import psycopg2

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


    # Connect to the PostgreSQL server
    conn = psycopg2.connect(
        host=db_host,
        user=db_user,
        password=db_password,
        database=db_name
    )

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



if __name__ == "__main__":
    setup_postgres()
