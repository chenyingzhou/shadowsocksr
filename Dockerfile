FROM ubuntu:16.04

# 安装ssr
RUN apt-get update \
    && apt-get install -y wget python \
    && wget -c -O shadowsocksr.tar.gz https://github.com/chenyingzhou/shadowsocksr/archive/3.2.3.tar.gz \
    && tar -zxf shadowsocksr.tar.gz \
    && cd shadowsocksr-3.2.3 \
    && ./install_local.sh \
    && cd ../ \
    && rm -rf shadowsocksr* \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# 安装privoxy，用于socks5转http
RUN apt-get update \
    && apt-get install -y privoxy \
    && sed -i 's/^listen-address/# listen-address/' /etc/privoxy/config \
    && echo 'listen-address 0.0.0.0:1081' >> /etc/privoxy/config \
    && echo 'forward-socks5t / 0.0.0.0:1080 .' >> /etc/privoxy/config \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# 编写启动脚本
RUN { \
        echo '#!/bin/sh'; \
        echo 'if [ ! -f "/etc/ssr/config-local.json" ]; then'; \
        echo '  cp /usr/local/ssr/conf/config-local.json /etc/ssr/config-local.json'; \
        echo 'fi'; \
        echo 'service ssrlocal start'; \
        echo 'service privoxy start'; \
        echo 'tail -f /dev/null'; \
    } | tee /start.sh \
    && chmod 755 /start.sh

EXPOSE 1081

VOLUME ["/etc/ssr"]

ENTRYPOINT ["/start.sh"]
