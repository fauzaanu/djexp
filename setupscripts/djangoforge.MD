# Install the nessesary packages

```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y
sudo apt install python3-virtualenv -y
```

# handle server security

This process involves the following

- Creating a new user
- Granting the new user sudo privileges
- Setting up a basic firewall
- Setting up SSH key-based authentication
- Disabling password authentication
- Disabling remote root login

# postgres setups

```bash
sudo -u postgres psql
CREATE DATABASE django_db;
CREATE USER dbadmin WITH PASSWORD 'django';
ALTER ROLE dbadmin SET client_encoding TO 'utf8';
ALTER ROLE dbadmin SET default_transaction_isolation TO 'read committed';
ALTER ROLE dbadmin SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_db TO dbadmin;
\q
```

chmod +x create_db.sh
./create_db.sh

# gunicon and nginx setups

```

```
