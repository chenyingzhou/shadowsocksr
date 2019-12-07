#!/bin/bash

rm -rf /usr/local/ssr > /dev/null 2>&1
rm -rf /etc/ssr > /dev/null 2>&1

update-rc.d ssrserver remove
update-rc.d ssrlocal remove
rm /etc/init.d/ssrlocal > /dev/null 2>&1
rm /etc/init.d/ssrserver > /dev/null 2>&1
rm /usr/local/bin/ssr_switch > /dev/null 2>&1

systemctl daemon-reload

echo 'done'