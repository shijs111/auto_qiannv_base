from src.common_operation import *


shouwei_location_list = [
    [r'F:\01_game_ctr\lib\img\zhanlong\shouwei_yaofang.png',   26],
    [r'F:\01_game_ctr\lib\img\zhanlong\shouwei_jinku.png' ,    16],
    [r'F:\01_game_ctr\lib\img\zhanlong\shouwei_zhongyang.png', 22],
    [r'F:\01_game_ctr\lib\img\zhanlong\shouwei_cangku.png',    15],
    [r'F:\01_game_ctr\lib\img\zhanlong\shouwei_fangwu.png',    20]
]

def submit_zhanlong_task(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\zhanlong_task_submit.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)

    if maxLoc != False:
        print('task complete!')
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.2)
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\complete_task.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.68)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.5)
            return True
    return False

def get_zhanlong_task(game:GameControl):
    print('get zhanlong task')
    time_start = time.time()
    retry_cnt = 0
    while True and time.time() - time_start < 60:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\accept_task.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,image_show=False,thread=0.62) 
        if maxLoc != False:
            print('find accept task directly')
            break
  
        tmp_flag = find_npc_by_search(game,r'F:\01_game_ctr\lib\img\zhanlong\npc_banghui_daiyunfei.png','dlf')
        time.sleep(0.5)
        if tmp_flag:
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\zhanlong_get_task_pre.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,image_show=False,thread=0.70)
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.5)
            else:
                print('not find [get_task_pre] pict')
                retry_cnt += 1
        else:
            print('not serach zhanlong npc')
            retry_cnt += 1     

        if  retry_cnt > 5:
            break 
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\accept_task.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
    if  False != maxLoc:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.5)
        print('get zhanlong task successfully')
        return True
    else:
        print('get zhanlong task failed')
        return False
def go_to_target_guild(game:GameControl):

    print('go to target guild')

    maxLoc =  game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\zhanglong_goto_target_pre.png',\
                                 part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if  False != maxLoc:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.5)
        maxLoc =  game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\zhanlong_target_guild.png',\
                                     part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)  
        if  False != maxLoc:
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.5)
            return True

    return False

def back_to_daiyunfei_npc(game:GameControl):
    game.press_single_key_in_background('f10')
    time.sleep(0.5)

    hangzhou_img_list = [r'F:\01_game_ctr\lib\img\zhanlong\zhanlong_hangzhou_map1.png']
    maxLoc = game.wait_game_multi_img(hangzhou_img_list,part=1,\
                                      pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=20)
    if maxLoc!= False:
        game.press_single_key_in_background('k')
        time.sleep(3)
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\back_to_dai.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)

        if maxLoc != False:
            print('back to daiyunfei!')
            gui.moveTo(maxLoc)
            print('move')
            gui.leftClick()
            print('click')
            time.sleep(0.5)
            return True
    return False

def wait_to_daiyunfei_npc(game:GameControl):

    time.sleep(7)
    close_all_table(game)

    print('waiting daiyunfei')
    maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\zhanlong\daiyunfei_task_table.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)

    if maxLoc != False:
        print('daiyunfei task table!')
        return True
    return False

def task_qingbaopu(game:GameControl):
    # open task table, check whether qingbaopu_zhongyangdating exists
    game.press_single_key_in_background('k')
    time.sleep(0.4)

    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\qingbaopu_zhongyangdating.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        location_offest = 51
    else:
        location_offest = 34
    #close task table
    game.press_single_key_in_background('k')
    time.sleep(0.4)
    
    qingbaopu_location_list = []
    qingbao_task_list = [r'F:\01_game_ctr\lib\img\zhanlong\qingbao_task1.png',
                         r'F:\01_game_ctr\lib\img\zhanlong\qingbao_task.png']
    maxLoc, img_name = game.find_game_multi_img(qingbao_task_list,\
                             part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
    if maxLoc != False:
        qingbaopu_location1 = (maxLoc[0],maxLoc[1]+17)
        qingbaopu_location_list.append(qingbaopu_location1)
        qingbaopu_location2 = (maxLoc[0],maxLoc[1]+location_offest)
        qingbaopu_location_list.append(qingbaopu_location2)

    for location in qingbaopu_location_list:
        retry_count = 0
        while retry_count < 1:
            gui.moveTo(location)
            gui.leftClick()
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\zhanlong\qingbao_do.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=40)
            if maxLoc != False:
                print('click qingbao_do!')
                gui.moveTo(maxLoc)
                gui.rightClick()
                time.sleep(2)
                break
            else:
                retry_count += 1
    qingbaopu_complete_list = [r'F:\01_game_ctr\lib\img\zhanlong\qingbao_complete.png',
                               r'F:\01_game_ctr\lib\img\zhanlong\qingbao_complete1.png']
    maxLoc, img_name = game.find_game_multi_img(qingbaopu_complete_list,\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    time.sleep(0.5)
    if maxLoc != False:
        print('qingbao task complete')
        return True
    return False

def task_shouwei(game:GameControl,location_list) :
    print('task_shouwei')
    shouwei_complete_img_list = [r'F:\01_game_ctr\lib\img\zhanlong\shouwei_complete.png',
                                 r'F:\01_game_ctr\lib\img\zhanlong\shouwei_complete1.png',
                                 r'F:\01_game_ctr\lib\img\zhanlong\shouwei_complete2.png',
                                 r'F:\01_game_ctr\lib\img\zhanlong\shouwei_complete3.png']

    for location_sub_list in location_list:
        map_sts = open_map(game,r'F:\01_game_ctr\lib\img\zhanlong\zhanlong_map.png')
        time.sleep(0.5)
        maxLoc = game.find_game_img(location_sub_list[0],\
                          part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            print('click')
            time.sleep(0.1)
            if map_sts:
                game.press_single_key_in_background('r') # close map
            tmp_time_cunt = 0
            while tmp_time_cunt < location_sub_list[1]:
                if tmp_time_cunt > 10:
                    maxLoc, img_name = game.find_game_multi_img(shouwei_complete_img_list,\
                                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                    if maxLoc != False:
                        print('shou wei ling complete!')
                        return True
                time.sleep(0.5)
                tmp_time_cunt = tmp_time_cunt + 1
                print('waiting....',tmp_time_cunt)
    
    return False

def task_bangzhu(game:GameControl):
    print('task_bangzhu')
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\clear_msg_window.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        print('clear banghui message')
        #get bangzhu task pre location
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_task.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            print('click bangzhu task pre location')
            time.sleep(0.5)
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_do.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
            if maxLoc != False:
                gui.moveTo(maxLoc)
                gui.rightClick()
                time.sleep(0.5)
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_location.png',\
                                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.5)

                    tmp_time_cunt = 0
                    tmp_recognize_cunt = 0
                    while tmp_recognize_cunt < 10:
                        if tmp_time_cunt > 11:
                            tmp_time_cunt = 0
                            # 36s之后尝试攻击一下
                            if tmp_recognize_cunt > 2:
                                game.press_single_key_in_background('tab')
                                time.sleep(0.1)
                                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_monster.png',\
                                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                                #有怪的话，攻击3s
                                if maxLoc != False:
                                    start_time = time.time()
                                    while time.time() - start_time < 3:
                                        print('attack bangzhu!')
                                        game.press_single_key_in_background('f4')
                                        time.sleep(0.5)
                                        game.press_single_key_in_background('1')
                                        time.sleep(0.5)
                                        tmp_time_cunt = tmp_time_cunt + 1

                            bangzhu_complete_list = [r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_complete.png',
                                                     r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_complete1.png',
                                                     r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_complete2.png']
                            maxLoc, img_name = game.find_game_multi_img(bangzhu_complete_list,part=1,\
                                                            pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                            if maxLoc != False:
                                print('bangzhu task complete!')
                                return True
                            
                            tmp_recognize_cunt = tmp_recognize_cunt + 1
                        time.sleep(0.5)
                        tmp_time_cunt = tmp_time_cunt + 1
                        print('waiting....',tmp_time_cunt)
        return False
    
def task_zijin(game:GameControl):
    print('task_zijin')
    zijin_task_list = [r'F:\01_game_ctr\lib\img\zhanlong\zijin_task.png',
                       r'F:\01_game_ctr\lib\img\zhanlong\zijin_task1.png',
                       r'F:\01_game_ctr\lib\img\zhanlong\zijin_task2.png']
    maxLoc, img_name = game.find_game_multi_img(zijin_task_list,part=1,\
                                pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        print('zijin task location click')
        
        maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\zhanlong\zijin_do.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.rightClick()
            time.sleep(6)

            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\zijin_complete.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
            if maxLoc!= False:
                print('zijin task complete')
                return True
    return False

def task_zhanlong_do(game:GameControl):
    zhanlong_task_list = [r'F:\01_game_ctr\lib\img\zhanlong\zijin_task.png',r'F:\01_game_ctr\lib\img\zhanlong\zijin_task1.png',r'F:\01_game_ctr\lib\img\zhanlong\zijin_task2.png',
                          r'F:\01_game_ctr\lib\img\zhanlong\shouwei_task.png',r'F:\01_game_ctr\lib\img\zhanlong\shouwei_task1.png',
                          r'F:\01_game_ctr\lib\img\zhanlong\qingbao_task.png',
                          r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_task.png',r'F:\01_game_ctr\lib\img\zhanlong\bangzhu_task1.png']

    task_status = False
    maxVal,maxLoc,image_name= game.find_multi_img(zhanlong_task_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=1)
    print('task_zhanlong_do:',maxVal,maxLoc,image_name)
    if maxLoc != False:
        print('zhanlong image:',image_name)
        #image_name = image_name.strip()
        if image_name == 'zijin_task.png' or image_name == 'zijin_task1.png'or image_name == 'zijin_task2.png':
            task_status = task_zijin(game)
        if image_name == 'shouwei_task.png' or image_name == 'shouwei_task1.png':
            task_status = task_shouwei(game,shouwei_location_list)
        if image_name == 'qingbao_task.png':
            task_status = task_qingbaopu(game)
        if image_name == 'bangzhu_task.png'or image_name == 'bangzhu_task1.png':
            task_status = task_bangzhu(game)     

    return task_status

def zhanlong_init_operation(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\clear_msg_window.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,image_show=False)
    if maxLoc != False:
        msg_window_img_pos1 = (maxLoc[0]-120,maxLoc[1]-50)
        msg_window_img_pos2 = (maxLoc[0]+320,maxLoc[1])
        img_list= [r'F:\01_game_ctr\lib\img\zhanlong\banghui_msg_window.png',
                   r'F:\01_game_ctr\lib\img\zhanlong\banghui_msg_window1.png']
        maxLoc1, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=msg_window_img_pos1,\
                                                    pos2=msg_window_img_pos2,thread=0.75,image_show=False)
        if maxLoc1 != False:
            gui.moveTo(maxLoc1)
            gui.leftClick()

def zhanlong_main(game:GameControl):
    '''
    0.角色需要处于战龙堂NPC跟前，再执行此脚本
    1.游戏窗口分辨率设置为1024*768
    2.消息窗口处于游戏窗口左下角，消息窗口切换到帮会消息界面
    3.地图界面 全部框 取消勾选
    4.宝宝 设置为 主动
    5.任务快捷键 设置为 'K'
    6.游戏视角 设置为 2.5D
    7.帮会飞行器放在 'f10'
    '''
    zhanlong_task_counter = 0

    zhanlong_init_operation(game)

    while zhanlong_task_counter< 10:

        #get task
        tmp_flag = get_zhanlong_task(game)
        if tmp_flag == False:
            print('get zhanlong task failed')
            break
        #go to target guild
        tmp_flag = go_to_target_guild(game)
        if tmp_flag == False:
            print('go to target guild failed')
            break
        
        time.sleep(0.5)
        #close all sub window
        close_all_table(game)

        #do task
        task_sts = task_zhanlong_do(game)
        if task_sts == False:
            print('zhanlong task failed')
            break

        #back to daiyunfei
        tmp_flag = back_to_daiyunfei_npc(game)   
        if tmp_flag == False:
            print('back to daiyunfei failed')
            break

        #wait daiyunfei task table
        tmp_flag = wait_to_daiyunfei_npc(game)
        if tmp_flag == False:
            print('wait daiyunfei timeout')
            break

        #submit task
        tmp_flag = submit_zhanlong_task(game)
        if tmp_flag == False:
            print('submit zhanlong task failde')
            break
    
        zhanlong_task_counter += 1