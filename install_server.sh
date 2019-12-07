#!/bin/bash

mkdir -p /usr/local/ssr
mkdir -p /etc/ssr
cp -r ./* /usr/local/ssr/
cp ./conf/config-server.json /etc/ssr/
cp ./init/ssrserver /etc/init.d/

systemctl daemon-reload
update-rc.d ssrlocal remove
update-rc.d ssrserver defaults

echo 'Now edit your config in /etc/ssr/config-server.json'
echo 'And then run'
echo '    service ssrserver start'
echo 'to start ssr server'