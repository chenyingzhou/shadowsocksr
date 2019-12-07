#!/usr/bin/env python
# coding=utf-8
import base64
import json
import os
import sys
import getpass
import urllib
from string import strip


def base64_decode(string):
    string = string.replace("_", "/")
    string = string.replace("-", "+")
    while 0 != len(string) % 4:
        string += "="
    return base64.b64decode(string)


def get_ssr_url_file_name():
    return "/etc/ssr/_url.txt"


def get_ssr_raw_data_file():
    return "/etc/ssr/_temp.txt"


def get_ssr_config_file():
    return "/etc/ssr/config-local.json"


def gen_url():
    fo = open(get_ssr_url_file_name(), "a+")
    current_url = strip(fo.read())
    fo.close()

    if "" == current_url:
        new_url = strip(raw_input("请输入订阅地址："))
    else:
        print "当前订阅地址为：", current_url
        new_url = strip(raw_input("更新为(直接回车跳过)："))
        if "" == new_url:
            new_url = current_url

    fo = open(get_ssr_url_file_name(), "w")
    fo.write(new_url)
    fo.close()
    return new_url


def craw_list(url):
    fo = open(get_ssr_raw_data_file(), "a+")
    config_temp = strip(fo.read())
    fo.close()

    need_update = True
    if "" != config_temp:
        ans = strip(raw_input("是否更新订阅(y/N)："))
        if "Y" != ans and "y" != ans:
            need_update = False
    if need_update:
        raw_response = urllib.urlopen(url).read()
    else:
        raw_response = config_temp

    fo = open(get_ssr_raw_data_file(), "w")
    fo.write(raw_response)
    fo.close()

    raw_data = base64_decode(raw_response)
    return raw_data.split()


def trans_config(raw):
    config = {
        "server": "",
        "server_ipv6": "::",
        "server_port": 1080,
        "local_address": "127.0.0.1",
        "local_port": 1080,
        "password": "",
        "timeout": 120,
        "method": "",
        "protocol": "",
        "protocol_param": "",
        "obfs": "",
        "obfs_param": "",
        "redirect": "",
        "dns_ipv6": False,
        "fast_open": True,
        "workers": 1
    }
    raw = raw[6:]
    raw_decode = base64_decode(raw)

    [base_param_str, other_param_str] = raw_decode.split("?")
    base_params = base_param_str.split(":")
    [config["server"], config["server_port"], config["protocol"], config["method"], config["obfs"], config["password"]] = base_params
    config["password"] = base64_decode(config["password"])
    config["password"] = config["password"][:-1]

    other_params = other_param_str.split("&")
    for other_param in other_params:
        [key, value] = other_param.split("=")
        if "obfsparam" == key:
            key = "obfs_param"
        if "protoparam" == key:
            key = "protocol_param"
        config[key] = base64_decode(value)

    return config


def select_config(config_list):
    step = 10
    ptr = 0
    target_config = {}
    while True:
        if ptr >= len(config_list):
            ptr = 0
        range_min = ptr
        range_max = min(ptr + step, len(config_list) - 1)
        os.system("clear")
        print "节点列表："
        for index, config in enumerate(config_list[range_min:range_max]):
            print " ", index + ptr, config["remarks"]
        choice = strip(raw_input("请选择(" + str(range_min) + "-" + str(range_max - 1) + ")(q退出，回车翻页)："))
        if "q" == choice or "Q" == choice:
            return
        if "" == choice:
            ptr += step
            continue
        if choice.isdigit() and range_min <= int(choice) < range_max:
            target_config = config_list[int(choice)]
            break
    json.dump(target_config, open(get_ssr_config_file(), "w"))
    os.system("service ssrlocal restart")


if __name__ == "__main__":
    user = getpass.getuser()
    if "root" != user:
        print "请以root权限运行"
        sys.exit()

    config_list = []
    ssr_url = gen_url()
    raw_config_list = craw_list(ssr_url)
    for raw_config in raw_config_list:
        config_list.append(trans_config(raw_config))
    select_config(config_list)

