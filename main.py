import minecraft_launcher_lib
import subprocess
import tkinter
from tkinter import *
import tkinter.messagebox


# 弹窗函数
def messageboxwrong(title, show):
    tkinter.messagebox.showinfo(title=title, message=show)

# 启动游戏函数（导入目录，启动版本，选项）
def start_minecraft(minecraft_directory, start_version, options):
    try:
    # 补全游戏文件
        minecraft_launcher_lib.install.install_minecraft_version(start_version, minecraft_directory)
    # 生成启动命令
        minecraft_command = minecraft_launcher_lib.command.get_minecraft_command(start_version, minecraft_directory,
                                                                             options)
    # 运行启动命令
        subprocess.run(minecraft_command)

    # 检测错误
    except Exception as wrong:
        messageboxwrong("错误", wrong)
