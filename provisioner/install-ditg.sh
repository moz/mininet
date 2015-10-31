#!/bin/sh

cd /home/vagrant
wget -c http://traffic.comics.unina.it/software/ITG/codice/D-ITG-2.8.1-r1023-src.zip
unzip D-ITG-2.8.1-r1023-src.zip
cd D-ITG-2.8.1-r1023/src
make

#sudo make install PREFIX=/home/vagrant/d-itg

