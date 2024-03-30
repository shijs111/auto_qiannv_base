from src.common_operation import *
import random

area_start_location = (776, 701)

area_one = [(898, 746),(908, 787),(974, 771),(984, 725),(980, 692),(933, 682)]

area_two = [(965, 619),(1025, 630),(979, 570),(920, 546),(879, 596),(818, 580),(829, 547)]

area_three = [(743, 587),(737, 552),(671, 558),(606, 563),(646, 603),(563, 596),(591, 639)]

area_four = [(581, 739),(541, 698),(529, 767),(627, 770),(610, 711),(587, 740)]

area_one_recover = [(911, 786),(955, 782),(891, 747),(1010, 694),(957, 684)]

area_two_recover = [(970, 615),(1008, 595),(976, 570),(916, 542),(898, 606),(836, 579),(833, 550)]

area_three_recover = [(736, 583),(740, 544),(661, 554),(590, 567),(644, 611)]

area_four_recover = [(581, 739),(541, 698),(529, 767),(627, 770),(610, 711),(587, 740)]

recover_area_two_three = [(979, 614),(910, 573),(843, 564),(749, 566),(661, 571),(563, 602),(605, 618)]

area_origin_list = [area_one,area_two,area_three,area_four]
area_origin_recover_list = [area_one_recover,area_two_recover,area_three_recover,area_four_recover]


def siseyu_area_location_list_preprocess(game:GameControl,loc_list:list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list


def siseyu_area_location_preprocess(game:GameControl):
    area_new_list = []
    for area_sublist in area_origin_list:
        new_list = []
        for loc in area_sublist:
            new_loc = (game.window_pos1[0]+loc[0], game.window_pos1[1]+loc[1])
            new_list.append(new_loc)
        area_new_list.append(new_list)

    return area_new_list

def siseyu_area_rec_location_preprocess(game:GameControl):
    area_rec_new_list = []
    for area_rec_sublist in area_origin_recover_list:
        new_rec_list = []
        for rec_loc in area_rec_sublist:
            new_rec_loc = (game.window_pos1[0]+rec_loc[0], game.window_pos1[1]+rec_loc[1])
            new_rec_list.append(new_rec_loc)
        area_rec_new_list.append(new_rec_list)

    return area_rec_new_list

def siseyu_area_move(game:GameControl,game_ctrl_list:list):
    area_list = siseyu_area_location_preprocess(game)
    pre_area_index = len(area_list)
    first_run_flag = True
    area_start_loc = (game.window_pos1[0]+area_start_location[0], game.window_pos1[1]+area_start_location[1])


    start_time = time.time()
    while True and time.time() - start_time < 360:
        rec_retry_cunt = 0
        over_max_retry_cunt = 0
        rec_num_list = []
        while True and rec_retry_cunt < 3 and over_max_retry_cunt < 12:
            monster_num = recognize_monster_number(game,gui=True)
            if int(monster_num) > 240 or (int(monster_num) == 0 and first_run_flag == False):
                over_max_retry_cunt = over_max_retry_cunt + 1
                if over_max_retry_cunt >5:
                    print(game.player,"over_max_retry_cunt:",over_max_retry_cunt," move to start loc to recognize again")
                    open_map(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_map.png')
                    gui.moveTo(area_start_loc)
                    gui.leftClick()
                    time.sleep(5)
                    game.press_single_key_in_background('escape') 
                continue
            if int(monster_num) % 60 != 0 and first_run_flag == False:
                time.sleep(0.5)
                index_tmp = int(int(monster_num) / 60)
                print(game.player,f'recognize_monster_number {monster_num}, area {index_tmp}')
                if int(monster_num) % 60 < 30 and int(monster_num) > 30:  # diff area, slightly more than the pre area,use pre area loctaion
                    random_loc_index = random.randint(0,len(area_list[index_tmp-1])-1)
                    gui.moveTo(area_list[index_tmp-1][random_loc_index])
                else: # same area, slightly less than the next area,use current area loctaion
                    random_loc_index = random.randint(0,len(area_list[index_tmp])-1)
                    gui.moveTo(area_list[index_tmp][random_loc_index])
                gui.leftClick()
                time.sleep(0.5)
                rec_num_list.append(monster_num)
                rec_retry_cunt = rec_retry_cunt + 1
            else:
                print(game.player,'monster_num:',monster_num)
                break
            if rec_retry_cunt == 3:
                monster_num = max(rec_num_list)
                print(game.player,'retry recognize monster_num three times, monster_num:',monster_num)

        area_index =  int(int(monster_num) / 60)

        print(game.player,f'area start---current area {area_index}, pre area {pre_area_index},current monster num {monster_num}')
        if area_index == 4:
            print(game.player,f'current area {area_index}, siseyu monster killed complete!')
            break
        
        #if area_index - pre_area_index >= 2, this recognize is invalid, continue
        if abs(area_index - pre_area_index) >=2 and pre_area_index != len(area_list):
            print(game.player,"area_index - pre_area_index >= 2, this recognize is invalid, continue")
            #错误识别，调整下角色位置，重新识别
            open_map_common(game)
            gui.moveTo(area_start_loc)
            gui.leftClick()
            time.sleep(0.2)
            game.press_single_key_in_background('escape')
            continue

        recover_start_loc = area_list[area_index][-1]
        #recognize the number of the monster to determin area_end_location
        if int(monster_num) % 60 == 0 or first_run_flag == True:
            print(game.player,'first run or area clear out',first_run_flag)
            first_run_flag = False
            if int(monster_num) == 0:
                area_end_location = area_start_loc
            else:
                area_end_location = area_list[area_index-1][-1]
                find_yanzhengma(game,game_ctrl_list)
        elif (int(monster_num) < (area_index+1)*60) and (int(monster_num) > (area_index+1)*60 - 10):
            print(game.player,f'monster num {monster_num} less than the threshold of the current area {area_index}')
            area_end_location = siseyu_area_recover_move(game,area_index,recover_start_loc)
            if area_end_location != None:
                area_index = area_index + 1
                if area_index == 4:
                    break
            else:
                print(game.player,f'process {area_index} area failed')
                break
        else:
            area_end_location = area_list[area_index-1][-1] # last area end loction
            find_yanzhengma(game,game_ctrl_list)
        
        for loc_index,location in enumerate(area_list[area_index]):
            print(game.player,f'current area {area_index}, loc_index {loc_index}, location {location}')
            #open map
            open_map(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_map.png')
            if area_index == pre_area_index: # loc_index != 0 is handled by this case
                #same area
                pre_location = area_list[area_index][loc_index-1]
                time_resolution = 2

            elif pre_area_index != area_index: #loc_index = 0 is handled by this case
                #cross different area
                time_resolution = 1
                if area_index == 0 :
                    #start, different area
                    pre_location = area_start_loc
                else:
                    #working, different area
                    pre_location = area_end_location
            time_gap = calculate_time_for_two_pointers(pre_location,location,time_resolution,[6,3])
            print(game.player,'time:',time_gap)
            gui.moveTo(location)
            gui.leftClick()
            game.press_single_key_in_background('escape')
            time.sleep(time_gap)

            #roll
            click_dice_to_get_materiel(game)

            yanzhengma_process(game)

            if loc_index > len(area_list[area_index]) -3 and area_index != 2:
                monster_num = recognize_monster_number(game,gui=True)
                if int(monster_num) % 60 == 0:
                    pre_area_index = area_index
                    break

            #after current arae is processed,record as pre area
            pre_area_index = area_index
    
    if area_index == 4:
        print(game.player,'move to start location')
        open_map(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_map.png')
        #time_gap = calculate_time_for_two_pointers(area_end_location,area_start_loc,2,[6,3])
        gui.moveTo(area_start_loc)
        gui.leftClick()
        #time.sleep(time_gap)
        find_yanzhengma(game,game_ctrl_list)
        time.sleep(5)
        return True

    return False

def siseyu_area_recover_move(game:GameControl,index,start_location):
    area_recover_list = siseyu_area_rec_location_preprocess(game)
    if (index + 1) > len(area_recover_list):
        print(game.player,'area_index exceed the area_recover_list')
        return

    if index != 2:
        print(game.player,f'recover start ---- recover area {index}')
        #open map
        map_flag = open_map(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_map.png')
        if map_flag == False:
            print(game.player,'open siseyu map failed')
            return None

        time_resolution = 2
        for rec_index, rec_loc in enumerate(area_recover_list[index]):
            if rec_index == 0:
                rec_pre_loc = start_location
            else:
                rec_pre_loc = area_recover_list[index][rec_index-1]

            rec_time_gap = calculate_time_for_two_pointers(rec_pre_loc,rec_loc,time_resolution,[6,3])

            gui.moveTo(rec_loc)
            gui.leftClick()
            time.sleep(rec_time_gap)

            #roll
            click_dice_to_get_materiel(game)

            rec_num = recognize_monster_number(game,gui=True)
            if int(rec_num) >= (index+1)*60:
                print(game.player,'recover to clear monster successfully!')
                return rec_loc
            
            if rec_index + 1 == len(area_recover_list[index]):
                return None
    else:
        print(game.player,'area three is porcessed, but smoe monsters are lost, run this to recover!')
        pre_rec_loc = start_location
        monster_appear = False
        area_two_three_rec_list = siseyu_area_location_list_preprocess(game, recover_area_two_three)
        for sub_rec_loc in area_two_three_rec_list:
            open_map_common(game)
            gui.moveTo(sub_rec_loc)
            gui.leftClick()
            time.sleep(0.1)
            game.press_single_key_in_background('escape')
            tmp_time_gap = calculate_time_for_two_pointers(pre_rec_loc,sub_rec_loc,2,[6,3])
            time.sleep(tmp_time_gap)
            while True:
                game.press_single_key_in_background('tab')
                time.sleep(0.5)
                monster_flag = check_is_monster(game)
                if monster_flag:
                    print(game.player,'recover area two and three, monster exists!!!')
                    monster_appear = True
                    game.press_single_key_in_background('0')
                    time.sleep(0.5)
                    game.press_single_key_in_background('escape')
                else:
                    break

            if monster_appear:
                monster_appear = False
                game.press_single_key_in_background('x')
                time.sleep(0.4)
                game.press_single_key_in_background('f9')
                time.sleep(3)

            pre_rec_loc = sub_rec_loc

            #roll
            click_dice_to_get_materiel(game)

            rec_num = recognize_monster_number(game,gui=True)
            if int(rec_num) >= (index+1)*60:
                print(game.player,'recover area two and three successfully in two areas!')
                return pre_rec_loc

        return None

def enter_siseyu_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    close_all_table(game)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_npc_mahaer.png','mhe')
    task_table_sts = False
    retry_enter_siseyu_cunt = 0
    while retry_enter_siseyu_cunt < 3:
        retry_cunt_tmp = 0
        while retry_cunt_tmp < 3:
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_table.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
            if maxLoc != False:
                task_table_sts = True
                break
            task_table_sts = False
            retry_cunt_tmp += 1
            find_npc_by_search(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_npc_mahaer.png','mhe')
            time.sleep(0.8)
            if retry_cunt_tmp == 3:
                close_all_table(game)
                print(game.player,'retry 3 times, not find SiSeYu task table')
            
        siseyu_task_table_list = [r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_pre.png',r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_pre1.png',
                                r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_get.png',r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_enter.png']
        
        retry_table_cunt = 0
        while task_table_sts and retry_table_cunt < 6:
            maxLoc,img_name = game.find_game_multi_img(siseyu_task_table_list,\
                                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.75)
            if maxLoc != False:
                if img_name == 'siseyu_task_pre.png' or img_name == 'siseyu_task_pre1.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)
                    accept_task(game)

                if img_name == 'siseyu_task_enter.png' or img_name == 'siseyu_task_get.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)

                    if img_name == 'siseyu_task_enter.png':
                        print(game.player,'waiting for entering into siseyu dungeon')
                        siseyu_map_img_list = [r'F:\01_game_ctr\lib\img\siseyu\siseyu_dungeon.png']
                        maxLoc = game.wait_game_multi_img(siseyu_map_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                        if maxLoc != False:
                            print(game.player,'enter into siseyu dungeon successfully!')
                            return True
                        else:
                            print(game.player,'Failed enter into dungeon after clicking entrance img!')
                            return False               
            retry_table_cunt += 1

        retry_enter_siseyu_cunt += 1
        print(game.player,'retry to enter siseyu dungeon times: ',retry_enter_siseyu_cunt)

    return False      

# TO DO leave dungeon method can be using flag to leave
def leave_siseyu_dungeon_with_flag(game:GameControl):
    pass
# def leave_siseyu_dungeon(game:GameControl):
#     maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_complete.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
#     if maxLoc != False:
#         print(game.player,'siseyu task complete')
#         flag_tmp = find_npc_by_drag(game,r'F:\01_game_ctr\lib\img\siseyu\siseyu_npc_yufu.png',0)
#         if flag_tmp:
#             time.sleep(0.5)
#             maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\siseyu\siseyu_leave_dungeon.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
#             if maxLoc != False:
#                 print(game.player,'leave siseyu dungeon')
#                 gui.moveTo(maxLoc)
#                 time.sleep(0.2)
#                 gui.leftClick()
#                 time.sleep(0.2)
#                 game.press_single_key('return')

def siseyu_task_submit(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    close_all_table(game)
    siseyu_complete_loc_img_list = [r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_complete1.png',
                                    r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_complete_loc.png']
    maxLoc1,img_name = game.find_game_multi_img(siseyu_complete_loc_img_list,part=1,\
                                      pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)

    if maxLoc1 != False:
        tmp_retry_cunt = 0
        while True:
            print(game.player,'siseyu task complete location')
            gui.moveTo(maxLoc1)
            time.sleep(0.2)
            gui.leftClick()
            time.sleep(0.5)
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_submit.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time = 2)
            if maxLoc != False:
                print(game.player,'siseyu task submit')
                gui.moveTo(maxLoc)
                time.sleep(0.2)
                gui.leftClick()
                time.sleep(0.5)
                tmp_flag = complete_task(game)
                if tmp_flag:
                    #提交任务成功之后，清除当前的界面
                    time.sleep(0.5)
                    game.press_single_key_in_background('escape')
                    return True
            else:
                tmp_retry_cunt = tmp_retry_cunt + 1
                if tmp_retry_cunt > 5:
                    print(game.player,'retry 5 times, not recognize the submit, maybe task has been submitted, skip!')
                    break            
    return False

def wait_siseyu_task_complete(game:GameControl):
    game.activate_window()
    time.sleep(0.5)

    siseyu_complete_img_list = [r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_complete.png']
    maxLoc = game.wait_game_multi_img(siseyu_complete_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=120)
    if maxLoc != False:
        time.sleep(0.5)
        #roll
        click_dice_to_get_materiel(game)
        time.sleep(0.3)
        print(game.player,'siseyu task complete!')
        #pick up money
        auto_pick_up_money(game)
        compound_equipment(game)
        followed_with_rightclick(game)
        time.sleep(2)
        game.press_single_key_in_background('f6')
        time.sleep(0.5)
        game.press_single_key_in_background('return')
        print(game.player,'leave siseyu dungeon')
        return True
    else:
        print(game.player,'not find siseyu task complete in 2 mins')
        return False

def siseyu_recognize_current_scen(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    siseyu_map_img_list = [r'F:\01_game_ctr\lib\img\common\map_agela.png',
                           r'F:\01_game_ctr\lib\img\siseyu\siseyu_dungeon.png']
    maxLoc, img_name = game.find_game_multi_img(siseyu_map_img_list,part=1,\
                               pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        if img_name == 'map_agela.png':
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_complete_loc.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
            if maxLoc != False:
                return 4 # submit task
            else:
                return 1

        if img_name == 'siseyu_dungeon.png':
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\siseyu\siseyu_task_complete.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
            if maxLoc != False:
                return 3
            else:
                return 2
    else:
        return 0

def siseyu_main(game:GameControl,game_siseyu_list:GameControl):
    cunt = 0
    first_run_flag = True
    retry_rec_sceen_cunt = 0

    while cunt < 5:

        if first_run_flag:
            first_run_flag = False

            #first run， set player buff
            # cancel_followed_with_leftclcik(game)
            # time.sleep(2)
            # for siseyu_game in game_siseyu_list:
            #     if siseyu_game.player_id in only_lingshou_list:
            #         modify_slaver_status(siseyu_game,'跟')
            #     else:
            #         set_player_buff(siseyu_game)
            #         time.sleep(0.3)
            #         modify_slaver_status(siseyu_game,'主')
            #         time.sleep(0.3)

            followed_with_rightclick(game)
            time.sleep(2)
            siseyu_map_img_list = [r'F:\01_game_ctr\lib\img\common\map_agela.png',
                                r'F:\01_game_ctr\lib\img\siseyu\siseyu_dungeon.png']
            maxLoc, img_name = game.find_game_multi_img(siseyu_map_img_list,part=1,\
                                    pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                print(game.player,'has been in SiSeYu dungeon, need not transfor')
            else:
                print(game.player,'transfor to SiSeYu in agela map!')
                game.press_single_key_in_background('f6')
                time.sleep(5)

            #first run
            time.sleep(2)

            #recognize the current scen to determine the start step
            start_step = siseyu_recognize_current_scen(game)
            print(game.player,'start_step:',start_step)

        if start_step == 0 :
            if retry_rec_sceen_cunt > 5:
                print(game.player, 'not recognize the current SiSeYu scen after retry, skip siseyu task!')
                break
            print(game.player, 'not recognize the current SiSeYu scen, retry!')
            retry_rec_sceen_cunt = retry_rec_sceen_cunt + 1
            continue

        #step 1, followed and get task and enter into dungeon
        if start_step == 1:
            followed_with_rightclick(game)

            sts_tmp = enter_siseyu_dungeon(game)
            if sts_tmp == False:
                print(game.player,'failed to enter into SiSeYu dungeon,skip SiSeYu task!')
                break

            start_step = start_step + 1
        
        #step 2, move in siseyu dungeon to kill monster
        if start_step == 2:
            
            #打小怪之前切换下队长和队员的装备设置，和slaver的状态
            change_player_status_in_monster(game,game_siseyu_list)

            #进副本之后，所有需要上状态的号，一起上状态
            reset_multi_player_status_in_dungon(game,game_siseyu_list,follow=True)

            #上完状态之后，队长上坐骑
            game.press_single_key_in_background('x')
            game.press_single_key_in_background('f9')
            time.sleep(4)

            #再次检查队友时候都跟随，重新拉跟随一下
            followed_with_rightclick(game)

            #开始再四色鱼的副本中移动
            sts_tmp = siseyu_area_move(game,game_siseyu_list)
            if sts_tmp == False:
                raise print(game.player,'failed to kill all siseyu monsters, skip siseyu task')

            print(game.player,'siseyu all monsters have been killed!!!')
            #打boss的时候，切换下player的装备设置，和slaver状态
            change_player_status_in_boss(game,game_siseyu_list)
            start_step = start_step + 1

        if start_step == 3:       
            #step 3, leave siseyu dungeon
            sts_tmp = wait_siseyu_task_complete(game)
            if sts_tmp == False:
                print('failed to leave the siseyu dungeon, try to transfer again')
                followed_with_rightclick(game)
                time.sleep(2)
                game.press_single_key_in_background('f6')
                time.sleep(0.5)
                game.press_single_key_in_background('return')
            find_yanzhengma(game,game_siseyu_list)
            start_step = start_step + 1

        if start_step == 4:   
            #step 4, submit siseyu task
            siseyu_map_img_list = [r'F:\01_game_ctr\lib\img\common\map_agela.png']
            maxLoc = game.wait_game_multi_img(siseyu_map_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.70,max_time=120)
            if maxLoc != False:
                error_case_process(game)

                time.sleep(0.5)
                cancel_followed_with_leftclcik(game)

                for siseyu_game in game_siseyu_list:
                    siseyu_task_submit(siseyu_game)
                    yanzhengma_process(siseyu_game)
                    #modify_slaver_status(siseyu_game,'主')

                    #set_player_buff(siseyu_game)  取消第四部提交任务时候，去设置buff，换成第二步进副本之后同时设置buff

                close_all_table(game)
            start_step = 1
        cunt = cunt + 1

    #四色鱼结束，重置下队长的宝宝
    reset_yiren_player_slaver(game)