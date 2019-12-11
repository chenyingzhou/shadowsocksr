ShadowsocksR
===========

本文档本地安装方式仅适用于Ubuntu/Debian，使用docker没有系统限制

### Install

```shell script
sudo apt update
sudo apt install git python
git clone https://github.com/chenyingzhou/shadowsocksr.git
cd shadowsocksr
# 安装客户端(在本地Ubuntu/Debian执行)
sudo ./install_local.sh
# 安装服务端(在境外vps上执行)
sudo ./install_server.sh
```

### Uninstall

```shell script
# 进入shadowsocksr项目目录
sudo ./uninstall.sh 
```

### 在docker中使用客户端
- 创建配置目录/path/to/config_dir，根据情况修改路径
- 创建并启动容器
```shell script
  docker run -d --name=ssr --restart=always -v /path/to/config_dir:/etc/ssr -p 1080:1081 chenyingzhou/ssr:latest
```
- 若使用ssr订阅，执行以下命令按照提示操作
```shell script
  docker exec -it ssr ssr_switch
```
- 若手动配置，修改/path/to/config_dir/config-local.json后，执行
```shell script
  docker container restart ssr
```
- 使用代理，http://127.0.0.1:1080
