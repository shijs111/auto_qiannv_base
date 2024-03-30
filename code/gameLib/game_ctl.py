import ctypes
import logging
import os
import sys
import time
import traceback
import random
import cv2
import numpy as np
import win32api
import win32con
import win32gui
import win32ui
from tools.logsystem import MyLog
from PIL import Image,ImageDraw
import pyautogui as gui
from cnocr import CnOcr
from ctypes import windll,byref
from ctypes.wintypes import POINT
from concurrent.futures import ThreadPoolExecutor
import string
import datetime

PostMessageW = windll.user32.PostMessageW
MapVirtualKeyW = windll.user32.MapVirtualKeyW
VkKeyScanA = windll.user32.VkKeyScanA
ClientToScreen = windll.user32.ClientToScreen

WM_KEYDOWN = 0x100
WM_KEYUP = 0x101
WM_MOUSEMOVE = 0x0200
WM_LBUTTONDOWN = 0x0201
WM_LBUTTONUP = 0x0202
WM_RBUTTONDOWN = 0x0204
WM_RBUTTONUP = 0x0205
WM_MOUSEWHEEL = 0x020A
WHEEL_DELTA = 120

VkCode = {
    "back":  0x08,
    "tab":  0x09,
    "return":  0x0D,
    "shift":  0x10,
    "control":  0x11,
    "menu":  0x12,
    "pause":  0x13,
    "capital":  0x14,
    "escape":  0x1B,
    "space":  0x20,
    "end":  0x23,
    "home":  0x24,
    "left":  0x25,
    "up":  0x26,
    "right":  0x27,
    "down":  0x28,
    "print":  0x2A,
    "snapshot":  0x2C,
    "insert":  0x2D,
    "delete":  0x2E,
    "lwin":  0x5B,
    "rwin":  0x5C,
    "numpad0":  0x60,
    "numpad1":  0x61,
    "numpad2":  0x62,
    "numpad3":  0x63,
    "numpad4":  0x64,
    "numpad5":  0x65,
    "numpad6":  0x66,
    "numpad7":  0x67,
    "numpad8":  0x68,
    "numpad9":  0x69,
    "multiply":  0x6A,
    "add":  0x6B,
    "separator":  0x6C,
    "subtract":  0x6D,
    "decimal":  0x6E,
    "divide":  0x6F,
    "f1":  0x70,
    "f2":  0x71,
    "f3":  0x72,
    "f4":  0x73,
    "f5":  0x74,
    "f7":  0x76,
    "f8":  0x77,
    "f6":  0x75,
    "f9":  0x78,
    "f10":  0x79,
    "f11":  0x7A,
    "f12":  0x7B,
    "numlock":  0x90,
    "scroll":  0x91,
    "lshift":  0xA0,
    "rshift":  0xA1,
    "lcontrol":  0xA2,
    "rcontrol":  0xA3,
    "lmenu":  0xA4,
    "rmenu":  0XA5
}

# "ID: 称呼"
player_info_dict = {

}

game_active_state_dict = {}

class GameControl():
    def __init__(self, hwnd,player_id, logger:logging, quit_game_enable=1):
        '''
        初始化
            :param hwnd: 需要绑定的窗口句柄
            :param quit_game_enable: 程序死掉时是否退出游戏。True为是，False为否
        '''
        self.log = logger
        self.monster_name_pos1 = (447, 48)                #bajiaota_task monster
        self.monster_name_pos2 = (547, 67)            #bajiaota_task monster
        self.monster_attribute_pos1 = (447, 78)
        self.monster_attribute_pos2 = (547, 98)
        self.time_pos_top = (816, 63)            #bajiaota_task time
        self.time_pos_bot = (870, 81)            #bajiaota_task time
        self.shangkuai_time = 0xFFFF
        self.shangkuai_complete_cunt = 0
        self.shangkuai_road = 0
        self.shangkuai_npc_num = 0
        self.run = True
        self.hwnd = hwnd
        self.player_id = player_id
        self.quit_game_enable = quit_game_enable
        self.debug_enable = False
        l1, t1, r1, b1 = win32gui.GetWindowRect(self.hwnd)
        self.window_pos1 = (l1, t1)
        self.window_pos2 = (r1, b1)
        print(l1,t1, r1,b1)
        self._window_h = b1 - t1
        self._window_w = r1 - l1
        self.clickpos = []
        self.player = self.get_player_chara_name() #log
        self.monster_appear_sts = 0xff                #bajiaota_task
        self.mem_img_w = 0                         #bitmap img size w
        self.mem_img_h = 0                         #bitmap img size h
        self.slaver_start_time = 0

        #for summoning retinue
        self.summon_wait_time = 0
        self.summon_target_count = 5
        self.summon_current_count = 0
        self.summon_timer = None
        #self.activate_window()
        #time.sleep(0.5)

        #for BaJiaoTa
        self.bajiaota_road_str = ''
        
        #for equipment
        self.roll_cunt = 0

    def set_summon_wait_time(self, wait_time):
        self.summon_wait_time = wait_time

    def set_summon_current_count(self, target_count):
        self.summon_target_count = target_count

    def get_slaver_run_time(self):
        return time.time() - self.slaver_start_time
    
    def reset_slaver_start_time(self):
        self.slaver_start_time = time.time()

    def bajiaota_set_monster_appear_sts(self,value):
        self.monster_appear_sts = value

    def bajiaota_get_monster_appear_sts(self):
        return self.monster_appear_sts

    def bajiaota_reset_monster_appear_sts(self):
        self.monster_appear_sts = 0xFF

    def get_player_chara_name(self):
        if self.player_id in player_info_dict:
            return player_info_dict[self.player_id]

    def move_to(self, hwnd, x: int, y: int):
        """移动鼠标到坐标(x,y)

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        wparam = 0
        lparam = x << 16 | y
        PostMessageW(hwnd, WM_MOUSEMOVE, wparam, lparam)


    def left_click_down(self, x: int, y: int):
        """在坐标(x, y)按下鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        wparam = 0
        lparam = x << 16 | y
        PostMessageW(self.hwnd, WM_LBUTTONDOWN, wparam, lparam)


    def left_click_up(self, x: int, y: int):
        """在坐标(x, y)放开鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(self.hwnd, WM_LBUTTONUP, wparam, lparam)

    def right_click_down(self, x: int, y: int):
        """在坐标(x, y)按下鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(self.hwnd, WM_RBUTTONDOWN, wparam, lparam)


    def right_click_up(self, x: int, y: int):
        """在坐标(x, y)放开鼠标左键

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        wparam = 0
        lparam = y << 16 | x
        PostMessageW(self.hwnd, WM_RBUTTONUP, wparam, lparam)

    def scroll(self, hwnd, delta: int, x: int, y: int):
        """在坐标(x, y)滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            delta (int): 为正向上滚动，为负向下滚动
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.move_to(hwnd, x, y)
        wparam = delta << 16
        p = POINT(x, y)
        ClientToScreen(hwnd, byref(p))
        lparam = p.y << 16 | p.x
        PostMessageW(hwnd, WM_MOUSEWHEEL, wparam, lparam)


    def scroll_up(self, x: int, y: int):
        """在坐标(x, y)向上滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.scroll(self.hwnd, WHEEL_DELTA, x, y)


    def scroll_down(self, x: int, y: int):
        """在坐标(x, y)向下滚动鼠标滚轮

        Args:
            handle (HWND): 窗口句柄
            x (int): 横坐标
            y (int): 纵坐标
        """
        self.scroll(self.hwnd, -WHEEL_DELTA, x, y)

    def get_virtual_keycode(self,key: str):
        """根据按键名获取虚拟按键码

        Args:
            key (str): 按键名

        Returns:
            int: 虚拟按键码
        """
        if len(key) == 1 and key in string.printable:
            return VkKeyScanA(ord(key)) & 0xff
        else:
            return VkCode[key]


    def key_down(self, key: str):
        """按下指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.get_virtual_keycode(key)
        scan_code = MapVirtualKeyW(vk_code, 0)
        wparam = vk_code
        lparam = (scan_code << 16) | 1
        PostMessageW(self.hwnd, WM_KEYDOWN, wparam, lparam)


    def key_up(self, key: str):
        """放开指定按键

        Args:
            handle (HWND): 窗口句柄
            key (str): 按键名
        """
        vk_code = self.get_virtual_keycode(key)
        scan_code = MapVirtualKeyW(vk_code, 0)
        wparam = vk_code
        lparam = (scan_code << 16) | 0XC0000001
        PostMessageW(self.hwnd, WM_KEYUP, wparam, lparam)

    def press_single_key_in_background(self,key: str,time_keep = 0):
        self.key_down(key)
        time.sleep(time_keep)
        self.key_up(key)
    
    def recognize_text(self,pos1,pos2,gray=1,gui_flag=False,image_show=False):
        #{'text': '死亡]亲奥卫兵', 'score': 0.9520835280418396}
        top_left = pos1#(447, 48)
        bottom_right = pos2#(547, 67)
        if gui_flag:
            img = self.window_part_shot_with_gui(top_left,bottom_right,gray=gray,shot=True)
        else:
            img = self.window_part_shot(top_left,bottom_right,gray=gray,image_show=image_show)

        ocr = CnOcr()
        res = ocr.ocr_for_single_line(img)
        return res

    def set_click_pos(self,x,y):
        self.clickpos = [x,y]

    def init_mem(self):
        self.hwindc = win32gui.GetWindowDC(self.hwnd)
        self.srcdc = win32ui.CreateDCFromHandle(self.hwindc)
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.bmp = win32ui.CreateBitmap()
        self.bmp.CreateCompatibleBitmap(
            self.srcdc, self._window_w, self._window_h)
        self.memdc.SelectObject(self.bmp)

    def capture_screen(self,pos1, pos2):
        try:
            #print('pos1, pos2:',pos1, pos2)
            left = min(pos1[0], pos2[0])
            top = min(pos1[1], pos2[1])
            right = max(pos1[0], pos2[0])
            bottom = max(pos1[1], pos2[1])

            width = right - left
            height = bottom - top

            screenshot = gui.screenshot()
            cropped_image = screenshot.crop((left, top, right, bottom))
            resized_image = cropped_image.resize((width, height))  # 可选：如果需要固定尺寸的截图，请添加此行代码

            rgb_image = resized_image.convert("RGB")
            rgb_data = np.array(rgb_image)

            # region_width = 40
            # region_height = 10

            # pt1 = (int(self.clickpos[0] - region_width/2), int(self.clickpos[1] - region_height/2))
            # pt2 = (int(self.clickpos[0] + region_width/2), int(self.clickpos[1]))

            # draw = ImageDraw.Draw(rgb_image)
            # draw.rectangle([pt1, pt2], outline="red")
            # rgb_image.show()

            return rgb_data
        except Exception as e:
            print(f"Error capturing screen: {str(e)}")
            return None

    def window_full_shot(self, gray=0,image_show=False):
        """
        窗口截图
            :param file_name=None: 截图文件的保存名称
            :param gray=0: 是否返回灰度图像，0：返回BGR彩色图像，其他：返回灰度黑白图像
            :return: file_name为空则返回RGB数据
        """
        try:
            if (not hasattr(self, 'memdc')):
                self.init_mem()

            current_time = datetime.datetime.now()
            img_file_name = 'FULL_'+current_time.strftime("%Y%m%d%H%M%S") + ".png"
            img_file_path = r"F:\01_game_ctr\lib\mem_screen_img" + '\\'+ img_file_name

            self.memdc.BitBlt((0, 0), (self._window_w, self._window_h), self.srcdc,
                                (0, 0), win32con.SRCCOPY)
            if image_show:
                self.bmp.SaveBitmapFile(self.memdc, img_file_path)

            signedIntsArray = self.bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (self._window_h, self._window_w, 4)
            if image_show:
                cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
                cv2.waitKey(0)

            if gray == 0:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        except Exception:
            self.init_mem()
            logging.warning('window_full_shot执行失败')
            a = traceback.format_exc()
            logging.warning(a)

    def window_part_shot(self, pos1, pos2, file_name=None, gray=0,image_show=False):
        """
        窗口区域截图
            :param pos1: (x,y) 截图区域的左上角坐标
            :param pos2: (x,y) 截图区域的右下角坐标
            :param file_name=None: 截图文件的保存路径
            :param gray=0: 是否返回灰度图像，0：返回BGR彩色图像，其他：返回灰度黑白图像
            :return: file_name为空则返回RGB数据
        """
        w = pos2[0]-pos1[0]
        h = pos2[1]-pos1[1]
        #self.log.info('%s,w:%d,h:%d',self.player,w,h,)
        hwindc = win32gui.GetWindowDC(self.hwnd)
        srcdc = win32ui.CreateDCFromHandle(hwindc)
        memdc = srcdc.CreateCompatibleDC()
        bmp = win32ui.CreateBitmap()
        bmp.CreateCompatibleBitmap(srcdc, w, h)
        memdc.SelectObject(bmp)

        memdc.BitBlt((0, 0), (w, h), srcdc,
                     (pos1[0], pos1[1]), win32con.SRCCOPY)

        if file_name != None:
            bmp.SaveBitmapFile(memdc, file_name)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            return
        else:
            signedIntsArray = bmp.GetBitmapBits(True)
            img = np.fromstring(signedIntsArray, dtype='uint8')
            img.shape = (h, w, 4)
            srcdc.DeleteDC()
            memdc.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwindc)
            win32gui.DeleteObject(bmp.GetHandle())
            if image_show:
                cv2.imshow("image", cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
                cv2.waitKey(0)
            if gray == 0:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            else:
                return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)

    def window_part_shot_with_gui(self, pos1, pos2, gray=0, shot = False):

        left = min(pos1[0], pos2[0])
        top = min(pos1[1], pos2[1])
        right = max(pos1[0], pos2[0])
        bottom = max(pos1[1], pos2[1])

        width = right - left
        height = bottom - top

        screenshot = gui.screenshot(region=(left, top, width, height))
        img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        if shot:
            
            cv2.imwrite(r'F:\01_game_ctr\lib\ScreenPrint\temp.png', img)
        if gray == 0:
            return cv2.cvtColor(img, cv2.IMREAD_COLOR)
        else:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #检查特定坐标范围的图片，调试使用
    def showPictureWithCoord(self,x,y):

        # 指定截取图片大小
        width, height = 50, 50

        # 计算目标坐标周围的区域
        left, top = x - width // 2, y - height // 2
        right, bottom = x + width // 2, y + height // 2

        # 使用 PyAutoGUI 截取制定范围的屏幕截图
        screenshot = gui.screenshot(region=(left, top, width, height))

        # 展示截屏结果
        screenshot.show()

    def find_color(self, region, color, tolerance=0):
        """
        寻找颜色
            :param region: ((x1,y1),(x2,y2)) 欲搜索区域的左上角坐标和右下角坐标
            :param color: (r,g,b) 欲搜索的颜色
            :param tolerance=0: 容差值
            :return: 成功返回客户区坐标，失败返回-1
        """
        img = Image.fromarray(self.window_part_shot(
            region[0], region[1]), 'RGB')
        width, height = img.size
        print('width, height:',width, height)
        r1, g1, b1 = color[:3]
        for x in range(width):
            for y in range(height):
                try:
                    pixel = img.getpixel((x, y))
                    r2, g2, b2 = pixel[:3]

                    if abs(r1-r2) <= tolerance and abs(g1-g2) <= tolerance and abs(b1-b2) <= tolerance:
                        return x+region[0][0], y+region[0][1]
                except Exception:
                    logging.warning('find_color执行失败')
                    a = traceback.format_exc()
                    logging.warning(a)
                    return -1,-1
        return -1,-1

    def check_color(self, pos, color, tolerance=0):
        """
        对比窗口内某一点的颜色
            :param pos: (x,y) 欲对比的坐标
            :param color: (r,g,b) 欲对比的颜色 
            :param tolerance=0: 容差值
            :return: 成功返回True,失败返回False
        """
        img = Image.fromarray(self.capture_screen(self.window_pos1,self.window_pos2), 'RGB')
        #print('img size:',img.size)
        #print('pos:',pos)
        try:
            r2, g2, b2 = img.getpixel(pos)[:3]
        except IndexError or UnboundLocalError:
            print('pos:',pos)
            print('img size:',img.size)

        for singl_color in color:
            r1, g1, b1 = singl_color[:3]
            
            if abs(r1-r2) <= tolerance and abs(g1-g2) <= tolerance and abs(b1-b2) <= tolerance: 
                print('r2, g2, b2:',singl_color)
                return True

        return False        

    def find_img_with_mem(self, img_template_path, part=0, pos1=None, pos2=None, image_show = False, gray=0):
        """
        查找图片
            :param img_template_path: 欲查找的图片路径
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
        """
        # 获取截图
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(gray)

        if image_show:
            show_img(img_src)

        # 读入文件
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        if image_show:
            show_img(img_template)

        try:
            res = cv2.matchTemplate(
                img_src, img_template, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            # print(maxLoc)
            h, w = img_template.shape[:2]
            self.mem_img_w = w
            self.mem_img_h = h

            top_left = maxLoc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            new_maxLoc = (top_left[0] + w/2, top_left[1] + h/2)
            cv2.rectangle(img_src, top_left, bottom_right, (0, 0, 255), 2)
            self.log.info(f"top_left:{top_left}, bottom_right:{bottom_right}")
            self.log.info(f"maxVal:{maxVal}, maxVal:{new_maxLoc}")
            if image_show:
                show_img(img_src)
            return maxVal, new_maxLoc
        except Exception:
            logging.warning('find_img执行失败')
            a = traceback.format_exc()
            logging.warning(a)
            return 0, 0

    def find_multi_img_with_mem(self, img_template_path_list, part=0, pos1=None, pos2=None, image_show = False, gray=0):
        """
        使用内存截图，且使用部分区域截图查找时，截取的图片处于窗口的相对位置坐标即可，即认为窗口右上角处于(0.0)位置
        part = 1， 使用的pos1 和 pos2， 为pos1和pos2所围成的图片对于(0.0)的坐标

        查找多张图片
            :param img_template_path: 欲查找的图片路径列表
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: (maxVal,maxLoc) maxVal为相关性列表，越接近1越好，maxLoc为得到的坐标列表
        """
        # 返回值列表
        maxVal_max = None
        maxLoc_max = None
        image_name = ''
        for item in img_template_path_list:
            # 窗口截图
            if part == 1:
                img_src = self.window_part_shot(pos1, pos2, None, gray)
            else:
                img_src = self.window_full_shot(gray)

            if image_show:
                show_img(img_src)

            # 读入文件
            if gray == 0:
                img_template = cv2.imread(item, cv2.IMREAD_COLOR)
            else:
                img_template = cv2.imread(item, cv2.IMREAD_GRAYSCALE)

            if image_show:
                show_img(img_template)

            # 开始识别
            try:
                res = cv2.matchTemplate(
                    img_src, img_template, cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                print(item)
                print(maxVal,maxLoc)

                h, w = img_template.shape[:2]
                top_left = maxLoc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                new_maxLoc = (top_left[0] + w/2, top_left[1] + h/2)
                cv2.rectangle(img_src, top_left, bottom_right, (0, 0, 255), 2)
                if image_show:
                    show_img(img_src)
            except Exception:
                logging.warning('find_multi_img执行失败')
                a = traceback.format_exc()
                logging.warning(a)
                minVal, new_maxLoc, minLoc, maxVal = 0,0,0,0
            
            if maxVal_max == None:
                maxVal_max = maxVal
                maxLoc_max = new_maxLoc
                image_name = item.split('\\')[-1]
            
            if maxVal_max < maxVal:
                maxVal_max = maxVal
                maxLoc_max = new_maxLoc
                image_name = item.split('\\')[-1]

        # 返回列表
        return maxVal_max, maxLoc_max,image_name

    def test_bitmap_and_window_diff(self,mem_img_path):
        #window screen
        img = self.window_part_shot_with_gui(self.window_pos1,self.window_pos2)
        #bitmap screen
        maxVal,maxLoc = self.find_img_with_mem(mem_img_path,image_show = False)
        if maxLoc != 0:

            # 计算框的左上角和右下角坐标
            left = maxLoc[0] - self.mem_img_w // 2
            top = maxLoc[1] - self.mem_img_h // 2
            right = maxLoc[0] + self.mem_img_w // 2
            bottom = maxLoc[1] + self.mem_img_h // 2
            
            top_left = (int(left),int(top))
            bottom_right = (int(right),int(bottom))

            left1 = maxLoc[0] * 1.5  - self.mem_img_w // 2
            top1 = maxLoc[1] * 1.5 - self.mem_img_h // 2
            right1 = maxLoc[0] * 1.5 + self.mem_img_w // 2
            bottom1 = maxLoc[1] * 1.5 + self.mem_img_h // 2

            top_left1 = (int(left1),int(top1))
            bottom_right1 = (int(right1),int(bottom1))

            print('bitmap position:',maxLoc)
            print('window position:',maxLoc[0] * 1.5,maxLoc[1] * 1.5)
            print('background')
            self.mouse_click_bg((int((maxLoc[0]-8)* 1.5),int((maxLoc[1]-31)* 1.5)))
            time.sleep(10)
            print('foreground')
            gui.moveTo((int(maxLoc[0]* 1.5 + self.window_pos1[0]),int(maxLoc[1]* 1.5+ self.window_pos1[1])))
            gui.leftClick()
            #self.left_click_down(int(maxLoc[0]* 1.5 + self.window_pos1[0]),int(maxLoc[1]* 1.5+ self.window_pos1[1]))
            #self.left_click_up(int(maxLoc[0]* 1.5 + self.window_pos1[0]),int(maxLoc[1]* 1.5+ self.window_pos1[1]))
            #cv2.rectangle(img, top_left, bottom_right, (0, 0, 255), 2)
            #cv2.rectangle(img, top_left1, bottom_right1, (0, 255, 0), 2)

            #show_img(img)

    def find_img(self, img_template_path, part=0, pos1=None, pos2=None, image_show = False, gray=0):
        """
        查找图片
            :param img_template_path: 欲查找的图片路径
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: (maxVal,maxLoc) maxVal为相关性，越接近1越好，maxLoc为得到的坐标
        """
        # 获取截图
        if part == 1:
            img_src = self.window_part_shot_with_gui(pos1, pos2, gray)
        else:
            img_src = self.window_full_shot(gray)

        if image_show:
            show_img(img_src)

        # 读入文件
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        if image_show:
            show_img(img_template)

        try:
            res = cv2.matchTemplate(
                img_src, img_template, cv2.TM_CCOEFF_NORMED)
            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
            # print(maxLoc)
            h, w = img_template.shape[:2]

            top_left = maxLoc
            bottom_right = (top_left[0] + w, top_left[1] + h)
            new_maxLoc = (top_left[0] + w/2, top_left[1] + h/2)
            # test
            print(top_left,bottom_right)
            #top_left = (top_left[0],top_left[1]+75)
            #bottom_right = (bottom_right[0],bottom_right[1]+75)
            cv2.rectangle(img_src, top_left, bottom_right, (0, 0, 255), 2)
            if image_show:
                show_img(img_src)
            return maxVal, new_maxLoc
        except Exception:
            logging.warning('find_img执行失败')
            a = traceback.format_exc()
            logging.warning(a)
            return 0, 0
        
    def find_multi_img_parallel(self, img_template_path_list, part=0, pos1=None, pos2=None, image_show=False, gray=0, thread=0.75):
        # 返回值列表
        max_results = []
        with ThreadPoolExecutor() as executor:
            futures = []
            for img_template_path in img_template_path_list:
                future = executor.submit(self.find_img, img_template_path, part, pos1, pos2, image_show, gray)  # 提交识别任务到线程池
                futures.append(future)
            for future in futures:
                maxVal, maxLoc = future.result()  # 获取每个图片的识别结果
                if maxVal > thread:
                    executor.shutdown(wait=False)
                    print('maxVal:',maxVal,'maxLoc',(maxLoc[0]+pos1[0],maxLoc[1]+pos1[1]))
                    return maxVal, (maxLoc[0]+pos1[0],maxLoc[1]+pos1[1])
                else:
                    max_results.append((maxVal, maxLoc))

        if max_results:  # 如果结果列表不为空
            maxVal_max, maxLoc_max = max(max_results, key=lambda x: x[0])  # 获取最大值的位置和值
            #如果查找玩，0.75的没有结果，降低门槛，大于0.65的值也可以使用
            if maxVal_max > 0.65:
                maxLoc_max = (maxLoc_max[0]+pos1[0],maxLoc_max[1]+pos1[1])
            else:
                maxLoc_max = False
        else:
            maxLoc_max = False
            maxVal_max = False
        print('maxVal_max:',maxVal_max,'maxLoc_max',maxLoc_max)
        return maxVal_max, maxLoc_max
        
    def find_img_knn(self, img_template_path, part=0, pos1=None, pos2=None, gray=0, thread=0):
        """
        查找图片，knn算法
            :param img_template_path: 欲查找的图片路径
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: 坐标(x, y)，未找到则返回(0, 0)，失败则返回-1
        """
        # 获取截图
        if part == 1:
            img_src = self.window_part_shot(pos1, pos2, None, gray)
        else:
            img_src = self.window_full_shot(gray)

        # show_img(img_src)

        # 读入文件
        if gray == 0:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_COLOR)
        else:
            img_template = cv2.imread(img_template_path, cv2.IMREAD_GRAYSCALE)

        try:
            maxLoc = match_img_knn(img_template, img_src, thread)
            # print(maxLoc)
            return maxLoc
        except Exception:
            logging.warning('find_img_knn执行失败')
            a = traceback.format_exc()
            logging.warning(a)
            return -1

    def find_multi_img(self, img_template_path_list, part=0, pos1=None, pos2=None, image_show = False,gray=0):
        """
        查找多张图片
            :param img_template_path: 欲查找的图片路径列表
            :param part=0: 是否全屏查找，1为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否彩色查找，0：查找彩色图片，1：查找黑白图片
            :return: (maxVal,maxLoc) maxVal为相关性列表，越接近1越好，maxLoc为得到的坐标列表
        """
        # 返回值列表
        maxVal_max = None
        maxLoc_max = None
        image_name = ''
        for item in img_template_path_list:
            # 窗口截图
            if part == 1:
                img_src = self.window_part_shot_with_gui(pos1, pos2, gray)
            else:
                img_src = self.window_full_shot(gray)

            if image_show:
                show_img(img_src)

            # 读入文件
            if gray == 0:
                img_template = cv2.imread(item, cv2.IMREAD_COLOR)
            else:
                img_template = cv2.imread(item, cv2.IMREAD_GRAYSCALE)

            if image_show:
                show_img(img_template)

            # 开始识别
            try:
                res = cv2.matchTemplate(
                    img_src, img_template, cv2.TM_CCOEFF_NORMED)
                minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)
                print(item)
                print(maxVal,maxLoc)

                h, w = img_template.shape[:2]
                top_left = maxLoc
                bottom_right = (top_left[0] + w, top_left[1] + h)
                new_maxLoc = (top_left[0] + w/2, top_left[1] + h/2)
                if image_show:
                    cv2.rectangle(img_src, top_left, bottom_right, (0, 0, 255), 2)
                    show_img(img_src)
            except Exception:
                logging.warning('find_multi_img执行失败')
                a = traceback.format_exc()
                logging.warning(a)
                minVal, new_maxLoc, minLoc, maxVal = 0,0,0,0
            
            if maxVal_max == None:
                maxVal_max = maxVal
                maxLoc_max = new_maxLoc
                image_name = item.split('\\')[-1]
            
            if maxVal_max < maxVal:
                maxVal_max = maxVal
                maxLoc_max = new_maxLoc
                image_name = item.split('\\')[-1]

        # 返回列表
        return maxVal_max, maxLoc_max,image_name

    def clear_active_state_dict(self):
        for hnwd_key, state_value in game_active_state_dict.items():
            game_active_state_dict[hnwd_key] = False

    def activate_window(self):
        if self.hwnd in game_active_state_dict:
            state = game_active_state_dict[self.hwnd]
            if state == True:
                pass
            else:
                user32 = ctypes.WinDLL('user32.dll')
                user32.SwitchToThisWindow(self.hwnd, True)
                self.clear_active_state_dict()
                game_active_state_dict[self.hwnd] = True
        else:
            user32 = ctypes.WinDLL('user32.dll')
            user32.SwitchToThisWindow(self.hwnd, True)
            self.clear_active_state_dict()
            game_active_state_dict[self.hwnd] = True
        print(game_active_state_dict,self.player)
    def mouse_move(self, pos, pos_end=None):
        """
        模拟鼠标移动
            :param pos: (x,y) 鼠标移动的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标移动至以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
        """
        pos2 = win32gui.ClientToScreen(self.hwnd, pos)
        if pos_end == None:
            win32api.SetCursorPos(pos2)
        else:
            pos_end2 = win32gui.ClientToScreen(self.hwnd, pos_end)
            pos_rand = (random.randint(
                pos2[0], pos_end2[0]), random.randint(pos2[1], pos_end2[1]))
            win32api.SetCursorPos(pos_rand)

    def mouse_click(self):
        """
        鼠标单击
        """
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(random.randint(20, 80)/1000)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_drag(self, pos1, pos2):
        """
        鼠标拖拽
            :param pos1: (x,y) 起点坐标
            :param pos2: (x,y) 终点坐标
        """
        pos1_s = win32gui.ClientToScreen(self.hwnd, pos1)
        pos2_s = win32gui.ClientToScreen(self.hwnd, pos2)
        screen_x = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        screen_y = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
        start_x = pos1_s[0]*65535//screen_x
        start_y = pos1_s[1]*65535//screen_y
        dst_x = pos2_s[0]*65535//screen_x
        dst_y = pos2_s[1]*65535//screen_y
        move_x = np.linspace(start_x, dst_x, num=20, endpoint=True)[0:]
        move_y = np.linspace(start_y, dst_y, num=20, endpoint=True)[0:]
        self.mouse_move(pos1)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        for i in range(20):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE |
                                 win32con.MOUSEEVENTF_ABSOLUTE, x, y, 0, 0)
            time.sleep(0.01)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    def mouse_click_bg(self, pos, pos_end=None,click_show=False):
        """
        后台鼠标单击
            :param pos: (x,y) 鼠标单击的坐标
            :param pos_end=None: (x,y) 若pos_end不为空，则鼠标单击以pos为左上角坐标pos_end为右下角坐标的区域内的随机位置
        """
        #pos = (int(pos[0]*1.5),int(pos[1]*1.5-48))

        print('pos:',pos)
        pos = (int(pos[0]),int(pos[1]))
        if pos_end == None:
            pos_rand = pos
        else:
            pos_rand = (random.randint(
                pos[0], pos_end[0]), random.randint(pos[1], pos_end[1]))

        if click_show:
            #img_src = self.window_part_shot_with_gui(self.window_pos1, self.window_pos2)
            img_src = self.window_full_shot()
            img = cv2.rectangle(img_src, pos, pos_end, (0, 255, 0), 3)
            show_img(img)

        print('pos_rand:',pos_rand)

        win32gui.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE,
                                0, win32api.MAKELONG(int(pos_rand[0]), int(pos_rand[1])))
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                win32con.MK_LBUTTON, win32api.MAKELONG(int(pos_rand[0]), int(pos_rand[1])))
        time.sleep(random.randint(20, 80)/1000)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                win32con.MK_LBUTTON, win32api.MAKELONG(int(pos_rand[0]), int(pos_rand[1])))

    #鼠标向上或者向下拖动一定距离
    def drag_up_or_down(slef,x,y,distance,direction = False):
        # 将鼠标移动到 (100, 100) 位置
        gui.moveTo(x,y)

        if direction:
            # 从当前位置向上拖动鼠标 distance 像素
            gui.dragTo(x, y - distance, duration=0.5)
        else:
            # 从当前位置向下拖动鼠标 distance 像素
            gui.dragTo(x, y + distance, duration=0.5)

    def mouse_drag_bg(self, pos1, pos2):
        """
        后台鼠标拖拽
            :param pos1: (x,y) 起点坐标
            :param pos2: (x,y) 终点坐标
        """
        move_x = np.linspace(pos1[0], pos2[0], num=20, endpoint=True)[0:]
        move_y = np.linspace(pos1[1], pos2[1], num=20, endpoint=True)[0:]
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                0, win32api.MAKELONG(pos1[0], pos1[1]))
        for i in range(20):
            x = int(round(move_x[i]))
            y = int(round(move_y[i]))
            win32gui.SendMessage(
                self.hwnd, win32con.WM_MOUSEMOVE, 0, win32api.MAKELONG(x, y))
            time.sleep(0.01)
        win32gui.SendMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                0, win32api.MAKELONG(pos2[0], pos2[1]))

    def wait_game_img(self, img_path,part = 0, pos1 = None, pos2 =None, thread = 0.9, image_show=False,max_time=100):
        """
        等待游戏图像
            :param img_path: 图片路径
            :param max_time=60: 超时时间
            :param quit=True: 超时后是否退出
            :return: 成功返回坐标，失败返回False
        """
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            maxVal, maxLoc = self.find_img(img_path,part,pos1,pos2,image_show)
            print(maxVal, maxLoc)
            if maxVal > thread:
                print('wait img_path:',img_path,maxVal,maxLoc)     
                if part == 1:
                    print('pos1:',pos1)
                    return (maxLoc[0] + pos1[0], maxLoc[1] + pos1[1])
                return maxLoc
            if max_time > 5:
                time.sleep(1)
            elif max_time > 3600:
                time.sleep(10)
            else:
                time.sleep(0.1)

        return False
    def wait_game_multi_img(self, img_list,part = 0, pos1 = None, pos2 =None, thread = 0.9, image_show=False,max_time=100):
        """
        等待游戏图像
            :param img_path: 图片路径
            :param max_time=60: 超时时间
            :param quit=True: 超时后是否退出
            :return: 成功返回坐标，失败返回False
        """
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            for img in img_list:
                maxVal, maxLoc = self.find_img(img,part,pos1,pos2,image_show)
                print(maxVal, maxLoc, ' ===>>> ',img)
                if maxVal > thread:
                    print('wait img_path:',img,maxVal,maxLoc)     
                    if part == 1:
                        print('pos1:',pos1)
                        return (maxLoc[0] + pos1[0], maxLoc[1] + pos1[1])
                    return maxLoc
            if max_time > 5:
                time.sleep(1)
            else:
                time.sleep(0.1)
        return False
    def wait_game_img_knn(self, img_path, max_time=100, quit=True, thread=0):
        """
        等待游戏图像
            :param img_path: 图片路径
            :param max_time=60: 超时时间
            :param quit=True: 超时后是否退出
            :return: 成功返回坐标，失败返回False
        """
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            maxLoc = self.find_img_knn(img_path, thread=thread)
            if maxLoc != (0, 0):
                return maxLoc
            if max_time > 5:
                time.sleep(1)
            else:
                time.sleep(0.1)
        if quit:
            # 超时则退出游戏
            self.quit_game()
        else:
            return False

    def wait_game_color(self, region, color, tolerance=0, max_time=60, quit=True):
        """
        等待游戏颜色
            :param region: ((x1,y1),(x2,y2)) 欲搜索的区域
            :param color: (r,g,b) 欲等待的颜色
            :param tolerance=0: 容差值
            :param max_time=30: 超时时间
            :param quit=True: 超时后是否退出
            :return: 成功返回True，失败返回False
        """
        start_time = time.time()
        while time.time()-start_time <= max_time and self.run:
            pos = self.find_color(region, color)
            if pos != -1:
                return True
            time.sleep(1)
        if quit:
            # 超时则退出游戏
            self.quit_game()
        else:
            return False

    def quit_game(self):
        """
        退出游戏
        """
        self.takescreenshot()  # 保存一下现场
        self.clean_mem()    # 清理内存

        if not self.run:
            return False

        if self.quit_game_enable:
            win32gui.SendMessage(
                self.hwnd, win32con.WM_DESTROY, 0, 0)  # 退出游戏

        logging.info('退出，最后显示已保存至/img/screenshots文件夹')
        sys.exit(0)

    def takescreenshot(self):
        '''
        截图
        '''
        name = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        img_src_path = 'img/screenshots/%s.png' %(name)
        self.window_full_shot(img_src_path)
        logging.info('截图已保存至img/screenshots/%s.png' %(name))

    def find_game_img(self, img_path, part=0, pos1=None, pos2=None, image_show= False,gray=0, thread=0.9):
        '''
        查找图片
            :param img_path: 查找路径
            :param part=0: 是否全屏查找，0为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否查找黑白图片，0：查找彩色图片，1：查找黑白图片
            :param thread=0.9: 自定义阈值
            :return: 查找成功返回位置坐标，否则返回False
        '''
        maxVal, maxLoc = self.find_img(img_path, part, pos1, pos2, image_show, gray)
        #print(maxVal,maxLoc,'===========',img_path)
        if maxVal > thread: 
            print(self.player,'img_path:',img_path,maxVal,maxLoc)     
            if part == 1:
                #print('pos1:',pos1)
                return (maxLoc[0] + pos1[0], maxLoc[1] + pos1[1])
            return maxLoc
        else:
            return False

    def find_game_multi_img(self, img_list, part=0, pos1=None, pos2=None, image_show= False,gray=0, thread=0.9):
        '''
        查找图片
            :param img_path: 查找路径
            :param part=0: 是否全屏查找，0为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否查找黑白图片，0：查找彩色图片，1：查找黑白图片
            :param thread=0.9: 自定义阈值
            :return: 查找成功返回位置坐标，否则返回False
        '''
        maxVal, maxLoc, image_name= self.find_multi_img(img_list, part, pos1, pos2, image_show, gray)
        #print(maxVal,maxLoc,'===========',image_name)
        if maxVal > thread: 
            print(self.player,'image_name:',image_name,maxVal,maxLoc)     
            if part == 1:
                return (maxLoc[0] + pos1[0], maxLoc[1] + pos1[1]),image_name
            return maxLoc,image_name
        else:
            return False,None
    def find_game_img_knn(self, img_path, part=0, pos1=None, pos2=None, gray=0, thread=0):
        '''
        查找图片
            :param img_path: 查找路径
            :param part=0: 是否全屏查找，0为否，其他为是
            :param pos1=None: 欲查找范围的左上角坐标
            :param pos2=None: 欲查找范围的右下角坐标
            :param gray=0: 是否查找黑白图片，0：查找彩色图片，1：查找黑白图片
            :param thread=0: 
            :return: 查找成功返回位置坐标，否则返回False
        '''
        maxLoc = self.find_img_knn(img_path, part, pos1, pos2, gray, thread)
        # print(maxVal)
        if maxLoc != (0, 0):
            return maxLoc
        else:
            return False

    def press_single_key(self, key_code, keep_time=0):
        '''
        向handle_id 输入 单个按键
        '''
        vk_code = self.get_virtual_keycode(key_code)
        self.activate_window()
        time.sleep(1)
        # 模拟按键按下和释放事件
        win32api.keybd_event(vk_code, 0, 0, 0)  # 按下按键
        time.sleep(keep_time)
        win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

    def press_combination_keys(self, combination_keys):
        '''
        向handle_id 输入 组合按键
        '''
        self.activate_window()
        time.sleep(2)
        # 按下组合按键
        tmp_list = []
        for combination_key in combination_keys:
            vk_code = self.get_virtual_keycode(combination_key)
            win32api.keybd_event(vk_code, 0, 0, 0)  # 按下按键
            tmp_list.insert(0,combination_key)

        # 松开组合按键
        for combination_key in tmp_list:
            vk_code = self.get_virtual_keycode(combination_key)
            win32api.keybd_event(vk_code, 0, win32con.KEYEVENTF_KEYUP, 0)

    def debug(self):
        '''
        自检分辨率和点击范围
        '''
        # 开启自检
        self.debug_enable = True

        # 分辨率
        self.img = self.window_full_shot()
        logging.info('游戏分辨率：' + str(self.img.shape))

        while(1):
            # 点击范围标记
            cv2.imshow('Click Area (Press \'q\' to exit)', self.img)

            # 候选图片

            k = cv2.waitKey(1) & 0xFF
            if k == ord('q'):
                break

        cv2.destroyAllWindows()
        self.debug_enable = False

    def clean_mem(self):
        '''
        清理内存
        '''
        self.srcdc.DeleteDC()
        self.memdc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwindc)
        win32gui.DeleteObject(self.bmp.GetHandle())

    def match_img_knn(self, queryImage, trainingImage, thread=0):
        sift = cv2.xfeatures2d.SIFT_create()  # 创建sift检测器
        kp1, des1 = sift.detectAndCompute(queryImage, None)
        kp2, des2 = sift.detectAndCompute(trainingImage, None)
        #print(len(kp1))
        # 设置Flannde参数
        FLANN_INDEX_KDTREE = 1
        indexParams = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
        searchParams = dict(checks=50)
        flann = cv2.FlannBasedMatcher(indexParams, searchParams)
        matches = flann.knnMatch(des1, des2, k=2)

        good = []

        # 设置好初始匹配值
        matchesMask = [[0, 0] for i in range(len(matches))]
        for i, (m, n) in enumerate(matches):
            if m.distance < 0.7*n.distance:  # 舍弃小于0.7的匹配结果
                matchesMask[i] = [1, 0]
                good.append(m)

        s = sorted(good, key=lambda x: x.distance)
        '''
        drawParams=dict(matchColor=(0,0,255),singlePointColor=(255,0,0),matchesMask=matchesMask,flags=0) #给特征点和匹配的线定义颜色
        resultimage=cv2.drawMatchesKnn(queryImage,kp1,trainingImage,kp2,matches,None,**drawParams) #画出匹配的结果
        cv2.imshow('res',resultimage)
        cv2.waitKey(0)
        '''
        #print(len(good))
        if len(good) > thread:
            maxLoc = kp2[s[0].trainIdx].pt
            #print(maxLoc)
            return (int(maxLoc[0]), int(maxLoc[1]))
        else:
            return (0, 0)
# 测试用


def show_img(img):
    cv2.namedWindow("image", cv2.WINDOW_NORMAL)
    cv2.imshow("image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


def main():
    hwnd = win32gui.FindWindow(0, u'new 16 - Notepad++')
    #tmp_game = GameControl(hwnd, 0)
    #tmp_game.debug()

    print(hwnd)


if __name__ == '__main__':
    main()
