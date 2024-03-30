from src.common_operation import *

qingwa_loc_origin_list = [(506, 788),(373, 693),(584, 628),(746, 531),(807, 453),\
                          (1064, 613),(752, 632),(1061, 753),(805, 838),(847, 886),\
                          (934, 834)]

qingwa_recover_loc_origin_list = [(521, 654),(810, 425),(1043, 623)]

qingwa_boss_origin_loc = (889, 831)
qingwa_start_origin_loc = (638, 863)

def qingwa_area_location_preprocess(game:GameControl,loc_list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list


def qingwa_area_move(game:GameControl,game_ctrl_list):
    game.activate_window()
    time.sleep(1)

    qingwa_move_loc = qingwa_area_location_preprocess(game,qingwa_loc_origin_list)
    qingwa_recover_loc = qingwa_area_location_preprocess(game,qingwa_recover_loc_origin_list)
    qingwa_boss_loc = (game.window_pos1[0]+qingwa_boss_origin_loc[0], game.window_pos1[1]+qingwa_boss_origin_loc[1])
    qingwa_start_loc = (game.window_pos1[0]+qingwa_start_origin_loc[0], game.window_pos1[1]+qingwa_start_origin_loc[1])

    pre_loc = qingwa_start_loc
    pre_rec_loc = qingwa_start_loc
    loc_index = 0
    pre_loc_index = 0
    error_rec_cunt = 0
    same_rec_cunt = 0
    pre_text = 0

    #初始识别一下怪物数量，如果怪物熟练不是小于20个，则需要一开始更新一下 pre_text 和 loc_index
    tmp_rec_cunt = 0
    while tmp_rec_cunt < 3:
        text = recognize_monster_number(game,extend=3,gui=True)
        if int(text) < 0 or int(text) > 150:
            tmp_rec_cunt = tmp_rec_cunt + 1
        else:
            if int(text) < 20:
                break
            elif int(text) == 150:
                pre_text = int(text)
                loc_index = -1
                pre_loc_index = loc_index
                pre_loc = qingwa_move_loc[loc_index]
                print(game.player,'first run, update pre_text:',pre_text,' and loc_index:',loc_index)
                break
            else:
                print(game.player,'first run, qingwa monster number:',int(text))
                pre_text = int(text)
                loc_index = int(text)//20
                pre_loc_index = loc_index
                pre_loc = qingwa_move_loc[loc_index]
                print(game.player,'first run, update pre_text:',pre_text,' and loc_index:',loc_index)
                break

    #打开地图，初始移动到loc_index 所在位置，并等待对应时间
    print(game.player,'fisrt run, move to init location!')
    open_map(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_map.png')
    gui.moveTo(qingwa_move_loc[loc_index])
    gui.leftClick()
    time.sleep(0.2)
    game.press_single_key_in_background('escape')
    time.sleep(5) #初始5s，这个5s待定，如果时间长了，可以缩减

    start_time = time.time()
    while time.time() - start_time < 300:

        tmp_start_time = time.time()

        # 识别下青蛙小怪击杀数量
        text = recognize_monster_number(game,extend=3,gui=True)
        print(game.player,'qingwa monster:',int(text),' pre monster number',pre_text)
        if int(text) < 0 or int(text) > 150:
            error_rec_cunt = error_rec_cunt + 1
        else:
            error_rec_cunt = 0

            if int(text) == pre_text :
                same_rec_cunt = same_rec_cunt + 1
            else:
                pre_text = int(text)
                same_rec_cunt = 0

        print(game.player,'same_rec_cunt:',same_rec_cunt, 'error_rec_cunt:',error_rec_cunt)
        # 相同次数达到3次，更新一下点位，若loc_index 超限14个点位，则判断当前击杀数量
        if same_rec_cunt > 2:
            loc_index = loc_index + 1
            if int(text) == 150:
                open_map(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_map.png')
                gui.moveTo(qingwa_boss_loc)
                gui.leftClick()
                time.sleep(0.2)
                game.press_single_key_in_background('escape')
                find_yanzhengma(game,game_ctrl_list)
                click_dice_to_get_materiel(game)
                return True
            if loc_index > len(qingwa_loc_origin_list)-1: 
                if int(text) == 150:
                    open_map(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_map.png')
                    gui.moveTo(qingwa_boss_loc)
                    gui.leftClick()
                    time.sleep(0.2)
                    game.press_single_key_in_background('escape')
                    find_yanzhengma(game,game_ctrl_list)
                    click_dice_to_get_materiel(game)
                    return True
                else:
                    #这里的raise 对于青蛙副本，需要增加一个 14点位走完还没完成击杀的recover
                    print(game.player,'loc_index has reached limitation(14 pos), but monster is not killed over, retry!')
                    monster_appear = False
                    pre_rec_loc = qingwa_move_loc[-1]

                    for rec_loc in qingwa_recover_loc:
                        open_map(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_map.png')
                        gui.moveTo(rec_loc)
                        gui.leftClick()
                        time.sleep(0.2)
                        game.press_single_key_in_background('escape')
                        tmp_time_gap = calculate_time_for_two_pointers(pre_rec_loc,rec_loc,1,[6,3])
                        time.sleep(tmp_time_gap)

                        while True:
                            game.press_single_key_in_background('tab')
                            time.sleep(0.5)
                            monster_flag = check_is_monster(game)
                            if monster_flag:
                                print(game.player,'qingwa recover, monster exists!!!')
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

                        pre_rec_loc = rec_loc

                        #roll
                        click_dice_to_get_materiel(game)

                        find_yanzhengma(game,game_ctrl_list)

                        rec_num = text = recognize_monster_number(game,extend=3,gui=True)
                        if int(rec_num[0]) == 150:
                            print(game.player,'recover qingwa successfully !')

                            open_map(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_map.png')
                            gui.moveTo(qingwa_boss_loc)
                            gui.leftClick()
                            time.sleep(0.2)
                            game.press_single_key_in_background('escape')
                            find_yanzhengma(game,game_ctrl_list)
                            click_dice_to_get_materiel(game)
                            time_gap = calculate_time_for_two_pointers(rec_loc,qingwa_boss_loc,1,[6,3])
                            time.sleep(time_gap)
                            return True
                        
                    #TBD 2024.03.14, 如果三次recover的尝试还没杀完怪物，跳过任务


        # 错误次数达到6次，更新一下点位，若loc_index 超限11个点位，则调整下位置，再次识别       
        if error_rec_cunt > 5:
            loc_index = loc_index + 1
            if loc_index > len(qingwa_loc_origin_list)-1:
                loc_index = loc_index - 2 #换个位置再识别一下

        # 1秒钟 识别更新一次青蛙击杀数量 （更新时间待测试确定，暂定1s）
        time.sleep(0.50)

        # 投点
        click_dice_to_get_materiel(game)

        print(game.player,'one recognization takes time: ',time.time()-tmp_start_time)

        print(game.player,'pre_loc_index:',pre_loc_index,' loc_index:',loc_index)
        #防止list越界
        if loc_index > len(qingwa_loc_origin_list)-1:
             loc_index = pre_loc_index

        # 如果index_loc 发生变更，则移动一下坐标
        if pre_loc_index != loc_index:
            same_rec_cunt = 0
            error_rec_cunt = 0
            pre_loc_index = loc_index
            #移动到新的 loc_index 位置
            open_map(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_map.png')
            gui.moveTo(qingwa_move_loc[loc_index])
            gui.leftClick()
            time.sleep(0.2)
            game.press_single_key_in_background('escape')
            #查看下是否有验证码，在每次点击地图移动之后
            yanzhengma_process(game)
            #计算下两个位置的时间，等待下行动时间
            tmp_time_gap = calculate_time_for_two_pointers(pre_loc,qingwa_move_loc[loc_index],2,[6,0])
            time.sleep(tmp_time_gap)
            #在行动时间结束之后，额外等下 2s
            time.sleep(1)
            #更新下 pre_loc
            pre_loc = qingwa_move_loc[loc_index]

    return False

def enter_qingwa_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    close_all_table(game)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_npc_humeiniang.png','hmn')
    task_table_sts = False
    retry_enter_qingwa_cunt = 0
    while retry_enter_qingwa_cunt < 3:
        retry_cunt_tmp = 0
        while retry_cunt_tmp < 3:
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_table.png',\
                                         part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
            if maxLoc != False:
                task_table_sts = True
                break
            task_table_sts = False
            retry_cunt_tmp += 1
            find_npc_by_search(game,r'F:\01_game_ctr\lib\img\qingwa\qingwa_npc_humeiniang.png','hmn')
            time.sleep(0.5)
            if retry_cunt_tmp == 3:
                close_all_table(game)
                print(game.player,'retry 3 times, not find qingwa task table')
            
        qingwa_task_table_list = [r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_pre.png',r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_pre1.png',
                                r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_get.png',r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_enter.png']
        
        retry_table_cunt = 0
        while task_table_sts and retry_table_cunt < 6:
            maxLoc,img_name = game.find_game_multi_img(qingwa_task_table_list,\
                                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.75)
            if maxLoc != False:
                if img_name == 'qingwa_task_pre.png' or img_name == 'qingwa_task_pre1.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)
                    accept_task(game)

                if img_name == 'qingwa_task_enter.png' or img_name == 'qingwa_task_get.png':
                    gui.moveTo(maxLoc)
                    time.sleep(0.2)
                    gui.leftClick()
                    time.sleep(0.5)

                    if img_name == 'qingwa_task_enter.png':
                        print(game.player,'waiting for entering into qingwa dungeon')
                        qingwa_map_img_list = [r'F:\01_game_ctr\lib\img\qingwa\qingwa_dungeon.png']
                        maxLoc = game.wait_game_multi_img(qingwa_map_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                        if maxLoc != False:
                            print(game.player,'enter into qingwa dungeon successfully!')
                            return True
                        else:
                            print(game.player,'Failed enter into dungeon after clicking entrance img!')
                            return False               
            retry_table_cunt += 1

        retry_enter_qingwa_cunt += 1
        print(game.player,'retry to enter qingwa dungeon times: ',retry_enter_qingwa_cunt)
        
    return False

def qingwa_task_submit(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    close_all_table(game)
    qingwa_complete_loc_img_list = [r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete1.png',
                                    r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete_loc.png']
    maxLoc1,img_name = game.find_game_multi_img(qingwa_complete_loc_img_list,part=1,\
                                      pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)

    if maxLoc1 != False:
        tmp_retry_cunt = 0
        while True:
            print(game.player,'qingwa task complete location')
            gui.moveTo(maxLoc1)
            time.sleep(0.2)
            gui.leftClick()
            time.sleep(0.5)
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_submit.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time = 2)
            if maxLoc != False:
                print(game.player,'qingwa task submit')
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

def wait_qingwa_task_complete(game:GameControl):
    game.activate_window()
    time.sleep(0.5)

    qingwa_complete_img_list = [r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete.png',
                                r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete1.png',
                                r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete2.png']
    maxLoc = game.wait_game_multi_img(qingwa_complete_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=120)
    if maxLoc != False:
        time.sleep(0.5)
        #roll
        click_dice_to_get_materiel(game)
        time.sleep(0.3)
        print(game.player,'qingwa task complete!')
        #pick up money
        auto_pick_up_money(game)
        compound_equipment(game)
        followed_with_rightclick(game)
        time.sleep(2)
        game.press_single_key_in_background('f7')
        time.sleep(0.5)
        game.press_single_key_in_background('return')
        print(game.player,'leave qingwa dungeon')
        return True
    else:
        print(game.player,'not find qingwa task complete in 2 mins')
        return False
    
def qingwa_recognize_current_scen(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    qingwa_map_img_list = [r'F:\01_game_ctr\lib\img\qingwa\map_hangzhou.png',
                           r'F:\01_game_ctr\lib\img\qingwa\qingwa_dungeon.png']
    maxLoc, img_name = game.find_game_multi_img(qingwa_map_img_list,part=1,\
                                                pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        if img_name == 'map_hangzhou.png':
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete_loc.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
            if maxLoc != False:
                return 4 # submit task
            else:
                return 1

        if img_name == 'qingwa_dungeon.png':
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\qingwa\qingwa_task_complete.png',\
                                        part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.65)
            if maxLoc != False:
                return 3
            else:
                return 2
    else:
        return 0
    
def qingwa_main(game:GameControl,game_qingwa_list:GameControl):
    cunt = 0
    first_run_flag = True
    retry_rec_sceen_cunt = 0

    while cunt < 5:

        if first_run_flag:
            first_run_flag = False

            #first run， set player buff
            # cancel_followed_with_leftclcik(game)
            # time.sleep(2)
            # for qingwa_game in game_qingwa_list:
            #     if qingwa_game.player_id in only_lingshou_list:
            #         modify_slaver_status(qingwa_game,'跟')
            #     else:
            #         set_player_buff(qingwa_game)
            #         time.sleep(0.3)
            #         modify_slaver_status(qingwa_game,'主')
            #         time.sleep(0.3)

            followed_with_rightclick(game)
            # time.sleep(2)
            qingwa_map_img_list = [r'F:\01_game_ctr\lib\img\qingwa\map_hangzhou.png',
                                    r'F:\01_game_ctr\lib\img\qingwa\qingwa_dungeon.png']
            maxLoc, img_name = game.find_game_multi_img(qingwa_map_img_list,part=1,\
                                                        pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
            if maxLoc != False:
                print(game.player,'has been in qingwad ungeon or map_hangzhou , need not transfor')
            else:
                print(game.player,'transfor to qingwa in hangzhou map!')
                game.press_single_key_in_background('f7')
                time.sleep(5)

            #first run
            time.sleep(2)

            #recognize the current scen to determine the start step
            start_step = qingwa_recognize_current_scen(game)
            print(game.player,'start_step:',start_step)

        if start_step == 0 :
            if retry_rec_sceen_cunt > 5:
                print(game.player,game.player, 'not recognize the current qingwa scen after retry, skip qingwa task!')
                break
            #没识别到地点，使用飞行器调整位置
            game.press_single_key_in_background('f7')
            time.sleep(0.5)
            game.press_single_key_in_background('return')
            time.sleep(5)
            print(game.player,game.player, 'not recognize the current BaJiaoTa scen, retry!')
            retry_rec_sceen_cunt = retry_rec_sceen_cunt + 1
            continue

        #step 1, followed and get task and enter into dungeon
        if start_step == 1:
            followed_with_rightclick(game)

            sts_tmp = enter_qingwa_dungeon(game)
            if sts_tmp == False:
                print(game.player,'failed to enter into dungeon')
                break
            
            start_step = start_step + 1
        
        #step 2, move in qingwa dungeon to kill monster
        if start_step == 2:
            
            #打小怪之前切换下队长和队员的装备设置，和slaver的状态
            change_player_status_in_monster(game,game_qingwa_list)

            #进副本之后，所有需要上状态的号，一起上状态
            reset_multi_player_status_in_dungon(game,game_qingwa_list,follow=True)

            #上完状态之后，队长上坐骑
            game.press_single_key_in_background('x')
            game.press_single_key_in_background('f9')
            time.sleep(5)

            #再次检查队友时候都跟随，重新拉跟随一下
            followed_with_rightclick(game)

            #开始再四色鱼的副本中移动
            sts_tmp = qingwa_area_move(game,game_qingwa_list)
            if sts_tmp == False:
                raise print(game.player,'failed to kill all qingwa monsters')

            print(game.player,'qingwa all monsters have been killed!!!')
            #打boss的时候，切换下player的装备设置，和slaver状态
            change_player_status_in_boss(game,game_qingwa_list)
            start_step = start_step + 1

        if start_step == 3:       
            #step 3, leave qingwa dungeon
            sts_tmp = wait_qingwa_task_complete(game)
            if sts_tmp == False:
                print(game.player,'failed to leave the qingwa dungeon, try to transfer again')
                followed_with_rightclick(game)
                time.sleep(2)
                game.press_single_key_in_background('f7')
                time.sleep(0.5)
                game.press_single_key_in_background('return')
            start_step = start_step + 1

        if start_step == 4:   
            #step 4, submit qingwa task
            qingwa_map_img_list = [r'F:\01_game_ctr\lib\img\qingwa\map_hangzhou.png']
            maxLoc = game.wait_game_multi_img(qingwa_map_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.70,max_time=120)
            if maxLoc != False:
                error_case_process(game)

                time.sleep(0.5)
                cancel_followed_with_leftclcik(game)

                for qingwa_game in game_qingwa_list:
                    qingwa_task_submit(qingwa_game)
                    yanzhengma_process(qingwa_game)
                    #modify_slaver_status(qingwa_game,'主')

                    #set_player_buff(qingwa_game)  取消第四部提交任务时候，去设置buff，换成第二步进副本之后同时设置buff

                close_all_table(game)
            start_step = 1
        cunt = cunt + 1

    #青蛙结束，重置下队长的宝宝
    reset_yiren_player_slaver(game)