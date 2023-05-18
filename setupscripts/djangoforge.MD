# Install the nessesary packages

```bash
sudo apt update -y
sudo apt upgrade -y
sudo apt install python3-pip python3-dev libpq-dev postgresql postgresql-contrib nginx curl -y
sudo apt install python3-virtualenv -y
sudo apt install supervisor -y
sudo apt install nodejs npm -y
```

# handle server security

# postgres setups (Or run create_db.sh)

<!-- make the sh file executable -->

```bash
chmod +x create_db.sh
```

<!-- set .env variables -->

```bash
export $(cat .env | xargs)
sudo -u postgres psql
CREATE DATABASE $DB_NAME;
CREATE USER $DB_USER WITH PASSWORD $DB_PASS;
ALTER ROLE $DB_USER SET client_encoding TO 'utf8';
ALTER ROLE $DB_USER SET default_transaction_isolation TO 'read committed';
ALTER ROLE $DB_USER SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE $DB_NAME TO $DB_USER;
\q
```

# Intial Django Setup

# gunicon and nginx setups

gunicorn --bind 0.0.0.0:8000 Project.wsgi
sudo mv /setupscripts/gunicorn.socket /etc/systemd/system/gunicorn.socket
sudo mv /setupscripts/gunicorn.service /etc/systemd/system/gunicorn.service
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket
sudo systemctl status gunicorn.socket
file /run/gunicorn.sock

### NGINX

sudo mv /setupscripts/Project /etc/nginx/sites-available/Project
sudo ln -s /etc/nginx/sites-available/Project /etc/nginx/sites-enabled
sudo nano /etc/nginx/nginx.conf
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
sudo systemctl restart nginx

# Optional tasks

client_max_body_size 20M;

# supervisord setups
