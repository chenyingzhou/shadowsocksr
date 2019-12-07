#!/bin/bash

mkdir -p /usr/local/ssr
mkdir -p /etc/ssr
cp -r ./* /usr/local/ssr/
cp ./conf/config-local.json /etc/ssr/
cp ./init/ssrlocal /etc/init.d/
cp ./ssr_switch.py /usr/local/bin/ssr_switch

systemctl daemon-reload
update-rc.d ssrserver remove
update-rc.d ssrlocal defaults

echo 'Now edit your config in /etc/ssr/config-local.json'
echo 'And then run'
echo '    service ssrlocal start'
echo 'to start ssr server'