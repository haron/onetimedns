# Installation

## Prerequisites

To deploy project, you should have `Fabric` installed on your workstation:

    pip install fabric

Your server should run Ubuntu (tested with 16.04). All remote commands should be run as `root` or prepended with `sudo`.

## Install dependencies

Run on your server:

    apt-get -y install ufw python python-pip python-redis python-flask ruby ruby-dev moreutils supervisor nginx
    gem install redis rubydns
    pip install -U certbot-nginx

## Deploy

Run on your workstation from project directory:

    fab

## Configure firewall

Add to beginning of `/etc/ufw/before.rules`:

    *nat
    :PREROUTING ACCEPT [0:0]
    :dns-redirect - [0:0]
    -A PREROUTING -j dns-redirect
    -A dns-redirect -i eth0 -p udp -m udp --dport 53 -m comment --comment dns-redirect -j REDIRECT --to-ports 5353
    COMMIT

    cp /var/www/onetimedns/ufw-onetimedns /etc/ufw/applications.d/onetimedns
    ufw allow onetimedns

## Configure web application

Create secret file:

    echo "local_secret = '$(head -c 50 /dev/urandom | base64)" > /var/www/onetimedns/secret.py

Edit `settings.py` and change `ZONE_NAME` and `SERVER_NAME` variables.

Install Nginx config `nginx-onetimedns.net` and configure SSL:

    cp /var/www/onetimedns/nginx-onetimedns.net /etc/nginx/sites-enabled/onetimedns.net

Edit Nginx config accordingly - change your domain name, add logging, etc, then reload Nginx.

Configure SSL:

    letsencrypt --nginx

## Configure DNS daemon

Edit `dns.rb` file and change server IP and domain name according to comments.

## Finally

Restart project daemons and check the log files in `/var/log/supervisor`:

    supervisor restart onetimedns:*
