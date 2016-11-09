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

Request(username, [password, string, url])

username: username for your mysql server.
password(optional but recommanded): password for your mysql server.
string(optional): string for url retrieval.
url(optional): url string to be shortened.

Attributes:
Request.result: The result of your request.
