from src.common_operation import *

yeyan_corner_loc_origin_list = [(1024, 701),(739, 543),(516, 732),(778, 864)] # each floor move and 86 monster slow move

yeyan_origin_center = (866, 667)

row3_origin_loc = [(541, 767),(717, 778),(877, 785)] #48 monsters floor


def yeyan_area_location_list_preprocess(game:GameControl,loc_list:list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list

def yeyan_location_preprocess(game:GameControl,loc):
    new_loc = (game.window_pos1[0]+loc[0], game.window_pos1[1]+loc[1])
    return new_loc

def yeyan_init_move_after_new_floor(game:GameControl):
    game.activate_window()
    time.sleep(0.5)

    #init_move_loc_list = yeyan_area_location_list_preprocess(game,yeyan_corner_loc_origin_list)
    center_loc = yeyan_location_preprocess(game,yeyan_origin_center)

    print('move to center loc')
    open_map_common(game)
    gui.moveTo(center_loc)
    gui.leftClick()
    time.sleep(0.1)
    game.press_single_key_in_background('escape')
    time.sleep(30)

def yeyan_go_to_next_floor(game:GameControl):

    game.activate_window()
    time.sleep(0.5)

    retry_rec_complete = False

    while True:
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\yeyan\yeyan_npc_baoxinxiaoyao.png','bxxy')
        
        yeyan_xiaoyao_img_list = [r'F:\01_game_ctr\lib\img\yeyan\yeyan_npc_table.png']
        maxLoc = game.wait_game_multi_img(yeyan_xiaoyao_img_list,part=1,\
                                        pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=20)
        if maxLoc != False:

            #通过table计算固定点位坐标，用于retry_rec_complete点击
            retry_click_loc = (maxLoc[0],maxLoc[1]+280)

            yeyan_table_img_list = [r'F:\01_game_ctr\lib\img\yeyan\yeyan_complete_back.png',\
                                    r'F:\01_game_ctr\lib\img\yeyan\yeyan_floor_complete.png',\
                                    r'F:\01_game_ctr\lib\img\yeyan\yeyan_extra_floor_entrance.png']
            loc, img_name = game.find_game_multi_img(yeyan_table_img_list,part=1,pos1=game.window_pos1,\
                                                        pos2=game.window_pos2,image_show= False,thread=0.70)

            if loc != False:
                if img_name == 'yeyan_complete_back.png':
                    #离开会阿格拉
                    #这里设置个离开夜宴的flag 为True，用于中止 yeyan 的 while循环
                    gui.moveTo(loc)
                    gui.leftClick()
                    time.sleep(0.2)
                    game.press_single_key_in_background('return')
                    print('yeyan task complete, leave to agela city!')
                    return 2 #表明回阿格拉，结束任务
                if img_name == 'yeyan_floor_complete.png' or img_name == 'yeyan_extra_floor_entrance.png':
                    #进入下一层
                    gui.moveTo(loc)
                    gui.leftClick()
                    time.sleep(0.2)
                    print('go to next yeyan floor!')
                    return 1 #代表进入下一层， 开启新的一轮识别

            else:
                if retry_rec_complete:
                    print('not rec the yeyan_complete_back or yeyan_floor_complete img, \
                          but retry has been done, cilck directly!')
                    #点击固定点位坐标
                    gui.moveTo(retry_click_loc)
                    gui.leftClick()
                    time.sleep(5)
                    #这里点击之后，识别下map_AGeLa, 如果是阿格拉地图，则也返回True，结束夜宴任务

                    if False: # 阿格拉地图
                        return 2 #表明回阿格拉，结束任务
                    else:
                        return 1 #代表进入下一层， 开启新的一轮识别

                #重新移动到地图中心点位，等待识别，怪物数量时候达到期望值

                #这里做一个30s的while等待，若30s之内数量达到目标则再次尝试进入下一层，并设置强势点table固定点位坐标（直接点那个位置） 
                tmp_start_time = time.time() 
                while time.time() - tmp_start_time < 30:
                    pass

                retry_rec_complete = True
                pass


#检查是否处于夜宴地图中
def yeyan_check_is_in_yeyan_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.2)

    yeyan_dungeon_img_list = [r'F:\01_game_ctr\lib\img\yeyan\yeyan_dungeon.png']
    loc, img_name = game.find_game_multi_img(yeyan_dungeon_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,image_show= False,thread=0.70)
    if loc != False:
        return True
    
    return False

#夜宴初始 移动一下
def yeyan_move_at_beginning(game:GameControl):
    game.activate_window()
    time.sleep(0.2)

    yeyan_move_pos = (game.window_pos1[0]+1176, game.window_pos1[1]+710)
    
    gui.moveTo(yeyan_move_pos)
    gui.leftClick()
    time.sleep(0.5)

def yeyan_main_task(game:GameControl,game_ctrl_list):

    while True:


        #查看下是否还处于夜宴地图，不是夜宴地图，结束任务，尝试飞回安全区。
        # tmp_yeyan_flag = yeyan_check_is_in_yeyan_dungeon(game)
        # if tmp_yeyan_flag == False:
        #     #game.press_single_key_in_background('f8')
        #     time.sleep(0.1)
        #     #game.press_single_key_in_background('return')
        #     print('not in yeyan dungeon, fly to JinLing map!!!')
        #     break
        
        time.sleep(5)

        close_all_table(game)
        #取消跟随，上一下状态
        cancel_followed_with_leftclcik(game)
        reset_multi_player_status_in_dungon(game,game_ctrl_list,follow=True)

        #初始移动一下
        #yeyan_move_at_beginning(game)

        #等待15s， 夜宴每进入新的一层大概延时20+s 出现怪物
        time.sleep(15)

        #出现之后进行怪物数量识别
        while True:
            text = recognize_monster_number(game,extend=2,gui=True)
            if int(text[-1]) != 0 and (int(text[0]) <= int(text[-1]) and int(text[0]) >= 0):
                #识别到特殊层，如48个怪，86(88)个怪，做移动处理 TBD 2024.003.05
                time.sleep(1)
                if int(text[-1]) == int(text[0]):
                    print('yeyan current floor has been cleared!')
                    break

            time.sleep(1)
    
        followed_with_rightclick(game)

        #达到执行进入下一层，或返回主城且结束任务
        yeyan_status = yeyan_go_to_next_floor(game)
        if yeyan_status == 0:
            #game.press_single_key_in_background('f8')
            time.sleep(0.1)
            #game.press_single_key_in_background('return')
            print('can not go to next floor, and retry not recover, fly to JinLing map!!!')
            break
        if yeyan_status == 1:
            continue
        if yeyan_status == 2:
            break

        time.sleep(10)
        # 0 这个标志，直接结束夜宴任务，并飞回安全区
        # 1 代表进入下一层， 开启新的一轮识别
        # 2 表明回阿格拉，结束任务