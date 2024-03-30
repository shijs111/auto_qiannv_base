from src.common_operation import *
dungeon_one_start_origin_loc = (1152, 442)

dungeon_one_origin_loc_list = [(1144, 475),(1183, 532),(1090, 547),(1091, 590),(971, 570),\
                               (971, 570),(872, 645),(872, 645),(872, 645),(781, 709),\
                               (781, 709),(583, 731),(583, 731),(583, 731),(434, 705)]

dungeon_one_boss_origin_loc = (434, 705)


dungeon_two_start_origin_loc = (1157, 624)

dungeon_two_origin_loc_list = [(993, 679),(993, 679),(993, 679),(812, 711),(812, 711),\
                               (812, 711),(671, 748),(671, 748),(671, 748),(611, 698),\
                                (611, 698),(725, 672),(725, 672),(845, 646),(845, 646)]

dungeon_two_boss_origin_loc = (845, 646)

dungeon_three_origin_loc = (790, 780)

dungeon_four_start_origin_loc = (954, 457)

dungeon_four_origin_loc_list = [(906, 549),(906, 549),(906, 549),(765, 580),(765, 580),\
                                (625, 582),(625, 582),(625, 582),(624, 645),(624, 645),\
                                (835, 727),(835, 727),(835, 727),(948, 792),(948, 792)]

dungeon_four_boss_origin_loc = (948, 792)

boss0_name_str_list = ['沙','岸','鬼']
boss1_name_str_list = ['幽','魂','骁','骑']
boss2_name_str_list = ['灯','烬','梦','魇']
boss3_name_str_list = ['幻','水','魔']

def qiujiang_area_location_list_preprocess(game:GameControl,loc_list:list):
    area_new_list = []
    for area_loc in loc_list:
        new_loc = (game.window_pos1[0]+area_loc[0], game.window_pos1[1]+area_loc[1])
        area_new_list.append(new_loc)

    return area_new_list

def qiujiang_location_preprocess(game:GameControl,loc):
    new_loc = (game.window_pos1[0]+loc[0], game.window_pos1[1]+loc[1])
    return new_loc


def qiujiang_dungeon_move(game:GameControl,game_ctrl_list,dungeon_index):

    first_run = True
    move_flag = False
    loc_index = 0

    err_rec_cunt = 0
    normal_rec_diff_cunt = 0
    pre_rec_monster_cunt = 0

    while True:
        #识别当前怪物数量
        # 1. 如果text[-1] 为0， text无效，不处理这个数据
        # 2. text有效时，识别text[0] 是否不变，不变次数累计到3，认为怪物处理完毕条件①满足
        # 3. 当text[0] 不变条件满足时，判断text[0]%怪物单位数量 是否为0， 为0 则任务怪物处理完毕条件②满足
        # 4. 条件① 和 条件②满足时，认为当前数量处理完毕，move_flag 设置为True， loc_index 加一，用于 坐标移动
        while True:
            text = recognize_monster_number(game,extend=2,gui=True)
            if int(text[-1]) != 0 and (int(text[0]) >= 0 and int(text[0]) <= 150):

                #识别正确，错误次数清零
                err_rec_cunt = 0

                #如果第一次运行时，发现识别到怪物数量有效，则根据怪物数量设置下loc_index的初始值
                if first_run:
                    first_run = False
                    pre_rec_monster_cunt = int(text[0])
                    #识别下怪物数量，设置loc_index的初始值
                    
                    #并初始移动到loc_index的地址

                    #移动完成之后，等待对应的时间，后面的判断代码，在初始first_run时，先不做判断

                    continue

                # 2. text有效时，识别text[0] 是否不变，不变次数累计到3，认为怪物处理完毕条件①满足
                if pre_rec_monster_cunt != text[0]:
                    pre_rec_monster_cunt = text[0]
                    normal_rec_diff_cunt = 0
                else:
                    normal_rec_diff_cunt = normal_rec_diff_cunt + 1

                # 3. 当text[0] 不变条件满足时，判断text[0]%怪物单位数量 是否为0， 为0 则任务怪物处理完毕条件②满足
                # 4. 条件① 和 条件②满足时，认为当前数量处理完毕，move_flag 设置为True， loc_index 加一，用于 坐标移动
                if  normal_rec_diff_cunt > 3:
                    #直接识别当前的怪物击杀数量 是否等于 当前副本的怪物数量上限，达到上限认为dungeon_move 处理完毕，返回True
                    if int(text[-1]) == int(text[0]):
                        print('qingjiang current dungeon has been cleared!, text: ',int(text[-1]), int(text[0]))
                        return True
                    else:
                        if int(text[0]) % 10 == 0: # 这里暂定10，因为dungen_two的单位数量不是10 TBD 2024.03.09
                            normal_rec_diff_cunt = 0
                            loc_index = loc_index + 1
                            move_flag = True
                        else:
                            print('waiting... waiting... waiting...!!!')
                            pass                           
            else:
                #未识别到怪物数量，且first_run 为True， 则执行一下移动到该副本的初始位置
                if first_run:
                    first_run = False
                    pass
                else:
                    #识别错误，正确次数清零
                    normal_rec_diff_cunt = 0

                    #不是第一次运行，但是又一直每识别到怪物数量，当识别错误次数累计到12次之后，种植数量识别循环，直接进入下一个loc_index
                    err_rec_cunt = err_rec_cunt + 1
                    if err_rec_cunt > 12:
                        err_rec_cunt = 0
                        print('retry 12 times to recognize the number, but not rec, go to next loc_index!!!')
                        break
            
            time.sleep(1)

        # move_flag 为 True时，处理移动
        # 1. move_flag 设置为False
        # 2. 判断loc_index 是否超过 loc_list 的最大数量，超过则结束当前move，反之使用loc_index的对应loc在当前地图移动
        if move_flag:
            move_flag = False
            if loc_index > len():
                break

        pass