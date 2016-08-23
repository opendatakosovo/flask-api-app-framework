# Kreotive

### Inslallation
#### Environment
- Ubuntu 16.04 LTS 64 bit
- MongoDB 3.2.x
- Apache Virtual Hosts (httpd)

#### Initial Setup
Apache Virtual Host:
```
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install libapache2-mod-wsgi
```

Checkout project:
```
cd /var/www
git clone https://github.com/Gaddea/kreotive.git
```

Create project .wsgi
```
cd /var/www/kreotive
sudo cp app-template.wsgi app.wsgi
```

Open the new file in your editor with root privileges:
```
sudo nano app.wsgi
```

And configure the project's path:
```
app_dir_path = '/var/www/kreotive'
```

Create and edit project config file:
```
sudo config-template.cfg config.cfg
sudo nano config.cfg
```

Install the app
```
bash install.sh
```

#### Create New Virtual Host
**IMPORTANT:** In production we are deploying this app under opendatakosovo.org domain so we are just adding a new virtual host to the *opendatakosovo.org.conf* file. The following instructions do not apply in our case but we still include them for documentation purposes on how to set this up from scratch:

Copy default virtual host config file to create new file specific to the project:
```
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/kreotive.com.conf
```

Open the new file in your editor with root privileges:
```
sudo nano /etc/apache2/sites-available/kreotive.com.conf
```

And configure it to point to the project's app.wsgi file:
```
<VirtualHost *:80>
  ServerAdmin admin@localhost
  #ServerName kreotive.com
  
  WSGIScriptAlias / /var/www/kreotive/app.wsgi
  <Directory /var/www/kreotive>
    Order allow,deny
    Allow from all
  </Directory>
    
  ErrorLog ${APACHE_LOG_DIR}/error.log
  CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>
```

#### Enable New Virtual Host
First disable the defaul one:
```
sudo a2dissite 000-default.conf
```

Then enable the new one we just created:
```
sudo a2ensite kreotive.com.conf
```

Restart the server for these changes to take effect:
```
sudo service apache2 restart
```
