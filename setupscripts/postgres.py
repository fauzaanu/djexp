import os
import subprocess
import sys
import psycopg2
from psycopg2 import sql
import dotenv

def get_postgres_version():
    postgres_version = subprocess.check_output("psql --version", shell=True).decode("utf-8").split(" ")[2].split(".")[0]
    print(f"Postgres version: {postgres_version}")
    return int(postgres_version)

def read_env_file():
    dotenv.load_dotenv(dotenv.find_dotenv())
    db_name = os.getenv('DB_NAME')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    return db_name, db_user, db_password, db_host, db_port

def create_database_and_user(conn, db_name, db_user, db_password):
    cur = conn.cursor()
    try:
        cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name)))
    except psycopg2.errors.DuplicateDatabase:
        # delete database and recreate
        cur.execute(sql.SQL("DROP DATABASE {};").format(sql.Identifier(db_name)))
        cur.execute(sql.SQL("CREATE DATABASE {};").format(sql.Identifier(db_name)))

    try:
        create_user_query = sql.SQL("CREATE USER {} WITH PASSWORD %s;").format(sql.Identifier(db_user))
        cur.execute(create_user_query, (db_password,))
    except psycopg2.errors.DuplicateObject:
        # delete user and recreate
        cur.execute(sql.SQL("DROP USER {};").format(sql.Identifier(db_user)))
        cur.execute(create_user_query, (db_password,))
        

    cur.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {};").format(sql.Identifier(db_name), sql.Identifier(db_user)))
    cur.close()

def update_user_settings(conn, db_user):
    cur = conn.cursor()
    cur.execute(sql.SQL("ALTER ROLE {} SET client_encoding TO 'utf8';").format(sql.Identifier(db_user)))
    cur.execute(sql.SQL("ALTER ROLE {} SET default_transaction_isolation TO 'read committed';").format(sql.Identifier(db_user)))
    cur.execute(sql.SQL("ALTER ROLE {} SET timezone TO 'UTC';").format(sql.Identifier(db_user)))
    conn.commit()
    cur.close()

def update_pg_hba_conf(postgres_version, settings):
    pg_hba_conf_path = f"/etc/postgresql/{postgres_version}/main/pg_hba.conf"
    with open(pg_hba_conf_path, "w") as file:
        file.write(settings)

def setup_postgres():
    postgres_version = get_postgres_version()
    db_name, db_user, db_password, db_host, db_port = read_env_file()
    print(f"db_name: {db_name}", f"db_user: {db_user}", f"db_password: {db_password}", f"db_host: {db_host}", f"db_port: {db_port}", sep="\n")

    without_password_settings = f"""\
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             {db_user}                               peer
local   all             all                                     trust
host    all             all             127.0.0.1/32            trust
host    all             all             ::1/128                 trust
"""

    update_pg_hba_conf(postgres_version, without_password_settings)
    os.system(f"sudo systemctl restart postgresql")

    conn = psycopg2.connect(host=db_host, port=db_port, user=db_user)
    conn.autocommit = True
    create_database_and_user(conn, db_name, db_user, db_password)
    conn.close()

    with_password_settings = f"""\
# TYPE  DATABASE        USER            ADDRESS                 METHOD
local   all             {db_user}                               password
local   all             all                                     password
host    all             all             127.0.0.1/32            password
host    all             all             ::1/128                 password
"""

    update_pg_hba_conf(postgres_version, with_password_settings)
    os.system(f"sudo systemctl restart postgresql")

    conn = psycopg2.connect(host=db_host, port=db_port, database=db_name, user=db_user, password=db_password)
    update_user_settings(conn, db_user)
    conn.close()



if __name__ == "__main__":
    setup_postgres()
