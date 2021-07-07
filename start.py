import os
import time
from core.worker import worker
from ppadb.client import Client
from cv2 import cv2
import json
import sys
from tqdm import tqdm
__author__ = "Paver(Zhen_Bo)"

os.system('cls')

root_path = os.path.dirname(os.path.abspath(__file__))


def setup():
    adb_path = "{}/adb/adb.exe".format(root_path)
    os.system("{0} start-server".format(adb_path))
    os.system("cls")
    client = Client(host="127.0.0.1", port=5037)
    devices = client.devices()
    device = select_devices(client, devices)
    return device


def get_template(version):
    templates = dict()
    templates_path = os.path.join(root_path, "templates")
    templates_path = os.path.join(templates_path, version)
    for name in os.listdir(templates_path):
        img = cv2.imread(os.path.join(templates_path, name))
        templates[name.replace('.png', '')] = img
    return templates


def select_devices(client, devices, error=0):
    for i in range(len(devices)):
        print("\033[1;32m{}: {}\033[0m".format(i, devices[i].serial))
    if error == 1:
        print("\033[1;31m{}\033[0m".format("!!!輸入設備編號過大!!!"))
    elif error == 2:
        print("\033[1;31m{}\033[0m".format("!!!編號輸入錯誤,請在試一次!!!"))
    print("輸入a以新增設備")
    try:
        inputIndex = input("請輸入編號 [1 ~ {0}]:".format(len(devices)))
        value = int(inputIndex)
        if value < 0:
            exit()
        elif value > len(devices):
            os.system('cls')
            return select_devices(client, devices, 1)
        else:
            device = devices[value]
            return device
    except (KeyboardInterrupt, SystemExit):
        raise Exception("KeyboardInterrupt")
    except:
        if inputIndex.lower() == "a":
            port = input("port號為?")
            if len(port) == 4 and port.isdigit():
                client.remote_connect("127.0.0.1", int(port))
                devices = client.devices()
                os.system('cls')
                return select_devices(client, devices)
            else:
                os.system('cls')
                return select_devices(client, devices, 2)
        else:
            os.system('cls')
            return select_devices(client, devices, 2)


def get_script():
    with open('{}/UserData/script.json'.format(root_path), newline='') as jsonfile:
        data = json.load(jsonfile)
        print("請選擇要使用的腳本")
        for i in range(len(data['script'])):
            print("{}: {}".format(i, data['script'][i]['name']))
        number = input("請輸入編號:")
        while not number.isdigit() or int(number) > len(data['script']) or int(number) < 0:
            print("輸入編號錯誤,請重新輸入")
            number = input("請輸入編號:")
        return data['script'][int(number)]


if __name__ == '__main__':
    os.system('cls')
    dev = setup()
    os.system('cls')
    script_data = get_script()
    templates = get_template(script_data["version"])
    times = input("請問要執行幾次:")
    bot = worker(root=root_path, device=dev, templates=templates, name=script_data["name"], times=times,
                 apple=script_data['apple'], count=script_data['count'], team=script_data['team'], support=script_data['support'], recover=script_data['recover'])
    total_runtime = 0
    singel_runtime = 0
    debug = False
    if debug:
        while debug:
            shell = input()
            exec("bot.{}".format(shell))
    else:
        while True:
            tstart = time.time()
            width = len(script_data['battle'])
            bar_format = "{{desc:}}{{percentage:3.0f}}%|{{bar:{}}}|".format(
                width)
            progress = tqdm(script_data['battle'], desc="關卡進度",
                            bar_format=bar_format, file=sys.stdout)
            for instruct in progress:
                if instruct == "start_battle()":
                    instruct = "start_battle({},{})".format(
                        round(total_runtime, 1), round(singel_runtime, 1))
                print("\r", end='')
                exec("bot.{}".format(instruct))
                time.sleep(1)
            tend = time.time()
            singel_runtime = int(tend)-int(tstart)
            total_runtime += singel_runtime
