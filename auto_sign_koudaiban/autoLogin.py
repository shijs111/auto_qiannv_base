import time
import win32con
from win32con import WM_LBUTTONDOWN, WM_LBUTTONUP
import win32gui as wg   # pip install pypiwin32
import pyautogui as gui
import cv2
import numpy as np
import win32api, win32con
import os

#通过图片获取坐标
def locate(path,count=3):
    print("finding image %s"%path)
    counter = 0
    x = 0 
    y = 0
    while(1):
        try:
            x,y = gui.locateCenterOnScreen(path)
        except:
            print('waiting for finding pict...')
            time.sleep(0.5)
            counter = counter + 1
            if(counter > count):
                print("find image failed %s"%path)
                break
        else:
            break
    return x,y

#寻找多个图片中的目标图片，并返回坐标
def locateMulti(path,count=3): 
    x = 0
    y = 0
    maxX_list = [] 
    maxY_list = []
    
    for item in path:
        counter = 0
        print("finding multi images %s: "%item)
        while(1):
            try:
                x,y = gui.locateCenterOnScreen(item)
            except:
                print('waiting for finding pict...')
                time.sleep(0.5)
                counter = counter + 1
                if(counter > count):
                    print("find image failed %s"%item)
                    break
            else:
                break
        maxX_list.append(x)
        maxY_list.append(y)
    
    maxX = max(maxX_list)
    maxY = max(maxY_list)
    return maxX,maxY

#寻找某个图片，找到并截图显示，调试使用
def showWithPictLocation(path ,showFlag=True, count=3):
    x,y = locate(path,count=count)
    if x!= 0 or y!=0:
        print(x,y)
        if showFlag:
            showPictureWithCoord(x,y)
        #gui.click(x,y)
        time.sleep(1)

#检查特定坐标范围的图片，调试使用
def showPictureWithCoord(x,y):

    # 指定截取图片大小
    width, height = 50, 50

    # 计算目标坐标周围的区域
    left, top = x - width // 2, y - height // 2
    right, bottom = x + width // 2, y + height // 2

    # 使用 PyAutoGUI 截取制定范围的屏幕截图
    screenshot = gui.screenshot(region=(left, top, width, height))

    # 展示截屏结果
    screenshot.show()

#查找某个图片，并点击改图片对应的坐标，并返回该坐标
def clickWithPict(path ,count=3):
    x,y = locate(path,count=count)
    if x!= 0 or y!=0:
        print(x,y)
        gui.click(x,y)
        time.sleep(1)
    
    return x,y

#等待多个目标图片中的某个图片出现，如果出现返回目标图片的名称和坐标  
def waitForImages(image_files, max_time=60):

    print("waiting for images:",image_files)
    start_time = time.time()

    while time.time()-start_time <= max_time:
        for control_image_file in image_files:
            control_pos = gui.locateCenterOnScreen(control_image_file)
            if control_pos is not None:
                return control_pos, control_image_file
    return None, None

#比较单个或者多个图片，检测桌面是否存在目标图片，如果存在返回True，反之False
def checkPictStatus(path,count=3,mutilFlag=False):
    #print("mutilFlag:",mutilFlag)
    if not mutilFlag:
        x,y = locate(path,count=count)
    else:
        x,y = locateMulti(path,count=count)
    if x!= 0 or y!=0:
        return True
    
    return False

#点击某个坐标（x,y）的位置，知道某个图片出现，mutilFlag用于检测多个图片中的某个目标图片
def cilckUntilPictAppear(path,x,y,maxTime=60,mutilFlag=False):
    startTime = time.time()
    while not checkPictStatus(path,mutilFlag=mutilFlag):
        gui.click(x,y)
        time.sleep(1)
        
        if time.time() - startTime > maxTime:
            return False
        
    return True
    
#鼠标向上或者向下拖动一定距离
def dragToUpOrDown(x,y,direction,distance):
    # 将鼠标移动到 (100, 100) 位置
    gui.moveTo(x,y)

    if direction:
        # 从当前位置向上拖动鼠标 distance 像素
        gui.dragTo(x, y - distance, duration=0.5)
    else:
        # 从当前位置向下拖动鼠标 distance 像素
        gui.dragTo(x, y + distance, duration=0.5)

#使用opencv查找目标图片，若没找到则向上或者向下拖拽，并再次查找，找到返回坐标，反之返回None，最多拖拽3次或者60s
def dragUntilImageWithCV(image_file,x,y,direction,distance,max_time=60):

    start_time = time.time()
    count = 0
    while time.time()-start_time <= max_time and count < 3:
        pict_pos, fileName = checkPictInSpecificScope(image_file,0,0,True)
        if pict_pos is not None:
            return pict_pos
        
        dragToUpOrDown(x,y,direction,distance)
        count = count + 1
        time.sleep(3)

    return None

#使用pyautogui查找目标图片，若没找到则向上或者向下拖拽，并再次查找，找到返回坐标，反之返回None，最多查找60s
def dragUntilImageWithGui(image_file,x,y,direction,distance,max_time=60):

    start_time = time.time()

    while time.time()-start_time <= max_time:
        xL,yL= locate(image_file)
        if xL!=0 or yL!=0:
            return xL,yL
        
        time.sleep(2)
        print(x,y,direction,distance)
        dragToUpOrDown(x,y,direction,distance)
        time.sleep(5)

    return 0,0

#检查特定坐标范围中的圆圈个数，并返回圆圈个数
def getCircleCount(x,y):
    # 指定截屏的范围   
    x = x - 140
    y = y - 678 
    w = 380
    h = 60

    # 从屏幕上截取指定的区域
    screenshot = gui.screenshot(region=(x, y, w, h))
    
    #screenshot.show()
    
    # 将截图转换为 OpenCV 图像格式
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=20, minRadius=20, maxRadius=30)
    
    list_circles = []
    
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            list_circles.append((x,y,r))
            print(x, y, r)
    
    # cv2.imshow('Result', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    print(len(list_circles))
    return len(list_circles)

#用opencv检测某个坐标的范围内或者全屏范围内，是否存在目标图片，mutilFlag用于检测多个图片中的某个目标图片
def checkPictInSpecificScope(path,x,y,matchFullFlag = False):
    if not matchFullFlag:
        # 指定截取图片大小
        width, height = 50, 50

        # 计算目标坐标周围的区域
        left, top = x - width // 2, y - height // 2
        right, bottom = x + width // 2, y + height // 2

        # 使用 PyAutoGUI 截取制定范围的屏幕截图
        screenshot = gui.screenshot(region=(left, top, width, height))
    else:
        # 获取屏幕大小
        screen_width, screen_height = gui.size()

        # 全屏截图
        screenshot = gui.screenshot(region=(0, 0, screen_width, screen_height))
    
    #screenshot.show()
    

    # 将截图转换为 OpenCV 图像格式
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    img_src = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    maxLoc = None
    
    for image_path in path:
        template = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        try:
            res = cv2.matchTemplate(
                img_src, template, cv2.TM_CCOEFF_NORMED)

            minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(res)

        except Exception:
            print('checkPictInSpecificScope执行失败:',image_path)
            maxVal = 0
            maxLoc = None

        # Check if found an approximate '+' symbol in the circle region
        THRESHOLD = 0.80
        if maxVal > THRESHOLD:
            print("match pict:",image_path, maxLoc)
            break
        else:
            print("No pict found:",image_path)
            maxLoc = None
    print("maxLoc:",maxLoc)
    return maxLoc,image_path

#累计签到，发现签到图标，并签到成功，返回True，否则返回False
def addupSignIn(x,y):
    print("darging init position...")
    #根据返回的坐标向下托拽，直到识别到'累计签到第一天',并返回第一天坐标
    x1,y1 = dragUntilImageWithGui(r'.\firstDayPict.png',x,y,False,200)
    if x1!=0 or y1!=0:
        print("firstDayPos:",x1,y1)
        #showPictureWithCoord(x1,y1)
        time.sleep(0.5)
    
        signInPos = dragUntilImageWithCV([r'.\get.png'],x,y,True,180)
        if signInPos is not None:
            print("signInPos:",signInPos[0],signInPos[1])
            #showPictureWithCoord(signInPos[0],signInPos[1])
            gui.click(signInPos[0],signInPos[1])
            
            time.sleep(1)
            
            #在检测玩累计签到之后，检测是否有满七天奖励，再次向上hua
            dragToUpOrDown(x,y,True,300)
            time.sleep(1)
            weeklyPos, fileName = checkPictInSpecificScope([r'.\get.png'],0,0,True)
            if weeklyPos is not None:
                gui.click(weeklyPos[0],weeklyPos[1])
                time.sleep(1)
            
            return True
        else:
            print('not find signIn button')
            return False

#登录账号界面，展开账号列表
def unfoldAccountList():

    x,y = locate(r'.\unfold.png')
    
    while checkPictStatus(r'.\login.png'):
        x,y = clickWithPict(r'.\unfold.png')

    return x,y           

def loginGame():
    #登录游戏
    clickWithPict(r'.\login.png')
    
    print(' login....')
    #等待第一次‘进入游戏’按钮出现
    firstEnterPos, tmpfileName = waitForImages([r'.\enterInto.png'])
    if  firstEnterPos is not None:
        print('firstEnterPos:',firstEnterPos)
        #点击‘进入游戏’
        gui.click(firstEnterPos[0],firstEnterPos[1])
        time.sleep(1)
        
        selectCharaPos, tmpfileName = waitForImages([r'.\selectCharaWindow.png'])
        #等待进入‘选择角色’ 界面
        if selectCharaPos is not None:
            #选择角色界面
            print('selectCharaPos:',selectCharaPos)
            time.sleep(1)

signedFlag = False
listChara = []
signedLimit = 1
blueStackPath = r'C:\Program Files\BlueStacks_nxt_cn\HD-Player.exe'

#自动启动buleStack
if wg.FindWindow(None, 'BlueStacks'):
    pass
else:
    os.startfile(blueStackPath)

qiannvPos, tmpfileName = waitForImages([r'.\qiannv.png',r'.\loginWindow.png'],180)
if qiannvPos is not None:
    print('qiannvPos:',qiannvPos)

    if tmpfileName == r'.\qiannv.png':
        #点击qiannv.apk 图标，并等待进入登录界面，中间check一次是否更新游戏
        gui.click(qiannvPos.x, qiannvPos.y-40)
        time.sleep(1)
    loginWindow = [r'.\update.png',r'.\loginWindow.png']
    loginWindowPos, tmpfileName = waitForImages(loginWindow,180)
    
    if loginWindowPos is not None:
        
        if tmpfileName == r'.\update.png':
            #游戏需要更新
            print('updating...')
            gui.click(loginWindowPos.x,loginWindowPos.y)
            time.sleep(1)
            #等待更新完成，进入游戏登录界面
            loginWindowPos, tmpfileName = waitForImages([r'.\loginWindow.png'])
            if loginWindowPos is not None:
                print('the update has been compeleted')

        print("enter into login window successfully!")
        
        while not signedFlag:
            #登录界面
            #1.点击扩展按钮, 并检测到 ‘登录’ 按钮消失
            listChara = []
            signedNum = 0
            x,y = unfoldAccountList()
            
            print("unfold pos:",x,y)
            #2.向上划动一定距离，显示最后一个账号
            if x!=0 or y!=0:
                gui.moveTo(x-50,y+80)
                time.sleep(0.5)
                dragToUpOrDown(x-50,y+80,True,180)
                time.sleep(1)
                #3.点击最后一个账号
                #showWithPictLocation(r'.\lastAccount.png')
                gui.click(x-144, y+150)
                time.sleep(1)
                #4.登录游戏
                clickWithPict(r'.\login.png')
                
                print(' login....')
                #等待第一次‘进入游戏’按钮出现
                firstEnterPos, tmpfileName = waitForImages([r'.\enterInto.png'])
                if  firstEnterPos is not None:
                    print('firstEnterPos:',firstEnterPos)
                    #点击‘进入游戏’
                    gui.click(firstEnterPos[0],firstEnterPos[1])
                    time.sleep(1)
                    
                    selectCharaPos, tmpfileName = waitForImages([r'.\selectCharaWindow.png'])
                    #等待进入‘选择角色’ 界面
                    if selectCharaPos is not None:
                        #选择角色界面
                        print('selectCharaPos:',selectCharaPos)
                        
                        #根据当前角色界面的圆圈数量，决定角色数量，并将角色数量坐标记录到list中
                        circle_num = getCircleCount(selectCharaPos[0],selectCharaPos[1])
                        
                        pictLoc, fileName = checkPictInSpecificScope([r'.\addPict.png'],0,0,True)
                        
                        if pictLoc is not None:
                            
                            print('pictLoc:',pictLoc,type(pictLoc))
                            tmpX, tmpY = pictLoc
                            if circle_num == 4:
                                # 3 characters
                                listChara.append([tmpX-41,tmpY+14])
                                listChara.append([tmpX-102,tmpY+14])
                                listChara.append([tmpX-162,tmpY+14])
                            elif circle_num == 3:
                                # 2 characters
                                listChara.append([tmpX-41,tmpY+14])
                                listChara.append([tmpX-102,tmpY+14])
                            elif circle_num == 2:
                                # 1 character
                                listChara.append([tmpX-41,tmpY+14])
                            else:
                                #返回登录账号界面
                                print('there is not character, switch account')
                        else:
                            if circle_num == 4:
                                # 4 characters
                                listChara.append((selectCharaPos[0]-63,selectCharaPos[1]-646))
                                listChara.append((selectCharaPos[0]-3,selectCharaPos[1]-646))
                                listChara.append((selectCharaPos[0]+58,selectCharaPos[1]-646))
                                listChara.append((selectCharaPos[0]+118,selectCharaPos[1]-646))
                            else:
                                print('circle detected error')
                                
                        for chara_location in listChara:
                            if len(listChara) != 1:
                                #根据chara_location 选择角色
                                gui.click(chara_location[0],chara_location[1])
                                time.sleep(0.5)
                            
                            if chara_location == listChara[-1]:
                                listChara.clear()
                            
                            #点击进入游戏
                            gui.click(selectCharaPos[0],selectCharaPos[1])
                                                    
                            time.sleep(5)
                            
                            #在点击进入游戏之前，判断当前是否有选择角色弹窗弹出
                            maxLoc, fileName = checkPictInSpecificScope([r'.\punishInfo.png',r'.\salingChara.png',r'.\pleaseSelect.png'],0,0,True)
                            if maxLoc is not None:
                                #若弹出，重新点击chara_location
                                clickWithPict(r'.\confirmButton.png')
                                time.sleep(0.5)
                                
                                if fileName == r'.\pleaseSelect.png':
                                    #重新选定角色
                                    gui.click(chara_location[0],chara_location[1])
                                    time.sleep(0.5)
                                    #点击进入游戏
                                    gui.click(selectCharaPos[0],selectCharaPos[1])
                                    time.sleep(5)
                                    
                                    locTmp,fileTmp = checkPictInSpecificScope([r'.\punishInfo.png',r'.\salingChara.png'],0,0,True)
                                    #若弹出，重新点击chara_location
                                    
                                    if locTmp is not None:
                                        clickWithPict(r'.\confirmButton.png')
                                        time.sleep(0.5)
                                        
                                        if fileTmp == r'.\salingChara.png' or fileTmp == r'.\punishInfo.png'or fileName == r'.\lockedAccount.png':
                                            print(fileTmp)
                                            if len(listChara) == 0:
                                                print('the selected character is wrong, and current account has not other character,switch next character')
                                                break
                                            else:
                                                #账号还有其他角色，跳过该角色，回到选择角色界面，重新选择下一个坐标
                                                loginGame()
                                                continue
                                    
                                if fileName == r'.\salingChara.png' or fileName == r'.\punishInfo.png'or fileName == r'.\lockedAccount.png':
                                    print(fileName)
                                    if len(listChara) == 0:
                                        print('the selected character is wrong, and current account has not other character,switch next character')
                                        break
                                    else:
                                        #账号还有其他角色，跳过该角色，回到选择角色界面，重新选择下一个坐标
                                        loginGame()
                                        continue
                            
                            #等待进入游戏界面，直到出现游戏画面图标
                            gameWindow = [r'.\gameWindow1.png',r'.\gameWindow1_1.png',r'.\gameWindow2.png',r'.\gameWindow2_1.png',r'.\gameWindow3.png',r'.\gameWindow3_1.png']
                            
                            gameWindowPos, tmpfileName = waitForImages(gameWindow)
                            
                            if gameWindowPos is not None:
                            
                                gameScene = [r'.\gameWindow2.png',r'.\gameWindow3.png',r'.\gameWindow1_1.png']
                                maxLoc, fileName = checkPictInSpecificScope(gameScene,0,0,True)
                                if maxLoc is not None:
                                    print('maxLoc:',maxLoc,'fileName:',fileName)
                                    
                                    #进入游戏主界面，能直接检测到‘易市’图标，需点击签到，展开签到窗口，查看是否签到
                                    if fileName == r'.\gameWindow2.png' or fileName == r'.\gameWindow3.png':
                                        print('enter into the game scene, but there is not signIn window, check signIn status')
                                        
                                        #检测签到图标
                                        maxLoc, fileName = checkPictInSpecificScope([r'.\signInIcon2.png',r'.\signInIcon3.png'],0,0,True)
                                        if maxLoc is not None:
                                            print('maxLoc:',maxLoc,'fileName:',fileName)
                                            gui.click(maxLoc[0]+20,maxLoc[1]+5)
                                            
                                            time.sleep(3)
                                            
                                            #检测签到界面
                                            
                                            maxLoc, fileName = checkPictInSpecificScope([r'.\signInWindow.png'],0,0,True)
                                            if maxLoc is not None:
                                                #累计签到检测
                                                addupSignFlag = addupSignIn(maxLoc[0],maxLoc[1]+200)
                                                
                                                #切换到日常签到
                                                gui.click(maxLoc[0]-285,maxLoc[1]+80)
                                                time.sleep(1)
                                                
                                                #检测是否进入日常签到界面
                                                maxLoc, fileName = checkPictInSpecificScope([r'.\dailySignWindow.png'],0,0,True)
                                                if maxLoc is not None:   
                                                    maxLoc, fileName = checkPictInSpecificScope([r'.\signed.png'],0,0,True)    
                                                    if maxLoc is not None:
                                                        #已日常签到
                                                        dailySignFlag = False
                                                    
                                                    maxLoc, fileName = checkPictInSpecificScope([r'.\sign.png'],0,0,True)    
                                                    if maxLoc is not None:
                                                        #未日常签到，点击签到
                                                        dailySignFlag = True
                                                        gui.click(maxLoc[0]+36,maxLoc[1]+13)
                                                        time.sleep(0.5)
                                                
                                                    #关闭签到界面
                                                    maxLoc, fileName = checkPictInSpecificScope([r'.\closeSign.png'],0,0,True)
                                                    if maxLoc is not None:
                                                        #showPictureWithCoord(maxLoc[0]+13,maxLoc[1]+13)
                                                        gui.click(maxLoc[0]+13,maxLoc[1]+13)
                                                        time.sleep(1)
                                                    
                                                    #判断当前已经签到的角色个数
                                                    print("1>>> dailySignFlag:",dailySignFlag,"addupSignFlag:",addupSignFlag)
                                                    if False == dailySignFlag and False == addupSignFlag:
                                                        signedNum = signedNum + 1
                                                        if signedNum >= signedLimit:
                                                            print('1>>> signed limited')
                                                            listChara.clear() #返回选择账号登录界面
                                                            signedFlag = True #结束签到循环
                                    #没有检测到 ‘易市’ 图标，说面游戏界面内有弹窗或者签到窗口阻挡             
                                    if fileName == r'.\gameWindow1_1.png':
                                        print('---- enter into the game ----')
                                        
                                        #检查是否有‘确认’图标        
                                        maxLoc, fileName = checkPictInSpecificScope([r'.\confirmButton.png'],0,0,True)
                                        if maxLoc is not None:
                                            gui.click(maxLoc[0]+21,maxLoc[1]+13)
                                            time.sleep(1)
                                            print('there is message box blocking the sign')
                                        
                                        #检测签到图标
                                        maxLoc, fileName = checkPictInSpecificScope([r'.\signInIcon2.png'],0,0,True)
                                        if maxLoc is None:
                                            print('there is not signIcon, maybe the characters level is too lower')
                                            
                                        #一进入游戏，自动弹出的签到界面
                                        maxLoc, fileName = checkPictInSpecificScope([r'.\signInWindow.png'],0,0,True)
                                        if maxLoc is not None:
                                            #累计签到检测
                                            addupSignFlag = addupSignIn(maxLoc[0],maxLoc[1]+200)
                                            
                                            #切换到日常签到
                                            gui.click(maxLoc[0]-285,maxLoc[1]+80)
                                            time.sleep(1)
                                            
                                            #检测是否进入日常签到界面
                                            maxLoc, fileName = checkPictInSpecificScope([r'.\dailySignWindow.png'],0,0,True)
                                            if maxLoc is not None:   
                                                maxLoc, fileName = checkPictInSpecificScope([r'.\signed.png'],0,0,True)    
                                                if maxLoc is not None:
                                                    #已日常签到
                                                    dailySignFlag = False
                                                
                                                maxLoc, fileName = checkPictInSpecificScope([r'.\sign.png'],0,0,True)    
                                                if maxLoc is not None:
                                                    #未日常签到，点击签到
                                                    dailySignFlag = True
                                                    gui.click(maxLoc[0]+36,maxLoc[1]+13)
                                                    time.sleep(0.5)
                                            
                                                #关闭签到界面
                                                maxLoc, fileName = checkPictInSpecificScope([r'.\closeSign.png'],0,0,True)
                                                if maxLoc is not None:
                                                    #showPictureWithCoord(maxLoc[0]+13,maxLoc[1]+13)
                                                    gui.click(maxLoc[0]+13,maxLoc[1]+13)
                                                    time.sleep(1)
                                                    
                                                #判断当前已经签到的角色个数
                                                print("2>>> dailySignFlag:",dailySignFlag,"addupSignFlag:",addupSignFlag)
                                                if False == dailySignFlag and False == addupSignFlag:
                                                    signedNum = signedNum + 1
                                                    if signedNum >= signedLimit:
                                                        print('2>>> signed limited')
                                                        listChara.clear() #返回选择账号登录界面
                                                        signedFlag = True #结束签到循环
                                            
                                    #进入‘系统设置’界面
                                    maxLoc, fileName = checkPictInSpecificScope([r'.\extension.png'],0,0,True)
                                    if maxLoc is not None:
                                        #showPictureWithCoord(maxLoc[0]+13,maxLoc[1]+13)
                                        gui.click(maxLoc[0]+13,maxLoc[1]+13)
                                        time.sleep(1)
                                        
                                        maxLoc, fileName = checkPictInSpecificScope([r'.\systemButton.png'],0,0,True)
                                        if maxLoc is not None:
                                            #showPictureWithCoord(maxLoc[0]+13,maxLoc[1]+13)
                                            gui.click(maxLoc[0]+13,maxLoc[1]+13)
                                            time.sleep(1)
                                    
                                        sysSettingPos, tmpfileName = waitForImages([r'.\switchChara.png'])
                                        if sysSettingPos is not None:
                                            if 0 == len(listChara):
                                                #chara 列表已处于最后一个，需切换账号
                                                print('switch account')
                                                clickWithPict(r'.\switchAcount.png')
                                                time.sleep(1)
                                                
                                            else:
                                                #继续切换角色
                                                print('switch character')
                                                clickWithPict(r'.\switchChara.png')
                                                time.sleep(1)
                                                
                                                selectCharaPos, tmpfileName = waitForImages([r'.\selectCharaWindow.png'])
                                                if selectCharaPos is not None:
                                                    print('select next character')
                                                    

if wg.FindWindow(None, 'BlueStacks'):
    print('close bule stack')                                             
    os.system("taskkill /f /im HD-Player.exe")