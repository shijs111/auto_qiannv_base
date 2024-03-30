from src.common_operation import *

first_area_origin_part_one      = [(398, 707),(428, 838),(545, 837)]
first_area_origin_part_two      = [(710, 826),(873, 779),(1003, 830),(1190, 810)]
first_area_origin_part_three    = [(1138, 734),(1262, 650),(1134, 630)]
first_boss_origin_loc = (1205, 649)  

second_area_origin_loc_list = [(990, 685),(904, 663),(882, 585),(743, 573),(674, 559),(731, 534)]
second_boss_origin_loc = (689, 536)

pre_start_origin_loc = (302, 689)


def hebo_area_location_list_preprocess(game:GameControl,loc_list:list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list

def hebo_location_preprocess(game:GameControl,loc):
    new_loc = (game.window_pos1[0]+loc[0], game.window_pos1[1]+loc[1])
    return new_loc

def hebo_move(game:GameControl,game_ctrl_list):
    first_area_part_one = hebo_area_location_list_preprocess(game,first_area_origin_part_one)
    first_area_part_two = hebo_area_location_list_preprocess(game,first_area_origin_part_two)
    first_area_part_three = hebo_area_location_list_preprocess(game,first_area_origin_part_three)
    second_area_loc_list = hebo_area_location_list_preprocess(game,second_area_origin_loc_list)

    part_one_start_loc = hebo_location_preprocess(game,pre_start_origin_loc)
    part_two_start_loc = first_area_part_two[0]
    part_three_start_loc = first_area_part_three[0]
    second_area_start_loc = second_area_loc_list[0]

    first_boss_loc = hebo_location_preprocess(game,first_boss_origin_loc)
    second_boss_loc = hebo_location_preprocess(game,second_boss_origin_loc)

    hebo_move_dict ={
        #   区域key                 区域起始位置            区域点位          
        'first_area_one':       [part_one_start_loc,    first_area_part_one],
        'first_area_two':       [part_two_start_loc,    first_area_part_two],
        'first_area_three':     [part_three_start_loc,  first_area_part_three],
        'second_area':          [second_area_start_loc, second_area_loc_list]
    }

    while True:
        pre_start_loc = part_one_start_loc
        process_area_key = 'first_area_one'
        to_kill_first_boss_flag = False
        to_kill_second_boss_flag = False

        #识别一下当前的个数，确认下处理的区域 key，用于选定 hebo_move_dict 中对应区域
        while True:
            text = recognize_monster_number(game,extend=2,gui=True)
            find_flag = find_npc_by_search(game,r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaolongxia.png','jhdxlx',moveToNpc=False)

            print('hebo recognization: ',text,'find npc flag: ',find_flag)
            if find_flag or int(text[-1]) == 15:
                process_area_key = 'second_area'
                if int(text[0]) == 25:
                    hebo_start_second_part(game)
                pre_start_loc = first_boss_loc
                break
            else:
                if int(text[0]) < 8:
                    process_area_key = 'first_area_one'
                    pre_start_loc = part_one_start_loc
                elif int(text[0]) < 16:
                    process_area_key = 'first_area_two'
                    pre_start_loc = first_area_part_one[-1]
                else:
                    process_area_key = 'first_area_three'
                    pre_start_loc = first_area_part_two[-1]
                break

        #开始处理选定的区域
        for cur_loc in hebo_move_dict[process_area_key][1]:
            print('process_area_key: ',process_area_key, 'cur_loc: ',cur_loc)
            print('area_loc_list: ',hebo_move_dict[process_area_key][1])
            open_map_common(game)
            gui.moveTo(cur_loc)
            gui.leftClick()
            time.sleep(0.1)
            game.press_single_key_in_background('escape')
            tmp_time_gap = calculate_time_for_two_pointers(pre_start_loc,cur_loc,1,[6,2])
            time.sleep(tmp_time_gap)
            hebo_wait_monster_disappeared(game,game_ctrl_list)
            click_dice_to_get_materiel(game)
            pre_start_loc = cur_loc

            #如果是处理的 'first_area_three' 和 'second_area' 两个区域，需要在每个点位结束时，识别下怪物数量，看是否需要执行击杀boss步骤
            if process_area_key == 'first_area_three' or process_area_key == 'second_area':
                tmp_rec_cunt = 0
                while True:
                    text = recognize_monster_number(game,extend=2,gui=True)
                    print('\nboss area rec: ',text,'\n')
                    if int(text[0]) < 0 or int(text[0]) > 25:
                        #调整下位置重新识别
                        open_map_common(game)
                        gui.moveTo(hebo_move_dict[process_area_key][0])
                        gui.leftClick()
                        time.sleep(0.1)
                        game.press_single_key_in_background('escape')
                        time.sleep(3)
                        tmp_rec_cunt = tmp_rec_cunt + 1
                        if tmp_rec_cunt > 3:
                            print('cannot recognize the current area killed monster number, go to next cycle!')
                            break
                    else:
                        if (int(text[0]) == 15 and process_area_key == 'second_area'):
                            #处理下击杀boss的步骤
                            to_kill_second_boss_flag = True
                            #去往第一个boss地点
                            open_map_common(game)
                            gui.moveTo(second_boss_loc)
                            gui.leftClick()
                            time.sleep(0.2)
                            game.press_single_key_in_background('escape')
                            tmp_time_gap = calculate_time_for_two_pointers(pre_start_loc,second_boss_loc,1,[6,2])
                            time.sleep(tmp_time_gap)
                    
                        elif (int(text[0]) == 25 and process_area_key == 'first_area_three'):
                            #处理下击杀boss的步骤
                            to_kill_first_boss_flag = True
                            #去往第二个boss地点
                            open_map_common(game)
                            gui.moveTo(first_boss_loc)
                            gui.leftClick()
                            time.sleep(0.2)
                            game.press_single_key_in_background('escape')
                            tmp_time_gap = calculate_time_for_two_pointers(pre_start_loc,first_boss_loc,1,[6,2])
                            time.sleep(tmp_time_gap)

                        else:
                            print('in process boss area, the monster number not reach the threshold, go to new cycle!')
                        break

            if to_kill_first_boss_flag or to_kill_second_boss_flag:

                change_player_status_in_boss(game,game_ctrl_list)
                reset_multi_player_status_in_dungon(game,game_ctrl_list)

                print('prepare to kill boss!')
                break # 跳出当前的 区域点位 移动. 去执行击杀boss处理            
       
        #执行击杀boss步骤
        if to_kill_first_boss_flag:
            print('kill first boss!')
            boss_killed = hebo_process_boss_case(game)
            if boss_killed:
                click_dice_to_get_materiel(game)
                auto_pick_up_money(game)
                find_yanzhengma(game,game_ctrl_list)
                compound_equipment(game)
                #start the second part
                hebo_start_second_part(game)
                #切换到打小怪，准备河伯第二部分
                change_player_status_in_monster(game,game_ctrl_list)
                reset_multi_player_status_in_dungon(game,game_ctrl_list)
                close_all_table(game) # 防止开启第二部的时候，其他窗口重叠没识别到小龙虾
                #拉跟随
                followed_with_rightclick(game)
                print('first boss killed!')

        if to_kill_second_boss_flag:
            print('kill second boss!')
            boss_killed = hebo_process_boss_case(game)
            if boss_killed:
                click_dice_to_get_materiel(game)
                auto_pick_up_money(game)
                find_yanzhengma(game,game_ctrl_list)
                compound_equipment(game)
                #拉跟随
                followed_with_rightclick(game)
                print('second boss killed!')
                break

def hebo_start_second_part(game:GameControl):
    game.activate_window()
    time.sleep(0.1)
    find_flag = find_npc_by_search(game,r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaolongxia.png','jhdxlx')
    hebo_start2_table_sts = False

    retry_cunt_tmp = 0
    while retry_cunt_tmp < 3:
        maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\hebo\hebo_start2_table.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
        if maxLoc != False:
            hebo_start2_table_sts = True
            break
        retry_cunt_tmp += 1
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaolongxia.png','jhdxlx')
        time.sleep(0.5)
        if retry_cunt_tmp == 3:
            close_all_table(game)
            print('retry 3 times, not find hebo task table')

    if hebo_start2_table_sts:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\hebo\hebo_start2_pre.png',\
                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)

        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(2)
            #跳过动画
            game.press_single_key_in_background('escape')
            time.sleep(1)
            return True
        
    return False

def hebo_process_boss_case(game:GameControl):
    game.activate_window()
    time.sleep(0.1)

    boss_name_str_list = ['水','冰']
    switch_to_boss = False
    check_boss_start_time = time.time()
    boss_killed_flag = False

    while True:
        game.press_single_key_in_background('tab')
        time.sleep(0.3)
        hebo_boss_flag = check_target_appear(game,boss_name_str_list)
        print('hebo_boss_flag: ',hebo_boss_flag)
        if hebo_boss_flag:
            switch_to_boss = True
            break
        if time.time() - check_boss_start_time > 30:
            print('this process not find the target hebo boss!!! go to next cycle')
            break

    if switch_to_boss:
        game.press_single_key_in_background('z')
        time.sleep(0.5)
        game.press_single_key_in_background('f1')
        game.press_single_key_in_background('f4')
        tmp_attack_cunt = 0
        check_boss_start_time = time.time()


        while switch_to_boss:

            game.press_single_key_in_background('1')
            time.sleep(0.8)
            tmp_attack_cunt = tmp_attack_cunt + 1

            print('hebo_process_boss_case cunt: ',tmp_attack_cunt)

            # after time pass two minutes, check whether boss exists.
            if tmp_attack_cunt % 1 == 0:
                game.press_single_key_in_background('2')
                time.sleep(0.5)

                hebo_boss_flag_in_attack = check_is_boss(game)
                print('hebo_boss_flag_in_attack: ',hebo_boss_flag_in_attack)
                if hebo_boss_flag_in_attack == False and switch_to_boss == True:
                    switch_to_boss = False
                    boss_killed_flag = True
                    print('there is some error, hebo boss is missed, but time has run 40s, boss cam be thought as dead!')

            if tmp_attack_cunt % 5 == 0:
                game.press_single_key_in_background('z')
                time.sleep(0.5)

            if tmp_attack_cunt % 5 == 0:
                tmp_attack_cunt = 0
                game.press_single_key_in_background('f1')
                time.sleep(0.5)
                game.press_single_key_in_background('f4')

    return boss_killed_flag

def hebo_wait_monster_disappeared(game:GameControl,game_list):
    game.activate_window()
    time.sleep(0.5)
    game.press_single_key_in_background('f4')

    boss_name_str_list = ['水','冰']

    while True:
        game.press_single_key_in_background('tab')
        time.sleep(0.5)
        boss_flag = check_is_boss(game)
        monster_flag = check_is_monster(game)
        hebo_boss_flag = check_target_appear(game,boss_name_str_list)
        print('boss_flag: ',boss_flag,'monster_flag: ',monster_flag,'hebo_boss_flag: ',hebo_boss_flag)
        #如果没有小怪和小boss， 或者boss直接出现了，都结束等待
        if (boss_flag != True and monster_flag != True) or (hebo_boss_flag == True) :
            break
        game.press_single_key_in_background('0')
        click_dice_to_get_materiel(game)
        game.press_single_key_in_background('escape')
        time.sleep(0.5)
        find_yanzhengma(game,game_list)


def enter_hebo_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    close_all_table(game)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\hebo\hebo_npc_dongmenbao.png','dmb')
    task_table_sts = False
    retry_enter_hebo_cunt = 0
    while retry_enter_hebo_cunt < 3:
        retry_cunt_tmp = 0
        while retry_cunt_tmp < 3:
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\hebo\hebo_task_table.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
            if maxLoc != False:
                task_table_sts = True
                break
            task_table_sts = False
            retry_cunt_tmp += 1
            find_npc_by_search(game,r'F:\01_game_ctr\lib\img\hebo\hebo_npc_dongmenbao.png','dmb')
            time.sleep(0.5)
            if retry_cunt_tmp == 3:
                close_all_table(game)
                print('retry 3 times, not find hebo task table')
            
        hebo_task_table_list = [r'F:\01_game_ctr\lib\img\hebo\hebo_task_pre.png',
                                r'F:\01_game_ctr\lib\img\hebo\hebo_task_get.png',
                                r'F:\01_game_ctr\lib\img\hebo\hebo_task_entrance.png']
        
        retry_table_cunt = 0
        while task_table_sts and retry_table_cunt < 6:
            maxLoc,img_name = game.find_game_multi_img(hebo_task_table_list,\
                                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.75)
            if maxLoc != False:
                if img_name == 'hebo_task_pre.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)
                    accept_task(game)

                if img_name == 'hebo_task_entrance.png' or img_name == 'hebo_task_get.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)

                    if img_name == 'hebo_task_entrance.png':
                        print('waiting for entering into hebo dungeon')
                        hebo_map_img_list = [r'F:\01_game_ctr\lib\img\hebo\hebo_dungeon.png']
                        maxLoc = game.wait_game_multi_img(hebo_map_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                        if maxLoc != False:
                            print('enter into hebo dungeon successfully!')
                            return True
                        else:
                            print('Failed enter into dungeon after clicking entrance img!')
                            return False               
            retry_table_cunt += 1

        retry_enter_hebo_cunt += 1
        print('retry to enter hebo dungeon times: ',retry_enter_hebo_cunt)

    return False      


def hebo_pre_start_process(game:GameControl):
    game.activate_window()
    time.sleep(0.3)

    pre_start_loc =(game.window_pos1[0] + pre_start_origin_loc[0],game.window_pos1[1] + pre_start_origin_loc[1])

    open_map(game,r'F:\01_game_ctr\lib\img\hebo\hebo_map.png')
    gui.moveTo(pre_start_loc)
    gui.leftClick()
    time.sleep(0.5)
    close_all_table(game)

    time.sleep(2)

    xiaoguijiao_img_list = [r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaoguijiao.png',
                            r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaoguijiao1.png',
                            r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaoguijiao2.png',
                            r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaoguijiao3.png',
                            r'F:\01_game_ctr\lib\img\hebo\hebo_npc_xiaoguijiao4.png']
    maxLoc, img_name = game.find_game_multi_img(xiaoguijiao_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.65,image_show=False)

    if maxLoc != False:
        gui.moveTo((maxLoc[0],maxLoc[1]+40))
        gui.leftClick()
        time.sleep(0.5)
        while True:
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\hebo\hebo_start_table.png',\
                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)
            if maxLoc != False:
                hebo_start_pre_list = [r'F:\01_game_ctr\lib\img\hebo\hebo_start_pre1.png',\
                                    r'F:\01_game_ctr\lib\img\hebo\hebo_start_pre2.png',\
                                    r'F:\01_game_ctr\lib\img\hebo\hebo_start_pre3.png']
                maxLoc, img_name = game.find_game_multi_img(hebo_start_pre_list,part=1,\
                                                    pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    gui.leftClick()
                    time.sleep(0.5)
            else:
                break


def hebo_recognize_current_scen(game:GameControl):
    game.activate_window()
    time.sleep(0.2)
    hebo_map_img_list = [r'F:\01_game_ctr\lib\img\hebo\map_hangzhou.png',
                         r'F:\01_game_ctr\lib\img\hebo\hebo_dungeon.png']
    maxLoc, img_name = game.find_game_multi_img(hebo_map_img_list,part=1,\
                            pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        
        if img_name == 'map_hangzhou.png':
            return 1

        if img_name == 'hebo_dungeon.png':
            return 2
    else:
        return 0

def hebo_fly_to_hangzhou_map(game:GameControl):
    game.activate_window()
    time.sleep(0.2)

    #拉跟随
    followed_with_rightclick(game)

    #借用青蛙飞行器飞到杭州
    game.press_single_key_in_background('f7')
    time.sleep(0.5)
    game.press_single_key_in_background('return')

    siseyu_map_img_list = [r'F:\01_game_ctr\lib\img\hebo\map_hangzhou.png']
    maxLoc = game.wait_game_multi_img(siseyu_map_img_list,part=1,pos1=game.window_pos1,\
                                        pos2=game.window_pos2,thread=0.70,max_time=120)
    if maxLoc != False:
        print('transfer to hangzhou map!')
        return True
    
    return False


def hebo_task_main(game:GameControl,game_list):

    week_day_number = datetime.date.today().weekday()
    hebo_day = [0,2,5,6]

    hebo_retry_rec_cunt = 0

    if week_day_number in hebo_day:
        #初始飞一下到杭州地图
        hebo_map_list = [r'F:\01_game_ctr\lib\img\hebo\hebo_dungeon.png',
                        r'F:\01_game_ctr\lib\img\hebo\map_hangzhou.png',]
        maxLoc, img_name = game.find_game_multi_img(hebo_map_list,part=1,\
                            pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
        if maxLoc == False:
            hebo_fly_to_hangzhou_map(game)
        else:
            print('has benn in hangzhou map or hebo dungeon, need not transfer!')

        #识别下当前场景，如果未识别到，则尝试五次，五次之后跳过这个任务
        while True:
            hebo_step = hebo_recognize_current_scen(game)

            if hebo_step == 0:
                hebo_retry_rec_cunt = hebo_retry_rec_cunt + 1
                if hebo_retry_rec_cunt > 5:
                    print('can not recgnize the current sceen after retry 5 times!!!,skip hebo task!!!')
                    return
                else:
                    #调整下位置，重新识别
                    hebo_fly_to_hangzhou_map(game)
            else:
                break
        
        #step 1， 进入副本
        if hebo_step == 1:
            tmp_flag = enter_hebo_dungeon(game)
            if tmp_flag:
                print("enter into hebo dungeon!!! next to process the pre-srtart")
                hebo_step = hebo_step + 1
        
        #step 2， 打河伯副本
            #河伯开始之前初始操作
        if hebo_step == 2:
            change_player_status_in_monster(game,game_list)
            reset_multi_player_status_in_dungon(game,game_list)
            close_info_table_for_all(game, game_list)
            followed_with_rightclick(game)

            hebo_pre_start_process(game)
            time.sleep(5)
            hebo_move(game,game_list)
            
            #飞出河伯副本
            hebo_fly_to_hangzhou_map(game)
    else:
        print('week_day_number: ',week_day_number, 'has not hebo activity!' )