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
import download
import os
import sys

downloadwindow = None

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

# 尝试从ini文件中读取所有选项，如果没有，就创建
try:
    # 读取并储存在Player_Name中
    Player_Name = conf.get("MPL", "Player_Name")
    JVM = conf.get("MPL","JVM")
    Java_Path = conf.get("MPL", "Java_Path")
    minecraft_directory = conf.get("MPL","Minecraft_directory")
    # 显示在输入框里
    Player_Name_Entry.insert(0, Player_Name)
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


# 展示图片的函数
def showimage(img_file):
    global Startgif
    global StartImg
    StartImg = tkinter.PhotoImage(file=img_file)
    StartImg = StartImg.subsample(2, 2)
    Startgif = tkinter.Label(window, image=StartImg)
    Startgif.place(x=50, y=90)


# 展示初始图片
showimage(get_path("picture/icon.png"))


# 启动游戏：
def game_run(minecraft_directory, start_version, options):
    # 切换图片展示
    showimage(get_path("picture/qidong.gif"))
    # 启动游戏
    main.start_minecraft(minecraft_directory, start_version, options)
    # 游戏结束了，换回图片
    if screen != "main":
        showimage(get_path("picture/icon.png"))
    else:
        pass


# 当按下启动按钮
def StartbuttonChick():
    # 获取输入框中的玩家名
    Player_Name = Player_Name_Entry.get()
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
        options = minecraft_launcher_lib.utils.generate_test_options()
        options["username"] = Player_Name
        options["jvmArguments"] = ["-Xms"+str(JVM)+"M", "-Xms"+str(JVM)+"M"]
        if Java_Path == "":
            main.messageboxwrong("提示", "未设置java，即将使用默认设置启动游戏")
        else:
            options["defaultExecutablePath"] = Java_Path
        # 用变量i实现多线程启动而不重名
        globals()[f"game{i}"] = Thread(target=game_run, args=(minecraft_directory, start_version, options))
        globals()[f"game{i}"].start()
    # 启动错误时弹出窗口
    except Exception as wrong:
        main.messageboxwrong("错误", wrong)


# 主页面隐藏
def forget_all_main_screen():
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


# 主页面显示
def place_main_screen():
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

    # 返回
    def from_AllOptions_screen_back_to_main_screen_command():
        # 全局设置隐藏
        JavaPathLabel.place_forget()
        from_AllOptions_screen_back_to_main_screen.place_forget()
        JavaPathCom.place_forget()
        ApplyAllOptionsButton.place_forget()
        JVMscale.place_forget()
        JVMLabel.place_forget()
        VersionDirLabel.place_forget()
        VersionsButton.place_forget()
        VersionDir.place_forget()
        screen = "main"
        showimage(get_path("picture/icon.png"))

        # 主页面显示
        place_main_screen()


    # 全局设置
    JavaPathLabel = tkinter.Label(window, text="Java路径设置:", font=("微软雅黑", 10))
    # JVM滑动条

    JVMLabelText.set("游戏内存设置(" + str(JVM) + "M):")
    JVMLabel = tkinter.Label(window, textvariable=JVMLabelText, font=("微软雅黑", 8))

    JVMscale.set(JVM)
    # 点击后隐藏
    from_AllOptions_screen_back_to_main_screen = tkinter.Button(window, text="返回", font="微软雅黑", command=from_AllOptions_screen_back_to_main_screen_command)
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
    minecraft_launcher_lib.install.install_minecraft_version(version, minecraft_directory, callback=callback)
    main.messageboxwrong("成功", "安装完成，请手动关闭下载页面")
    return


########################################################################################################################
########################################################################################################################
########################################################################################################################


def minecraft_install_windows(download_version,minecraft_directory):
    downloadwindow = tkinter.Tk()
    downloadwindow.title('下载中...')
    downloadwindow.geometry("250x200")
    downloadwindow.resizable(False, False)
    downloadwindow_label = tkinter.Label(downloadwindow, text="下载中...", font=("Arial", 15), bg="#426D90", fg="white", width=20)
    downloadwindow_label.pack()
    downloadwindow_text = tkinter.Text(downloadwindow)
    main.redirect_stdout_to_tkinter(downloadwindow_text)
    downloadwindow_text.pack()
    downing_thread = Thread(target=minecraft_install,args=(download_version, minecraft_directory))
    downing_thread.start()
    downloadwindow.mainloop()
    #download.minecraft_install(download_version,minecraft_directory)

    #downloadwindow.quit()


def DownloadButtonCilck():
    global minecraft_directory
    for aaa in DownloadList.curselection():
        download_version = DownloadList.get(aaa)
    try:
        download_version = download_version
        try:
            main.messageboxwrong("即将安装", "版本：" + download_version + "目录：" + minecraft_directory)
            installing_thread = Thread(target=minecraft_install_windows,args=(download_version,minecraft_directory))
            installing_thread.start()
        except Exception as wrong:
            main.messageboxwrong("安装失败", wrong)
    except:
        main.messageboxwrong("错误", "你没有选择要安装的版本！")
        return

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
DownloadListLabel = tkinter.Label(window, text="下载列表(刚下载的版本找不到请重启)：")
DownloadButtun = tkinter.Button(window, text="点击下载该版本", command=DownloadButtonCilck)

def version_list_len():
    global VersionsList
    global versionlistlen
    global minecraft_directory
    for i in range(2):
        versionlistlen = 0
        VersionsList.delete(0, "end")
        while versionlistlen < len(minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory)):
            VersionsList.insert(versionlistlen, minecraft_launcher_lib.utils.get_installed_versions(minecraft_directory=minecraft_directory)[versionlistlen]["id"])
            versionlistlen = versionlistlen + 1
        print(111)
    #time.sleep(2)

# 刷新列表
refreshButton = tkinter.Button(window, text="刷新列表", command=version_list_len())

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
