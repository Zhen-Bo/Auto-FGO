import os
import json
root_path = os.path.dirname(os.path.abspath(__file__))
UserData_path = os.path.join(root_path, "UserData")
script_path = os.path.join(UserData_path, "script.json")


def new_script():
    # =======================================================================
    # 新增腳本
    # =======================================================================
    os.system('cls')
    script = dict()
    script["name"] = input("請輸入腳本名稱: ")

    version_dict = {"0": "JP", "1": "TW"}
    version_naem = {"0": "日版", "1": "台版"}
    while True:
        os.system('cls')
        print("腳本名稱: {}".format(script["name"]))
        print("======================================")
        print("選擇遊戲版本:\n0 = 日版\n1 = 台版")
        version = input("請輸入遊戲版本: ")
        if version not in ["0", "1"]:
            continue
        else:
            script["version"] = version_dict[version]
            break

    while True:
        os.system('cls')
        print("腳本名稱: {} /遊戲版本: {}".format(
            script["name"], version_naem[version]))
        print("======================================")
        team = input("請輸入使用編隊編號(1~10): ")
        team_range = range(1, 11, 1)
        if int(team) in team_range:
            script["team"] = team
            break
        else:
            continue

    apple_dict = {"": "", "0": "quartz",
                  "1": "goldden", "2": "silver", "3": "copper"}
    apple_name = {"": "自然回體", "0": "聖晶石", "1": "金蘋果", "2": "銀蘋果", "3": "銅蘋果"}
    while True:
        os.system('cls')
        print("腳本名稱: {} /遊戲版本: {}".format(
            script["name"], version_naem[version]))
        print("使用隊伍:第 {} 隊".format(team))
        print("======================================")
        for i in range(4):
            print("{} = {}".format(i, apple_name["{}".format(i)]))
        print("不輸入為自然回體")
        apple = input("請選擇方案: ")
        if apple not in apple_dict:
            continue
        else:
            script["apple"] = apple_dict[apple]
            break
    if script["apple"] != "":
        while True:
            os.system('cls')
            print("腳本名稱: {} /遊戲版本: {}".format(
                script["name"], version_naem[version]))
            print("使用隊伍:第 {} 隊".format(team))
            print("回體方案: {}".format(apple_name[apple]))
            print("======================================")
            count = input("請輸入使用上限: ")
            if count.isdigit():
                script["count"] = count
                break
    else:
        script["count"] = ""

    userdata_path = os.path.join(root_path, "UserData")
    support_path = os.path.join(userdata_path, "support")
    while True:
        os.system('cls')
        print("腳本名稱: {} /遊戲版本: {}".format(
            script["name"], version_naem[version]))
        print("使用隊伍:第 {} 隊".format(team))
        if script["count"] == "":
            print("回體方案: {} 額度 無".format(apple_name[apple]))
        else:
            print("回體方案: {} 額度 {}".format(apple_name[apple], script["count"]))
        print("======================================")
        script["support"] = input("請輸入好友圖檔全名或資料夾名稱: ")
        if script["support"] != "":
            if not os.path.exists(os.path.join(support_path, script["support"])):
                status = "(不存在)"
                break
            elif os.path.isdir(os.path.join(support_path, script["support"])):
                status = "(資料夾)"
                break
            elif os.path.isfile(os.path.join(support_path, script["support"])):
                status = "(單一圖片檔)"
                break
            else:
                continue
    while True:
        os.system('cls')
        print("腳本名稱: {} /遊戲版本: {}".format(
            script["name"], version_naem[version]))
        print("使用隊伍:第 {} 隊".format(team))
        print("回體方案: {} 額度 {}".format(apple_name[apple], script["count"]))
        print("選擇支援者: {} {}".format(script["support"], status))
        print("======================================")
        ap = input("請輸入關卡耗體: ")
        if ap.isdigit():
            script["recover"] = int(ap)*5
            break
    err_flag = False
    script["battle"] = []
    script["battle"].append("start_battle()")
    while True:
        os.system('cls')
        print("腳本概況:")
        for i in range(len(script["battle"])):
            print("指令{} : {}".format(i, script["battle"][i]))
        print("======================================")
        print("請輸入要使用的指令")
        print("0 = 開始攻擊(選擇指令卡)")
        print("1 = 施放從者技能(非指定)")
        print("2 = 施放從者技能(需指定)")
        print("3 = 使用換人技能(魔術禮裝)")
        print("4 = 施放御主技能(非指定)")
        print("5 = 施放御主技能(需指定)")
        print("9 = 結束戰鬥(並離開配置模式)")
        print("======================================")
        if err_flag:
            print("指令輸入錯誤!!")
            err_flag = False
        instr = input("請選擇指令: ")
        if instr not in ["0", "1", "2", "3", "4", "5", "9"]:
            continue
        elif instr == "0":
            os.system('cls')
            card = []
            print("開始新增攻擊指令")
            print("請輸入指令卡編號:")
            print("寶具從左至右為:\n6 / 7 / 8")
            print("普通卡片從左至右為:\n1 / 2 / 3 / 4 / 5")
            print("自動選擇直接按enter即可")
            number = input("第 {} 張指令卡: ".format(len(card)+1))
            # 第一張
            if number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                card.append(number)
            else:
                card.append("")
            # 第二張
            number = input("第 {} 張指令卡: ".format(len(card)+1))
            if number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                card.append(number)
            else:
                card.append("")
            # 第三張
            number = input("第 {} 張指令卡: ".format(len(card)+1))
            if number in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                card.append(number)
            else:
                card.append("")
            # 合併
            instrument = "attack("
            for number in card:
                if number == "":
                    instrument += "None,"
                else:
                    instrument += "{},".format(number)
            instrument = instrument[:-1]
            instrument += ")"
            script["battle"].append(instrument)
            continue
        elif instr == "1" or instr == "4":
            if instr == "1":
                instrument = "skill("
            else:
                instrument = "master("
            if instr == "1":
                while True:
                    position = input("請問是第幾位從者要施放技能(1~3): ")
                    if position not in ["1", "2", "3"]:
                        continue
                    else:
                        instrument += "{},".format(position)
                        break
            while True:
                if instr == "1":
                    position = input("請問是要施放該從者第幾個技能(1~3): ")
                else:
                    position = input("請問是要施放第幾個御主技能(1~3): ")
                if position not in ["1", "2", "3"]:
                    continue
                else:
                    instrument += "{}".format(position)
                    break
            instrument += ")"
            script["battle"].append(instrument)
        elif instr == "2" or instr == "5":
            if instr == "2":
                instrument = "skill("
            else:
                instrument = "master("
            if instr == "2":
                while True:
                    position = input("請問是第幾位從者要施放技能(1~3): ")
                    if position not in ["1", "2", "3"]:
                        continue
                    else:
                        instrument += "{},".format(position)
                        break
            while True:
                if instr == "2":
                    position = input("請問是要施放該從者第幾個技能(1~3): ")
                else:
                    position = input("請問是要施放第幾個御主技能(1~3): ")
                if position not in ["1", "2", "3"]:
                    continue
                else:
                    instrument += "{},".format(position)
                    break
            while True:
                position = input("請問是要施放的對象是第幾個從者(1~3): ")
                if position not in ["1", "2", "3"]:
                    continue
                else:
                    instrument += "{}".format(position)
                    break
            instrument += ")"
            script["battle"].append(instrument)
        elif instr == "3":
            instrument = "change("
            while True:
                position = input("要更換的前排從者為(1~3): ")
                if position not in ["1", "2", "3"]:
                    continue
                else:
                    instrument += "{},".format(position)
                    break
            while True:
                position = input("要更換的後排從者為(1~3): ")
                if position not in ["1", "2", "3"]:
                    continue
                else:
                    instrument += "{}".format(position)
                    break
            instrument += ")"
            script["battle"].append(instrument)
        elif instr == "9":
            script["battle"].append("finish_stage()")
            break
        else:
            err_flag = True
            continue

    with open(script_path, newline='', encoding='utf8') as jsonfile:
        data = json.load(jsonfile)
    data["script"].append(script)
    with open(script_path, "w", encoding='utf8') as jsonfile:
        json.dump(data, jsonfile)


def del_script():
    # =======================================================================
    # 刪除腳本
    # =======================================================================
    with open(script_path, newline='') as jsonfile:
        data = json.load(jsonfile)
    print("請選擇要刪除的腳本")
    for i in range(len(data['script'])):
        print("{}: {}".format(i, data['script'][i]['name']))
    number = input("請輸入編號:")
    while not number.isdigit() or int(number) > len(data['script']) or int(number) < 0:
        os.system('cls')
        print("請選擇要刪除的腳本")
        for i in range(len(data['script'])):
            print("{}: {}".format(i, data['script'][i]['name']))
        print("輸入編號錯誤,請重新輸入")
        number = input("請輸入編號:")
    data["script"].pop(int(number))
    with open(script_path, "w", encoding='utf8') as jsonfile:
        json.dump(data, jsonfile)


def edit_script():
    # =======================================================================
    # 修改腳本
    # =======================================================================
    with open(script_path, newline='') as jsonfile:
        data = json.load(jsonfile)
    print("請選擇要修改的腳本")
    for i in range(len(data['script'])):
        print("{}: {}".format(i, data['script'][i]['name']))
    number = input("請輸入編號:")
    while not number.isdigit() or int(number) > len(data['script']) or int(number) < 0:
        os.system('cls')
        print("請選擇要修改的腳本")
        for i in range(len(data['script'])):
            print("{}: {}".format(i, data['script'][i]['name']))
        print("輸入編號錯誤,請重新輸入")
        number = input("請輸入編號:")
    select = data["script"][int(number)]
    # TODO 細項修改
    pass


if __name__ == '__main__':
    while True:
        os.system('cls')
        print("請選擇操作,0=新增 1=修改 2=刪除")
        action = input("模式: ")
        if action not in ["0", "1", "2"]:
            continue
        if action == "0":
            new_script()
        elif action == "1":
            edit_script()
        elif action == "2":
            del_script()
