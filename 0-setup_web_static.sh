#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static.

# update & install Nginx if it not already installed.
sudo apt-get -y update
sudo apt-get -y install nginx

# Create the folder /data/ if it doesn’t already exist.
sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

# Create a fake HTML file /data/web_static/releases/test/index.html.
echo "Holberton School" | sudo tee /data/web_static/releases/test/index.html > /dev/null

# Create a symbolic link.
sudo ln -sf /data/web_static/releases/test/ /data/web_static/current
sudo chown -R ubuntu:ubuntu /data/

# Update the Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
config="/etc/nginx/sites-available/default"
    sudo sed -i '/server_name localhost;/a\
\
    location /hbnb_static/ {\
        alias /data/web_static/current/;\
    }' "$config"

# Restart nginx.
sudo service nginx restart
