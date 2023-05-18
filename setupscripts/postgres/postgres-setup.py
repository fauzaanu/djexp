import os

os.system("sudo chmod +x create-db.sh")

# find the .env file from the parent directory
# and copy it to the current directory

os.system("sudo cp ../../.env .")
os.system("sudo ./create-db.sh")

print("Postgres setup complete!")