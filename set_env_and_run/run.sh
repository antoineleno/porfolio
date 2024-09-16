#!/bin/bash

# Check if the username argument is provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <username>"
    exit 1
fi

# Set up a new virtual environment
python3 -m venv ../myenv

# Activate the virtual environment
source ../myenv/bin/activate

# Upgrade pip, setuptools, and wheel
pip install --upgrade pip setuptools wheel

# Upgrade dependencies to ensure compatibility with the current Python version
pip install --upgrade blinker certifi charset-normalizer click colorama Flask

# Optionally, you can regenerate requirements.txt with the updated dependencies
pip freeze > requirements.txt

# Install all dependencies listed in requirements.txt
pip install flask_login
pip install sqlalchemy
pip install mysqlclient
pip install pycountry
pip install flask_wtf
pip install flask_cors
pip install Pillow
pip install -r requirements.txt




# Assign command-line arguments to variables
USER=$1
read -sp "Enter MySQL password: " PASSWORD
echo

# Name of the SQL file
SQL_FILE="set_up_mysql.sql"

# Run the MySQL command with the provided user, password, and fixed SQL file
mysql -u "$USER" -p"$PASSWORD" < "$SQL_FILE"

# Create preliminery objects in the database like hostels
cat objects | CAMPUS_MYSQL_USER=campus_dev CAMPUS_MYSQL_PWD=campus_dev_pwd CAMPUS_MYSQL_HOST=localhost CAMPUS_MYSQL_DB=campus_dev_db CAMPUS_TYPE_STORAGE=db ../myenv/bin/python  ../console.py


# Activate venv in the web_flask dir, install dependencies and run the app.
python3 -m venv ../web_flask/myenv
source ../web_flask/myenv/bin/activate
pip install flask_login
pip install sqlalchemy
pip install mysqlclient
pip install pycountry
pip install flask_cors
pip install flask_wtf
pip install Pillow
pip install -r requirements.txt
CAMPUS_MYSQL_USER=campus_dev \
CAMPUS_MYSQL_PWD=campus_dev_pwd \
CAMPUS_MYSQL_HOST=localhost \
CAMPUS_MYSQL_DB=campus_dev_db \
CAMPUS_TYPE_STORAGE=db \
python ../web_flask/app.py
