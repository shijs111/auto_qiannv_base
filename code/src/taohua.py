from src.common_operation import *

area_one_origin_list = [(822, 774),(939, 732),(916, 837),(895, 852),(994, 912)]
area_two_origin_list = [(992, 938),(1117, 906),(1176, 861),(1194, 833),(1173, 761)]
area_three_origin_list = [(1039, 739),(1080, 685),(1213, 698),(1121, 608),(937, 612)]
area_four_origin_list = [(801, 691),(669, 752),(578, 699),(485, 678),(440, 651)]
area_five_origin_list = [(502, 571),(600, 593),(666, 559),(708, 522),(808, 612)]

area_start_origin_loc = (570, 874)

boss_origin_loc = (900, 573)

def taohua_area_location_list_preprocess(game:GameControl,loc_list:list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list

def taohua_location_preprocess(game:GameControl,loc):
    new_loc = (game.window_pos1[0]+loc[0], game.window_pos1[1]+loc[1])
    return new_loc

def taohua_wait_certain_count(game:GameControl,game_list,time_cunt,area_str:str,loc_index):
    if area_str == 'area_one':
        area_index = 0
    if area_str == 'area_two':
        area_index = 1
    if area_str == 'area_three':
        area_index = 2
    if area_str == 'area_four':
        area_index = 3
    if area_str == 'area_five':
        area_index = 4

    cur_time_cunt = 0
    yanzhengma_process_flag = False
    #游戏窗口中心到左边缘的中点
    retry_rec_left_move_pos = (game.window_pos1[0]+392, game.window_pos1[1]+710)
    tmp_rec_cunt = 0


    while cur_time_cunt < time_cunt:
        start_time = time.time()
        time.sleep(0.8)
        click_dice_to_get_materiel(game)
        cur_time_cunt = cur_time_cunt + 1
        #防止60，160，260，360点错误识别,而直接去下一个点位
        if (cur_time_cunt > (time_cunt // 3) and loc_index != 3) or \
            (cur_time_cunt > (time_cunt // 2 + 5) and loc_index == 3):
            # 处理下验证码
            if yanzhengma_process_flag == False:
                yanzhengma_process_flag = True
                find_yanzhengma(game,game_list)

            text = recognize_monster_number(game,extend=4,gui=True)
            print('taohua_wait_certain_count: ',text, \
                  'lower limit: ',(area_index*100 + (loc_index+1)*20 - (area_index+1)*2),\
                  'upper limit: ',(area_index*100 + (loc_index+1)*20))
            if int(text) < 0 or int(text) > 500:
                pass
            else:
                if int(text) > (area_index*100 + (loc_index+1)*20 - (area_index+1)*2) and\
                   int(text) <= (area_index*100 + (loc_index+1)*20):
                    print('in wait time count, monster number meets the expection','text: ',text,\
                          'expection: ',(area_index*100 + (loc_index+1)*20 - (area_index+1)*2))
                    return int(text)
                elif int(text) > (area_index*100 + (loc_index+1)*20):
                    print('taohua_wait_certain_count,error rec while wait cunt, move and retry!')
                    tmp_rec_cunt = tmp_rec_cunt + 1
                    if tmp_rec_cunt > 3: # 执行三次，超过这个数值识别，如果大于三次，则认为这个数据有效，返回这个数据
                        return int(text)
                    #open_map_common(game)
                    gui.moveTo(retry_rec_left_move_pos)
                    gui.leftClick()
                    time.sleep(0.1)
                    #game.press_single_key_in_background('escape')

        print('taohua_wait_certain_count, time resolution: ',time.time() - start_time)

    return 0

def taohua_move(game:GameControl,game_ctrl_list):
    area_one = taohua_area_location_list_preprocess(game,area_one_origin_list)
    area_two = taohua_area_location_list_preprocess(game,area_two_origin_list)
    area_three = taohua_area_location_list_preprocess(game,area_three_origin_list)
    area_four = taohua_area_location_list_preprocess(game,area_four_origin_list)
    area_five = taohua_area_location_list_preprocess(game,area_five_origin_list)

    area_one_start_loc = taohua_location_preprocess(game,area_start_origin_loc)
    area_two_start_loc = area_one[-1]
    area_three_start_loc = area_two[-1]
    area_four_start_loc = area_three[-1]
    area_five_start_loc = area_four[-1]

    boss_loc = taohua_location_preprocess(game,boss_origin_loc)

    retry_rec_right_move_pos = (game.window_pos1[0]+1176, game.window_pos1[1]+710)


    taohua_move_dict ={
        #   区域key                 区域起始位置      区域点位          
        'area_one':         [area_one_start_loc,    area_one],
        'area_two':         [area_two_start_loc,    area_two],
        'area_three':       [area_three_start_loc,  area_three],
        'area_four':        [area_four_start_loc,   area_four],
        'area_five':        [area_five_start_loc,   area_five]
    }

    to_kill_boss_flag = False
    tmp_rec_cunt = 0
    cur_killed_num = 0
    pre_killed_num = 0
    rec_lower_threshold = 0

    #副本中初始状态
    change_player_status_in_boss(game,game_ctrl_list) #桃花只需要主号切幸运装打

    #进副本之后，所有需要上状态的号，一起上状态
    reset_multi_player_status_in_dungon(game,game_ctrl_list,follow=True)

    #上完状态之后，队长上坐骑
    game.press_single_key_in_background('x')
    game.press_single_key_in_background('f9')
    time.sleep(4)

    while True:

        loc_index = 0
        pre_start_loc = area_one_start_loc
        process_area_key = 'area_one'
        new_cycle_rec_cunt = 0

        #识别一下当前的个数，确认下处理的区域 key，用于选定 taohua_move_dict 中对应区域
        while True:
            text = recognize_monster_number(game,extend=4,gui=True)

            #用 cur_killed_num 来限制每次识别的下限
            if cur_killed_num -5 < 0:
                rec_lower_threshold = 0
            else:
                rec_lower_threshold = cur_killed_num - 5

            print('taohua recognization: ',text)
            #把上一次cycle的killed num 做下限比较处理，三次识别不符合，则用 rec_lower_threshold 代表当前识别数据
            if int(text) < rec_lower_threshold or int(text) > 500:
                tmp_rec_cunt = tmp_rec_cunt + 1
                #调整下位置，右侧点击移动一下
                gui.moveTo(retry_rec_right_move_pos)
                gui.leftClick()
                time.sleep(0.2)
                if tmp_rec_cunt > 3:
                    print('can not recognize the current area, use area one to process!!!')
                    new_cycle_rec_cunt = rec_lower_threshold
                else:
                    continue
            else:
                new_cycle_rec_cunt = int(text)

            #对识别的数据做处理
            if new_cycle_rec_cunt < 94:
                process_area_key = 'area_one'
                loc_index = new_cycle_rec_cunt // 20
            elif new_cycle_rec_cunt < 192:
                process_area_key = 'area_two'
                loc_index = (new_cycle_rec_cunt - 94) // 20
            elif new_cycle_rec_cunt < 290:
                process_area_key = 'area_three'
                loc_index = (new_cycle_rec_cunt - 192) // 20
            elif new_cycle_rec_cunt < 388:
                process_area_key = 'area_four'
                loc_index = (new_cycle_rec_cunt - 290) // 20
            elif new_cycle_rec_cunt < 486:
                process_area_key = 'area_five'
                loc_index = (new_cycle_rec_cunt - 388) // 20
            else:
                process_area_key = 'area_five'
                loc_index = 4
            break

        pre_start_loc = taohua_move_dict[process_area_key][0]

        #开始处理选定的区域
        #for cur_loc in taohua_move_dict[process_area_key][1]:
        while True:
            print('process_area_key: ',process_area_key, 'cur_loc: ',taohua_move_dict[process_area_key][1][loc_index])
            print('area_loc_list: ',taohua_move_dict[process_area_key][1])
            cur_loc = taohua_move_dict[process_area_key][1][loc_index]
            open_map_common(game)
            gui.moveTo(cur_loc)
            gui.leftClick()
            time.sleep(0.1)
            game.press_single_key_in_background('escape')
            #桃花这里的时间处理 需要根据实际刷的速度做调整，目前 [6,2] 为移动之后延时6s
            tmp_time_gap = calculate_time_for_two_pointers(pre_start_loc,cur_loc,1,[25,2])
            print('tmp_time_gap: ',tmp_time_gap)
            tmp_wait_cunt = 0
            while tmp_wait_cunt < 2:
                #等待开始之前执行一次验证码查询
                find_yanzhengma(game,game_ctrl_list)
                #等待中，达到目标cunt的三分之一会再次执行一直验证码查询
                cur_killed_num = taohua_wait_certain_count(game,game_ctrl_list,int(tmp_time_gap),process_area_key,loc_index)
                #等待结束再做一次验证码查询
                find_yanzhengma(game,game_ctrl_list)
                if cur_killed_num != 0:
                    #如果等待cunt的结果不为0，则记录 cur_killed_num 到 pre_killed_num
                    pre_killed_num = cur_killed_num
                    break
                else:
                    #如果等待cunt的结果为0，则用记录 pre_killed_num 给到 cur_killed_num 做下限容限处理
                    cur_killed_num = pre_killed_num
                    tmp_wait_cunt = tmp_wait_cunt + 1
            click_dice_to_get_materiel(game)
            pre_start_loc = cur_loc

            #如果是处理的 'first_area_three' 和 'second_area' 两个区域，需要在每个点位结束时，识别下怪物数量，看是否需要执行击杀boss步骤
            if process_area_key == 'area_five':
                tmp_rec_cunt = 0
                while True:
                    text = recognize_monster_number(game,extend=4,gui=True)
                    print('boss area rec: ',text)
                    if int(text) < 0 or int(text) > 500:
                        #调整下位置重新识别
                        open_map_common(game)
                        gui.moveTo(taohua_move_dict[process_area_key][0])
                        pre_start_loc = taohua_move_dict[process_area_key][0]
                        gui.leftClick()
                        time.sleep(0.1)
                        game.press_single_key_in_background('escape')
                        time.sleep(3)
                        tmp_rec_cunt = tmp_rec_cunt + 1
                        if tmp_rec_cunt > 3:
                            print('cannot recognize the current area killed monster number, go to next cycle!')
                            break
                    else:
                        if int(text) > 470:
                            to_kill_boss_flag = True
                            #切换角色状态
                            change_player_status_in_boss(game,game_ctrl_list)
                            reset_multi_player_status_in_dungon(game,game_ctrl_list)
                            followed_with_rightclick(game)
                            #去boss的位置
                            open_map_common(game)
                            gui.moveTo(boss_loc)
                            gui.leftClick()
                            time.sleep(0.1)
                            game.press_single_key_in_background('escape')
                            break
                        else:
                            print('in process boss area, the monster number not reach the threshold, go to new cycle!')
                            break

            #增加一个 处理完area_three的最后一个 index 的loc之后， 重置下角色状态
            if 'area_three' == process_area_key and loc_index == (len(taohua_move_dict[process_area_key][1]) - 1):
                reset_multi_player_status_in_dungon(game,game_ctrl_list,follow=True)

            # 检查 loc_index 是否达到 list边界                  
            if loc_index >= (len(taohua_move_dict[process_area_key][1]) - 1) or to_kill_boss_flag == True:
                print('current area is processed over, go to next process!',\
                      'loc_index: ',loc_index, 'to_kill_boss_flag: ',to_kill_boss_flag)
                break
            else:
                loc_index = loc_index + 1

        #执行击杀boss步骤
        if to_kill_boss_flag:
            boss_killed = taohua_process_boss_case(game)
            if boss_killed:
                click_dice_to_get_materiel(game)
                auto_pick_up_money(game)
                #boss击杀结束之后，查询一下是否有验证码
                find_yanzhengma(game,game_ctrl_list)
                #合成装备
                compound_equipment(game)
                print('taohua boss killed!')
                break

def taohua_process_boss_case(game:GameControl):
    game.activate_window()
    time.sleep(0.1)

    boss_name_str_list = ['香','君','魂']
    switch_to_boss = False
    check_boss_start_time = time.time()
    boss_killed_flag = False

    while True:
        game.press_single_key_in_background('tab')
        time.sleep(0.3)
        taohua_boss_flag = check_target_appear(game,boss_name_str_list)
        print('taohua_boss_flag: ',taohua_boss_flag)
        if taohua_boss_flag:
            switch_to_boss = True
            break
        if time.time() - check_boss_start_time > 30:
            print('this process not find the target taohua boss!!! go to next cycle')
            break

    if switch_to_boss:
        game.press_single_key_in_background('z')
        time.sleep(0.5)
        game.press_single_key_in_background('f1')
        time.sleep(0.1)
        game.press_single_key_in_background('f4')
        tmp_attack_cunt = 0
        check_boss_delay = 0

        while switch_to_boss:
            game.press_single_key_in_background('1')
            time.sleep(1)
            tmp_attack_cunt = tmp_attack_cunt + 1

            # after time pass two minutes, check whether boss exists.
            if tmp_attack_cunt % 1 == 0:
                check_boss_delay = check_boss_delay + 1
                if check_boss_delay > 6:
                    taohua_boss_flag_in_attack = check_is_boss(game)
                    print('taohua_boss_flag_in_attack: ',taohua_boss_flag_in_attack)
                    if taohua_boss_flag_in_attack == False and switch_to_boss == True:
                        switch_to_boss = False
                        boss_killed_flag = True
                        print('taohua boss is missed, but in this case, taohua boss can be thought as dead!')

            print('tmp_attack_cunt:',tmp_attack_cunt)
            if tmp_attack_cunt % 5 == 0:
                game.press_single_key_in_background('2')
                time.sleep(0.5)
                game.press_single_key_in_background('z')
                time.sleep(0.5)

            if tmp_attack_cunt % 5 == 0:
                tmp_attack_cunt = 0
                game.press_single_key_in_background('f1')
                time.sleep(0.1)
                game.press_single_key_in_background('f4')

            # 桃花最后几十个小怪，在打boss得时候需要处理下投点
            click_dice_to_get_materiel(game)
    return boss_killed_flag


def check_boss_taohuajun_is_dead(game:GameControl):
    try:
        text_tmp = game.recognize_text(game.monster_name_pos1,game.monster_name_pos2,image_show=False)
    except:
        text_tmp = {'text':''}
        print(game.player,' check_boss_taohuajun_is_dead error appear: ',text_tmp)
    print('check_boss_taohuajun_is_dead:',text_tmp)
    if '死' in text_tmp['text'] or '亡' in text_tmp['text'] or\
        '吻' in text_tmp['text'] or '创' in text_tmp['text'] or '阈' in text_tmp['text']:
        return True
    
    return False


def enter_taohua_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.2)
    close_all_table(game)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\taohua\taohua_npc_bitaoxian.png','btx')
    task_table_sts = False
    retry_enter_taohua_cunt = 0
    while retry_enter_taohua_cunt < 3:
        retry_cunt_tmp = 0
        while retry_cunt_tmp < 3:
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\taohua\taohua_task_table.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
            if maxLoc != False:
                task_table_sts = True
                break
            task_table_sts = False
            retry_cunt_tmp += 1
            find_npc_by_search(game,r'F:\01_game_ctr\lib\img\taohua\taohua_npc_bitaoxian.png','btx')
            time.sleep(0.5)
            if retry_cunt_tmp == 3:
                close_all_table(game)
                print('retry 3 times, not find taohua task table')
            
        taohua_task_table_list = [r'F:\01_game_ctr\lib\img\taohua\taohua_task_pre.png',
                                r'F:\01_game_ctr\lib\img\taohua\taohua_task_get.png',
                                r'F:\01_game_ctr\lib\img\taohua\taohua_task_entrance.png']
        
        retry_table_cunt = 0
        while task_table_sts and retry_table_cunt < 6:
            maxLoc,img_name = game.find_game_multi_img(taohua_task_table_list,\
                                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.75)
            if maxLoc != False:
                if img_name == 'taohua_task_pre.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)
                    accept_task(game)

                if img_name == 'taohua_task_entrance.png' or img_name == 'taohua_task_get.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)

                    if img_name == 'taohua_task_entrance.png':
                        print('waiting for entering into taohua dungeon')
                        taohua_map_img_list = [r'F:\01_game_ctr\lib\img\taohua\taohua_dungeon.png']
                        maxLoc = game.wait_game_multi_img(taohua_map_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                        if maxLoc != False:
                            print('enter into taohua dungeon successfully!')
                            return True
                        else:
                            print('Failed enter into dungeon after clicking entrance img!')
                            return False               
            retry_table_cunt += 1

        retry_enter_taohua_cunt += 1
        print('retry to enter taohua dungeon times: ',retry_enter_taohua_cunt)

    return False      

def taohua_fly_to_jinling_map(game:GameControl):
    game.activate_window()
    time.sleep(0.2)

    #拉跟随
    followed_with_rightclick(game)

    #金陵飞行旗
    game.press_single_key_in_background('f8')
    time.sleep(0.5)
    game.press_single_key_in_background('return')

    taohua_map_img_list = [r'F:\01_game_ctr\lib\img\common\map_jinling.png',
                           r'F:\01_game_ctr\lib\img\common\map_jinling1.png']
    maxLoc = game.wait_game_multi_img(taohua_map_img_list,part=1,pos1=game.window_pos1,\
                                        pos2=game.window_pos2,thread=0.70,max_time=120)
    if maxLoc != False:
        print('transfer to jinling map!')
        return True
    
    return False

def taohua_recognize_current_scen(game:GameControl):
    game.activate_window()
    time.sleep(0.2)
    taohua_map_list = [r'F:\01_game_ctr\lib\img\taohua\taohua_dungeon.png',
                        r'F:\01_game_ctr\lib\img\common\map_jinling.png',
                        r'F:\01_game_ctr\lib\img\common\map_jinling1.png']
    maxLoc, img_name = game.find_game_multi_img(taohua_map_list,part=1,\
                            pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        
        if img_name == 'map_jinling.png' or img_name == 'map_jinling1.png':
            return 1

        if img_name == 'taohua_dungeon.png':
            return 2
    else:
        return 0

def taohua_task_main(game:GameControl,game_list):
    taohua_retry_rec_cunt = 0

    #初始飞一下到金陵地图
    taohua_map_list = [r'F:\01_game_ctr\lib\img\taohua\taohua_dungeon.png',
                        r'F:\01_game_ctr\lib\img\common\map_jinling.png',
                        r'F:\01_game_ctr\lib\img\common\map_jinling1.png']
    maxLoc, img_name = game.find_game_multi_img(taohua_map_list,part=1,\
                        pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
   
    if maxLoc == False:
        taohua_fly_to_jinling_map(game)
    else:
        print('has benn in jinling map or taohua dungeon, need not transfer!') 

    #识别下当前场景，如果未识别到，则尝试五次，五次之后跳过这个任务
    while True:
        taohua_step = taohua_recognize_current_scen(game)

        if taohua_step == 0:
            taohua_retry_rec_cunt = taohua_retry_rec_cunt + 1
            if taohua_retry_rec_cunt > 5:
                print('can not recgnize the current sceen after retry 5 times!!!,skip taohua task!!!')
                return
            else:
                #调整下位置，重新识别
                taohua_fly_to_jinling_map(game)
        else:
            break
    
    if taohua_step == 1:
        tmp_flag = enter_taohua_dungeon(game)
        if tmp_flag == False:
            print('enter into taohua dungeon error, skip taohua task!!!')
        taohua_step = taohua_step + 1

    if taohua_step == 2:
        taohua_move(game,game_list)