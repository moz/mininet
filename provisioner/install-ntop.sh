#!/bin/sh

apt-get install build-essential git libglib2.0 libxml2-dev libpcap-dev libtool rrdtool librrd-dev autoconf automake autogen redis-server wget libsqlite3-dev libhiredis-dev libgeoip-dev libcurl4-openssl-dev libpango1.0-dev libcairo2-dev libpng12-dev libmysqlclient-dev

cd /home/vagrant

git clone https://github.com/ntop/nDPI.git
cd nDPI
./configure -with-pic
make

cd /home/vagrant

git clone https://github.com/ntop/ntopng.git
cd ntopng
./autogen.sh
./configure
make
make install

