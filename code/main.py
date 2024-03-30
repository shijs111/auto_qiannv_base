from tools.logsystem import MyLog
from src.zhanlong import *
from src.shangkuai import *
from src.siseyu import *
from src.leifengta import *
from src.hebo import *
from src.qingwa import *
from src.taohua import *
from src.yeyan import *
from src.zhuagui import *
import ctypes
import logging
import sys
import win32gui



def init():
    pass

def custom_excepthook(type, value, traceback, logger):
    # 记录异常信息到日志
    logger.error("Uncaught exception", exc_info=(type, value, traceback))

class UseModelFilter(logging.Filter):
    def filter(self, record):
        return "use model" not in record.getMessage()
    
def setup_logger():
    # 获取当前时间
    current_time = datetime.datetime.now()
    # 构造日志文件名
    log_file_name = current_time.strftime("%Y%m%d%H%M%S") + ".txt"
    # 创建日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 创建文件处理器
    file_handler = logging.FileHandler(r'F:\01_game_ctr\lib\log'+'\\'+log_file_name,encoding='utf-8')
    print(r'F:\01_game_ctr\lib'+'\\'+log_file_name)
    file_handler.setLevel(logging.INFO)

    # 创建格式化器
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 创建自定义过滤器
    use_model_filter = UseModelFilter()
    file_handler.addFilter(use_model_filter)

    # 将处理器添加到记录器
    logger.addHandler(file_handler)

    # 设置异常处理钩子
    sys.excepthook = lambda etype, value, traceback: custom_excepthook(etype, value, traceback, logger)

    return logger

def is_admin():
    # UAC申请，获得管理员权限
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def my_excepthook(exc_type, exc_value, tb):
    msg = ' Traceback (most recent call last):\n'
    while tb:
        filename = tb.tb_frame.f_code.co_filename
        name = tb.tb_frame.f_code.co_name
        lineno = tb.tb_lineno
        msg += '   File "%.500s", line %d, in %.500s\n' % (
            filename, lineno, name)
        tb = tb.tb_next

    msg += ' %s: %s\n' % (exc_type.__name__, exc_value)

    logging.error(msg)

def get_game_control_boject(version,server,player_list,logger:logging):
    gameControl_list = []
    for player in player_list:
        try:
            hwnd = win32gui.FindWindow(0, f'新倩女幽魂Online 版本[{version}] 服务器[{server}] 玩家ID[{player}] 次世代')
        except:
            hwnd = 0
        
        print('hwnd:',hwnd)

        if hwnd != 0:
           tmp_game = GameControl(hwnd,player,logger)
           gameControl_list.append(tmp_game)

    return gameControl_list

def get_single_player_game_ctrl(version,server,player_list,logger:logging):

    for player in player_list:
        try:
            hwnd = win32gui.FindWindow(0, f'新倩女幽魂Online 版本[{version}] 服务器[{server}] 玩家ID[{player}] 次世代')
        except:
            hwnd = 0
        
        if hwnd != 0:
            single_game = GameControl(hwnd,player,logger)
            return single_game
    return None

team_list1 = []# member

team_list2 = []# member

version_id = '911086'
server_name1 = '' #
server_name = '' # 区名

team_leader =[] # leader

player_shangkuai_list = []


if __name__ == "__main__":

    if is_admin():
        
        log = setup_logger()

        #init
        #game_members_list = get_game_control_boject(version_id,server_name,team_list2,log)
        #game_leader = get_single_player_game_ctrl(version_id,server_name,team_leader,log)

        #zhuagui_main(game_leader)

        #快速退游戏
        #close_all_game_windows()

        #set buff
        #set_player_buff_main(game_leader,game_members_list,pick_up=True)

        #yeyan_main_task(game_leader,game_members_list)
        
        # 初始登录账号之后，六个窗口叠加一起，这时记录的窗口坐标都一样
        # 执行完 auto_operation 之后，窗口位置调整了，这时不能继续执行任务，需要取消 auto_operation 重置初始化game对象
        #auto_operation_at_init(game_leader,game_members_list)
        
        # summon_retinue(game_leader,game_members_list,bone=False)

        # siseyu_main(game_leader,game_members_list)
        # qingwa_main(game_leader,game_members_list)
        # hebo_task_main(game_leader,game_members_list)
        # taohua_task_main(game_leader,game_members_list)

        # summon_retinue(game_leader,game_members_list,bone=True)
        # bajiaota_main(log,game_leader,game_members_list)

        # try:
        #     bajiaota_main(log,game_leader,game_members_list)
        # except:
        #     print('1/n')
        #     print('1/n')
        #     print('1/n')
        #     print('shutdown!')
        #     time.sleep(60)
        #     os.system("shutdown /s /t 1")

        # print('22/n')
        # print('22/n')
        # print('22/n')
        # print('shutdown!')
        # time.sleep(60)
        # os.system("shutdown /s /t 1")

        #leifengta_main(game_leader,game_members_list)
        
        #关机，关闭电脑
        #os.system("shutdown /s /t 1")

        game = get_single_player_game_ctrl(version_id,server_name,[''],log)

        zhanlong_main(game)

        #task_shangkuai(game)

        # leifengta_fangshi_main(game)

        # game.activate_window()
        # time.sleep(0.5)

        # img_list= [r'F:\01_game_ctr\lib\img\leifengta\monster_wengguai.png']
        # maxLoc, img_name1 = game.find_game_multi_img(img_list,part=1,pos1=game.window_pos1,\
        #                                                pos2=game.window_pos2,thread=0.65,image_show=False)  
        # if maxLoc != False:
        #     gui.moveTo(maxLoc)


        #game.window_port_shot_with_gui(pos1=game.window_pos1,pos2=game.window_pos2,shot=True)
        #get_location_whit_pict()
        
        #game_shuangkuai_list = get_game_control_boject(version_id,server_name,player_for_shangkuai_list,log)
        #shangkuai_main(game_shuangkuai_list)


        # single test
        # game_single = get_single_player_game_ctrl(version_id,server_name,[''],log)

        # game_single.activate_window()
        # while True:


        #     img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_entrance_pre.png']
        #     maxLoc1, img_name1 = game_single.find_game_multi_img(img_list,part=1,pos1=game_single.window_pos1,\
        #                                                 pos2=game_single.window_pos2,thread=0.75,image_show=False)  
        #     if maxLoc1 != False:
        #         gui_npc_loc = (maxLoc1[0],maxLoc1[1]+50)
        #         gui.moveTo(gui_npc_loc)
        #         gui.leftClick()
        #         time.sleep(0.2)

        #     entrance_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_entrance.png']
        #     maxLoc, img_name = game_single.find_game_multi_img(entrance_img_list,part=1,pos1=game_single.window_pos1,\
        #                                                 pos2=game_single.window_pos2,thread=0.75,image_show=False)  
        #     if maxLoc != False:
        #         gui.moveTo(maxLoc)
        #         break
        #     else:
        #         npc_loc_img_list= [r'F:\01_game_ctr\lib\img\zhuagui\gui_npc_loc.png']
        #         maxLoc2, img_name2 = game_single.find_game_multi_img(npc_loc_img_list,part=1,pos1=game_single.window_pos1,\
        #                                                     pos2=game_single.window_pos2,thread=0.75,image_show=False)
        #         if maxLoc2 != False:
        #             npc_loc = (maxLoc2[0]+50,maxLoc2[1])
        #             gui.moveTo(npc_loc)
        #             gui.leftClick()
        #             time.sleep(1)
        #     time.sleep(2)


        #获取窗口坐标
        #get_location_whit_pict(game_leader)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
