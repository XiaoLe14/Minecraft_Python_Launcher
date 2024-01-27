import subprocess
import time
import tkinter
from tkinter import ttk
import minecraft_launcher_lib
import main
from threading import Thread
import tkinter.messagebox
import configparser
import psutil
from tkinter.filedialog import askdirectory
import os
import sys
import mysql.connector
import login

dbmysql = "123456"

try:
    # 创建数据库连接
    db = mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        password=dbmysql,  # 密码
        user="root",  # 用户名
        database="mysql"  # 数据库名称
    )

    # 创建游标对象，用于执行SQL查询
    cursor = db.cursor()
except Exception as wrong:
    main.messageboxwrong("错误:数据库连接失败，请检查网络设置",wrong)

# 查询所有记录
cursor.execute("SELECT name FROM serverlist.user")

# 获取查询结果
results = cursor.fetchall()
users_name = []
for row in results:
    users_name = users_name + list(row)

try:
    os.makedirs(".minecraft")
except:
    pass
downloadwindow_if = False
launcher_version = 0.12

# 获取剩余内存（M）
RAM = psutil.virtual_memory()
RAM = int(RAM.available / 1024 / 1024)

# 创建窗口
window = tkinter.Tk()

# 标题
window.title('Minecraft Python Launcher')
# 大小
window.geometry("600x400")
# 设置能不能改变长和宽
window.resizable(False, False)

if login.user_name_logined in users_name:
    pass
else:
    exit()


def get_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".")  # 当前工作目录的路径

    return os.path.normpath(os.path.join(base_path, relative_path))  # 返回实际路径

window.iconbitmap(get_path("picture/ico.ico"))

minecraft_directory = ".minecraft"
install_version = "1.17"
start_version = None
screen = "main"
JVMLabelText = tkinter.StringVar()
Java_Path = ""
JVM = 1024
versionlistlen = 0
downloadlistlen = 0
download_version = None

# Java路径下拉列表创建
JavaPathCom = ttk.Combobox(window, width=40)

# 初始化配置文件读取
conf = configparser.ConfigParser()
# 尝试读取ini配置文件，如果没成功就是没有文件，那就创建
try:
    # 读取
    conf.read("MPL.ini")
except:
    # 创建
    open("MPL.ini", "w")

# 创建玩家名输入框
Player_Name_Entry = tkinter.Entry(window)

VersionDir = tkinter.Entry(window, width=35)
user_name =  login.user_name_logined

print(login.user_name_logined)
cursor.execute(f"SELECT player_name FROM serverlist.user WHERE name='"+user_name+"'")
Player_Name = cursor.fetchall()
Player_Name = str(Player_Name)
Player_Name = Player_Name[3:-4]
Player_Name_Entry.insert(0, Player_Name)
print(Player_Name)
# 尝试从ini文件中读取所有选项，如果没有，就创建
try:
    # 读取并储存
    JVM = conf.get("MPL","JVM")
    Java_Path = conf.get("MPL", "Java_Path")
    minecraft_directory = conf.get("MPL","Minecraft_directory")
    # 显示在输入框里
    JavaPathCom.set(Java_Path)
    VersionDir.insert(0, minecraft_directory)


except:
    # 如果读取不了ini，那就创建一个
    conf.add_section("MPL")
    conf.set("MPL", "Player_Name", "")
    conf.set("MPL", "JVM", "1024")
    conf.set("MPL", "Java_Path", "")
    conf.set("MPL","Minecraft_directory",".minecraft")
    VersionDir.insert(0, minecraft_directory)
    # 进行操作
    conf.write(open("MPL.ini", "w"))

i = 0

# 标题
tilelable = tkinter.Label(window, text="Minecraft Python Launcher", bg="#426D90", fg="white", width=40, height=2,
                          font=('Arial', 20))
Player_Entry_Name = tkinter.Label(window, text="请输入玩家名:", font=("微软雅黑", 12))

Startgif = tkinter.Label(window)
StartImg = tkinter.PhotoImage()
# 展示图片的函数
def showimage(img_file):
    global StartImg
    global Startgif
    StartImg = tkinter.PhotoImage(file=img_file)
    StartImg = StartImg.subsample(2, 2)
    Startgif = tkinter.Label(window, image=StartImg)



# 展示初始图片
showimage(get_path("picture/icon.png"))


# 启动游戏：
def game_run(minecraft_directory, start_version, options):
    # 切换图片展示
    #showimage(get_path("picture/qidong.gif"))
    #Startgif.place(x=50, y=90)
    # 启动游戏
    main.messageboxwrong("正在启动", "正在启动请等待")
    main.start_minecraft(minecraft_directory, start_version, options)
    # 游戏结束了，换回图片
    #if screen == "main":
    #    showimage(get_path("picture/icon.png"))
    #    Startgif.place(x=50, y=90)
    #else:
    #    showimage(get_path("picture/icon.png"))


# 当按下启动按钮
def StartbuttonChick():
    global user_name
    global Player_Name
    # 获取输入框中的玩家名
    Player_Name = Player_Name_Entry.get()
    sql = "UPDATE serverlist.user SET player_name='"+Player_Name+"' where name='"+user_name+"'"
    cursor.execute(sql)

    # 提交更改到数据库
    db.commit()
    # 引入配置文件`
    global conf
    # 设置ini文件中的player name选项为输入框中的文字
    conf.set("MPL", "Player_Name", Player_Name)
    # 进行操作
    conf.write(open("MPL.ini", "w"))
    # 引入变量i
    global i

    # 尝试启动游戏
    try:
        global Java_Path
        global JVM
        global minecraft_directory
        for aaa in VersionsList.curselection():
            start_version = VersionsList.get(aaa)
        try:
            start_version = start_version
        except:
            main.messageboxwrong("错误","你没有选择要启动的版本！")
            return
        if not Player_Name:
            main.messageboxwrong("错误", "你没有填写玩家名")
            return
        else:
            pass
        i += 1
        #minecraft_directory = eval(repr(minecraft_directory).replace('/', '\\'))
        # 设置启动选项
        global launcher_version
        options = minecraft_launcher_lib.utils.generate_test_options()
        options["username"] = Player_Name
        options["jvmArguments"] = ["-Xms"+str(JVM)+"M", "-Xms"+str(JVM)+"M"]
        if Java_Path == "":
            main.messageboxwrong("提示", "未设置java，即将使用默认设置启动游戏")
        else:
            options["executablePath"] = Java_Path + "\\\\bin\\\\javaw.exe"
            options["launcherVersion"] = str(launcher_version)
            options["launcherName"] = "MPL" + str(launcher_version)
        # 用变量i实现多线程启动而不重名
        globals()[f"game{i}"] = Thread(target=game_run, args=(minecraft_directory, start_version, options))
        globals()[f"game{i}"].start()
    # 启动错误时弹出窗口
    except Exception as wrong:
        main.messageboxwrong("错误", wrong)


# 主页面隐藏
def forget_all_main_screen():
    global Startgif
    global StartImg
    Player_Entry_Name.place_forget()
    Player_Name_Entry.place_forget()
    Startbutton.place_forget()
    Startgif.place_forget()
    AllOptions.place_forget()
    VersionsList.place_forget()
    VersionsListLabel.place_forget()
    DownloadListLabel.place_forget()
    DownloadList.place_forget()
    DownloadButtun.place_forget()
    refreshButton.place_forget()
    MultiplayerButton.place_forget()


# 主页面显示
def place_main_screen():
    global Startgif
    tilelable.pack()
    # 请输入
    Player_Entry_Name.place(x=22, y=215)
    # 玩家名
    Player_Name_Entry.place(x=38, y=245)
    Startbutton.place(x=30, y=270)
    Startgif.place(x=50, y=90)
    AllOptions.place(x=30, y=310)
    VersionsList.place(x=220, y=110)
    VersionsListLabel.place(x=210, y=80)
    DownloadList.place(x=400,y=110)
    DownloadListLabel.place(x=380, y=85)
    DownloadButtun.place(x=460,y=350)
    refreshButton.place(x=400, y=350)
    MultiplayerButton.place(x=30, y=353)
    Startgif.place(x=50, y=90)

    # 全局设置
JavaPathLabel = tkinter.Label(window, text="Java路径设置:", font=("微软雅黑", 10))

def forget_multiplayer():
    backtomainButton.place_forget()
    serverList.place_forget()

JVMLabelText.set("游戏内存设置(" + str(JVM) + "M):")
JVMLabel = tkinter.Label(window, textvariable=JVMLabelText, font=("微软雅黑", 8))
def forget_alloptions_screen():
    global from_AllOptions_screen_back_to_main_screen
    JavaPathLabel.place_forget()
    from_AllOptions_screen_back_to_main_screen.place_forget()
    JavaPathCom.place_forget()
    ApplyAllOptionsButton.place_forget()
    JVMscale.place_forget()
    JVMLabel.place_forget()
    VersionDirLabel.place_forget()
    VersionsButton.place_forget()
    VersionDir.place_forget()

def from_AllOptions_screen_back_to_main_screen_command():
    # 全局设置隐藏
    forget_alloptions_screen()

    # 主页面显示
    place_main_screen()
    screen = "main"
    #showimage(get_path("picture/icon.png"))
    #Startgif.place(x=50, y=90)

from_AllOptions_screen_back_to_main_screen = tkinter.Button(window, text="返回", font="微软雅黑", command=from_AllOptions_screen_back_to_main_screen_command)

def AllOptionsCilck():
    # 主页面隐藏
    forget_all_main_screen()
    # 变量设置
    screen = "alloptions"

    # 引入下拉表格
    global JavaPathCom
    global JVM
    global JVMLabelText
    global JVMscale
    global JavaPathLabel

    JVMscale.set(JVM)
    # 点击后隐藏

    # 向下拉列表元组添加数据
    JavaPathCom["value"] = minecraft_launcher_lib.java_utils.find_system_java_versions()


    # 全局设置页显示
    JavaPathLabel.place(x=45, y=80)
    from_AllOptions_screen_back_to_main_screen.place(x=530, y=340)
    JavaPathCom.place(x=155, y=82)
    ApplyAllOptionsButton.place(x=480, y=340)
    JVMscale.place(x=155, y=110)
    JVMLabel.place(x=25, y=120)
    VersionDirLabel.place(x=70, y=160)
    VersionDir.place(x=155,y=165)
    VersionsButton.place(x=420,y=160)

def version_dir():
    global minecraft_directory
    minecraft_directory = askdirectory()
    VersionDir.insert(0, minecraft_directory)


def JVM_label_set(self):
    global JVM
    global JVMLabelText
    global JVMscale

    JVM = JVMscale.get()
    JVMLabelText.set("游戏内存设置(" + str(JVM) + "M):")

# 当应用按钮被点击
def apply_all_options():
    global Java_Path
    global JVM
    global conf
    global Minecraft_directory
    if JavaPathCom.get() == "":
        main.messageboxwrong("警告", "java路径为空，将使用默认设置")
        Java_Path = JavaPathCom.get()
        conf.set("MPL", "jvm", str(JVM))
        conf.set("MPL", "Java_Path", Java_Path)
        conf.set("MPL","Minecraft_directory", minecraft_directory)
        # 进行操作
        conf.write(open("MPL.ini", "w"))
        main.messageboxwrong("成功", "应用设置成功")
    else:
        Java_Path = JavaPathCom.get()
        conf.set("MPL","jvm",str(JVM))
        conf.set("MPL","Java_Path", Java_Path)
        conf.set("MPL", "Minecraft_directory", minecraft_directory)
        # 进行操作
        conf.write(open("MPL.ini", "w"))
        main.messageboxwrong("成功", "应用设置成功")


########################################################################################################################
########################################################################################################################
########################################################################################################################
# copy from https://minecraft-launcher-lib.readthedocs.io/

current_max = 0

def set_status(status: str):
    print(status)


def set_progress(progress: int):
    if current_max != 0:
        print(f"{progress}/{current_max}")

def set_max(new_max: int):
    global current_max
    current_max = new_max

callback = {
    "setStatus": set_status,
    "setProgress": set_progress,
    "setMax": set_max
}


def minecraft_install(version, minecraft_directory):
    global downloadwindow_if
    downloadwindow_if = True
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory, callback=callback)
    downloadwindow_if = False
    main.messageboxwrong("成功", "安装完成，请手动关闭下载页面，找不到版本请点击刷新按钮")


########################################################################################################################
########################################################################################################################
########################################################################################################################


def minecraft_install_windows(download_version,minecraft_directory):
    a=0
    global downloadwindow_if
    downloadwindow = tkinter.Tk()

    downloadwindow.title('下载中...')
    downloadwindow.geometry("250x250")
    #downloadwindow.resizable(False, False)
    downloadwindow_label = tkinter.Label(downloadwindow ,text="下载中...", font=("Arial", 15), bg="#426D90", fg="white", width=22)
    downloadwindow_label.pack()
    downloadwindow_text = tkinter.Text(downloadwindow, width=35, height=14)
    main.redirect_stdout_to_tkinter(downloadwindow_text)
    downloadwindow_text.pack()
    def close_downloadwindow():
        global downloadwindow_if
        if downloadwindow_if == True:
            main.messageboxwrong("警告", "你还没下载完成！")
            downloadwindow_if = False
        else:
            downloadwindow.quit()
    downloadwindow_button = tkinter.Button(downloadwindow, text="退出", command=close_downloadwindow)
    downloadwindow_button.place(x=190, y=210)
    globals()[f"downing_thread{a}"] = Thread(target=minecraft_install,args=(download_version, minecraft_directory))
    globals()[f"downing_thread{a}"].start()
    a = a + 1
    downloadwindow.mainloop()


def DownloadButtonCilck():
    global minecraft_directory
    for aaa in DownloadList.curselection():
        download_version = DownloadList.get(aaa)
    try:
        download_version = download_version
        try:
            if downloadwindow_if == True:
                main.messageboxwrong("错误", "请等待当前版本下载完成")
                return
            main.messageboxwrong("即将安装", "版本：" + download_version + "目录：" + minecraft_directory)
            a = 0
            globals()[f"installing_thread{a}"] = Thread(target=minecraft_install_windows,args=(download_version,minecraft_directory))
            globals()[f"installing_thread{a}"].start()
            a = a + 1
        except Exception as wrong:
            main.messageboxwrong("安装失败", wrong)
    except:
        main.messageboxwrong("错误", "你没有选择要安装的版本！")
        return
def backtomainbuttonCilck():
    global screen
    forget_multiplayer()
    place_main_screen()
    screen = "main"
    #showimage(get_path("picture/icon.png"))
    #Startgif.place(x=50, y=90)

#返回按钮
backtomainButton = tkinter.Button(window, text="返回", command=backtomainbuttonCilck)
serverList = tkinter.Listbox(window, width=60, height=15)
def showMultiplayer():
    global backtomainButton
    backtomainButton.place(x=550, y=20)
    serverList.place(x=130, y=80)

def MultiplayerButtonCilck():
    global screen
    global cursor
    global Startgif
    screen = "Multiplayerscreen"
    global backtomainButton
    forget_all_main_screen()
    forget_alloptions_screen()
    showMultiplayer()
    Startgif.place_forget()
    #sql = "INSERT INTO serverlist.serverslist (name, ip) VALUES (%s, %s)"
    #values = ("test", "127.0.0.1")
    #cursor.execute(sql, values)
    #db.commit()



# 启动按钮
Startbutton = tkinter.Button(window, text="启动该版本", font="微软雅黑", width="15", height="1", command=StartbuttonChick)
# 全局设置按钮
AllOptions = tkinter.Button(window, text="设置", font="微软雅黑", width="15", height="1", command=AllOptionsCilck)
# 应用按钮
ApplyAllOptionsButton = tkinter.Button(window, text="应用", font="微软雅黑", command=apply_all_options)
# JVM滑动条
JVMscale = tkinter.Scale(window, orient="horizontal", width=10, highlightthickness=0, resolution=1, from_=200, to=RAM, length=300, command=JVM_label_set)
# 版本列表
VersionsList = tkinter.Listbox(window, width=23, height=13)
VersionsListLabel = tkinter.Label(window, text="已安装的版本列表(点击选择):", font=("微软雅黑", 10))
# 游戏目录
VersionDirLabel = tkinter.Label(window, text="游戏目录：")
VersionsButton = tkinter.Button(window,text="选择",command=version_dir)
# 下载列表
DownloadList = tkinter.Listbox(window, width=23, height=13)
DownloadListLabel = tkinter.Label(window, text="下载列表：")
DownloadButtun = tkinter.Button(window, text="点击下载该版本", command=DownloadButtonCilck)
# 联机按钮
MultiplayerButton = tkinter.Button(window, text="多人联机", width=15, height=1, font="微软雅黑", command=MultiplayerButtonCilck)

def version_list_len():
    for i in range(2):
        versionlistlen = 0
        VersionsList.delete(0, "end")
        while versionlistlen < len(minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory)):
            VersionsList.insert(versionlistlen, minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory)[versionlistlen]["id"])
            versionlistlen = versionlistlen + 1
    #time.sleep(2)

def refreshButtonClick():
    global VersionsList
    global versionlistlen
    global minecraft_directory
    VersionsList.delete(0, "end")
    versionlistlen = 0
    while versionlistlen < len(minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory)):
        VersionsList.insert(versionlistlen, minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory)[versionlistlen]["id"])
        versionlistlen = versionlistlen + 1

# 刷新列表
refreshButton = tkinter.Button(window, text="刷新列表", command=refreshButtonClick)

def download_list_len(DownloadList, downloadlistlen):
    while downloadlistlen < len(minecraft_launcher_lib.utils.get_version_list()):
        DownloadList.insert(downloadlistlen, minecraft_launcher_lib.utils.get_version_list()[downloadlistlen]["id"])
        downloadlistlen = downloadlistlen + 1


if __name__ == '__main__':
    version_list_len()

    download_list_len_thread = Thread(target=download_list_len, args=(DownloadList, downloadlistlen))
    download_list_len_thread.daemon = True
    download_list_len_thread.start()
    # 主页面显示
    place_main_screen()
    window.mainloop()
