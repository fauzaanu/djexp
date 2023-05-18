import os


# gunicorn --bind 0.0.0.0:8000 Project.wsgi
# sudo mv /setupscripts/gunicorn.socket /etc/systemd/system/gunicorn.socket
# sudo mv /setupscripts/gunicorn.service /etc/systemd/system/gunicorn.service
# sudo systemctl start gunicorn.socket
# sudo systemctl enable gunicorn.socket
# sudo systemctl status gunicorn.socket
# file /run/gunicorn.sock

os.chdir('/home/djexp/')
os.system("gunicorn --bind 0.0.0.0:8000 Project.wsgi")
os.system("sudo mv /setupscripts/gunicorn.socket /etc/systemd/system/gunicorn.socket")
os.system("sudo mv /setupscripts/gunicorn.service /etc/systemd/system/gunicorn.service")
os.system("sudo systemctl start gunicorn.socket")
os.system("sudo systemctl enable gunicorn.socket")
os.system("sudo systemctl status gunicorn.socket")
os.system("file /run/gunicorn.sock")

print("Gunicorn setup complete!")