import os


# sudo ufw allow 8000
# python3 manage.py migrate
# python3 manage.py collectstatic
# python3 manage.py createsuperuser
# python3 manage.py runserver

os.chdir('/home/djexp/')
os.system("sudo ufw allow 8000")
os.system("python3 manage.py migrate")
os.system("python3 manage.py collectstatic")
os.system("python3 manage.py createsuperuser")
os.system("python3 manage.py runserver")

print("Django setup complete!")