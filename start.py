import os
import time
from core.worker import worker, box
from ppadb.client import Client
from cv2 import cv2
import json
import sys
from tqdm import tqdm
import argparse
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


def get_template(version, folder=None):
    templates = dict()
    templates_path = os.path.join(root_path, "templates")
    templates_path = os.path.join(templates_path, version)
    if folder is not None:
        templates_path = os.path.join(templates_path, folder)
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", type=bool, default=False)
    parser.add_argument("--boxmode", type=bool, default=True)
    parser.add_argument("--version", type=str, default="JP")
    args = parser.parse_args()
    debug = args.debug
    boxmode = args.boxmode
    version = args.version
    os.system('cls')
    dev = setup()
    os.system('cls')
    if boxmode == False:
        script_data = get_script()
        templates = get_template(script_data["version"])
        times = input("請問要執行幾次:")
        width = len(script_data['battle'])+2
        bar_format = "{{desc:}}{{percentage:3.0f}}%|{{bar:{}}}|".format(
            width)
        progress = tqdm(range(width), desc="腳本進度",
                        bar_format=bar_format, file=sys.stdout)
        bot = worker(root=root_path, device=dev, templates=templates, name=script_data["name"], times=times,
                     apple=script_data['apple'], count=script_data['count'], team=script_data['team'],
                     support=script_data['support'], recover=script_data['recover'], progress_bar=progress)
        print("\r\x1b[2K", end='')
        total_runtime = 0
        singel_runtime = 0
        if debug:
            while debug:
                shell = input("\r\x1b[2K指令: ")
                exec("bot.{}".format(shell))
        else:
            while True:
                tstart = time.time()
                bot.pbar.reset()
                for instruct in script_data["battle"]:
                    if instruct == "start_battle()":
                        instruct = "start_battle({},{})".format(
                            round(total_runtime, 1), round(singel_runtime, 1))
                    exec("bot.{}".format(instruct))
                    time.sleep(1)
                # for instruct in progress:
                #     if instruct == "start_battle()":
                #         instruct = "start_battle({},{})".format(
                #             round(total_runtime, 1), round(singel_runtime, 1))
                #     print("\r", end='')
                #     exec("bot.{}".format(instruct))
                #     time.sleep(1)
                tend = time.time()
                singel_runtime = int(tend)-int(tstart)
                total_runtime += singel_runtime
    else:
        game = {"0": "JP", "1": "TW"}
        print("\033[31m Scrpit made by\033[0m\033[41;37mPaver\033[0m,github:\033[37;34mhttps://github.com/Zhen-Bo\033[0m")
        print(
            "\033[31m此腳本作者為\033[0m\033[41;37mPaver\033[0m,github頁面:\033[37;34mhttps://github.com/Zhen-Bo\033[0m")
        print("\033[31m請勿使用於商業用途,此程式包含MIT授權\033[0m")
        while True:
            print("請問遊戲版本?")
            print("輸入0 = 日版")
            print("輸入1 = 台版")
            version = input("請輸入版本(0/1): ")
            if version in ["0", "1"]:
                break
        bot = box(device=dev, templates=get_template(
            "{}".format(game[version]), folder="box"))

        while True:
            os.system('cls')
            print(
                "\033[31m Scrpit made by\033[0m\033[41;37mPaver\033[0m,github:\033[37;34mhttps://github.com/Zhen-Bo\033[0m")
            print(
                "\033[31m此腳本作者為\033[0m\033[41;37mPaver\033[0m,github頁面:\033[37;34mhttps://github.com/Zhen-Bo\033[0m")
            print("\033[31m請勿使用於商業用途,此程式包含MIT授權\033[0m")
            i = 0
            times = int(input("請問要抽幾箱: "))
            while i <= times:
                i += 1
                if i > times:
                    break
                elif i > 1:
                    bot.tap(bot.result[1])
                    bot.standby("execute")
                    bot.standby("close")
                print("目前在抽第 {} 箱".format(i))
                status = bot.box_gacha()
                if status == True:
                    break
            os.system('PAUSE')
