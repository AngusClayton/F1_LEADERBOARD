# How to launch an apache2 wsgi app

based off [digital ocean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps)

### Prerequisites:

apache2

pip3 

venv: `sudo apt-get install virtualenv`

```
sudo apt-get install libapache2-mod-wsgi python-dev
```

**run this command for python3**

```
sudo apt-get install libapache2-mod-wsgi-py3
```

# Steps:

## One: enable mod_wsgi

```
sudo a2enmod wsgi 
```

## Two: create flask app

replace **FlaskApp** with the name of the application

*make base directory*

```
cd /var/www 
```

```
sudo mkdir FlaskApp/FlaskApp
```

```
cd FlaskApp/FlaskApp
```

*make templates and static folder used by flask*

```
sudo mkdir static templates
```

make a python file called `__init__.py`or rename existing main flask app file to that.

put all the main app logic in there.

## Step Three – Install Flask

*this is installed in a venv to keep everything separate to the system.*

**make new virtual environment. can call it something other than venv**

```
sudo virtualenv venv
```

```
sudo pip3 install Flask 
```

**test the flask script:**

```
sudo python3 __init__.py 
```

**exit the virtual environment

```
deactivate
```

## Step Four – Configure and Enable a New Virtual Host

*remember you can rename the **FlaskApp** bit of the filename.*

```
sudo nano /etc/apache2/sites-available/FlaskApp.conf
```

insert this: replacing the server name with the ip/domain. **and replacing all instances of FlaskApp with the name of your app**

You can also change the directory of the app, by changing the / on line 4 after wsgiscriptAlias to a directory name.

e.g.**

`WSGIScriptAlias /leaderboard /var/www/leaderboardApp/leaderboardApp.wsgi` App will be present by going to domain/leader board. instead of domain

```
<VirtualHost *:80>
		ServerName mywebsite.com
		ServerAdmin admin@mywebsite.com
		WSGIScriptAlias / /var/www/FlaskApp/flaskapp.wsgi
		<Directory /var/www/FlaskApp/FlaskApp/>
			Order allow,deny
			Allow from all
		</Directory>
		Alias /static /var/www/FlaskApp/FlaskApp/static
		<Directory /var/www/FlaskApp/FlaskApp/static/>
			Order allow,deny
			Allow from all
		</Directory>
		ErrorLog ${APACHE_LOG_DIR}/error.log
		LogLevel warn
		CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

## Step Five – Create the .wsgi File

The file apache uses 

**cd into the <u>FIRST FlaskApp directory!</u>**

```
cd /var/www/FlaskApp
sudo nano flaskapp.wsgi 
```

Add the following lines of code to the flaskapp.wsgi file:

```
#!/usr/bin/python
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/FlaskApp/")

from FlaskApp import app as application
application.secret_key = 'Add your secret key'
```

**can ignore the secret key part.**

Now your directory structure should look like this:

```
|--------FlaskApp
|----------------FlaskApp
|-----------------------static
|-----------------------templates
|-----------------------venv
|-----------------------__init__.py
|----------------flaskapp.wsgi
```

## Step Six – Restart Apache

```
sudo service apache2 restart 
```

## Points to note:

If you import a library, must be in the python library folders (check this tho.)

If you use a file, list the entire directory.