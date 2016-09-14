#!/usr/bin/env bash

# Initial system setup. Meant to be run as privileged user.
apt-get update
apt-get upgrade

# System packages
apt-get install -y build-essential
apt-get install -y libssl-dev libffi-dev
apt-get install -y git gettext

# MySQL
debconf-set-selections <<< 'mysql-server mysql-server/root_password password 123456'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 123456'
apt-get install -y libmysqlclient-dev
apt-get install -y mysql-server mysql-client

# Python
apt-get install -y python-software-properties python
apt-get install -y python-pip python-virtualenv
apt-get install -y python-dev
