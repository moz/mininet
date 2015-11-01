#!/bin/sh

apt-get update -y
apt-get upgrade -y

apt-get install git -y
apt-get install unzip -y
apt-get install build-essential -y

#for ntopng
apt-get install libglib2.0 libxml2-dev libpcap-dev libtool rrdtool librrd-dev autoconf automake autogen redis-server wget libsqlite3-dev libhiredis-dev libgeoip-dev libcurl4-openssl-dev libpango1.0-dev libcairo2-dev libpng12-dev libmysqlclient-dev -y

