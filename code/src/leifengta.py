from src.common_operation import *
'''
area_loc_list = [(668, 640),(701, 679),(747, 715),(793, 750),
                 (861, 710),(812, 672),(769, 641),(727, 608),
                 (782, 566),(821, 596),(861, 626),(909, 668)]
area_loc_list = [(663, 642),(724,697),(793, 750),
                 (856, 710),(790,656),(727, 608),
                 (777, 566),(841,611),(909, 668)]                 

area_loc_list = [(688, 666),(724,697),(793, 750),
                 (856, 710),(790,656),(727, 608),
                 (777, 566),(841,611),(909, 668)]
area_recover_loc_list = [(777, 566),(727, 608),(856, 710),(793, 750)]
'''
area_loc_list = [(452, 441),(493, 472),(530, 500),
                 (574, 470),(539, 443),(495, 410),
                 (530, 384),(572, 414),(609, 442)]

area_recover_loc_list = [(530, 384),(495, 410),(574, 470),(530, 500)]
area_start_loc = (452, 441) #(627, 662)

def leifengta_area_location_preprocess(game:GameControl,loc_list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list

def enter_leifengta_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\leifengta\npc_baiyundashi.png','byds')
    task_table_sts = False
    retry_cunt_tmp = 0
    while retry_cunt_tmp < 3:
        maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\leifengta\npc_baiyun_table.png',\
                                    part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
        if maxLoc != False:
            task_table_sts = True
            break
        task_table_sts = False
        retry_cunt_tmp += 1
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\leifengta\npc_baiyundashi.png','byds')
        if retry_cunt_tmp == 3:
            close_all_table(game)
            print('retry 3 times, not find BaiYunDaShi npc table')

    if task_table_sts:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\leifengta\enter_floor_pre.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            time.sleep(0.5)
            gui.leftClick()
            time.sleep(0.5)
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\leifengta\enter_floor_136floor.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)
            if maxLoc != False:
                gui.moveTo(maxLoc)
                time.sleep(0.5)
                gui.leftClick()
                time.sleep(0.5)
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\leifengta\sure.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)
                if maxLoc != False:
                    gui.moveTo(maxLoc)
                    time.sleep(0.5)
                    gui.leftClick()
                    time.sleep(0.5)
                    game.press_single_key_in_background('return')
                    print('waiting for entering into leifengta 136th floor')
                    leifengta_map_img_list = [r'F:\01_game_ctr\lib\img\leifengta\136th_floor.png']
                    maxLoc = game.wait_game_multi_img(leifengta_map_img_list,part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                    if maxLoc != False:
                        print('enter into leifengta 136th floor successfully!')
                        return True
    
    print('Failed enter into 136th floor after clicking entrance img!')
    return False

def leave_leifengta_dungeon(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\leifengta\npc_xiaoyishi.png','xys')

    retry_cunt_tmp = 0
    while retry_cunt_tmp < 3:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\leifengta\leave_floor.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            time.sleep(0.5)
            gui.leftClick()
            time.sleep(0.5)
            game.press_single_key_in_background('return')
            maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\leifengta\map_leifengta.png',\
                               part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
            if maxLoc != False:
                return True
            print('not find the scene outside the tower')
            break
        retry_cunt_tmp += 1
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\leifengta\npc_xiaoyishi.png','xys')
        if retry_cunt_tmp == 3:
            close_all_table(game)
            print('retry 3 times, not find XiaoYiShi npc')

    return False


def move_around_centre(game:GameControl,centre_loc,radius = 35):
    # 等角度取圆上的三个点
    angles = np.linspace(0, 2*np.pi, 4)[:-1]  # 等角度划分为三个点
    print('angles:',angles,type(angles[0]))
    points = []
    for angle in angles:
        # 计算圆上的点的坐标
        x_point = int(centre_loc[0] + radius * np.cos(angle))
        y_point = int(centre_loc[1] + radius * np.sin(angle))
        points.append((x_point, y_point))

    start_loc_tmp = centre_loc
    random.shuffle(points)

    for point in points:
        gui.moveTo(point)
        #time.sleep(0.25)
        gui.leftClick()
        time_tmp = calculate_time_for_two_pointers(start_loc_tmp,point,2,[3,0.8])
        time.sleep(time_tmp)
        start_loc_tmp = point

def leifengta_move_recover(game:GameControl,start_loc):
    reco_start_loc = start_loc
    new_reco_list = leifengta_area_location_preprocess(game,area_recover_loc_list)
    for reco_loc in new_reco_list:
        gui.moveTo(reco_loc)
        time.sleep(0.10)
        gui.leftClick()
        time_tmp = calculate_time_for_two_pointers(reco_start_loc,reco_loc,2,[4,2])
        time.sleep(time_tmp)
        reco_start_loc = reco_loc

        text_list = recognize_monster_number(game,extend=1,gui=True)
        if int(text_list[-1]) == 180:
            text_list[-1] = '160'
        
        if int(text_list[-1]) >= 160 and int(text_list[0]) <= int(text_list[-1])\
          and  int(text_list[0]) >= 0:
            if int(text_list[0]) >= int(int(text_list[-1]) * 0.82):
                go_to_next_floor(game)
                print('current area recover completed!')
                return True
    return False
def leifengta_move(game:GameControl,start_index=0):
    new_loc_list = leifengta_area_location_preprocess(game,area_loc_list)
    new_area_start = (area_start_loc[0] + game.window_pos1[0],area_start_loc[1] + game.window_pos1[1])

    map_flag = open_map(game,r'F:\01_game_ctr\lib\img\common\map.png')
    if map_flag == False:
        print('open leifengta dungeon map failed')
        return False

    for index, loc in enumerate(new_loc_list):
        if index < start_index:
            continue
        gui.moveTo(loc)
        #time.sleep(0.10)
        gui.leftClick()
        time_tmp = calculate_time_for_two_pointers(new_area_start,loc,1,[3,0.8])
        time.sleep(time_tmp)
        move_around_centre(game,loc)
        new_area_start = loc

        # loc[2], loc[5]   and   loc[3], loc[6]
        # if index == 2 or index == 5:
        #     gui.moveTo(new_loc_list[index+3])
        #     gui.leftClick()
        #     time_tmp = calculate_time_for_two_pointers(new_area_start,new_loc_list[index+3],1,[4,2])
        #     time.sleep(time_tmp)

        # if index == 3 or index == 6:
        #     time.sleep(4)
        #     gui.moveTo(new_loc_list[index-3])
        #     gui.leftClick()
        #     time_tmp = calculate_time_for_two_pointers(new_area_start,new_loc_list[index-3],1,[4,2])
        #     time.sleep(time_tmp)

        if index > len(new_loc_list) - 4:
            text_list = recognize_monster_number(game,extend=1,gui=True)
            if int(text_list[-1]) >= 180:
                text_list[-1] = '160'
            
            if int(text_list[-1]) >= 160 and int(text_list[0]) <= int(text_list[-1])\
               and  int(text_list[0]) >= 0:
                if int(text_list[0]) >= int(int(text_list[-1]) * 0.82):
                    go_to_next_floor(game)
                    print('current area monster num has been completed!')
                    return True
            else:
                print('LeiFengTa monster number recognized error!')
                pass
    
            if index == len(new_loc_list)-1:
                tmp_flag = leifengta_move_recover(game,loc)
                return tmp_flag
    return False

def go_to_next_floor(game:GameControl):

    game.activate_window()
    time.sleep(0.5)

    find_npc_by_search(game,r'F:\01_game_ctr\lib\img\leifengta\npc_baiyunhuashen.png','byds')

    game.wait_game_img(r'F:\01_game_ctr\lib\img\leifengta\baiyun_npc_table.png',\
                       part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70)
    
    retry_cunt_tmp = 0
    while retry_cunt_tmp < 3:
        maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\leifengta\next_floor.png',part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64)
        if maxLoc != False:
            gui.moveTo(maxLoc)
            time.sleep(0.5)
            gui.leftClick()
            #time.sleep(0.5)
            #game.press_single_key_in_background('return')
            return True

        retry_cunt_tmp += 1
        find_npc_by_search(game,r'F:\01_game_ctr\lib\img\leifengta\npc_baiyunhuashen.png','byds')
        if retry_cunt_tmp == 3:
            close_all_table(game)
            print('retry 3 times, not find BaiYunDaShi npc table')

    print('Failed enter into 136th floor after clicking entrance img!')
    return False

def wait_for_master_player(game:GameControl,team:str):
    if team == 'team1':
        team_img = r'F:\01_game_ctr\lib\img\leifengta\teamA1.png'
    elif team == 'team2':
        team_img = r'F:\01_game_ctr\lib\img\leifengta\teamA2.png'
    else:
        team_img = r'F:\01_game_ctr\lib\img\leifengta\teamA1.png'

    open_team_table(game,r'F:\01_game_ctr\lib\img\leifengta\team_table.png')

    start_time = time.time()
    while True and time.time() - start_time < 300:
        maxLoc = game.find_game_img(team_img,part=1,\
                        pos1=game.window_pos1,pos2=game.window_pos2,image_show=False,thread=0.67)
        if maxLoc != False:
            left_top = (maxLoc[0]-100,maxLoc[1])
            right_buttom = (maxLoc[0]+100,maxLoc[1]+210)
            maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\leifengta\wait_for_player.png',part=1,\
                        pos1=left_top,pos2=right_buttom,image_show=False,thread=0.67)

            if maxLoc != False:
                print('master player has entered into team ,ready to leave LeiFengTa dungeon')
                close_all_table(game)
                time.sleep(15)
                return True
        time.sleep(5)

    return False

def lengfengta_do(game:GameControl,game_list):

    first_run_tmp = True
    floor_img = [r'F:\01_game_ctr\lib\img\leifengta\floor_136.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_137.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_138.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_139.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_140.png']
    while True:
        img_index = 5
        start_loc_index = 0
        reset_slaver = False
        find_yanzhengma(game,game_list)
        maxLoc, img_name = game.find_game_multi_img(floor_img,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            if img_name == 'floor_136.png':
                img_index = 0
            if img_name == 'floor_137.png':
                img_index = 1
            if img_name == 'floor_138.png':
                img_index = 2
            if img_name == 'floor_139.png':
                img_index = 3
            if img_name == 'floor_140.png':
                img_index = 4

            if img_index < 4:
                #before moving, check number of killed monster, if condition is met, go to next floor directly
                text_list = recognize_monster_number(game,extend=1,gui=True)
                if int(text_list[-1]) >= 180:
                    text_list[-1] = '160'
                
                if int(text_list[0]) >= int(int(text_list[-1]) * 0.82) and int(text_list[-1]) >= 160 \
                    and int(text_list[0]) <= int(text_list[-1]) and  int(text_list[0]) >= 0:
                    go_to_next_floor(game)
                    game.wait_game_img(floor_img[img_index+1],part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                else:
                    if first_run_tmp:
                        first_run_tmp = False
                        if game.get_slaver_run_time() > 1800 or game.slaver_start_time == 0:
                            game.reset_slaver_start_time()
                            reset_slaver = True
                        reset_multi_player_status_in_dungon(game,game_list,follow=True,reset_slver=reset_slaver)
                        game.press_single_key_in_background('f9')
                        time.sleep(5)

                    if int(text_list[0]) <= int(int(text_list[-1]) * 0.2):
                        start_loc_index = 0
                    elif int(text_list[0]) <= int(int(text_list[-1]) * 0.4):
                        start_loc_index = 2
                    elif int(text_list[0]) <= int(int(text_list[-1]) * 0.6):
                        start_loc_index = 5

                    tmp_flag = leifengta_move(game,start_loc_index)
                    if tmp_flag:
                        game.wait_game_img(floor_img[img_index+1],part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
            elif img_index == 4:
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\map.png',part=1,\
                                pos1=game.window_pos1,pos2=game.window_pos2,image_show=False,thread=0.67)
                if maxLoc != False:
                    game.press_single_key_in_background('r') # close map
                followed_with_rightclick(game)
                return True
            else:
                return False

def leifengta_determin_scene(game:GameControl):
    game.activate_window()
    time.sleep(0.5)
    leifengta_img = [r'F:\01_game_ctr\lib\img\leifengta\map_leifengta.png']
    maxLoc, img_name = game.find_game_multi_img(leifengta_img,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        print('outside the tower')
        return True
    print('in the tower')
    return False

def leifengta_main(game:GameControl,game_list):

    first_run_flag = True
    srart_step = 0
    while True:

        if first_run_flag:
            first_run_flag = True
            tmp_sts = leifengta_determin_scene(game)
            if tmp_sts:
                srart_step = 1
            else:
                srart_step = 2

        if srart_step == 1:
            tmp_flag = enter_leifengta_dungeon(game)
            if tmp_flag == False:
                raise print('enter into leifengta dungeon failed')
            srart_step = srart_step + 1
        
        if srart_step == 2:
            tmp_flag = lengfengta_do(game,game_list)
            if tmp_flag == False:
                raise print('cannot recognize the scene of the tower')
            srart_step = srart_step + 1

        if srart_step == 3:
            tmp_flag = wait_for_master_player(game,'team2')
            if tmp_flag == False:
                print('not wait for player')
            srart_step = srart_step + 1

        if srart_step == 4:
            tmp_flag = leave_leifengta_dungeon(game)
            if tmp_flag == False:
                print('leave LeiFengTa dungeon Failed, reset first_run_flag')
                first_run_flag = True
                continue
            srart_step = 1

#============================================== 方士刷塔======================================#
                                    #     右          右下         右上      左上
leifengta_direction_origin_loc_list = [(1529, 626),(1526, 1175),(1497, 89),(39, 64)]
leifengta_monster_range_origin_loc_list = [(14, 272),(1294, 1196)]

def leifengta_move_with_guangjiao(game:GameControl):

    game.activate_window()
    time.sleep(0.3)

    direction_loc_list = leifengta_area_location_preprocess(game, leifengta_direction_origin_loc_list)
    monster_range_list = leifengta_area_location_preprocess(game, leifengta_monster_range_origin_loc_list)

    monster_range_loc1 = monster_range_list[0]
    monster_range_loc2 = monster_range_list[1]

    right_direc_loc = direction_loc_list[0]
    lowright_direc_loc = direction_loc_list[1]
    upright_direc_loc = direction_loc_list[2]
    upleft_direc_loc = direction_loc_list[3]

    #  
    #                           ----> 10
    #                                   || 
    # 0 ----> 1         <----9          ---->11
    #            ||           ||               ||      
    #           ----> 2         <----8         ----> 12              
    #                    ||          ||                 ||
    #                   ----> 3         <----7          ----> 13
    #                            ||         ||                  ||               
    #                           ----> 4        <----6           ----> 14      
    #                                    ||      ||     
    #                                   ----> 5 
 
    
    i = 0
    while True:
        i = i + 1
        print('i: ', i)
        if i == 1:
            gui.moveTo(right_direc_loc)
            time.sleep(0.2)
            game.press_single_key_in_background('e')
            
        elif i <= 5:
            gui.moveTo(lowright_direc_loc)
            time.sleep(0.2)
            game.press_single_key_in_background('e')
            
        elif i == 6:
            gui.moveTo(upright_direc_loc)
            time.sleep(0.2)
            game.press_single_key_in_background('e')
            
        elif i <= 9:
            gui.moveTo(upleft_direc_loc)
            time.sleep(0.2)
            game.press_single_key_in_background('e')
            
        elif i == 10:
            gui.moveTo(upright_direc_loc)
            time.sleep(0.2)
            game.press_single_key_in_background('e')
            
        elif i <= 14:
            gui.moveTo(lowright_direc_loc)
            time.sleep(0.2)
            game.press_single_key_in_background('e')
        
        else:
            leifengta_guangjiao_close(game)
            tmp_flag = leifengta_fangshi_rec_floor_complete(game)
            if tmp_flag == True:
                return True
    
            break          

        time.sleep(0.4)
        leifengta_monster_process(game,monster_range_loc1,monster_range_loc2)

        #识别怪物数量，或者识别文字提示，决定是否进入下一层
        tmp_flag = leifengta_fangshi_rec_floor_complete(game)
        if tmp_flag == True:
            return True
    
    return False

#识别怪物数量，或者识别文字提示(暂定，如果数字识别不好使，添加文字识别，在leifengta_monster_process中添加文字识别)，决定是否进入下一层
def leifengta_fangshi_rec_floor_complete(game):

    text_list = recognize_monster_number(game,extend=1,gui=True)
    if int(text_list[-1]) >= 180:
        text_list[-1] = '160'
    
    if int(text_list[-1]) >= 160 and int(text_list[0]) <= int(text_list[-1])\
         and  int(text_list[0]) >= 0:
        if int(text_list[0]) >= int(int(text_list[-1]) * 0.82):
            leifengta_guangjiao_close(game)
            go_to_next_floor(game)
            print('current area monster num has been completed!')
            return True
    else:
        print('LeiFengTa monster number recognized error!')
        pass 

    return False

def leifengta_monster_process(game:GameControl, range_loc1, range_loc2):
    
    start_time = time.time()

    coordinate_list = []
    loc_repeat_flag = False

    wengguai_img_list= [r'F:\01_game_ctr\lib\img\leifengta\monster_wengguai.png',
                        r'F:\01_game_ctr\lib\img\leifengta\monster_wengguai1.png',
                        r'F:\01_game_ctr\lib\img\leifengta\monster_wengguai2.png']

    tmp_retry_cunt = 0
    tmp_attacck_cunt = 0

    while True and (False == loc_repeat_flag):

        maxLoc, img_name = game.find_game_multi_img(wengguai_img_list,part=1,pos1=range_loc1,\
                                                    pos2=range_loc2,thread=0.65,image_show=False)  
        if maxLoc != False:
            coordinate_list.append(maxLoc)
            gui.moveTo(maxLoc)
            game.press_single_key_in_background('2') # 卷风
            time.sleep(1.2)
            tmp_attacck_cunt = tmp_attacck_cunt + 1
            #game.press_single_key_in_background('3') # 长风
            #time.sleep(0.5)
        else:
            tmp_retry_cunt = tmp_retry_cunt + 1
            time.sleep(0.2)
            if tmp_retry_cunt > 3: 
                break

        coordinate_counts = Counter(coordinate_list)
        for coordinate, count in coordinate_counts.items():
            print('coordinate:',coordinate, count)
            if count > 3:
                loc_repeat_flag = True
                break

        print('tmp_attacck_cunt: ', tmp_attacck_cunt)
        #每次攻击次数不能超过4
        if tmp_attacck_cunt > 4:
            break

    game.press_single_key_in_background('6')
    time.sleep(0.5)

    print('leifengta_monster_process time:', time.time() - start_time)
    if time.time() - start_time < 5:
        time.sleep(5 - (time.time() - start_time))

def leifengta_guangjiao_close(game:GameControl):
                
    close_img_list = [r'F:\01_game_ctr\lib\img\leifengta\guangjiao_close.png']
    maxLoc,img_name= game.find_game_multi_img(close_img_list,part=1,pos1=game.window_pos1,\
                                              pos2=game.window_pos2,thread=0.80)
    if maxLoc != False:
        print('close guangjiao!')
        gui.moveTo(maxLoc)
        gui.leftClick()
        time.sleep(0.5)

def leifengta_check_is_guangjiao(game:GameControl):
    gungjiao_img_list = [r'F:\01_game_ctr\lib\img\leifengta\guangjiao.png']
    maxLoc,img_name= game.find_game_multi_img(gungjiao_img_list,part=1,pos1=game.window_pos1,\
                                              pos2=game.window_pos2,thread=0.70)
    if maxLoc != False:
        return True

    return False

def leifengta_guangjiao_open(game:GameControl):

    tmp_flag = leifengta_check_is_guangjiao(game)

    if False == tmp_flag:
        guangjiao_entre_img_list = [r'F:\01_game_ctr\lib\img\leifengta\guangjiao_entrance.png']
        maxLoc,img_name= game.find_game_multi_img(guangjiao_entre_img_list,part=1,pos1=game.window_pos1,\
                                                pos2=game.window_pos2,thread=0.80)
        if maxLoc != False:
            print('open guangjiao!')
            gui.moveTo(maxLoc)
            gui.leftClick()
            time.sleep(0.5)

def leifengta_guangjiao_modify_at_floor_start(game:GameControl):
        
    game.activate_window()
    time.sleep(0.5)

    img_list= [r'F:\01_game_ctr\lib\img\leifengta\guangjiao.png']
    maxLoc, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.65,image_show=False)  
    if maxLoc != False:
        #gui.moveTo(maxLoc1)
        button_pos1 = (maxLoc[0]-25,maxLoc[1]-25)
        button_pos2 = (maxLoc[0]+290,maxLoc[1]+25)
        img_list= [r'F:\01_game_ctr\lib\img\leifengta\guangjiao_button.png']
        maxLoc1, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=button_pos1,\
                                                        pos2=button_pos2,thread=0.65,image_show=False)
        if maxLoc1 != False:
            print(maxLoc[0]-maxLoc1[0])
            if maxLoc1[0] - maxLoc[0] > 80:
                gui.moveTo(maxLoc1)
                gui.dragRel(maxLoc[0]-maxLoc1[0],0,0.5)
            else:
                gui.moveTo(maxLoc1)
                #先右移调整视角
                gui.dragRel(maxLoc1[0]-maxLoc[0],0,0.5)
                time.sleep(0.5)
                #再左移
                gui.dragRel(2*(maxLoc[0]-maxLoc1[0]),0,0.5)

def lengfengta_fangshi_do(game:GameControl):

    first_run_tmp = True
    floor_img = [r'F:\01_game_ctr\lib\img\leifengta\floor_136.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_137.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_138.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_139.png',
                 r'F:\01_game_ctr\lib\img\leifengta\floor_140.png']
    while True:
        img_index = 5
        start_loc_index = 0
        reset_slaver = False
        #find_yanzhengma(game,game_list)
        maxLoc, img_name = game.find_game_multi_img(floor_img,part=1,pos1=game.window_pos1,\
                                                    pos2=game.window_pos2,thread=0.70)
        if maxLoc != False:
            if img_name == 'floor_136.png':
                img_index = 0
                leifengta_recover_health(game)
            if img_name == 'floor_137.png':
                img_index = 1
            if img_name == 'floor_138.png':
                img_index = 2
            if img_name == 'floor_139.png':
                img_index = 3
            if img_name == 'floor_140.png':
                img_index = 4

            if img_index < 4:
                #before moving, check number of killed monster, if condition is met, go to next floor directly
                text_list = recognize_monster_number(game,extend=1,gui=True)
                if int(text_list[-1]) >= 180:
                    text_list[-1] = '160'
                
                if int(text_list[0]) >= int(int(text_list[-1]) * 0.82) and int(text_list[-1]) >= 160\
                  and int(text_list[0]) <= int(text_list[-1]) and  int(text_list[0]) >= 0:
                    go_to_next_floor(game)
                    game.wait_game_img(floor_img[img_index+1],part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
                else:
                    if first_run_tmp:
                        first_run_tmp = False
                        # if game.get_slaver_run_time() > 1800 or game.slaver_start_time == 0:
                        #     game.reset_slaver_start_time()
                        #     reset_slaver = True
                        # reset_multi_player_status_in_dungon(game,game_list,follow=True,reset_slver=reset_slaver)
                        # game.press_single_key_in_background('f9')
                        # time.sleep(5)

                    # 对于方士运行脚本时，初始位置定位暂定，目前默认都是每层开始的位置
                    # if int(text_list[0]) <= int(int(text_list[-1]) * 0.2):
                    #     start_loc_index = 0
                    # elif int(text_list[0]) <= int(int(text_list[-1]) * 0.4):
                    #     start_loc_index = 2
                    # elif int(text_list[0]) <= int(int(text_list[-1]) * 0.6):
                    #     start_loc_index = 5

                    cancel_followed_with_leftclcik(game)
                    leifengta_guangjiao_open(game)
                    leifengta_guangjiao_modify_at_floor_start(game)
                    tmp_flag = leifengta_move_with_guangjiao(game)
                    if tmp_flag:
                        game.wait_game_img(floor_img[img_index+1],part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.70,max_time=10)
            elif img_index == 4:
                maxLoc = game.find_game_img(r'F:\01_game_ctr\lib\img\common\map.png',part=1,\
                                pos1=game.window_pos1,pos2=game.window_pos2,image_show=False,thread=0.67)
                if maxLoc != False:
                    game.press_single_key_in_background('r') # close map
                followed_with_rightclick(game)
                return True
            else:
                return False

def leifengta_recover_health(game:GameControl):
    
    game.activate_window()
    time.sleep(0.2)

    find_npc_by_search(game, r'F:\01_game_ctr\lib\img\leifengta\npc_yishi.png', 'ys')

    maxLoc = game.wait_game_img(r'F:\01_game_ctr\lib\img\leifengta\recover_health.png',\
                            part=1,pos1=game.window_pos1,pos2=game.window_pos2,thread=0.64,max_time=10)
    if maxLoc != False:
        gui.moveTo(maxLoc)
        gui.leftClick()

def leifengta_fangshi_main(game:GameControl):

    first_run_flag = True
    srart_step = 0
    while True:

        if first_run_flag:
            first_run_flag = True
            tmp_sts = leifengta_determin_scene(game)
            if tmp_sts:
                srart_step = 1
            else:
                srart_step = 2

        if srart_step == 1:
            tmp_flag = enter_leifengta_dungeon(game)
            if tmp_flag == False:
                raise print('enter into leifengta dungeon failed')
            srart_step = srart_step + 1
        
        if srart_step == 2:
            tmp_flag = lengfengta_fangshi_do(game)
            if tmp_flag == False:
                raise print('cannot recognize the scene of the tower')
            srart_step = srart_step + 1

        if srart_step == 3:
            tmp_flag = wait_for_master_player(game,'team1')
            if tmp_flag == False:
                print('not wait for player')
            srart_step = srart_step + 1

        #一台电脑，爬塔每次执行一次
        break

        if srart_step == 4:
            tmp_flag = leave_leifengta_dungeon(game)
            if tmp_flag == False:
                print('leave LeiFengTa dungeon Failed, reset first_run_flag')
                first_run_flag = True
                
            srart_step = 1
