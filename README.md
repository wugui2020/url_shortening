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
pip install flask-restful
```

### sqlserver
See: https://help.ubuntu.com/12.04/serverguide/mysql.html
```
sudo apt-get install mysql-server
```

## Usage

Database Username and password should be stored in 'credentials.conf' in the PATH.
The first line of the conf should be the username and the second line should be the password. If there is no password, you need to leave an empty line.

Then run api.py

```
python api.py
```

GET    YOUR_URL/SHORT_URL
will redirect to the original url if short url is valid.

POST   YOUR_URL/[SHORT_URL]&data=[THE_URL_TO_BE_SHORTENED] 
will return a json object with orginal url under 'data' and short url under 'short_url'.

Note that the url to be shortened should have the prefix of 'http://' or 'https://'. Otherwise the api will add the 'http://' to the url automatically.

Examples:
With api.py running:

```
$curl http://localhost:5000/
"Please specify a valid short_url"

$ curl http://localhost:5000/ -d "data=http://www.google.com" -X POST
{
    "data": "http://http://www.google.com", 
    "short_url": "http://localhost:5000/UV20h"
}

$ curl http://localhost:5000/UV20h
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>Redirecting...</title>
<h1>Redirecting...</h1>
<p>You should be redirected automatically to target URL: <a href="http://http://www.google.com">http://http://www.google.com</a>.  If not click the link.
```


