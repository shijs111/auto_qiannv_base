from src.common_operation import *

yinming_origin_loc_list = [(726, 608),(900, 559)]
fengdu_origin_loc_list = [(772, 775),(914, 690),(816, 613),(914, 690)]
guizhai_origin_loc_list = [(844, 848),(973, 703),(883, 623)]
lanruosi_origin_loc_list = [(867, 686),(972, 774),(899, 839),(905, 764)]
muxue_origin_loc_list = [(752, 752),(796, 594)]
jinling_origin_loc_list = [(746, 757),(769, 567),(829, 672)]

def zhuagui_area_location_list_preprocess(game:GameControl,loc_list:list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list


def zhuagui_serach_zhongkui(game:GameControl):
    #判断当前地图是否再酆都，在酆都使用 find_npc_by_search

    fengdu_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\map_fengdu.png']
    maxLoc, img_name = game.find_game_multi_img(fengdu_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.75,image_show=False)  
    if maxLoc != False:
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\zhuagui\npc_zhongkui.png','zk')
    else:
        #不在酆都，使用 倩女精灵
        search_target_loc_by_qiannvjingling(game,'zhuagui',[r'F:\01_game_ctr\lib\img\zhuagui\zhongkui_loc.png'])
        maxLoc = game.wait_game_multi_img(fengdu_img_list,part=1,pos1=game.window_pos1,\
                                    pos2=game.window_pos2,thread=0.70,max_time=20)
        #关闭精灵窗口
        game.press_single_key_in_background('escape')
    pass

def zhuagui_wait_zhongkui_table(game:GameControl):
    zhongkui_table_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\zhongkui_task_table.png']
    maxLoc = game.wait_game_multi_img(zhongkui_table_img_list,part=1,pos1=game.window_pos1,\
                                      pos2=game.window_pos2,thread=0.70,max_time=360)
    pass


def zhuagui_get_task(game:GameControl):

    task_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_task_pre.png']
    maxLoc, img_name = game.find_game_multi_img(task_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.75,image_show=False)  

    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.2)
        accept_task(game)
        #这里结尾需要添加领取任务之后的所有目标地图，用来判断传送到目标图了，领取任务完成
        time.sleep(2)
        zhuaguizhuagui_wait_to_gui_npc_map(game)
    pass


def zhuaguizhuagui_wait_to_gui_npc_map(game:GameControl):
    gui_map_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\map_diyu.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_kunlunhuangmo.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_lanruodigong.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_lanruosi.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_pujiacun.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_taizhouhaian.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_wangchuan.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_youtandixue.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_zhenjiaohuangye.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_tianmuxianshan.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\map_heifengdong.png']
    maxLoc = game.wait_game_multi_img(gui_map_img_list,part=1,pos1=game.window_pos1,\
                                        pos2=game.window_pos2,thread=0.70,max_time=10)

def zhuagui_switch_to_duiwu_message_window(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\clear_msg_window.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,image_show=False)
    if maxLoc != False:
        msg_window_img_pos1 = (maxLoc[0]-120,maxLoc[1]-50)
        msg_window_img_pos2 = (maxLoc[0]+320,maxLoc[1])
        img_list= [r'F:\01_game_ctr\lib\img\zhuagui\msg_window_duiwu.png',
                   r'F:\01_game_ctr\lib\img\zhuagui\msg_window_duiwu1.png']
        maxLoc1, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=msg_window_img_pos1,\
                                                    pos2=msg_window_img_pos2,thread=0.75,image_show=False)
        if maxLoc1 != False:
            gui.moveTo(maxLoc1)
            gui.leftClick()

def zhuagui_clear_duiwu_message(game:GameControl):
    maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\zhanlong\clear_msg_window.png',\
                                part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,image_show=False)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.1)

def zhuagui_go_to_gui_npc(game:GameControl):

    game.activate_window()
    time.sleep(0.1)

    #1. 关闭所有窗口
    close_all_table(game)
    #2. message窗口在游戏左下角，且处于‘队伍’message窗口
    zhuagui_switch_to_duiwu_message_window(game)

    #3. 使用天眼道具
    game.press_combination_keys(['control','8'])
    time.sleep(0.1)
    #4. 识别鬼入口npc的location并点击
    npc_loc_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_npc_loc.png',
                       r'F:\01_game_ctr\lib\img\zhuagui\gui_npc_loc1.png']
    maxLoc, img_name = game.find_game_multi_img(npc_loc_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.70,image_show=False)
    if maxLoc != False:
        npc_loc = (maxLoc[0]+25,maxLoc[1])
        gui.moveTo(npc_loc)
        gui.leftClick()
        time.sleep(1)
    pass

def zhuagui_wait_gui_npc(game:GameControl):
    gui_npc_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_entrance_pre.png']
    maxLoc = game.wait_game_multi_img(gui_npc_img_list,part=1,pos1=game.window_pos1,\
                                      pos2=game.window_pos2,thread=0.70,max_time=360)
    if maxLoc != False:
        return True
    
    return False

def zhuagui_goto_gui_dungeon(game:GameControl):
    game.activate_window()
    while True:

        img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_entrance_pre.png']
        maxLoc1, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.75,image_show=False)  
        if maxLoc1 != False:
            gui_loc = (maxLoc1[0]-50,maxLoc1[1]+50)
            gui.moveTo(gui_loc)
            gui.leftClick()
            time.sleep(1)

        entrance_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_entrance.png']
        maxLoc, img_name = game.find_game_multi_img(entrance_img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.75,image_show=False)  
        if maxLoc != False:
            gui.moveTo(maxLoc)
            gui.leftClick()

            gui_dungeon_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_fengdu.png',
                                   r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_jinling.png',
                                   r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_lanruosi.png',
                                   r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_yinming.png',
                                   r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_muxue.png',
                                   r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_guizhai.png']
            maxLoc = game.wait_game_multi_img(gui_dungeon_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.70,max_time=20)
            zhuagui_clear_duiwu_message(game)
            break
        else:
            npc_loc_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_npc_loc.png']
            maxLoc2, img_name2 = game.find_game_multi_img(npc_loc_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,thread=0.70,image_show=False)
            if maxLoc2 != False:
                npc_loc = (maxLoc2[0]+25,maxLoc2[1])
                gui.moveTo(npc_loc)
                gui.leftClick()
                time.sleep(1)
        time.sleep(2)

def zhuagui_dungeon_process(game:GameControl):

    yinming_loc_list  = zhuagui_area_location_list_preprocess(game, yinming_origin_loc_list)
    fengdu_loc_list   = zhuagui_area_location_list_preprocess(game, fengdu_origin_loc_list)
    guizhai_loc_list  = zhuagui_area_location_list_preprocess(game, guizhai_origin_loc_list)
    lanruosi_loc_list = zhuagui_area_location_list_preprocess(game, lanruosi_origin_loc_list)
    muxue_loc_list    = zhuagui_area_location_list_preprocess(game, muxue_origin_loc_list)
    jinling_loc_list  = zhuagui_area_location_list_preprocess(game, jinling_origin_loc_list)

    process_loc_list = []
    boss_name_str_list = ['僵','尸']

    cancel_followed_with_leftclcik(game)

    gui_dungeon_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_fengdu.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_jinling.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_lanruosi.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_yinming.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_muxue.png',
                            r'F:\01_game_ctr\lib\img\zhuagui\gui_dungeon_guizhai.png']
    maxLoc,image = game.find_game_multi_img(gui_dungeon_img_list,part=1,pos1=game.window_pos1,\
                                            pos2=game.window_pos2,thread=0.70)
    #根据不同副本地图，做出不同移动操作
    if maxLoc != False:
        if image == 'gui_dungeon_fengdu.png':
            process_loc_list = fengdu_loc_list
            pass
        if image == 'gui_dungeon_jinling.png':
            process_loc_list = jinling_loc_list
            pass
        if image == 'gui_dungeon_lanruosi.png':
            process_loc_list = lanruosi_loc_list
            pass
        if image == 'gui_dungeon_yinming.png':
            process_loc_list = yinming_loc_list
            pass
        if image == 'gui_dungeon_muxue.png':
            process_loc_list = muxue_loc_list
            pass
        if image == 'gui_dungeon_guizhai.png':
            process_loc_list = guizhai_loc_list
            pass
    
    print('process_loc_list: ',process_loc_list)
    modify_slaver_status(game,'主')
    game.press_combination_keys(['menu','w'])
    set_player_buff(game)
    open_map_common(game)

    for loc in process_loc_list:
        gui.moveTo(loc)
        gui.leftClick()
        game.press_single_key_in_background('f1')
        time.sleep(4)
        click_dice_to_get_materiel(game)

    #关闭地图
    game.press_single_key_in_background('escape')
    boss_appear = False

    while True:
        game.press_single_key_in_background('tab')
        time.sleep(1)
        boss_flag = check_is_boss(game)
        monster_flag = check_is_monster(game)
        if boss_flag == True:
            boss_appear = True
            break
        if monster_flag == True:
            game.press_single_key_in_background('1')

    click_dice_to_get_materiel(game)

    # #归位，去打boss
    # open_map_common(game)
    # gui.moveTo(loc)
    # gui.leftClick(process_loc_list[-1])
    # time.sleep(0.5)
    # game.press_single_key_in_background('escape')

    if boss_appear:
        gui_boss_flag = check_target_appear(game,boss_name_str_list)
        if gui_boss_flag:
            game.press_combination_keys(['menu','w'])
        else:
            game.press_combination_keys(['menu','q'])

        game.press_single_key_in_background('z')
        time.sleep(0.5)
        game.press_single_key_in_background('f1')
        time.sleep(0.1)
        game.press_single_key_in_background('f4')

        #处理boss
        tmp_attack_cunt = 0
        check_boss_delay = 0
    
        while boss_appear:
            game.press_single_key_in_background('tab')
            time.sleep(1)
            # monster_dead_flag = check_boss_guiboss_is_dead(game)
            # if monster_dead_flag:
            #     print('current boss is killed.')
            #     break
            game.press_single_key_in_background('1')
            time.sleep(0.5)
            tmp_attack_cunt = tmp_attack_cunt + 1

            print('tmp_attack_cunt:',tmp_attack_cunt)
            if tmp_attack_cunt % 5 == 0:
                game.press_single_key_in_background('z')
                time.sleep(0.5)

            # after time pass two minutes, check whether boss exists.
            if tmp_attack_cunt % 1 == 0:
                game.press_single_key_in_background('2')
                time.sleep(0.5)
                gui_boss_flag_in_attack = check_is_boss(game)
                print('gui_boss_flag_in_attack: ',gui_boss_flag_in_attack)
                if gui_boss_flag_in_attack == False and boss_appear == True:
                    check_boss_delay = check_boss_delay + 1
                    if check_boss_delay > 1:
                        boss_appear = False
                        print('gui boss is missed, but in this case, gui boss can be thought as dead!')
                elif gui_boss_flag_in_attack == True:
                    check_boss_delay = 0
                    #game.press_single_key_in_background('escape')

            if tmp_attack_cunt % 5 == 0:
                tmp_attack_cunt = 0
                game.press_single_key_in_background('f1')
                time.sleep(0.1)
                game.press_single_key_in_background('f4')

        click_dice_to_get_materiel(game)

def check_boss_guiboss_is_dead(game:GameControl):
    try:
        text_tmp = game.recognize_text(game.monster_name_pos1,game.monster_name_pos2,image_show=False)
    except:
        text_tmp = {'text':''}
        print(game.player,' check_boss_guiboss_is_dead error appear: ',text_tmp)
    print('check_boss_guiboss_is_dead:',text_tmp)
    if '死' in text_tmp['text'] or '亡' in text_tmp['text']:
        return True
    
    return False

def zhuagui_fly_to_jinlling(game:GameControl):
    game.activate_window()
    time.sleep(0.2)

    #拉跟随
    followed_with_rightclick(game)

    #金陵飞行旗
    game.press_single_key_in_background('f8')
    time.sleep(0.5)
    game.press_single_key_in_background('return')

    gui_map_img_list = [r'F:\01_game_ctr\lib\img\common\map_jinling.png',
                           r'F:\01_game_ctr\lib\img\common\map_jinling1.png']
    maxLoc = game.wait_game_multi_img(gui_map_img_list,part=1,pos1=game.window_pos1,\
                                        pos2=game.window_pos2,thread=0.70,max_time=120)
    if maxLoc != False:
        print('transfer to jinling map!')
        time.sleep(2)
        return True
    
    return False

def zhuagui_main(game:GameControl):

    #判断是否领取了任务，领取任务是否在副本中
    # 在副本中，执行dungeon_process, 不在副本执行goto_gui_npc（这个时候不能清除队伍消息窗口）
    
    #没有领取任务 则执行serach_zhongkui

    zhuagui_cunt = 0

    while zhuagui_cunt < 10:

        zhuagui_fly_to_jinlling(game)
        zhuagui_serach_zhongkui(game)
        zhuagui_wait_zhongkui_table(game)
        zhuagui_get_task(game)
        #time.sleep(5)#这里延时是等待领取任务之后进入目标地图，等待这个操作需要在zhuagui_get_task中实现，收集目标地图

        zhuagui_go_to_gui_npc(game)
        zhuagui_wait_gui_npc(game)
        zhuagui_goto_gui_dungeon(game)
        zhuagui_dungeon_process(game)
        zhuagui_cunt = zhuagui_cunt + 1