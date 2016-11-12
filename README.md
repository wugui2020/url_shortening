# url_shortening

## Intro
This is a basic url shortening app written in Python. The app takes urls of any length and gives a short url as the output.

## Requirements
You need mysqldb package and sqlserver installed on your system.

### mysqldb
Prerequisites:

For Ubuntu, Debian:
```
sudo apt-get install python-pip libmysqlclient-dev python-dev 
```
After that:
```
sudo apt-get install python-pip python-dev build-essential 
pip install MySQL-python
```

### sqlserver
See: https://help.ubuntu.com/12.04/serverguide/mysql.html
```
sudo apt-get install mysql-server
```

## Usage

Database Username and password should be stored in 'credentials.conf' in the PATH.
The first line of the conf should be the username and the second line should be the password. If there is no password, you need to leave an empty line.

GET    YOUR_URL/SHORT_URL

POST   YOUR_URL/[SHORT_URL]&data=[THE_URL_TO_BE_SHORTENED]

Note that the url to be shortened should have the prefix of 'http://' or 'https://'.
