# pylint: disable=unused-variable
from cv2 import cv2
import numpy as np
import os
import time
import random
import sys
from tqdm import tqdm
import json
from core.match_func import sift
from core.match_func import match_template as match
import threading


class base_unit():
    def __init__(self, device, templates):
        self.device = device
        self.templates = templates
        self.screenshot = None
        self.screen_muti = int(self.get_screen(detect=True))

    def get_screen(self, mode=0, detect=False):
        image = cv2.imdecode(np.fromstring(
            bytes(self.device.screencap()), np.uint8), cv2.IMREAD_COLOR)
        if detect:
            return image.shape[0]/540
        else:
            if self.screen_muti != 1:
                self.screenshot = cv2.resize(image, (960, 540))
            else:
                self.screenshot = image
        if mode == 1:
            self.screenshot = cv2.cvtColor(self.screenshot, cv2.COLOR_BGR2GRAY)

    def compare(self, imgs, screenshot=None, crop=None, mode=0, debug=False):
        if screenshot is None:
            if mode == 1:
                self.get_screen(mode=1)
            else:
                self.get_screen()
        if crop is not None:
            self.screenshot = self.screenshot[int(crop['y']):int(crop['y'])+int(crop['height']),
                                              int(crop['x']):int(crop['x'])+int(crop['width'])]
        if isinstance(imgs, dict):
            if mode == 1:
                for name in imgs:
                    pos = sift(imgs[name], self.screenshot, debug=debug)
                    if isinstance(pos, list):
                        return [name, np.int32(pos)]
            else:
                for name in imgs:
                    pos = match(imgs[name], self.screenshot, debug=debug)
                    if isinstance(pos, list):
                        return [name, np.int32(pos)]
        else:
            if mode == 1:
                pos = sift(imgs, self.screenshot, debug=debug)
                if isinstance(pos, list):
                    pos = np.int32(pos)
                    return ["", [pos[0], pos[1]]]
            else:
                pos = match(imgs, self.screenshot, debug=debug)
                if isinstance(pos, list):
                    pos = np.int32(pos)
                    return ["", [pos[0], pos[1]]]
        return False

    def standby(self, img, coordinate=None, mode=0, tap=True, disapper=False, debug=False):
        flag = False
        if isinstance(img, list):
            template = dict()
            for name in img:
                template[name] = self.templates[name]
        else:
            template = self.templates[img]
        if not disapper:
            while True:
                flag = self.compare(template, mode=mode, debug=debug)
                if not isinstance(flag, bool):
                    break
                if coordinate is not None:
                    self.tap([coordinate[0], coordinate[1]])
            if tap:
                self.tap(flag[1])
            else:
                return flag
        else:
            while True:
                flag = self.compare(template, mode=mode, debug=debug)
                if isinstance(flag, bool):
                    break
                if coordinate is not None:
                    self.tap([coordinate[0], coordinate[1]])

    def tap(self, pos):
        pos = np.multiply(self.screen_muti, pos)
        self.device.shell("input tap {} {}".format(pos[0], pos[1]))

    def swipe(self, pos1, pos2, delay=1000):
        pos1 = np.multiply(self.screen_muti, pos1)
        pos2 = np.multiply(self.screen_muti, pos2)
        self.device.shell(
            "input swipe {} {} {} {} {}".format(pos1[0], pos1[1], pos2[0], pos2[1], delay))


class worker(base_unit):
    def __init__(self, root, device, templates, name, times: int, apple: str, count: int, team: int, support, recover: int, progress_bar):
        self.root = root
        super().__init__(device, templates)
        self.name = name
        self.max_times = int(times)
        self.runtimes = 0
        self.apple = apple
        if apple != '':
            self.maxapple = int(count)
            self.count = int(count)
        else:
            self.maxapple = 0
            self.count = 0
        self.use = 0
        self.team = team
        self.recover = recover
        self.friend = self.get_friend(support)
        self.button = self.get_button()
        self.pbar = progress_bar

    def get_button(self):
        with open('{}/UserData/button.json'.format(self.root), newline='') as jsonfile:
            return json.load(jsonfile)

    def timecal(self, time):
        if time > 60:
            return "{} ??????".format(round(time/60, 1))
        else:
            return "{} ??????".format(round(time, 1))

    def enter_stage(self, total, singel, quit=False):
        os.system("cls")
        result = self.standby(["continue", "menu"], tap=False)
        if self.apple == "quartz":
            applestr = "?????????"
        elif self.apple == "goldden":
            applestr = "?????????"
        elif self.apple == "silver":
            applestr = "?????????"
        elif self.apple == "copper":
            applestr = "?????????"
        elif self.apple == "":
            applestr = "????????????"
        print("??????????????????:{}".format(self.name))
        with tqdm(total=self.max_times, desc="????????????", bar_format="{{desc:}}{{percentage:3.0f}}%|{{bar:20}}|??????: {}/ {}".format(self.runtimes-1, self.max_times)) as rbar:
            rbar.update(self.runtimes-1)
        print("????????????: {} /??????: {} /?????????: {} /??????: {}".format(
            applestr, self.maxapple, self.use, self.count))
        print("??????????????????: {} /?????????????????????: {}".format(
            self.timecal(total), self.timecal(singel)))
        if quit:
            if result[0] == "continue":
                self.standby("close")
            print("====================================================")
            print("[EXIT]??????????????????!!")
            exit()
        else:
            print("===============================================")
            print("[INFO]??????????????? {} ???".format(self.runtimes))
            self.pbar.display()
            if result[0] == "menu":
                state = result[0]
                self.tap((750, 160))
            else:
                state = result[0]
                self.tap(result[1])
            print("\r\x1b[2K", end='')
            print("[INFO]??????????????????")
            self.pbar.reset()
            result = self.standby(["noap", "select_friend"], tap=False)
            if result[0] == "noap":
                print("\r\x1b[2K", end='')
                print("[Waring]????????????")
                self.pbar.display()
                if self.count > 0:
                    self.tap(self.button["apple"][self.apple])
                    self.standby("confirm")
                    self.count -= 1
                    self.use += 1
                    print("\r\x1b[2K", end='')
                    if self.apple == "quartz":
                        print("[INFO]?????????????????????!")
                    elif self.apple == "goldden":
                        print("[INFO]?????????????????????!")
                    elif self.apple == "silver":
                        print("[INFO]?????????????????????!")
                    elif self.apple == "copper":
                        print("[INFO]?????????????????????!")
                else:
                    self.tap((470, 470))
                    print("\r\x1b[2K", end='')
                    print("[INFO]???????????????...")
                    start_time = time.time()
                    end_time = time.time()
                    while not int(end_time-start_time) >= int(self.recover)*60:
                        remain = round(
                            int(self.recover) - float(int(end_time-start_time)/60), 1)
                        if remain >= 60:
                            print("\x1b[1A\r\x1b[2K", end='')
                            print("[INFO]???????????????...,?????? {} ??????".format(remain))
                        else:
                            print("\x1b[1A\r\x1b[2K", end='')
                            print("[INFO]???????????????...,?????? {} ??????".format(remain))
                        for i in range(30):
                            end_time = time.time()
                            if int(end_time-start_time) >= int(self.recover)*60:
                                break
                            time.sleep(1)
                    state = self.enter_stage(total, singel)
            self.pbar.update(1)
            return state

    def skill(self, position: int, skill: int, target=None):
        self.standby("attack", tap=False, coordinate=(670, 25))
        self.tap(self.button["servert{}".format(position)]
                 ["skill{}".format(skill)])
        print("\r\x1b[2K", end='')
        print("[BATTLE]???????????? {} ?????? {} ".format(
            position, skill), end='')
        if target is not None:
            print("??????????????? {}".format(target))
            self.standby("select", tap=False)
            self.tap(self.button["servert{}".format(target)]["locate"])
        else:
            print("")
        self.pbar.update(1)

    def attack(self, first=None, second=None, third=None):
        self.standby("attack", coordinate=(670, 25))
        print("\r\x1b[2K", end='')
        print("[BATTLE]?????????????????????")
        self.pbar.display()
        time.sleep(2)
        select = [first, second, third]
        card = ""
        for i in range(len(select)):
            if select[i] is None:
                rnd = random.randrange(1, 6)
                while rnd in select:
                    rnd = random.randrange(1, 6)
                select[i] = rnd
                card += "????????? {}/".format(rnd)
                self.tap(self.button["card"]["{}".format(rnd)])
            else:
                if select[i] > 5:
                    card += "?????? {}/".format(int(select[i])-5)
                else:
                    card += "????????? {}/".format(select[i])
                self.tap(self.button["card"]["{}".format(select[i])])
        print("\r\x1b[2K", end='')
        print("[BATTLE]?????? {}".format(card))
        self.pbar.update(1)

    def master(self, skill, target=None):
        self.standby("attack", tap=False, coordinate=(670, 25))
        print("\r\x1b[2K", end='')
        print("[MASTER]????????????????????????")
        self.pbar.display()
        self.tap(self.button["master"]["locate"])
        time.sleep(1)
        print("\r\x1b[2K", end='')
        print("[MASTER]?????????????????? {}".format(skill), end='')
        self.tap(self.button["master"]["skill{}".format(skill)])
        if target is not None:
            print("??????????????? {}".format(target))
            self.standby("select", tap=False)
            self.tap(self.button["servert{}".format(target)]["locate"])
        else:
            print("")
        self.pbar.update(1)

    def change(self, front: int, back: int):
        self.standby("attack", tap=False, coordinate=(670, 25))
        print("\r\x1b[2K", end='')
        print("[Change]??????????????????")
        self.pbar.display()
        self.tap(self.button["master"]["locate"])
        time.sleep(1)
        self.tap(self.button["master"]["skill3"])
        self.standby("order_change", tap=False)
        print("\r\x1b[2K", end='')
        print("[Change]?????? {} ?????????,??????????????? {} ?????????".format(front, back))
        self.tap(self.button["change"]["{}".format(front)])
        self.tap(self.button["change"]["{}".format(back+3)])
        self.tap(self.button["change"]["confirm"])
        self.pbar.update(1)

    def start_battle(self, total, singel):
        self.runtimes += 1
        if self.runtimes > self.max_times:
            self.enter_stage(total, singel, quit=True)
        else:
            state = self.enter_stage(total, singel)
        self.select_friend()
        if state == "menu":
            start = self.standby("start", tap=False)
            select = self.compare(self.templates["yello_dot"], self.screenshot,
                                  crop=self.button["team_select"]["{}".format(self.team)])
            if isinstance(select, bool):
                self.tap(self.button["team"]["{}".format(self.team)])
                time.sleep(1)
            self.standby("start")
        print("\r\x1b[2K", end='')
        print("[BATTLE]????????????")
        self.pbar.update(1)

    def finish_stage(self):
        print("\r\x1b[2K", end='')
        print("[Finish]???????????????...")
        self.pbar.update(1)
        self.standby("next", coordinate=(670, 25))
        result = self.standby(["continue", "menu", "friendrequest"], tap=False)
        if result[0] == "friendrequest":
            print("\r\x1b[2K", end='')
            print("[Finish]??????????????????")
            self.pbar.display()
            self.tap([250, 465])
        print("\r\x1b[2K", end='')
        print("[Finish]????????????!!")

    def get_friend(self, support):
        support_path = os.path.join(self.root, "UserData")
        support_path = os.path.join(support_path, "support")
        if os.path.isfile(os.path.join(support_path, support)):
            return cv2.imread(os.path.join(support_path, support))
        else:
            friend = dict()
            support_dict = os.path.join(support_path, support)
            for img in os.listdir(support_dict):
                friend[img.split('.')[0]] = cv2.imread(
                    os.path.join(support_dict, img))
            return friend

    def select_friend(self):
        have_bar = False
        found = False
        bar_crop = {'x': 910, 'y': 140, 'width': 50, 'height': 400}
        print("\r\x1b[2K", end='')
        print("[Support]????????????Support??????")
        self.pbar.display()
        while not found:
            have_bar = self.compare(self.templates["bar"], crop=bar_crop)
            if isinstance(have_bar, list):
                have_bar = False
            else:
                have_bar = True
            result = self.standby(["no_friend", "friend_bar"], tap=False)
            if result[0] == "no_friend":
                print("\r\x1b[2K", end='')
                print("[Support]????????????????????????,???????????????")
                self.pbar.display()
                self.standby("update")
                self.standby("refresh")
                self.standby("dis_refresh", disapper=True)
            else:
                result = self.compare(self.friend)
                if isinstance(result, list):
                    print("\r\x1b[2K", end='')
                    print("[Support]????????????????????????!")
                    self.tap(result[1])
                    self.pbar.update(1)
                    found = True
                else:
                    if have_bar:
                        while True:
                            self.swipe((100, 440), (100, 180))
                            time.sleep(1)
                            result = self.compare(self.friend)
                            if isinstance(result, list):
                                print("\r\x1b[2K", end='')
                                print("[Support]????????????????????????!")
                                self.tap(result[1])
                                self.pbar.update(1)
                                found = True
                                break
                            else:
                                end_crop = {'x': 925, 'y': 520,
                                            'width': 35, 'height': 20}
                                result = self.compare(
                                    self.templates["friendEnd"], self.screenshot, crop=end_crop)
                                if isinstance(result, list):
                                    print("\r\x1b[2K", end='')
                                    print("[Support]????????????????????????,???????????????")
                                    self.pbar.display()
                                    self.standby("update")
                                    self.standby("refresh")
                                    self.standby("dis_refresh", disapper=True)
                                    break
                    else:
                        print("\r\x1b[2K", end='')
                        print("[Support]????????????????????????,???????????????")
                        self.pbar.display()
                        self.standby("update")
                        self.standby("refresh")
                        self.standby("dis_refresh", disapper=True)


class box(base_unit):
    def __init__(self, device, templates):
        super().__init__(device, templates)
        self.status = "stop"
        self.result = None

    def gacha_tap(self):
        while True:
            if self.status not in ["full", "complete"]:
                self.tap([300, 330])
            else:
                break

    def box_gacha(self):
        self.status = "start"
        job = threading.Thread(target=self.gacha_tap)
        job.start()
        self.result = self.standby(["reset", "box_full"], tap=False)
        if self.result[0] == "box_full":
            self.status = "full"
            self.tap(self.result[1])
            print("???????????????!!")
            job.join()
            return True
        else:
            self.status = "complete"
            time.sleep(0.5)
            # self.tap(self.result[1])
            print("??????!!")
            # self.standby("execute")
            # self.standby("close")
            job.join()
            return False
