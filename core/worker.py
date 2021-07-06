# pylint: disable=unused-variable
from cv2 import cv2
import numpy as np
import os
import time
import random
import json
from core.match_func import sift
from core.match_func import match_template as match


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
                    return [pos[0], pos[1]]
            else:
                pos = match(imgs, self.screenshot, debug=debug)
                if isinstance(pos, list):
                    pos = np.int32(pos)
                    return [pos[0], pos[1]]
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
                try:
                    self.tap(flag)
                except:
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
    def __init__(self, root, device, templates, times: int, apple: str, count: int, support, recover: int):
        super().__init__(device, templates)
        self.root = root
        self.max_times = int(times)
        self.runtime = 0
        self.apple = apple
        if apple != '':
            self.count = int(count)
        else:
            self.count = 0
        self.recover = recover
        self.friend = self.get_friend(support)
        self.button = self.get_button()

    def get_button(self):
        with open('{}/UserData/button.json'.format(self.root), newline='') as jsonfile:
            data = json.load(jsonfile)
        return data

    def enter_stage(self, quit=False):
        result = self.standby(["continue", "menu"], tap=False)
        if quit:
            if result[0] == "continue":
                self.standby("close")
            print("[EXIT]腳本運行完成!!")
            exit()
        else:
            print("===============================================")
            print("[INFO]準備開始第 {} 輪".format(self.runtime))
            if result[0] == "menu":
                state = result[0]
                self.tap((750, 160))
            else:
                state = result[0]
                self.tap(result[1])
            print("[INFO]進入關卡                    ")
            result = self.standby(["noap", "select_friend"], tap=False)
            if result[0] == "noap":
                print("[Waring]體力耗盡")
                if self.apple == "saint" and self.count > 0:
                    self.tap((370, 130))
                    self.standby("confirm")
                    self.count -= 1
                    print("[INFO]使用聖晶石回體!")
                elif self.apple == "gold" and self.count > 0:
                    self.tap((370, 230))
                    self.standby("confirm")
                    self.count -= 1
                    print("[INFO]使用金蘋果回體!")
                elif self.apple == "silver" and self.count > 0:
                    self.tap((370, 330))
                    self.standby("confirm")
                    self.count -= 1
                    print("[INFO]使用銀蘋果回體!")
                elif self.apple == "copper" and self.count > 0:
                    self.tap((370, 425))
                    self.standby("confirm")
                    self.count -= 1
                    print("[INFO]使用銅蘋果回體!")
                else:
                    self.tap((470, 470))
                    print("[INFO]等帶回體中...")
                    start_time = time.time()
                    end_time = time.time()
                    while not int(end_time-start_time) >= self.recover*60:
                        remain = round(
                            self.recover - float(int(end_time-start_time)/60), 1)
                        if remain >= 60:
                            print("[INFO]等待回體中...,剩餘 {} 分鐘      ".format(
                                remain), end='\r')
                        else:
                            print("[INFO]等待回體中...,剩餘 {} 秒鐘       ".format(
                                remain), end='\r')
                        for i in range(30):
                            end_time = time.time()
                            if int(end_time-start_time) >= self.recover*60:
                                break
                            time.sleep(1)
                    self.enter_stage()
            return state

    def skill(self, position: int, skill: int, target=None):
        self.standby("attack", tap=False, coordinate=(670, 25))
        self.tap(self.button["servert{}".format(position)]
                 ["skill{}".format(skill)])
        print("[BATTLE]使用從者 {} 技能 {} ".format(position, skill), end='')
        if target is not None:
            print("附加給從者 {}".format(target))
            self.standby("select", tap=False)
            self.tap(self.button["servert{}".format(target)]["locate"])
        else:
            print("")

    def attack(self, first=None, second=None, third=None):
        self.standby("attack", coordinate=(670, 25))
        print("[BATTLE]準備使用指令卡")
        time.sleep(3)
        select = [first, second, third]
        for i in range(len(select)):
            if select[i] is None:
                rnd = random.randrange(1, 6)
                while rnd in select:
                    rnd = random.randrange(1, 6)
                select[i] = rnd
                print("[BATTLE]使用 {} 號指令卡".format(rnd))
                self.tap(self.button["card"]["{}".format(rnd)])
            else:
                if select[i] > 5:
                    print("[BATTLE]使用寶具 {} ".format(int(select[i])-5))
                else:
                    print("[BATTLE]使用 {} 號指令卡".format(select[i]))
                self.tap(self.button["card"]["{}".format(select[i])])

    def master(self, skill, target=None):
        self.standby("attack", tap=False, coordinate=(670, 25))
        print("[MASTER]準備使用御主技能")
        self.tap(self.button["master"]["locate"])
        time.sleep(1)
        print("[MASTER]使用御主技能 {}".format(skill), end='')
        self.tap(self.button["master"]["skill{}".format(skill)])
        if target is not None:
            print("附加給從者 {}".format(target))
            self.standby("select", tap=False)
            self.tap(self.button["servert{}".format(target)]["locate"])
        else:
            print("")

    def change(self, front: int, back: int):
        self.standby("attack", tap=False, coordinate=(670, 25))
        print("[Change]準備更換角色")
        self.tap(self.button["master"]["locate"])
        time.sleep(1)
        self.tap(self.button["master"]["skill3"])
        self.standby("order_change", tap=False)
        print("[Change]前排 {} 號從者,更換成後排 {} 號從者".format(front, back))
        self.tap(self.button["change"]["{}".format(front)])
        self.tap(self.button["change"]["{}".format(back+3)])
        self.tap(self.button["change"]["confirm"])

    def start_battle(self):
        self.runtime += 1
        if self.runtime > self.max_times:
            self.enter_stage(quit=True)
        else:
            state = self.enter_stage()
        self.select_friend()
        if state == "menu":
            self.standby("start")
        print("[BATTLE]進入關卡")

    def finish_stage(self):
        print("[Finish]等待下一步...")
        self.standby("next", coordinate=(670, 25))
        result = self.standby(["continue", "menu", "friendrequest"], tap=False)
        if result[0] == "friendrequest":
            print("[Finish]拒絕好友申請")
            self.tap([250, 465])
        print("[Finish]完成關卡!!")

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
        print("[Support]開始選擇Support角色")
        while not found:
            have_bar = self.compare(self.templates["bar"], crop=bar_crop)
            if isinstance(have_bar, list):
                have_bar = False
            else:
                have_bar = True
            result = self.standby(["no_friend", "friend_bar"], tap=False)
            if result[0] == "no_friend":
                print("[Support]沒有符合條件好友,將更新列表")
                self.standby("update")
                self.standby("refresh")
                self.standby("dis_refresh", disapper=True)
            else:
                result = self.compare(self.friend)
                if isinstance(result, list):
                    print("[Support]發現符合好友角色!")
                    self.tap(result[1])
                    found = True
                else:
                    if have_bar:
                        while True:
                            self.swipe((100, 440), (100, 180))
                            time.sleep(1)
                            result = self.compare(self.friend)
                            if isinstance(result, list):
                                print("[Support]發現符合好友角色!")
                                self.tap(result[1])
                                found = True
                                break
                            else:
                                end_crop = {'x': 925, 'y': 520,
                                            'width': 35, 'height': 20}
                                result = self.compare(
                                    self.templates["friendEnd"], self.screenshot, crop=end_crop)
                                if isinstance(result, list):
                                    print("[Support]好友列表已經至底,將更新列表")
                                    self.standby("update")
                                    self.standby("refresh")
                                    self.standby("dis_refresh", disapper=True)
                                    break
                    else:
                        print("[Support]沒有符合條件好友,將更新列表")
                        self.standby("update")
                        self.standby("refresh")
                        self.standby("dis_refresh", disapper=True)
