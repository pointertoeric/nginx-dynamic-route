#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install build-essential
sudo apt-get install git
git clone git@github.com:nginx/nginx.git
cd nginx
./auto/configure --with-http_auth_request_module
make
sudo make install
nginx -c /nginx.conf
