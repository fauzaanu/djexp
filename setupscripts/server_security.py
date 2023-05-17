import os

new_user = input("Enter a new username: ")
os.system("sudo adduser {}".format(new_user))
os.system("sudo usermod -aG sudo {}".format(new_user))
print(f"User {new_user} created and given root permissions successfully!")

os.system("sudo ufw allow OpenSSH")
os.system("sudo ufw enable")
os.system("sudo ufw status")
print(f"Firewall enabled successfully!")


public_key_from_local_machine = input("Please run 'ssh-keygen' on your local machine and copy paste the contents of the .pub file in here. Press enter to continue...")

with open("{}.pub".format(new_user), "w") as file:
    file.write(public_key_from_local_machine)
    
os.system("sudo mkdir /home/{}/.ssh".format(new_user))
os.system("sudo mv {}.pub /home/{}/.ssh/authorized_keys".format(new_user, new_user))
os.system("sudo chown -R {}:{} /home/{}/.ssh".format(new_user, new_user, new_user))
os.system("sudo chmod 700 /home/{}/.ssh".format(new_user))
os.system("sudo chmod 600 /home/{}/.ssh/authorized_keys".format(new_user))
with open("/etc/ssh/sshd_config", "r") as file:
    lines = file.readlines()

with open("/etc/ssh/sshd_config", "w") as file:
    for line in lines:
        if "PasswordAuthentication" in line:
            file.write("PasswordAuthentication no\n")
        elif "PermitRootLogin" in line:
            file.write("PermitRootLogin no\n")
        else:
            file.write(line)

os.system("sudo systemctl restart ssh")

print(f"SSH key authentication enabled successfully!")
print("Please try logging in with your new user now. If you are able to login, you can disable root login by running 'sudo passwd -l root'")
