from tkinter import *
from PIL import Image, ImageTk
from gameLib.game_ctl import *
import win32api
import win32con
import win32gui
import win32ui
import keyboard
import threading
import re
import math
import queue
from concurrent.futures import ThreadPoolExecutor
from collections import Counter

target_sts_dict = {
    '主': 1,
    '被': 2,
    '跟': 3,
    '停': 4
}

#用于八角塔 第四步 提交任务之后，队长从幸运套装切换到输出套

bajiaota_team_leader_list = []

only_lingshou_list = []

yiren_list = []

xiake_list = []

yanshi_list = []

fangshi_list = []

#用于打宝，一个队伍最多只有一个高幸运的异人作为队长，且以幸运优先，能力向幸运兼容
#通过能力区分一下异人队长
# 1.异人打宝读档一面(始终用幸运装打宝，包括boss和小怪)     high_ability_yiren_list
# 2.异人打宝防御够，但输出不足(能用幸运装打怪，但是输出不够，幸运装能抗但是需要队友输出) middle_ability_yiren_list
# 3.异人打宝能力弱(不能用幸运装抗小怪和boss)              low_ability_yiren_list

#通过幸运区分一下异人队长
# 1. 500幸运以上异人       high_luck_yiren_list
# 2. 400 ~ 500 幸运异人    middle_luck_yiren_list
# 3. 400幸运以下异人        low_luck_yiren_list

#结合上面的条件，队长的幸运最高，然后根据队长能力和幸运设置队长和队友打怪的时候的切装设置以及队友的slaver状态
#小怪时
# 队长符合 high_ability_yiren_list 时   队长全程幸运装，全员队友slaver跟随
# 队长符合 middle_ability_yiren_list 时   队长全程幸运装，全员队友slaver主动且全程幸运装
# 队长符合 low_ability_yiren_list 时     队长和队友全程slaver主动，输出装
#boss时
# 队长符合 luck_high 时  队长幸运装，全员队友slaver跟随
# 队长符合 luck_middle 时  队长幸运装，全员队友slaver跟随
# 队长符合 luck_low 时    队友和队员slaver主动，切幸运装

dabao_team_leader_dict = {
    'ability_high'  : [],
    'ability_middle': [],
    'ability_low'   : [],
    'luck_high'     : [],
    'luck_middle'   : [],
    'luck_low'      : [],
    'other'         : []
}

def change_equipment_to_luck_setting(game:GameControl):
    if game.player_id not in yiren_list and game.player_id not in only_lingshou_list:
        print('palyer need not change equipment setting',game.player)
        return
    game.activate_window()
    time.sleep(0.5)
    game.press_combination_keys((['menu','w']))#切换到幸运装

def change_equipment_to_attack_setting(game:GameControl):
    if game.player_id not in yiren_list and game.player_id not in only_lingshou_list:
        print('palyer need not change equipment setting',game.player)
        return
    game.activate_window()
    time.sleep(0.5)
    game.press_combination_keys((['menu','q']))#切换到输出装

def change_player_status_in_monster(game:GameControl,game_list:GameControl):
    cancel_followed_with_leftclcik(game)
    time.sleep(0.5)

    # high ability
    if game.player_id in dabao_team_leader_dict['ability_high']:
        for sub_game in game_list:
            if sub_game.player_id == game.player_id:
                modify_slaver_status(sub_game,'主')
                change_equipment_to_luck_setting(sub_game)
            elif sub_game.player_id in dabao_team_leader_dict['other']:
                modify_slaver_status(sub_game,'跟')
            else:
                modify_slaver_status(sub_game,'跟')
        return
    # middle ability
    if game.player_id in dabao_team_leader_dict['ability_middle']:
        for sub_game in game_list:
            if sub_game.player_id == game.player_id:
                modify_slaver_status(sub_game,'主')
                change_equipment_to_luck_setting(sub_game)
            elif sub_game.player_id in dabao_team_leader_dict['other']:
                modify_slaver_status(sub_game,'跟')
            else:
                modify_slaver_status(sub_game,'跟')
        return
    # low ability
    if game.player_id in dabao_team_leader_dict['ability_low']:
        for sub_game in game_list:
            if sub_game.player_id in dabao_team_leader_dict['other']:
                modify_slaver_status(sub_game,'跟')
            else:
                modify_slaver_status(sub_game,'主')
                change_equipment_to_attack_setting(sub_game)
        return 

def change_player_status_in_boss(game:GameControl,game_list:GameControl):
    print('change player status before attacking boss')
    cancel_followed_with_leftclcik(game)
    time.sleep(0.5)
    # high ability
    if game.player_id in dabao_team_leader_dict['luck_high']:
        print('change_player_status_in_boss: high luck',game.player)
        for sub_game in game_list:
            if sub_game.player_id == game.player_id:
                modify_slaver_status(sub_game,'主')
                change_equipment_to_luck_setting(sub_game)
            elif sub_game.player_id in dabao_team_leader_dict['other']:
                modify_slaver_status(sub_game,'跟')
            else:
                modify_slaver_status(sub_game,'跟')
        return
    # middle ability
    if game.player_id in dabao_team_leader_dict['luck_middle']:
        print('change_player_status_in_boss: middle luck',game.player)
        for sub_game in game_list:
            if sub_game.player_id in dabao_team_leader_dict['other']:
                modify_slaver_status(sub_game,'跟')
            else:
                modify_slaver_status(sub_game,'主')
                change_equipment_to_luck_setting(sub_game)
        return
    # low ability
    if game.player_id in dabao_team_leader_dict['luck_low']:
        print('change_player_status_in_boss: low luck',game.player)
        for sub_game in game_list:
            if sub_game.player_id in dabao_team_leader_dict['other']:
                modify_slaver_status(sub_game,'跟')
            else:
                modify_slaver_status(sub_game,'主')
                change_equipment_to_luck_setting(sub_game)
        return 
   
def calculate_time_for_two_pointers(loc1,loc2,time_resolution,time_offset=[0,0]):
    # 计算两个坐标的直线距离
    distance = math.sqrt((loc2[0] - loc1[0])**2 + (loc2[1] - loc1[1])**2)
    
    if time_resolution == 1: #diff area 
        distance_time = distance * float(2/75) + time_offset[0]
    elif time_resolution == 2:# #same area
        distance_time = distance * float(2/75) + time_offset[1]
    else:
        distance_time = distance * float(2/849)
        print(distance_time)
    return distance_time

def close_all_game_windows():
    os.system(f"taskkill /f /im {'GacRunner'}.exe")

def recognize_monster_number(game:GameControl,extend = 0,gui = False):
    #(779, 83) (878, 98) 
    # 如果是用内存截图识别，就不需要game.window_pos1作为左上角基准
    #内存截图左上角基准是（0，0）
    '''
    0: 四色鱼
    1: 雷峰塔
    2: 河伯，夜宴，秋江
    3: 青蛙
    4: 桃花
    '''
    # monster_num_pos1 = (game.window_pos1[0]+1175, game.window_pos1[1]+120)
    # monster_num_pos2 = (game.window_pos1[0]+1317, game.window_pos1[1]+151)
    monster_num_pos1 = (game.window_pos1[0]+779, game.window_pos1[1]+83)
    monster_num_pos2 = (game.window_pos1[0]+878, game.window_pos1[1]+98)
    try:
        res = game.recognize_text(monster_num_pos1,monster_num_pos2,gray=0,gui_flag=gui)
    except:
        if extend == 0: #四色鱼
            res = {'text':'0/240'}
        elif extend == 1: # 雷峰塔
            res = {'text':'0/160'}
        elif extend == 2: # 河伯 ,夜宴
            res = {'text':'0/0'}
        elif extend == 3: # 青蛙
            res = {'text':'0/150'}
        elif extend == 4: # 桃花
            res = {'text':'0/500'}
    print(res)
    text = res['text']  # 获取字典中'text'对应的字符串
    try:
        if extend == 0: #四色鱼
            extracted_text = re.search(r'\d+/\d+', text).group().split('/')[0]
        elif extend == 1: #雷峰塔
            extracted_text = re.search(r'\d+/\d+', text).group().split('/')
        elif extend == 2: #河伯
            extracted_text = re.search(r'\d+/\d+', text).group().split('/')
        elif extend == 3: #青蛙
            extracted_text = re.search(r'\d+/\d+', text).group().split('/')[0]
        elif extend == 4: #桃花
            extracted_text = re.search(r'\d+/\d+', text).group().split('/')[0]
    except:
        if extend == 0:
            extracted_text = '0'
        elif extend == 1: #雷峰塔
            extracted_text = ['0','0']
        elif extend == 2: #河伯
            extracted_text = ['0','0']
        elif extend == 3: #青蛙
            extracted_text = '0'
        elif extend == 4: #桃花
            extracted_text = '0'

    print(extracted_text)
    return extracted_text

def check_is_boss(game:GameControl):
    try:
        text_tmp = game.recognize_text(game.monster_attribute_pos1,game.monster_attribute_pos2,image_show=False)
    except:
        text_tmp = {'text':''}
        print(game.player,' check_is_boss error appear: ',text_tmp)
    print('check_is_boss:',text_tmp)
    if 'boss' in text_tmp['text'] or 'Boss' in text_tmp['text']:
        return True
    
    return False

def check_is_monster(game:GameControl):
    try:
        text_tmp = game.recognize_text(game.monster_attribute_pos1,game.monster_attribute_pos2,image_show=False)
    except:
        text_tmp = {'text':''}
        print(game.player,' check_is_monster error appear: ',text_tmp)
    print('check_is_monster:',text_tmp)
    if '道' in text_tmp['text']:
        return True
    
    return False

def check_monster_is_dead(game:GameControl):
    try:
        text_tmp = game.recognize_text(game.monster_name_pos1,game.monster_name_pos2,image_show=False)
    except:
        text_tmp = {'text':''}
        print(game.player,' check_monster_is_dead error appear: ',text_tmp)
    print('check_monster_is_dead:',text_tmp)
    if '死' in text_tmp['text'] or '亡' in text_tmp['text']:
        return True
    
    return False

def check_target_appear(game:GameControl,target_str_list):
    try:
        text_tmp = game.recognize_text(game.monster_name_pos1,game.monster_name_pos2,image_show=False)
    except:
        text_tmp = {'text':''}
        print(game.player,' check_target_appear error appear: ',text_tmp)
    print('check_monster_is_dead:',text_tmp)
    for str in target_str_list:
        if str in text_tmp['text']:
            return True
    
    return False

# the function of recognizing the color is not ok, TBD
def check_color_with_position(game:GameControl,x,y,limit_pos1,limit_pos2):
    region_width = 2
    region_height = 2
    target_color = [(0, 0, 0),
                    (28,28,28),(212,212,212),(250,250,250),
                    (127,128,128),(82,83,83),(212,212,212),
                    (172,172,172),(240,240,240),
                    (199,102,8),(239,122,10),(49,25,2),
                    (18,8,1),(126,64,5),(147,75,6),
                    (159,81,6),(61,31,2),(178,91,7)]
    counter = 0
    position1 = (int(x - region_width), int(y - region_height/2))
    position2 = (int(x), int(y))
    time_start = time.time()
    for cur_x in range(position1[0],position2[0]):
        for cur_y in range(position1[1],position2[1]):
            if cur_x >= limit_pos1[0] and cur_x <= limit_pos2[0] and cur_y >= limit_pos1[1] and cur_y <= limit_pos2[1]:
                tmp = time.time()
                flag = game.check_color((cur_x,cur_y),target_color,tolerance = 10)
                print(time.time() - tmp)
                if flag:
                    counter = counter + 1
                    if counter >= 1:
                        time_end = time.time()
                        print('success:',time_end - time_start)
                        return True
    time_end = time.time()
    print('fail:',time_end - time_start)
    return False

def get_location_whit_pict(game:GameControl):

    game.activate_window()
    time.sleep(0.5)

    # 从game对象中获取窗口的宽度和高度信息
    width = game._window_w
    height = game._window_h

    # 创建窗口
    window = Tk()

    # 设置窗口大小和标题
    window.geometry(f"{width}x{height}")
    window.title("Mouse Click Coordinates")

    # 截取窗口图像
    screenshot = gui.screenshot(region=(game.window_pos1[0], game.window_pos1[1], width, height))
    image = Image.frombytes("RGB", screenshot.size, screenshot.tobytes())

    # 在窗口中显示图像
    canvas = Canvas(window, width=width, height=height)
    canvas.pack()
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=NW, image=photo)
    # 存储描点的坐标
    points = []

    # 鼠标点击事件回调函数
    def mouse_click(event):
        # 获取鼠标点击点的坐标
        x = event.x
        y = event.y
        
        # 绘制红色圆点
        canvas.create_oval(x-2, y-2, x+2, y+2, fill="red", outline="red")

        # 将坐标添加到points列表
        points.append((x, y))

    # 绑定鼠标点击事件
    canvas.bind("<Button-1>", mouse_click)

    # 进入主循环
    window.mainloop()

    str_print = ''
    # 输出所有鼠标描点的相对坐标
    for point in points:
        x = point[0]
        y = point[1]
        if  str_print == '':
            str_print = str_print + f"({x}, {y}),"
        else:
            str_print = str_print + f"({x}, {y}),"
    print(str_print)

def open_self_task_table(game:GameControl):
    retry_cunt = 0
    while True and retry_cunt < 5:
        map_loc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\self_task_table.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=0,thread=0.80)
        if map_loc != False:
            return True
        else:
            time.sleep(0.5)
            game.press_single_key('k') #task
            time.sleep(0.079)
            retry_cunt = retry_cunt + 1
    return False

def accept_task(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\accept_task.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
    if  False != maxLoc:
        gui.moveTo(maxLoc)
        gui.leftClick()
        print('get task successfully')
        return True
    else:
        print('get task failed')
        return False

def complete_task(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\complete_task.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
    if  False != maxLoc:
        gui.moveTo(maxLoc)
        gui.leftClick()
        print(game.player,'complete task successfully')
        return True
    else:
        print(game.player,'complete task failed')
        return False   

def confirm(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\confirm.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
    if  False != maxLoc:
        gui.moveTo(maxLoc)
        gui.leftClick()
        print('confirm successfully')
        return True
    else:
        print('confirm failed')
        return False   

def drag_auto_road_table(game:GameControl,distance,direction = 'up'):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\auto_road_slide_bar.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,image_show=False,gray=1,thread=0.91)
    if maxLoc != False:
        print('auto road slide bar')
        if direction == 'up':
            game.drag_up_or_down(maxLoc[0],maxLoc[1],distance,True)
        else:
            game.drag_up_or_down(maxLoc[0],maxLoc[1],distance,False)
        return True
    return False

def find_npc_by_drag(game:GameControl,npc_image,retry_distance):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\autoFindRoad1.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.7)
    retry_cunt_tmp = 0
    
    if maxLoc != False:
        autoFindRoad1_location = maxLoc
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.2)
        maxLoc = game.find_game_img(npc_image,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.63)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.2)
            gui.moveTo(autoFindRoad1_location)
            gui.leftClick()
            time.sleep(0.2)
            return True
        
        while retry_cunt_tmp < 5:
            tmp_flag = drag_auto_road_table(game,retry_distance,'down')
            if tmp_flag == False:
                print('failed drag to find npc, retry cunt ',retry_cunt_tmp)
            time.sleep(2)
            maxLoc = game.find_game_img(npc_image,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.63)
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
                gui.moveTo(autoFindRoad1_location)
                gui.leftClick()
                time.sleep(0.2)
                return True
            retry_cunt_tmp = retry_cunt_tmp + 1
    print('not find auto road pict!')
    return False

def input_content(game:GameControl,content_str):
    for single_char in content_str:
        game.press_single_key_in_background(single_char,0.03)

def find_npc_by_search(game:GameControl,npc_image,npc_str,moveToNpc=True):

    close_all_table(game)

    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\autoFindRoad1.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.7)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.5)
        maxLoc = game.find_game_img(npc_image,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            if moveToNpc:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
            else:
                game.press_single_key_in_background('escape')
            return True

        #in auto-find window, find 'serach'
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\autofind_serach.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.63)
        if maxLoc != False:
            gui.moveTo((maxLoc[0]+50,maxLoc[1]))
            gui.leftClick()
            time.sleep(0.2)
            input_content(game,npc_str)
            time.sleep(0.5)
            maxLoc = game.find_game_img(npc_image,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                if moveToNpc:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                else:
                    game.press_single_key_in_background('escape')
                return True

    if moveToNpc == False:      
        game.press_single_key_in_background('escape')
    return False

def open_map(game:GameControl,map_img_path):
    #check whether map has been opened in current window
    #if open return
    #else input key to open the map
    retry_cunt = 0
    while True and retry_cunt < 5:
        map_loc = game.find_game_img(map_img_path,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=0,thread=0.80)
        if map_loc != False:
            return True
        else:
            game.press_single_key('r') #map
            retry_cunt = retry_cunt + 1
            time.sleep(1)
    return False

def open_map_common(game:GameControl):
    map_img_path = r'F:\01_game_ctr\lib\img\common\common_map.png'
    retry_cunt = 0
    while True and retry_cunt < 5:
        map_loc = game.find_game_img(map_img_path,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=0,thread=0.80)
        if map_loc != False:
            return True
        else:
            game.press_single_key('r') #map
            retry_cunt = retry_cunt + 1
            time.sleep(1)
    return False 

def open_team_table(game:GameControl,team_img_path):
    retry_cunt = 0
    while True and retry_cunt < 5:
        map_loc = game.find_game_img(team_img_path,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=0,thread=0.80)
        if map_loc != False:
            return True
        else:
            game.press_single_key('m') #team
            retry_cunt = retry_cunt + 1
        time.sleep(0.5)
    return False

def close_all_table(game:GameControl):

    window_center_pos = (game.window_pos1[0]+519, game.window_pos1[1]+459) #(game.window_pos1[0]+784, game.window_pos1[1]+710)
    close_table_img_list = [r'F:\01_game_ctr\lib\img\common\close_table.png',
                            r'F:\01_game_ctr\lib\img\common\close_table1.png']
                            #r'F:\01_game_ctr\lib\img\common\close_table2.png']
    maxLoc,img_name= game.find_game_multi_img(close_table_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.80)
    if maxLoc != False:
        print('close table!')
        gui.moveTo(maxLoc)
        gui.rightClick()
        time.sleep(0.5)
        #调整下鼠标的位置，防止遮挡
        gui.moveTo(window_center_pos)
'''
not used, the function is commented  2024.01.25
def make_window_top(game:GameControl):
    game.press_single_key('f4')
    win32gui.SetForegroundWindow(game.hwnd)
    time.sleep(0.5)
'''

flag = 0
add_key_sts = False
def moniter_keyboard(key):
    global flag
    global add_key_sts
    a = keyboard.KeyboardEvent(event_type='down', scan_code=58, name='caps lock')
    b = keyboard.KeyboardEvent(event_type='down', scan_code=29, name='ctrl')
    c = keyboard.KeyboardEvent(event_type='down', scan_code=78, name='add')
    d = keyboard.KeyboardEvent(event_type='down', scan_code=74, name='minus')
    # # get key code and name
    # print("current key code:  {}".format(x.scan_code))
    # print("current key name:  {}".format(x.name))

    if key.event_type == a.event_type and key.scan_code == a.scan_code:
        flag += 1
        print("You pressed {}.".format(a.name))
        if flag % 4 == 0 and flag != 0:
            print('slow click')
        elif flag % 4 == 1 :
            print('fast click')
        elif flag % 4 == 2 :
            print(flag % 4)
            print('left click')
        
    elif key.event_type == b.event_type and key.scan_code == b.scan_code:
        print("You pressed {}.".format(b.name))
        flag = 0

    elif key.event_type == c.event_type and key.scan_code == c.scan_code:
        add_key_sts = True
    
    elif key.event_type == d.event_type and key.scan_code == d.scan_code:
        add_key_sts = False

keyboard.hook(moniter_keyboard)

def suspend():
    global add_key_sts
    while add_key_sts:
        time.sleep(0.5)

def mouse_right_click(gap_time=0):
    while True:
        if flag % 4 == 1 or flag % 4 == 0:
            gui.rightClick()
            time.sleep(gap_time)

def mouse_left_click(gap_time=0):
    while True:
        if flag % 4 == 2:
            gui.leftClick()
            time.sleep(gap_time)



yiren_buff_key_list = ['4','5','6','7','8']

def set_player_buff(game:GameControl):
    if game.player_id in yiren_list:
        for key in yiren_buff_key_list:
            game.press_single_key_in_background(key)
            time.sleep(0.8)

    if game.player_id in xiake_list:
        game.press_single_key_in_background('0')
        time.sleep(0.5)
        game.press_single_key_in_background('z')
        time.sleep(0.5)

def reset_all_player_slaver(game:GameControl):
    if game.player_id in yiren_list:
        game.press_single_key_in_background('l') # reset slaver
        time.sleep(0.9)
        game.press_single_key_in_background('l')
        time.sleep(0.8)
    if game.player_id in yanshi_list:
        game.press_single_key_in_background('f5')
        time.sleep(7)
        game.press_single_key_in_background('f5')
        time.sleep(7)
        game.press_single_key_in_background('f5')
        time.sleep(0.5)
        game.press_single_key_in_background('f6')

def reset_yiren_player_slaver(game:GameControl):
    if game.player_id in yiren_list:
        game.press_single_key_in_background('l') # reset slaver
        time.sleep(0.9)
        game.press_single_key_in_background('l')
        time.sleep(0.8)

def set_buff_and_reset_slaver(game:GameControl,slaver_reset=False):
    if slaver_reset:
        reset_all_player_slaver(game)

    set_player_buff(game)
    
def reset_multi_player_status(game:GameControl, game_list, follow=False, reset_slver=False):
    cancel_followed_with_leftclcik(game)
    time.sleep(0.5)

    for sub_game in game_list:
        set_buff_and_reset_slaver(sub_game,slaver_reset=reset_slver)

    if follow:
        followed_with_rightclick(game)

def reset_multi_player_status_in_dungon(game:GameControl, game_list, follow=False, reset_slver=False):
    cancel_followed_with_leftclcik(game)
    time.sleep(0.5)

    executor = ThreadPoolExecutor(max_workers=6)
    futures = []
    for sub_game in game_list:
        future = executor.submit(set_buff_and_reset_slaver, sub_game,slaver_reset=reset_slver)
        futures.append(future)
    # 等待所有任务执行完成
    for future in futures:
        future.result()

    if follow:
        followed_with_rightclick(game)

def set_player_buff_main(game:GameControl,game_list,pick_up=False):
    tmp_cunt = 0
    rst_slaver = False
    all_equiment_cunt = 0
    miss_cunt = 0

    reset_multi_player_status(game,game_list,reset_slver=True)
    if game.slaver_start_time == 0:
        game.reset_slaver_start_time()

    while True:
        rst_slaver = False
        if int(game.get_slaver_run_time()) > 600:
            game.reset_slaver_start_time()
            tmp_cunt = tmp_cunt + 1
            if tmp_cunt >= 3:
                rst_slaver = True
                tmp_cunt = 0
            reset_multi_player_status(game,game_list,reset_slver=rst_slaver)

        print('all_equiment_cunt:',all_equiment_cunt)  
        if all_equiment_cunt > 15:
            all_equiment_cunt = 0
            compound_equipment(game) 

        if miss_cunt > 3:
            miss_cunt = 0
            game.press_single_key_in_background('p')
            time.sleep(3)
            game.press_single_key_in_background('p')

        if pick_up:
            #pick_flag = pick_up_money(game)
            pick_equipment = pick_up_equipment(game)
            all_equiment_cunt = all_equiment_cunt + pick_equipment
            if pick_equipment == 0:
                miss_cunt = miss_cunt + 1
            else:
                miss_cunt = 0
            
            #如果包裹满了，直接取合成装备
            package_full_img_list = [r'F:\01_game_ctr\lib\img\common\package_full.png']
            loc, img_name = game.find_game_multi_img(package_full_img_list,part=1,pos1=game.window_pos1,\
                                                      pos2=game.window_pos2,image_show= False,thread=0.70)
            if loc != False:
                all_equiment_cunt = 16
                miss_cunt = 0
                #等2s,提示包裹满的字条消失
                time.sleep(2) 
        click_dice_to_get_materiel(game)
        find_yanzhengma(game,game_list)
        time.sleep(0.5)

def followed_with_rightclick(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    followed_img_list = [r'F:\01_game_ctr\lib\img\common\followed1.png', r'F:\01_game_ctr\lib\img\common\not_followed1.png']
          
    followed_loc, img_name = game.find_game_multi_img(followed_img_list,part=1,pos1=game.window_pos1,\
                                                      pos2=game.window_pos2,image_show= False,thread=0.65)
    if followed_loc != False:
        if img_name == "not_followed1.png":
            print('not followed, right click to follow all player')
            gui.moveTo(followed_loc)
            gui.rightClick()
            time.sleep(0.2)
            time.sleep(2)
            return True
        if img_name == "followed1.png":
            print('followed, right click to follow all player')
            gui.moveTo(followed_loc)
            gui.rightClick()
            time.sleep(0.2)
            time.sleep(2)
            return True

    print('cannot recognize the followed img to determine the status')
    return False

def cancel_followed_with_leftclcik(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    followed_img_list = [r'F:\01_game_ctr\lib\img\common\followed.png', r'F:\01_game_ctr\lib\img\common\not_followed.png']
           #                
    followed_loc, img_name = game.find_game_multi_img(followed_img_list,part=1,pos1=game.window_pos1,\
                                                      pos2=game.window_pos2,image_show= False,thread=0.65)
    if followed_loc != False:
        if img_name == "not_followed.png":
            print('not followed, do nothing')
            return True
        if img_name == "followed.png":
            print('followed, left click to cancel followed')
            gui.moveTo(followed_loc)
            time.sleep(0.2)
            gui.leftClick()
            time.sleep(0.2)
            time.sleep(2)
            return True

    print('cannot recognize the followed img to determine the status')
    return False

def modify_slaver_status(game:GameControl,target_sts:str):
    if target_sts not in target_sts_dict:
        print('input target_sts is not in range!',game.player)
        return
    
    if game.player_id not in yiren_list and game.player_id not in only_lingshou_list:
        print('palyer has not slvaer',game.player)
        return 

    tar_sts = target_sts_dict[target_sts]

    mem_img_list = [r'F:\01_game_ctr\lib\mem_img\common\slaver_beidong.png',r'F:\01_game_ctr\lib\mem_img\common\slaver_gensui.png',
                    r'F:\01_game_ctr\lib\mem_img\common\slaver_zhudong.png',r'F:\01_game_ctr\lib\mem_img\common\slaver_tingzhi.png']
   
    slaver_img_pos1 = (190, 70)
    slaver_img_pos2 = (280, 100)
    val, loc, img_name = game.find_multi_img_with_mem(mem_img_list,part=1,pos1=slaver_img_pos1,\
                                                                pos2=slaver_img_pos2,image_show = False, gray=0)
    
    if val > 0.9:
        if img_name == 'slaver_beidong.png':
            cur_sts = 2
        if img_name == 'slaver_gensui.png':
            cur_sts = 3
        if img_name == 'slaver_zhudong.png':
            cur_sts = 1
        if img_name == 'slaver_tingzhi.png':
            cur_sts = 4

        if tar_sts >= cur_sts:
            key_press_cunt = tar_sts - cur_sts
        else:
            key_press_cunt = tar_sts - cur_sts + 4
        
        if key_press_cunt == 0:
            print('need not change slaver status',game.player)
        else:
            for i in range(key_press_cunt):
                print(i ,'press key [I]')
                game.press_single_key_in_background('i')
                time.sleep(0.32)
    else:
        print('not find slaver for yiren, then check LingShou status',game.player)
        lingshou_state = check_lingshou_exist(game)
        if lingshou_state == False:
            game.press_single_key_in_background('o')
            time.sleep(3) # 等待灵兽召唤 读条时间

        slaver_img_pos3 = (160, 135)
        slaver_img_pos4 = (220, 190)
        val, loc, img_name = game.find_multi_img_with_mem(mem_img_list,part=1,pos1=slaver_img_pos3,\
                                                                 pos2=slaver_img_pos4,image_show = False, gray=0)
        if val > 0.9:
            if img_name == 'slaver_beidong.png':
                cur_sts = 2
            if img_name == 'slaver_gensui.png':
                cur_sts = 3
            if img_name == 'slaver_zhudong.png':
                cur_sts = 1
            if img_name == 'slaver_tingzhi.png':
                cur_sts = 4

            if tar_sts >= cur_sts:
                key_press_cunt = tar_sts - cur_sts
            else:
                key_press_cunt = tar_sts - cur_sts + 4
            
            if key_press_cunt == 0:
                print('need not change LingShou status',game.player)
            else:
                for i in range(key_press_cunt):
                    print(i ,'press key [I] for LingShou')
                    game.press_single_key_in_background('i')
                    time.sleep(0.32)
        else:
            print('not find LingShou',game.player)


def check_lingshou_exist(game:GameControl):
    #game.activate_window()
    #time.sleep(0.5)

    lingshou_status_img_list = [r'F:\01_game_ctr\lib\mem_img\common\slaver_beidong.png',r'F:\01_game_ctr\lib\mem_img\common\slaver_gensui.png',
                                r'F:\01_game_ctr\lib\mem_img\common\slaver_zhudong.png',r'F:\01_game_ctr\lib\mem_img\common\slaver_tingzhi.png']
  
    lingshou_img_pos3 = (160, 135)
    lingshou_img_pos4 = (220, 190)
    val, loc, img_name = game.find_multi_img_with_mem(lingshou_status_img_list,part=1,pos1=lingshou_img_pos3,\
                                                                pos2=lingshou_img_pos4,image_show = False, gray=0)
    if val > 0.9:
        return True
    
    return False

def error_case_process(game:GameControl):
    #check error case
    maxVal, maxLox = game.find_img_with_mem(r"F:\01_game_ctr\lib\mem_img\common\error1.png")
    if maxVal > 0.7:
        print('esc')
        game.press_single_key_in_background('escape')

def click_dice_to_get_materiel(game:GameControl):

    roll_img_list = [r'F:\01_game_ctr\lib\img\common\roll.png',r'F:\01_game_ctr\lib\img\common\roll1.png']
    roll_loc, img_name = game.find_game_multi_img(roll_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)

    if roll_loc != False:
        #roll to get material
        game.press_single_key_in_background('u')
        game.roll_cunt = game.roll_cunt + 1
        if game.roll_cunt > 10:
            compound_equipment(game)
        time.sleep(0.1)

pickup_pre_pos = None
def auto_pick_up_money(game:GameControl):

    start_time = time.time()
    start_time_tmp = time.time()
    while True and time.time() - start_time < 45:
        game.activate_window()
        pick_flag = pick_up_money(game)
        if pick_flag:
            # pick successfully, update start_time_tmp
            start_time_tmp = time.time()

        if time.time() - start_time_tmp > 6:
            break

    global pickup_pre_pos
    pickup_pre_pos = None

def pick_up_money(game:GameControl):
    global pickup_pre_pos

    window_center_pos = (game.window_pos1[0]+519, game.window_pos1[1]+459) #(game.window_pos1[0]+784, game.window_pos1[1]+710)
    #r'F:\01_game_ctr\lib\img\common\zhuangbei_dao.png',
    if pickup_pre_pos == None:
        pickup_pre_pos = window_center_pos
    pickup_img_list = [r'F:\01_game_ctr\lib\img\common\yinliang.png',r'F:\01_game_ctr\lib\img\common\yinpiao.png']
    maxLoc, img_name = game.find_game_multi_img(pickup_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.65)
    if maxLoc != False:
        if maxLoc != pickup_pre_pos:
            pickup_pre_pos = maxLoc
            gui.moveTo(maxLoc)
            gui.leftClick()
            time_tmp = calculate_time_for_two_pointers(window_center_pos,maxLoc,3)
            time.sleep(time_tmp)
            return True
        else:
            pickup_pre_pos = ((maxLoc[0]+window_center_pos[0])//2,(maxLoc[1]+window_center_pos[1])//2)
            gui.moveTo(pickup_pre_pos)
            gui.leftClick()
            time_tmp = calculate_time_for_two_pointers(pickup_pre_pos,maxLoc,3)
            time.sleep(time_tmp)
    return False

def pick_up_equipment(game:GameControl):
    global pickup_pre_pos
    pickup_equipment_cunt = 0


    window_center_pos = (game.window_pos1[0]+519, game.window_pos1[1]+459) # (game.window_pos1[0]+784, game.window_pos1[1]+710)

    if pickup_pre_pos == None:
        pickup_pre_pos = window_center_pos
    pickup_img_list = [r'F:\01_game_ctr\lib\img\common\zhuangbei_deng.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_dao.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_fuchen.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_gong.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_huwan.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_huwan1.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_huwan2.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_ji.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_jiezi.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_jiezi1.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_jiezi2.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_jiezi3.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_maobi.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_maozi.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_maozi1.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_maozi2.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_qin.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_shoutao.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_shouzhuo.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_xianglian.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_xiezi.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_yaodai.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_yifu.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_yifu1.png',
                       r'F:\01_game_ctr\lib\img\common\zhuangbei_yifu2.png',r'F:\01_game_ctr\lib\img\common\zhuangbei_yifu3.png']
    maxVal, maxLoc = game.find_multi_img_parallel(pickup_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2)
    if maxVal > 0.65:
        if maxLoc != False:
            if maxLoc != pickup_pre_pos:
                pickup_equipment_cunt = pickup_equipment_cunt + 1
                pickup_pre_pos = maxLoc
                gui.moveTo(maxLoc)
                gui.leftClick()
                time_tmp = calculate_time_for_two_pointers(window_center_pos,maxLoc,3)
                time.sleep(time_tmp)
            else:
                pickup_pre_pos = ((maxLoc[0]+window_center_pos[0])//2,(maxLoc[1]+window_center_pos[1])//2)
                gui.moveTo(pickup_pre_pos)
                gui.leftClick()
                time_tmp = calculate_time_for_two_pointers(pickup_pre_pos,maxLoc,3)
                time.sleep(time_tmp)
    return pickup_equipment_cunt
'''
自动召唤初版功能，测试用途，可移除
def auto_summon_retinue_for_yiren(game:GameControl, bone_flag = False):
    summon_cunt = 0
    wood_img_list= [r'F:\01_game_ctr\lib\img\common\wood.png']

    game.activate_window()
    time.sleep(0.5)

    #move cursor to the center of the game window
    center_pos = (game.window_pos1[0]+784, game.window_pos1[1]+710)
    gui.moveTo(center_pos)

    game.press_combination_keys(['menu','q']) #switch gear set to first set
    time.sleep(0.1)

    while summon_cunt < 3:

        game.press_combination_keys(['control','2'])
        time.sleep(0.6)
        game.press_combination_keys(['control','3'])
        time.sleep(0.6)
        if bone_flag:
            maxLoc, img_name = game.find_game_multi_img(wood_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.65)  
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                gui.moveTo(center_pos)
            game.press_single_key_in_background('v')
            time.sleep(0.6)
            game.press_combination_keys(['control','1'])
            time.sleep(13)
        time.sleep(5)
        summon_cunt = summon_cunt + 1

    summon_cunt = 0
    game.press_combination_keys(['menu','t']) #switch gear set to JU HUN YIN set
    while True:
        game.press_combination_keys(['control','2'])
        time.sleep(0.6)
        game.press_single_key_in_background('v')
        time.sleep(0.6)
        game.press_combination_keys(['control','1'])
        summon_cunt = summon_cunt + 1
        if summon_cunt > 1:
            break
        time.sleep(20)

    
    if bone_flag == False: #not all BONE, need to summon WOOD once
        game.press_combination_keys(['control','2'])
        time.sleep(0.6)
    game.press_combination_keys(['menu','q']) #switch gear set to first set

def auto_summon_retinue_for_all_palyer(game_list:GameControl,bone=False):
    for game in game_list:
        if game.player_id in yiren_list:
           auto_summon_retinue_for_yiren(game, bone_flag=bone)
'''

def draw_in_window(pos1,pos2,circul_pos,radius = 30):
    left = min(pos1[0], pos2[0])
    top = min(pos1[1], pos2[1])
    right = max(pos1[0], pos2[0])
    bottom = max(pos1[1], pos2[1])

    width = right - left
    height = bottom - top

    screenshot = gui.screenshot(region=(left, top, width, height))
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    circul_pos = (circul_pos[0]-pos1[0],circul_pos[1]-pos1[1])

    cv2.circle(img, circul_pos, radius, (0, 0, 255), 2)
    
    # 等角度取圆上的四个点
    angles = np.linspace(0, 2*np.pi, 4)[:-1]  # 等角度划分为四个点
    points = []
    for angle in angles:
        # 计算圆上的点的坐标
        x_point = int(circul_pos[0] + radius * np.cos(angle))
        y_point = int(circul_pos[1] + radius * np.sin(angle))
        points.append((x_point, y_point))

    # 在图像上绘制点
    for point in points:
        cv2.circle(img, point, 4, (0, 255, 0), -1)

    # 显示图像
    cv2.imshow('Circle', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def yanzhengma_process(game:GameControl):

    game.activate_window()
    time.sleep(0.3)

    yanzhengma_list= [r'F:\01_game_ctr\lib\img\common\yanzhengma_click.png']
    maxLoc1, img_name1 = game.find_game_multi_img(yanzhengma_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.65)                                                
    if maxLoc1 != False:
        gui.moveTo(maxLoc1)
        gui.leftClick()
        print(maxLoc1)

        time.sleep(0.3)
        maxLoc2 = game.find_game_img(r'F:\01_game_ctr\lib\img\common\yanzhengma_table.png',\
                                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
                                                        
        if maxLoc2 != False:
            print(maxLoc2,'table')
            start_time = time.time()
            rec_update_cunt = 0
            while True and time.time() - start_time< 20:
                yanzhengma_slection_list= [r'F:\01_game_ctr\lib\img\common\yanzhengma_false.png',r'F:\01_game_ctr\lib\img\common\yanzhengma_baitian.png']
                maxLoc3, img_name3 = game.find_game_multi_img(yanzhengma_slection_list,part=1,pos1=game.window_pos1,\
                                                            pos2=game.window_pos2,thread=0.65)
                if maxLoc3 != False:
                    gui.moveTo(maxLoc3)
                    gui.leftClick()
                    time.sleep(0.3)
                    print('yanzhengma selsetion')
                    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\yanzhengma_submit.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
                    if maxLoc != False:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.3)
                        print('yanzhengma submit')
                        return True

                time.sleep(0.3)
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\yanzhengma_update.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
                if maxLoc != False:
                    rec_update_cunt = 0
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.3)
                    print('yanzhengma update')
                else:
                    rec_update_cunt = rec_update_cunt + 1
                
                if rec_update_cunt > 3:
                    break
    close_all_table(game)
    return False

def find_yanzhengma(game:GameControl,game_ctrl_list):
    game.activate_window()
    time.sleep(0.5)

    close_all_table(game)

    yanzhengma_pre_list = [r'F:\01_game_ctr\lib\img\common\yanzhengma_pre.png',r'F:\01_game_ctr\lib\img\common\yanzhengma_click.png']
    maxLoc, img_name = game.find_game_multi_img(yanzhengma_pre_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.65)

    result = False
    if maxLoc != False:
        if img_name == 'yanzhengma_click.png':
            result = yanzhengma_process(game)
            print('click yanzhengma entrance img!')

        if img_name == 'yanzhengma_pre.png':
            result_list = []
            print('find yanzhengma pre img, please check which player has yazhengma limitation!')
            for sub_game in game_ctrl_list:
                result = yanzhengma_process(sub_game)
                result_list.append(result)
            
            if True in result_list:
                result = True
            else:
                result = False
        game.activate_window()
        time.sleep(0.5)
        
    return result

# start ################ summon retinue #######################################

def target_function(game_player, player_queue, bone_flag):
    print(f"Processing task for game_player {game_player.player},{game_player.player_id}")
    # 假设这里是实际的任务处理
    wood_img_list= [r'F:\01_game_ctr\lib\img\common\wood.png']
    game_player.activate_window()
    time.sleep(0.3)
    #move cursor to the center of the game window
    #(519, 459)
    center_pos = (game_player.window_pos1[0]+519, game_player.window_pos1[1]+459)

    #center_pos = (game_player.window_pos1[0]+784, game_player.window_pos1[1]+710)

    game_player.press_combination_keys(['menu','t']) #switch gear set to JU HUN set

    if game_player.summon_current_count < 3:

        game_player.summon_wait_time = 17 # wait GU ROU JI cd

        game_player.press_combination_keys(['control','2'])
        time.sleep(0.2)
        game_player.press_combination_keys(['control','3'])
        time.sleep(0.2)
        maxLoc, img_name = game_player.find_game_multi_img(wood_img_list,part=1,pos1=game_player.window_pos1,\
                                            pos2=game_player.window_pos2,thread=0.85)  
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            gui.moveTo(center_pos)
            game_player.press_single_key_in_background('v')
            time.sleep(0.2)
            game_player.press_combination_keys(['control','1'])
    else:
        if bone_flag:

            game_player.summon_wait_time = 18 # wait GU ROU JI cd
            
            maxLoc, img_name = game_player.find_game_multi_img(wood_img_list,part=1,pos1=game_player.window_pos1,\
                                                pos2=game_player.window_pos2,thread=0.85)  
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                gui.moveTo(center_pos)
                game_player.press_single_key_in_background('v')
                time.sleep(0.2)
                game_player.press_combination_keys(['control','1'])
            else:
                game_player.press_combination_keys(['control','2'])
                time.sleep(0.2)
                gui.moveTo(center_pos)
                game_player.press_single_key_in_background('v')
                time.sleep(0.2)
                game_player.press_combination_keys(['control','1'])
        else:

            game_player.summon_wait_time = 6 # wait MU LING cd
            
            game_player.press_combination_keys(['control','2'])
            time.sleep(0.2)
            game_player.press_combination_keys(['control','3'])

    print(f"Processed task for game_player {game_player.player}")
    game_player.summon_current_count += 1
    if game_player.summon_current_count < game_player.summon_target_count:
        set_timer(game_player, game_player.summon_wait_time, player_queue)
    else:
        print(f"game_player {game_player.player}'s task is done.")
        game_player.press_combination_keys(['menu','q']) #switch gear set to first set
        time.sleep(1)
        lingshou_state = check_lingshou_exist(game_player)
        if lingshou_state == False:
            game_player.press_single_key_in_background('o')
            time.sleep(2) #等待灵兽召唤读条

        #同步一下灵兽和召唤兽的状态，按四下 ‘I’ 键
        for i in range(4):
            print(i ,'press key [I] for LingShou')
            game_player.press_single_key_in_background('i')
            time.sleep(0.22)

    player_queue.task_done()

def set_timer(game_player, interval, player_queue):
    game_player.summon_timer = threading.Timer(interval, lambda: timer_callback(game_player, player_queue))
    game_player.summon_timer.start()
    print(f"summon_timer started for game_player {game_player.player}")

def timer_callback(game_player, player_queue):
    print(f"summon_timer callback for game_player {game_player.player}")
    player_queue.put(game_player.player_id)

def summon_retinue(game:GameControl,game_ctrl_list,bone=False):

    cancel_followed_with_leftclcik(game)

    player_queue = queue.Queue()

    for game_player in game_ctrl_list:
        if game_player.player_id in only_lingshou_list:
            lingshou_state = check_lingshou_exist(game_player)
            if lingshou_state == False:
                game_player.press_single_key_in_background('o')
        if game_player.player_id in yiren_list:
            set_timer(game_player, game_player.summon_wait_time, player_queue)

    while True:
        try:
            player_id = player_queue.get(timeout=1)
            game_player = next((p for p in game_ctrl_list if p.player_id == player_id), None)
            if game_player:
                t = threading.Thread(target=target_function, args=(game_player, player_queue, bone))
                t.start()
                t.join()
        except queue.Empty:
            pass

        if all(game_player.summon_current_count >= game_player.summon_target_count for game_player in game_ctrl_list if game_player.player_id in yiren_list):
            print("All players task done. Ending the program.")
            break

    #召唤结束，清空召唤次数
    for game_player in game_ctrl_list:
        if game_player.player_id in yiren_list:
            game_player.summon_current_count = 0

# end ################ summon retinue #######################################
        



# start ################ 装备合成 #######################################
def switch_to_package_one(game:GameControl):
    package_one_img_list = [r'F:\01_game_ctr\lib\img\common\baoguo_packageOne1.png',
                            r'F:\01_game_ctr\lib\img\common\baoguo_packageOne2.png']
    maxLoc, img_name = game.find_game_multi_img(package_one_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.65,image_show=False)
    if maxLoc != False:
        print('switch to package one')
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.1)


# generate the coordinates of the package 
# 游戏窗口分表率 1024*768
# line(1，6）代表 第1 到 第6 行
def get_package_line_coordinate(x,y,line):
	start_x = x - 420
	start_y = y - 370
	step = 60
	table = []
	for i in range(6):
		row = []
		for j in range(8):
			row.append((start_x + step*j, start_y + step*i))
		table.append(row)
		
	return table[line-1]


def get_package_coordinate(game:GameControl):
    zheng_img_list = [r'F:\01_game_ctr\lib\img\common\bag_zhengli.png']
    maxLoc, img_name = game.find_game_multi_img(zheng_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.65,image_show=False)
    if maxLoc != False:
        zheng_coor = (maxLoc[0],maxLoc[1])
        qiankundai_coor = (zheng_coor[0]-240,zheng_coor[1])
        gui.moveTo(qiankundai_coor)
        gui.leftClick()
        time.sleep(0.2)
        #after reset the QIAN KUN DAI window, recognize the posisiton again to get coordinate
        maxLoc, img_name = game.find_game_multi_img(zheng_img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.65,image_show=False)

        if maxLoc != False:
            zheng_coor = (maxLoc[0],maxLoc[1])
            qiankundai_coor = (zheng_coor[0]-240,zheng_coor[1])
            #row_list = get_package_line_coordinate(zheng_coor[0],zheng_coor[1],5) # 倒数第二行包裹的坐标list
            return zheng_coor,qiankundai_coor
        
    return False,False

def compound_equipment(game:GameControl):
    game.activate_window()
    time.sleep(0.3)

    #只要 compound_equipment 被调用 则清除累计投点次数
    game.roll_cunt = 0

    close_all_table(game)
    time.sleep(1)
    #open package
    game.press_single_key_in_background('b')
    time.sleep(0.7)   
    #recognize the picture 'Zheng' (整)

    switch_to_package_one(game)

    zheng_coor, qian_coor = get_package_coordinate(game)
    package_loc_list = []

    if zheng_coor != False and qian_coor != False :
        #切换到幸运套
        game.press_combination_keys(['menu','w'])

        row_4_list = get_package_line_coordinate(zheng_coor[0],zheng_coor[1],4)
        row_5_list = get_package_line_coordinate(zheng_coor[0],zheng_coor[1],5)
        row_6_list = get_package_line_coordinate(zheng_coor[0],zheng_coor[1],6)
        package_loc_list = row_4_list + row_5_list + row_6_list

        while True:
            package_null_cunt = 0
            package_equip_cunt = 0

            #点击 整 图标
            gui.moveTo(zheng_coor)
            gui.leftClick()
            time.sleep(0.3)

            #点击每个包裹
            for package_loc in package_loc_list:
                gui.moveTo(package_loc)
                time.sleep(0.3)
                equip_info_img_list = [r'F:\01_game_ctr\lib\img\common\equipment_bangding.png',
                                       r'F:\01_game_ctr\lib\img\common\equipment_bangding1.png',
                                       r'F:\01_game_ctr\lib\img\common\equipment_guizhong.png',]
                equip_rec_pos1 = (package_loc[0]-430,game.window_pos1[1])
                if package_loc[0]+430 < game.window_pos2[0]:
                    equip_rec_pos2 = (package_loc[0]+430,game.window_pos2[1])
                else:
                    equip_rec_pos2 = (game.window_pos2[0],game.window_pos2[1])
                maxLoc, img_name = game.find_game_multi_img(equip_info_img_list,part=1,pos1=equip_rec_pos1,\
                                            pos2=equip_rec_pos2,thread=0.65,image_show=False)
                if maxLoc != False:
                    print('equipment is BangDing or GuiZhong! skip this loc!')
                    #time.sleep(1)
                    continue
                else:
                    equip_exist_img_list = [r'F:\01_game_ctr\lib\img\common\equipment_exist.png']
                    maxLoc, img_name = game.find_game_multi_img(equip_exist_img_list,part=1,pos1=equip_rec_pos1,\
                                                pos2=equip_rec_pos2,thread=0.65,image_show=False)
                    if maxLoc != False:
                        package_null_cunt = 0
                        gui.rightClick()
                        #time.sleep(1)
                        package_equip_cunt = package_equip_cunt + 1
                    else:
                        package_null_cunt = package_null_cunt + 1
                        #time.sleep(1)

                if package_null_cunt > 3 or package_equip_cunt > 8:
                    # break for package_loc in package_loc_list:
                    break

            click_dice_to_get_materiel(game)

            if package_null_cunt > 3 and package_equip_cunt < 5:
                # break while True:
                break

            #点完装备之后，调整下鼠标位置
            gui.moveTo(zheng_coor)
            time.sleep(0.1)

            if package_equip_cunt > 4:
                #识别乾坤袋 转换 按钮， 并点击
                zhuanghua_img_list = [r'F:\01_game_ctr\lib\img\common\qiankundai_zhuanhua.png']
                maxLoc, img_name = game.find_game_multi_img(zhuanghua_img_list,part=1,pos1=game.window_pos1,\
                                                            pos2=game.window_pos2,thread=0.65,image_show=False)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.3)

                    #输入两次回车
                    game.press_single_key_in_background('return')
                    time.sleep(0.2)
                    game.press_single_key_in_background('return')

            time.sleep(0.5)
            #合成之后，将乾坤袋的东西先放回包裹
            zhuanghua_img_list = [r'F:\01_game_ctr\lib\img\common\back_to_package.png']
            maxLoc, img_name = game.find_game_multi_img(zhuanghua_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.75,image_show=False)
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.3)

        #整理下包裹 以及撤销因为两次回车 而弹出的聊天输入框
        gui.moveTo(zheng_coor)
        gui.leftClick()
        time.sleep(0.05)

        #切换到输出套
        game.press_combination_keys(['menu','w'])

    #操作结束，关闭当前所有界面
    game.press_single_key_in_background('escape')
    time.sleep(0.3)
    game.press_single_key_in_background('escape')

    pass



# end ################ 装备合成 #######################################


# start ################ 隐藏其他玩家 #######################################
def hide_others(game:GameControl):
    game.activate_window()
    time.sleep(0.2)
    game.press_combination_keys(['control','f10'])
    time.sleep(0.1)
    game.press_combination_keys(['control','f11'])

def hide_others_for_all_player(game_ctrl_list):
    for sub_game in game_ctrl_list:
        hide_others(sub_game)
# end ################ 隐藏其他玩家 #######################################
        

# start ################ 自动签到 #######################################
def auto_sign(game:GameControl):
    game.activate_window()
    time.sleep(0.3)
    close_all_table(game)

    auto_sign_window_flag = False

    # 登录时，发现签到图标
    find_sign_cunt = 0
    while find_sign_cunt < 5:
        game.press_single_key_in_background('escape')
        time.sleep(1)

        auto_sign_img_list = [r'F:\01_game_ctr\lib\img\common\qiandao_entrance.png',
                              r'F:\01_game_ctr\lib\img\common\qiandao_entrance1.png',
                              r'F:\01_game_ctr\lib\img\common\qiandao_get.png']
        maxLoc, img_name = game.find_game_multi_img(auto_sign_img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.75,image_show=False)

        if img_name == 'qiandao_get.png':
            auto_sign_window_flag = True
        
        if img_name == 'qiandao_entrance.png' or img_name == 'qiandao_entrance1.png':
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.1)
                auto_sign_window_flag = True
                print('enter into auto sign window!')
                break

        find_sign_cunt = find_sign_cunt + 1

    if auto_sign_window_flag:
        # 登录时，发现签到图标
        find_sign_cunt = 0
        while find_sign_cunt < 5:
            auto_sign_img_list = [r'F:\01_game_ctr\lib\img\common\qiandao_get.png']
            maxLoc, img_name = game.find_game_multi_img(auto_sign_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.68,image_show=False)

            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.1)
                print('auto sign!')
                break

            find_sign_cunt = find_sign_cunt + 1

    game.press_single_key_in_background('escape')
    # 若不是从 qiandao_entrance.png 进入签到界面，则这个操作可关闭 窗口右边的登录签到提示
    close_sign_img_list = [r'F:\01_game_ctr\lib\img\common\qiandao_get.png']
    maxLoc, img_name = game.find_game_multi_img(close_sign_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.75,image_show=False)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.1)


def auto_sign_for_all_player(game_ctrl_list):
    for sub_game in game_ctrl_list:
        auto_sign(sub_game)
# end ################ 自动签到 #######################################
        
# start ################ 自动邀请队员 #######################################
def check_team_is_full(game:GameControl):
    img_list= [r'F:\01_game_ctr\lib\img\common\team_full_check.png']
    maxLoc, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.75,image_show=False)  
    if maxLoc != False:
        memeber_check_pos1 = (maxLoc[0]-150,maxLoc[1])
        memeber_check_pos2 = (maxLoc[0],maxLoc[1]+400)
        img_list= [r'F:\01_game_ctr\lib\img\common\team_member_tag.png']
        maxLoc1, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=memeber_check_pos1,\
                                                    pos2=memeber_check_pos2,thread=0.75,image_show=False)
        if maxLoc1 != False:
            return True
    
    return False

#创建队伍
def create_team(game:GameControl):
    game.activate_window()
    time.sleep(0.3)

    #打开队伍界面
    game.press_single_key_in_background('m')

    time.sleep(0.5)

    img_list= [r'F:\01_game_ctr\lib\img\common\team_create.png',
               r'F:\01_game_ctr\lib\img\common\team_invite_entrance.png']
    maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.70,image_show=False)  
    if maxLoc != False:
        if img_name == 'team_invite_entrance.png':
            print('team has been created!')
            return True
        if img_name == 'team_create.png':
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.1)
            print('creat team!')
            #这个函数结束保持在队伍界面
            game.press_single_key_in_background('m')
            return True
    
    print('error, not find team realted image!!!')
    return False

def check_is_team_window(game:GameControl):
    game.activate_window()
    time.sleep(0.3)

    retry_cunt = 0
    while True:
        img_list= [r'F:\01_game_ctr\lib\img\common\team_invite_entrance.png']
        maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.75,image_show=False)  
        if maxLoc != False:
            print('has been in team window')
            return True,maxLoc
        else:
            retry_cunt = retry_cunt + 1
            time.sleep(0.2)
            game.press_single_key_in_background('m')
            time.sleep(0.5)

        if retry_cunt > 3:
            print('retry 3 times, not find team window!!!')
            return False,False
#邀请队员
def invite_member(game:GameControl):
    game.activate_window()
    time.sleep(0.2)

    close_all_table(game)

    create_team(game)

    team_window_flag,invite_loc = check_is_team_window(game)
    if team_window_flag:
        team_full_flag = check_team_is_full(game)
        if False == team_full_flag:
            gui.moveTo(invite_loc)
            gui.leftClick()
            time.sleep(0.2)
            # '好友' 列表
            img_list= [r'F:\01_game_ctr\lib\img\common\team_invite_pre1.png']
            maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                            pos2=game.window_pos2,thread=0.75,image_show=False)
            if maxLoc:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
                #'好友列表二 -- 全选'
                img_list= [r'F:\01_game_ctr\lib\img\common\team_invite_selectall.png']
                maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                                pos2=game.window_pos2,thread=0.75,image_show=False)
                if maxLoc:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                    #'好友列表二 -- 邀请'
                    img_list= [r'F:\01_game_ctr\lib\img\common\team_invite.png']
                    maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                                    pos2=game.window_pos2,thread=0.75,image_show=False)
                    if maxLoc:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
                        return True
                else:
                    #'好友列表二'
                    img_list= [r'F:\01_game_ctr\lib\img\common\team_invite_pre2.png']
                    maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                                    pos2=game.window_pos2,thread=0.75,image_show=False)
                    if maxLoc:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.5)
                        #'好友列表二 -- 全选'
                        img_list= [r'F:\01_game_ctr\lib\img\common\team_invite_selectall.png']
                        maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                                        pos2=game.window_pos2,thread=0.75,image_show=False)
                        if maxLoc:
                            gui.moveTo(maxLoc)
                            gui.leftClick()
                            time.sleep(0.2)
                            #'好友列表二 -- 邀请'
                            img_list= [r'F:\01_game_ctr\lib\img\common\team_invite.png']
                            maxLoc, img_name = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                                            pos2=game.window_pos2,thread=0.75,image_show=False)
                            if maxLoc:
                                gui.moveTo(maxLoc)
                                gui.leftClick()
                                time.sleep(0.2)
                                return True
        else:
            print('team is full, need not invite memeber!')
            return True
    return False
    pass

#队员同意邀请
def confirm_invite(game:GameControl):
    game.activate_window()
    time.sleep(0.3)

    tmp_flag = confirm(game)
    if tmp_flag:
        game.press_single_key_in_background('p')
    pass

#重新检查队员是否入队，如果队伍不满，重新在邀请下
def check_and_retry_invite_memeber(game:GameControl,game_ctrl_list):
    game.activate_window()
    time.sleep(0.3)

    team_window_flag,invite_loc = check_is_team_window(game)

    if team_window_flag:
        tmp_team_full_flag = check_team_is_full(game)

        if tmp_team_full_flag:
            return True
        else:
            invite_member(game)
            for sub_game in game_ctrl_list:
                if sub_game.player_id != game.player_id:
                    confirm_invite(sub_game)

# end ################ 自动邀请队员 #######################################

# start ################ 放置窗口 #######################################
def place_all_windows(game_list):
    # 窗口大小
    window_width = 1560
    window_height = 1211

    # 显示器分辨率
    screen_width = 2560
    screen_height = 1392

    # 前四个窗口右下斜45度间距
    spacing = (screen_height - window_height) // 3

    # 设置前四个窗口的位置
    for i, sub_game in enumerate(game_list[:4]):
        x = i * spacing
        y = i * spacing
        win32gui.SetWindowPos(sub_game.hwnd, win32con.HWND_TOP, x, y, window_width, window_height, 0)

    # 设置后两个窗口的位置
    for i, sub_game in enumerate(game_list[-2:]):
        if i == 0:  # 最后一个窗口
            x = screen_width - window_width
            y = 0
        else:  # 倒数第二个窗口
            x = screen_width - window_width - spacing
            y = spacing
        win32gui.SetWindowPos(sub_game.hwnd, win32con.HWND_TOP, x, y, window_width, window_height, 0)
# end ################ 放置窗口 #######################################

# start ################ 初始自动操作 #######################################
def auto_fengtian_dailytask_click(game:GameControl):
    img_list= [r'F:\01_game_ctr\lib\img\common\fengtian_entrance.png']
    maxLoc, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.75,image_show=False)  
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.3)

        img_list= [r'F:\01_game_ctr\lib\img\common\fengtian_dailytask.png']
        maxLoc, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.75,image_show=False)  
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.1)
            game.press_single_key_in_background('escape')

def auto_operation_at_init(game:GameControl,game_list):
    close_info_table_for_all(game,game_list)
    invite_member(game)

    for sub_game in game_list:
        if sub_game.player_id != game.player_id:
            confirm_invite(sub_game)
        auto_sign(sub_game)
        auto_fengtian_dailytask_click(sub_game)
        hide_others(sub_game)
    place_all_windows(game_list)

    #组队再检查并尝试下
    check_and_retry_invite_memeber(game,game_list)

# end ################ 初始自动操作 #######################################
    
def close_info_table(game:GameControl):
    game.activate_window()
    time.sleep(0.3)
    info_img_list = [r'F:\01_game_ctr\lib\img\common\info_table_close.png']
    maxLoc, img_name = game.find_game_multi_img(info_img_list,part=1,\
                                    pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.1)

def close_info_table_for_all(game:GameControl,game_list):
    game.activate_window()
    time.sleep(0.3)
    info_img_list = [r'F:\01_game_ctr\lib\img\common\info_table_close.png']
    maxLoc, img_name = game.find_game_multi_img(info_img_list,part=1,\
                                    pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        for sub_game in game_list:
            close_info_table(sub_game)


# start ################ 倩女精灵 #######################################

def search_target_loc_by_qiannvjingling(game:GameControl, search_str:str, img_path_list):

    #打开倩女精灵
    game.press_single_key('j')
    time.sleep(0.3)

    input_content(game,search_str)
    send_img_list = [r'F:\01_game_ctr\lib\img\common\jingling_send.png']
    maxLoc, img_name = game.find_game_multi_img(send_img_list,part=1,\
                                    pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.5)

        maxLoc, img_name = game.find_game_multi_img(img_path_list,part=1,\
                                pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.1)

            return True
    return False

# end ################ 倩女精灵 #######################################