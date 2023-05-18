import os

os.system("sudo mv gunicorn.conf /etc/supervisor/conf.d/gunicorn.conf")
os.system("sudo mv nginx.conf /etc/supervisor/conf.d/nginx.conf")
os.system("sudo supervisorctl reread")
os.system("sudo supervisorctl start all")
os.system("sudo supervisorctl status")

print("Supervisor setup complete!")
