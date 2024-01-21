import minecraft_launcher_lib
import main
import tkinter

# 直接从文档上抄的，懒得写了（qwq
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
    main.messageboxwrong("成功","安装完成")