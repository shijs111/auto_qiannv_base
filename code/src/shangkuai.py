from http.client import CONFLICT
from src.common_operation import *

road1_map_img_list = [  r'F:\01_game_ctr\lib\img\shangkuai\map_banghui.png',
                        r'F:\01_game_ctr\lib\img\shangkuai\map_hangzhou.png',
                        r'F:\01_game_ctr\lib\img\shangkuai\map_yangjiazhen.png',
                        r'F:\01_game_ctr\lib\img\shangkuai\map_zhenjiaohuangye.png',
                        r'F:\01_game_ctr\lib\img\shangkuai\map_sichougulu.png',
                        r'F:\01_game_ctr\lib\img\shangkuai\road1_map_loc2.png',
                        r'F:\01_game_ctr\lib\img\shangkuai\road1_map_loc3.png']
road1_npc_loc_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_npc1_loc.png',
                      r'F:\01_game_ctr\lib\img\shangkuai\road1_npc2_loc.png',
                      r'F:\01_game_ctr\lib\img\shangkuai\road1_npc3_loc.png',
                      r'F:\01_game_ctr\lib\img\shangkuai\road1_complete.png']              
road1_npc_task_table_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_huifang_task_table.png',
                             r'F:\01_game_ctr\lib\img\shangkuai\road1_kunlunhuoshang_task_table.png',
                             r'F:\01_game_ctr\lib\img\shangkuai\road1_buluwo_task_table.png',
                             r'F:\01_game_ctr\lib\img\shangkuai\lieyun_task_table.png']
road1_npc_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_npc_huifang.png',
                  r'F:\01_game_ctr\lib\img\shangkuai\road1_npc_kunlunhuoshang.png',
                  r'F:\01_game_ctr\lib\img\shangkuai\road1_npc_buluwo.png',
                  r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png']
road1_npc_str_list = ['hf','klhs','blw','ley']

road2_map_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\map_banghui.png',
                          r'F:\01_game_ctr\lib\img\shangkuai\map_hangzhou.png',
                          r'F:\01_game_ctr\lib\img\shangkuai\road2_map_loc1.png',
                          r'F:\01_game_ctr\lib\img\shangkuai\road2_map_loc2.png',
                          r'F:\01_game_ctr\lib\img\shangkuai\road1_map_loc3.png', # 阿格拉地图
                          r'F:\01_game_ctr\lib\img\shangkuai\road2_map_loc3.png']
road2_npc_loc_list = [r'F:\01_game_ctr\lib\img\shangkuai\road2_npc1_loc.png',
                      r'F:\01_game_ctr\lib\img\shangkuai\road2_npc2_loc.png',
                      r'F:\01_game_ctr\lib\img\shangkuai\road2_npc3_loc.png',
                      r'F:\01_game_ctr\lib\img\shangkuai\road2_complete.png']
road2_npc_task_table_list = [r'F:\01_game_ctr\lib\img\shangkuai\road2_xumangshan_task_table.png',
                             r'F:\01_game_ctr\lib\img\shangkuai\road2_xianshanshangren_task_table.png',
                             r'F:\01_game_ctr\lib\img\shangkuai\road2_kunlunshangren_task_table.png',
                             r'F:\01_game_ctr\lib\img\shangkuai\lieyun_task_table.png']
road2_npc_list = [r'F:\01_game_ctr\lib\img\shangkuai\road2_npc_xumangshan.png',
                  r'F:\01_game_ctr\lib\img\shangkuai\road2_npc_xianshanshangren.png',
                  r'F:\01_game_ctr\lib\img\shangkuai\road2_npc_kunlunshangren.png',
                  r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png']
road2_npc_str_list = ['xws','xssr','klsr','ley']

def determin_shangkuai_timer(game:GameControl):
    shangkuai_road_img_lsit = [r'F:\01_game_ctr\lib\img\shangkuai\road1_npc1_loc.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\road2_npc1_loc.png']
    maxLoc,img_name = game.find_game_multi_img(shangkuai_road_img_lsit,\
                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        if img_name == 'road1_npc1_loc.png':
            game.shangkuai_road = 1
        if img_name == 'road2_npc1_loc.png':
            game.shangkuai_road = 2

    task_complete_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_complete.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\road2_complete.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\complete_retry.png']
    maxLoc,img_name = game.find_game_multi_img(task_complete_img_list,\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.2)
        if img_name == 'road1_complete.png':
            game.shangkuai_time = 120
        if img_name == 'road2_complete.png':
            game.shangkuai_time = 170
        if img_name == 'complete_retry.png':
            game.shangkuai_time = 40
    else:
        game.shangkuai_npc_num = 0
        if game.shangkuai_road == 1: #镇郊荒野 路
            maxLoc,img_name = game.find_game_multi_img(road1_map_img_list,\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                if img_name == 'map_banghui.png':
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 200
                if img_name == 'map_hangzhou.png':
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 160
                if img_name == 'map_yangjiazhen.png':
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 130
                if img_name == 'map_zhenjiaohuangye.png': # zhenjiaohuangye
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 100
                if img_name == 'map_sichougulu.png':
                    game.shangkuai_npc_num = 2
                    game.shangkuai_time = 150
                if img_name == 'road1_map_loc2.png': # kunlunhuangmo
                    game.shangkuai_npc_num = 2
                    game.shangkuai_time = 40
                if img_name == 'road1_map_loc2.png': # agela
                    game.shangkuai_npc_num = 3
                    game.shangkuai_time = 30
            
            if game.shangkuai_npc_num != 0:
                maxLoc = game.find_game_img( road1_npc_loc_list[game.shangkuai_npc_num-1],\
                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
        
        if game.shangkuai_road == 2: #台州海岸 路
            maxLoc,img_name = game.find_game_multi_img(road2_map_img_list,\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                if img_name == 'map_banghui.png':
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 200
                if img_name == 'map_hangzhou.png':
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 150
                if img_name == 'road2_map_loc1.png': # taizhouhaian
                    game.shangkuai_npc_num = 1
                    game.shangkuai_time = 80
                if img_name == 'road2_map_loc2.png': # tianmuxianshan
                    game.shangkuai_npc_num = 2
                    game.shangkuai_time = 70
                if img_name == 'road1_map_loc3.png':
                    game.shangkuai_npc_num = 3
                    game.shangkuai_time = 70
                if img_name == 'road2_map_loc3.png': # kunlunhuangmo
                    game.shangkuai_npc_num = 3
                    game.shangkuai_time = 40
            
            if game.shangkuai_npc_num != 0:
                maxLoc = game.find_game_img( road2_npc_loc_list[game.shangkuai_npc_num-1],\
                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)     

def determin_shangkuai_run_timer(game:GameControl):
    game.activate_window()
    time.sleep(0.5)

    close_all_table(game)
    open_self_task_table(game)
    shuangkuai_task_get_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\get_task_post.png',
                                    r'F:\01_game_ctr\lib\img\shangkuai\get_task_post1.png',
                                    r'F:\01_game_ctr\lib\img\shangkuai\get_task_post2.png']
    maxLoc,img_name = game.find_game_multi_img(shuangkuai_task_get_img_list,\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        determin_shangkuai_timer(game)
    else:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\map_banghui.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            find_npc_by_search(game,r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png','ley')
            game.shangkuai_time = 20 # 设置40s ，等timer到期之后，自动设置成0xffff，去领取任务
        else:
            # 回帮会
            # game.press_single_key_in_background('f10')
            pass
                                           
def get_self_shangkuai_task(game:GameControl):
    print('get self shangkuai task from npc LiEYun')

    game.activate_window()
    time.sleep(0.5)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png','ley')
    task_table_sts = False
    retry_cunt_tmp = 0
    while retry_cunt_tmp < 3:
        maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\shangkuai\lieyun_task_table.png',\
                                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
        if maxLoc != False:
            task_table_sts = True
            break
        retry_cunt_tmp += 1
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png','ley')
        if retry_cunt_tmp == 3:
            close_all_table(game)
            print('retry 3 times, not find ShangKuai LiEYun npc table')

    if task_table_sts:

        shuangkuai_task_state_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\get_task_pre.png',
                                          r'F:\01_game_ctr\lib\img\shangkuai\submit_subtask.png']

        maxLoc,img_name = game.find_game_multi_img(shuangkuai_task_state_img_list, \
                                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            if img_name == 'get_task_pre.png':
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
                tmp_flag = accept_task(game)
                if tmp_flag:
                    game.shangkuai_npc_num = 1
                    return True

            if img_name == 'submit_subtask.png':
                game.shangkuai_npc_num = 1
                return True
    return False

def shangkuai_subtask_submit(game:GameControl,table_img_list:list, npc_img_list:list, npc_loc_list:list,str_list:list):
    '''
    game: game control class;
    table_img_list: shangkuai subtask npc task table img, uesd for checking whether the palyer arrives the required npc loc
    npc_img_list: shangkuai subtask npc img in auto find, uesd for retry to find the the required npc by auto find
    npc_loc_list: shangkuai subtask npc loc img in self task table, used for arriving to the required npc
    str_list: shangkuai subtask npc name str, used for retry to find the the required npc by auto find
    '''
    maxLoc = game.find_game_img(table_img_list[game.shangkuai_npc_num-1],\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        task_submit_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\submit_subtask.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\task_submit.png']
        maxLoc,img_name = game.find_game_multi_img(task_submit_img_list,\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            if img_name == 'task_submit.png':
                game.shangkuai_time = 0xFFFE
                print("recognize submit task window, set timer to 0xFFFE to submit task")
                return True
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.2)
            if game.shangkuai_npc_num == 3:
                game.shangkuai_npc_num = game.shangkuai_npc_num + 1
                task_complete_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_complete.png',
                            r'F:\01_game_ctr\lib\img\shangkuai\road2_complete.png',
                            r'F:\01_game_ctr\lib\img\shangkuai\complete_retry.png']
                maxLoc,img_name = game.find_game_multi_img(task_complete_img_list,\
                                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                    if game.shangkuai_road == 1:
                        game.shangkuai_time = 120
                    else:
                        game.shangkuai_time = 170
                    return True
                else:
                    print('all substask has been submitted, but not find complete img, please check!','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
            elif game.shangkuai_npc_num < 3 and game.shangkuai_npc_num >= 0:
                game.shangkuai_npc_num = game.shangkuai_npc_num + 1
                close_all_table(game)
                time.sleep(0.5)
                game.press_single_key_in_background('k')# self task table
                time.sleep(0.5)
                maxLoc = game.find_game_img(npc_loc_list[game.shangkuai_npc_num-1],\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                    if game.shangkuai_road == 1:
                        if game.shangkuai_npc_num == 3:
                            game.shangkuai_time = 55
                        if game.shangkuai_npc_num == 2:
                            game.shangkuai_time = 150
                        if game.shangkuai_npc_num == 1:
                            game.shangkuai_time = 200
                    if game.shangkuai_road == 2:
                        if game.shangkuai_npc_num == 3:
                            game.shangkuai_time = 80
                        if game.shangkuai_npc_num == 2:
                            game.shangkuai_time = 80
                        if game.shangkuai_npc_num == 1:
                            game.shangkuai_time = 200
                    return True
                else:
                    print('not find self task table','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
            else:
                print('shangkuai_npc_num error')
        else:
            if game.shangkuai_npc_num == 3:
                task_complete_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_complete.png',
                            r'F:\01_game_ctr\lib\img\shangkuai\road2_complete.png',
                            r'F:\01_game_ctr\lib\img\shangkuai\complete_retry.png']
                maxLoc,img_name = game.find_game_multi_img(task_complete_img_list,\
                                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                    if game.shangkuai_road == 1:
                        game.shangkuai_time = 120
                    else:
                        game.shangkuai_time = 170
                    return True
                else:
                    print('all substask has been submitted, but not find complete img, please check!','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
            elif game.shangkuai_npc_num < 3 and game.shangkuai_npc_num >= 0:
                game.shangkuai_npc_num = game.shangkuai_npc_num + 1
                close_all_table(game)
                time.sleep(0.5)
                game.press_single_key_in_background('k')# self task table
                time.sleep(0.5)
                maxLoc = game.find_game_img(npc_loc_list[game.shangkuai_npc_num-1],\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                    if game.shangkuai_road == 1:
                        if game.shangkuai_npc_num == 3:
                            game.shangkuai_time = 55
                        if game.shangkuai_npc_num == 2:
                            game.shangkuai_time = 150
                        if game.shangkuai_npc_num == 1:
                            game.shangkuai_time = 200
                    if game.shangkuai_road == 2:
                        if game.shangkuai_npc_num == 3:
                            game.shangkuai_time = 80
                        if game.shangkuai_npc_num == 2:
                            game.shangkuai_time = 80
                        if game.shangkuai_npc_num == 1:
                            game.shangkuai_time = 200
                    return True
                else:
                    print('not find self task table','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
            else:
                print('shangkuai_npc_num error')
        return False
    else:
        print('retry find the required subtask npc task table')
        find_npc_by_search(game,npc_img_list[game.shangkuai_npc_num-1],str_list[game.shangkuai_npc_num-1])
        retry_cunt_tmp = 0
        task_table_sts = False
        while retry_cunt_tmp < 3:
            maxLoc = game.find_game_img(table_img_list[game.shangkuai_npc_num-1],\
                                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                task_table_sts = True
                break
            retry_cunt_tmp += 1
            find_npc_by_search(game,npc_img_list[game.shangkuai_npc_num-1],str_list[game.shangkuai_npc_num-1])
            time.sleep(0.5)
            if retry_cunt_tmp == 3:
                close_all_table(game)
                print('retry 3 times, not find npc table, shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
            
        if task_table_sts:
            task_submit_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\submit_subtask.png',
                                    r'F:\01_game_ctr\lib\img\shangkuai\task_submit.png']
            maxLoc,img_name = game.find_game_multi_img(task_submit_img_list,\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                if img_name == 'task_submit.png':
                    game.shangkuai_time = 0xFFFE
                    return True
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
                if game.shangkuai_npc_num == 3:
                    game.shangkuai_npc_num = game.shangkuai_npc_num + 1
                    task_complete_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_complete.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\road2_complete.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\complete_retry.png']
                    maxLoc,img_name = game.find_game_multi_img(task_complete_img_list,\
                                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                    if maxLoc != False:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
                        if game.shangkuai_road == 1:
                            game.shangkuai_time = 120
                        else:
                            game.shangkuai_time = 170
                        return True
                    else:
                        print('all substask has been submitted, but not find complete img, please check!','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
                elif game.shangkuai_npc_num < 3 and game.shangkuai_npc_num >= 0:
                    game.shangkuai_npc_num = game.shangkuai_npc_num + 1
                    close_all_table(game)
                    time.sleep(0.5)
                    game.press_single_key_in_background('k')# self task table
                    time.sleep(0.5)
                    maxLoc = game.find_game_img(npc_loc_list[game.shangkuai_npc_num-1],\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                    if maxLoc != False:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
                        if game.shangkuai_road == 1:
                            if game.shangkuai_npc_num == 3:
                                game.shangkuai_time = 55
                            if game.shangkuai_npc_num == 2:
                                game.shangkuai_time = 150
                            if game.shangkuai_npc_num == 1:
                                game.shangkuai_time = 200
                        if game.shangkuai_road == 2:
                            if game.shangkuai_npc_num == 3:
                                game.shangkuai_time = 80
                            if game.shangkuai_npc_num == 2:
                                game.shangkuai_time = 80
                            if game.shangkuai_npc_num == 1:
                                game.shangkuai_time = 200
                        return True
                    else:
                        print('not find self task table','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
                else:
                    print('shangkuai_npc_num error')
            else:
                if game.shangkuai_npc_num == 3:
                    task_complete_img_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_complete.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\road2_complete.png',
                                r'F:\01_game_ctr\lib\img\shangkuai\complete_retry.png']
                    maxLoc,img_name = game.find_game_multi_img(task_complete_img_list,\
                                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                    if maxLoc != False:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
                        if game.shangkuai_road == 1:
                            game.shangkuai_time = 120
                        else:
                            game.shangkuai_time = 170
                        return True
                    else:
                        print('all substask has been submitted, but not find complete img, please check!','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
                elif game.shangkuai_npc_num < 3 and game.shangkuai_npc_num >= 0:
                    game.shangkuai_npc_num = game.shangkuai_npc_num + 1
                    close_all_table(game)
                    time.sleep(0.5)
                    game.press_single_key_in_background('k')# self task table
                    time.sleep(0.5)
                    maxLoc = game.find_game_img(npc_loc_list[game.shangkuai_npc_num-1],\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                    if maxLoc != False:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
                        if game.shangkuai_road == 1:
                            if game.shangkuai_npc_num == 3:
                                game.shangkuai_time = 55
                            if game.shangkuai_npc_num == 2:
                                game.shangkuai_time = 150
                            if game.shangkuai_npc_num == 1:
                                game.shangkuai_time = 200
                        if game.shangkuai_road == 2:
                            if game.shangkuai_npc_num == 3:
                                game.shangkuai_time = 80
                            if game.shangkuai_npc_num == 2:
                                game.shangkuai_time = 80
                            if game.shangkuai_npc_num == 1:
                                game.shangkuai_time = 200
                        return True
                    else:
                        print('not find self task table','shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
                else:
                    print('shangkuai_npc_num error')
            return False

    print('not find shuangkuai subtask npc task table!')
    return False

def shangkuai_task_do(game:GameControl):
    
    game.activate_window()
    time.sleep(0.5)

    tmp_flag = False
    retry_cunt_for_subtask_submit = 0
    while True:
        if game.shangkuai_road == 0 or game.shangkuai_road == 0:
            game.shangkuai_time = 0xFFFF
            return True
        if game.shangkuai_road == 1:
            tmp_flag = shangkuai_subtask_submit(game,road1_npc_task_table_list,road1_npc_list,road1_npc_loc_list,road1_npc_str_list)
        if game.shangkuai_road == 2:
            tmp_flag = shangkuai_subtask_submit(game,road2_npc_task_table_list,road2_npc_list,road2_npc_loc_list,road2_npc_str_list)

        if tmp_flag:
            close_all_table(game)
            time.sleep(0.5)
            return True
        else:
            retry_cunt_for_subtask_submit = retry_cunt_for_subtask_submit + 1

        if retry_cunt_for_subtask_submit == 3:
            print('submit subtask retry three times failed, enter next setp to check the scence for new cycle retry')
            break
    
    determin_shangkuai_run_timer(game)
    return False

def get_other_shangkuai_task(game:GameControl):
    print('get other shangkuai task from npc LiLuoFeng')
    retry_cunt = 0
    while retry_cunt < 2:
        tmp_flag = find_npc_by_search(game,r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_liluofeng.png','ley')
        if tmp_flag:
            time.sleep(4)
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\shangkuai\shangkuai_get_others_task_pre.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
            if maxLoc != False:
                print('enter shangkuai table')
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\shangkuai_others_task.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    print('select other shangkuai task')
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.2)
                    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\shangkuai_get_others_task.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.62)
                    if maxLoc != False:
                        print('get other shangkuai task')
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\shangkuai_get_task_post.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            print('get other shangkuai task successfully')
            return True
        else:
            retry_cunt += 1
    
    return False

def shangkuai_first_subtask_npc_click(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    first_subtask_npc_list = [r'F:\01_game_ctr\lib\img\shangkuai\road1_npc1_loc.png',\
                              r'F:\01_game_ctr\lib\img\shangkuai\road2_npc1_loc.png']
    maxLoc,img_name = game.find_game_multi_img(first_subtask_npc_list,\
                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc!=False:
        print('click fisrt subtask npc location')
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.5)
        close_all_table(game)
        game.shangkuai_time = 200
        if img_name == 'road1_npc1_loc.png':
            game.shangkuai_road = 1
        else:
            game.shangkuai_road = 2
        return True
    else:
        print('not find first shangkuai npc location')
        return False
    
def submit_shangkuai_task(game:GameControl):
    print('SUBMIT shangkuai task!!!!!!!!!!!!!')

    game.activate_window()
    time.sleep(0.5)

    retry_count = 0
    while retry_count < 2:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\lieyun_task_table.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            task_table_sts = True
        else:
            find_npc_by_search(game,r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png','ley')
            retry_cunt_tmp = 0
            task_table_sts = False
            while retry_cunt_tmp < 3:
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\lieyun_task_table.png',\
                                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    task_table_sts = True
                    break
                retry_cunt_tmp += 1
                find_npc_by_search(game,r'F:\01_game_ctr\lib\img\shangkuai\npc_banghui_lieyun.png','ley')
                time.sleep(0.5)
                if retry_cunt_tmp == 3:
                    close_all_table(game)
                    print('retry 3 times, not find npc table, shuangkuai road:',game.shangkuai_road, ' shuangkuai npc num:',game.shangkuai_npc_num)
            
        if task_table_sts:
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\task_submit.png',\
                                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc!=False:
                print('submit')
                gui.moveTo(maxLoc)
                gui.leftClick()
                time.sleep(0.2)
                complete_task(game)
                #xing shang ling
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\shangkuai_xingshangling.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    print('use xingshangling')
                    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\shangkuai\shangkuai_xingshangling_confirm.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.60)
                    if maxLoc!=False:
                        gui.moveTo(maxLoc)
                        gui.leftClick()
                        time.sleep(0.2)
                        game.shangkuai_complete_cunt += 2
                        game.shangkuai_time = 0xFFFF
                        game.shangkuai_road = 0
                        game.shangkuai_npc_num = 0
                        return True
                game.shangkuai_time = 0xFFFF
                game.shangkuai_complete_cunt += 1
                game.shangkuai_road = 0
                game.shangkuai_npc_num = 0
                return True 
        retry_count = retry_count +1
    
    determin_shangkuai_run_timer(game)
    return False 

'''
def shangkuai_task_do(game:GameControl):
    # while shangkuai task is doing, wait for btask submit window
    # 
    # if recognize task submit window, submit the task,
    #   "and then recognize whether the shangkuai task is completed" in this case, it is always false (no shangkuai task)  
    #       if true, recognize the pict shangkuai_complete.png to arrive the guild
    #       if false, according playerID to get next shangkuai task(self or others)
    #
    # if recognize subtask submit window, submit this subtask, 
    #   and then recognize whether the shangkuai task is completed,
    #       if true, recognize the pict shangkuai_complete.png to arrive the guild
    #       if false, according the current map to select the next loction
    game.activate_window()
    time.sleep(0.5)

    submit_window_list = [r'F:\01_game_ctr\lib\img\shangkuai_submit_subtask1.png',r'F:\01_game_ctr\lib\img\shangkuai_submit_subtask.png',
                          r'F:\01_game_ctr\lib\img\shangkuai_task_submit1.png',r'F:\01_game_ctr\lib\img\shangkuai_task_submit.png']
    maxVal,maxLoc,image_name= game.find_multi_img(submit_window_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=1)
    if maxLoc != False and maxVal > 0.6:
        if image_name == 'shangkuai_submit_subtask1.png' or image_name == 'shangkuai_submit_subtask.png':
            print('submit subtask')
            print((maxLoc[0] + game.window_pos1[0], maxLoc[1] + game.window_pos1[1]),maxVal,image_name)
            gui.moveTo((maxLoc[0] + game.window_pos1[0], maxLoc[1] + game.window_pos1[1]))
            gui.leftClick()
            time.sleep(0.5)
            close_all_table(game)
            time.sleep(0.5)
            shangkuai_complete_img_list = [r'F:\01_game_ctr\lib\img\shangkuai_complete0.png',r'F:\01_game_ctr\lib\img\shangkuai_complete1.png']
            maxVal,maxLoc,image_name= game.find_multi_img(shangkuai_complete_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=1)
            print('is complete?:',maxVal,maxLoc,image_name)
            if maxLoc != False and maxVal > 0.7:
                print('shangkuai task condition complete, back to submit')
                gui.moveTo((maxLoc[0] + game.window_pos1[0], maxLoc[1] + game.window_pos1[1]))
                gui.leftClick()
                time.sleep(0.1)
                if image_name == 'shangkuai_complete0.png':
                    game.shangkuai_time = 170
                if image_name == 'shangkuai_complete1.png':
                    game.shangkuai_time = 120
                return True
            else:
                shangkuai_map_location_list = [r'F:\01_game_ctr\lib\img\shangkuai_second_location0.png',r'F:\01_game_ctr\lib\img\shangkuai_second_location1.png',
                                               r'F:\01_game_ctr\lib\img\shangkuai_third_location0.png',r'F:\01_game_ctr\lib\img\shangkuai_third_location1.png']
                maxVal,maxLoc,image_name= game.find_multi_img(shangkuai_map_location_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=1)
                print('next subtask location:',maxVal,maxLoc,image_name)
                if maxLoc != False and maxVal > 0.6:
                    print('determin to select next subtask location')
                    if image_name == 'shangkuai_second_location0.png' or image_name == 'shangkuai_second_location1.png':
                        print('select second subtask npc')
                        second_subtask_npc_list = [r'F:\01_game_ctr\lib\img\shangkuai_npc2_0.png',r'F:\01_game_ctr\lib\img\shangkuai_npc2_1.png']
                        game.press_single_key('k')#open task table
                        time.sleep(0.50)
                        maxVal,maxLoc,image_name= game.find_multi_img(second_subtask_npc_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=1)
                        if maxLoc != False:
                            print('go to second subtask npc')
                            gui.moveTo((maxLoc[0] + game.window_pos1[0], maxLoc[1] + game.window_pos1[1]))
                            gui.leftClick()
                            time.sleep(0.1)
                            game.press_single_key('k')#close task table
                            if image_name == 'shangkuai_npc2_0.png':
                                game.shangkuai_time = 150
                            if image_name == 'shangkuai_npc2_1.png':
                                game.shangkuai_time = 80
                            return True
                        print('failed to find third subtask npc')
                        return False
                    if image_name == 'shangkuai_third_location0.png' or image_name == 'shangkuai_third_location1.png':
                        print('select third subtask npc')
                        third_subtask_npc_list = [r'F:\01_game_ctr\lib\img\shangkuai_npc3_0.png',r'F:\01_game_ctr\lib\img\shangkuai_npc3_1.png']
                        game.press_single_key('k')#open task table
                        time.sleep(0.50)
                        maxVal,maxLoc,image_name= game.find_multi_img(third_subtask_npc_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,gray=1)
                        if maxLoc != False:
                            print('go to third subtask npc')
                            gui.moveTo((maxLoc[0] + game.window_pos1[0], maxLoc[1] + game.window_pos1[1]))
                            gui.leftClick()
                            time.sleep(0.1)
                            game.press_single_key('k')#close task table
                            if image_name == 'shangkuai_npc3_0.png':
                                game.shangkuai_time = 55
                            if image_name == 'shangkuai_npc3_1.png':
                                game.shangkuai_time = 80
                            return True
                        print('failed to find third subtask npc')
                        return False
                    print('failed to find map location')           
        if image_name == 'shangkuai_task_submit1.png' or image_name == 'shangkuai_task_submit.png':
            print((maxLoc[0] + game.window_pos1[0], maxLoc[1] + game.window_pos1[1]),maxVal,image_name)
            submit_sts = submit_shangkuai_task(game)
            if submit_sts:
                return True
            print('submit shangkuai task failed')
    return False
'''

# 初始化信号量
semaphore = threading.Semaphore(1)

def task_shangkuai(game_ctrl:GameControl):
    err_cunt = 0
    determin_shangkuai_run_timer(game_ctrl)
    game_ctrl.log.info('timer:%s,npc_num:%d,road:%d',game_ctrl.shangkuai_time,game_ctrl.shangkuai_npc_num,game_ctrl.shangkuai_road)
    while err_cunt < 15:
    
        if game_ctrl.shangkuai_time == 0xFFFF:
            semaphore.acquire()
            if game_ctrl.player_id != '4286510403' and game_ctrl.player_id != '4415020403':
                game_ctrl.activate_window()
                tmp_flag = get_self_shangkuai_task(game_ctrl)
                if tmp_flag == False:
                    err_cunt += 1
                    game_ctrl.log.info('\n\n\n%s1.FAILED TO GET OTHER SHANGKUAI TASK\n\n\n',game_ctrl.player)
                    time.sleep(5)
                    semaphore.release()
                    continue
                else:
                    tmp_flag = shangkuai_first_subtask_npc_click(game_ctrl)
                    if tmp_flag == False:
                        err_cunt += 1
                        game_ctrl.log.info('\n\n\n%s2.FAILED TO FIND FIRST NPC\n\n\n',game_ctrl.player)
                        time.sleep(5)
                        semaphore.release()
                        continue
            else:
                tmp_flag = get_self_shangkuai_task(game_ctrl)
                if tmp_flag == False:                  
                    err_cunt += 1
                    game_ctrl.log.info('\n\n\n%s3.FAILED TO GET SELF SHANGKUAI TASK\n\n\n',game_ctrl.player)         
                    time.sleep(5)
                    semaphore.release()
                    continue
                else:
                    tmp_flag = shangkuai_first_subtask_npc_click(game_ctrl)
                    if tmp_flag == False:
                        err_cunt += 1
                        game_ctrl.log.info('\n\n\n%s4.FAILED TO FIND FIRST NPC\n\n\n',game_ctrl.player)    
                        time.sleep(5)
                        semaphore.release()
                        continue
            semaphore.release()   

        if game_ctrl.shangkuai_time == 0xFFFE:
            semaphore.acquire()
            tmp_flag = submit_shangkuai_task(game_ctrl)
            if tmp_flag == False:
                err_cunt += 1
                game_ctrl.log.info('\n\n\n%s6.FAILED TO SUBMIT SHANGKUAI TASK\n\n\n',game_ctrl.player)
                time.sleep(5)
                semaphore.release()
                continue
            err_cunt = 0
            semaphore.release()

        if game_ctrl.shangkuai_time == 0:
            semaphore.acquire()
            tmp_flag = shangkuai_task_do(game_ctrl)
            if tmp_flag == False:
                err_cunt += 1
                game_ctrl.log.info('\n\n\n%s5.FAILED TO EXECUTE SHANGKUAI TASK\n\n\n',game_ctrl.player)
                time.sleep(5)
                semaphore.release()
                continue
            semaphore.release()

        time.sleep(1.0)
        if game_ctrl.shangkuai_time != 0 and game_ctrl.shangkuai_time !=0xFFFF and game_ctrl.shangkuai_time !=0xFFFE:
            game_ctrl.shangkuai_time = game_ctrl.shangkuai_time - 1

        game_ctrl.log.info('%s,timer:%s,npc_num:%d,road:%d',game_ctrl.player,game_ctrl.shangkuai_time,game_ctrl.shangkuai_npc_num,game_ctrl.shangkuai_road)
        if game_ctrl.shangkuai_complete_cunt == 4:
            break

def shangkuai_main(game_list):
    executor = ThreadPoolExecutor(max_workers=6)

    # 提交任务到线程池执行
    futures = []
    for game in game_list:
        future = executor.submit(task_shangkuai, game)
        futures.append(future)

    # 等待所有任务执行完成
    for future in futures:
        future.result()

    print("\nAll threads finished\n")