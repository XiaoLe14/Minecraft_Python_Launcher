# -*- coding: utf-8 -*-
"""
@date:  2022/01/09 17:40
@author: Anker
@python：v3.10
"""
import main
import sys
import configparser
dbmysql = "123456"
def get_path(relative_path):
    try:
        base_path = sys._MEIPASS  # pyinstaller打包后的路径
    except AttributeError:
        base_path = os.path.abspath(".")  # 当前工作目录的路径

    return os.path.normpath(os.path.join(base_path, relative_path))  # 返回实际路径


import tkinter as tk
import tkinter.messagebox
import pymysql
from threading import Thread
import os

user_name_logined = None

# 登录窗口
window = tk.Tk()
window.title('登录')
window.geometry('220x200')
window.iconbitmap(get_path("picture/ico.ico"))
window.resizable(False, False)

#提示
tk.Label(window, text="登录完成请手动关闭此窗口").pack()
# 用户名密码标签
tk.Label(window, text='用户名:', bg='yellow').place(x=10, y=20)
tk.Label(window, text='密   码:', bg='yellow').place(x=10, y=50)

# 用户名输入框
var_user_name = tk.StringVar()
entry_user_name = tk.Entry(window, textvariable=var_user_name)
entry_user_name.place(x=70, y=20)

# 密码输入框
var_user_pwd = tk.StringVar()
entry_user_pwd = tk.Entry(window, textvariable=var_user_pwd, show='*')
entry_user_pwd.place(x=70, y=50)

# 记住密码
chVarDis = tk.IntVar()
remember_password_checkbutton = tk.Checkbutton(window, text="记住账号&密码", variable=chVarDis).place(x=100, y=70)
conf = configparser.ConfigParser()
try:
    # 读取
    conf.read("MPL.ini")
except:
    # 创建
    open("MPL.ini", "w")

try:
    entry_user_name.insert(0, conf.get("login", "user_name"))
    entry_user_pwd.insert(0, conf.get("login", "password"))
except:
    conf.add_section("login")
    conf.set("login", "user_name", "")
    conf.set("login", "password", "")
    conf.write(open("MPL.ini", "w"))

# 登录函数
def user_login():
    # 输入框获取用户名密码
    user_name = var_user_name.get()
    user_password = var_user_pwd.get()
    # 连接test_sql数据库
    try:
        conn = pymysql.connect(host="localhost", user="root", password=dbmysql, database="serverlist", charset="utf8mb4")
        curs = conn.cursor()
    except Exception as wrong:
        main.messageboxwrong("错误:数据库连接失败，请检查网络设置", wrong)
    # 执行SQL语句，创建user数据表
    #curs.execute(test_sql)
    # 执行SQL语句，从user数据表中查询name和password字段值
    curs.execute("SELECT name,password FROM user")
    # 将数据库查询的结果保存在result中
    result = curs.fetchall()
    # fetchone()函数它的返回值是单个的元组, 也就是一行记录, 如果没有结果, 那就会返回null
    # fetchall()函数它的返回值是多个元组, 即返回多个行记录, 如果没有结果, 返回的是()
    # assert result, "数据库无该用户信息"   # 添加断言，判断数据库有无该用户信息，没有就直接断言错误

    # 登录账号操作
    name_list = [it[0] for it in result]  # 从数据库查询的result中遍历查询元组中第一个元素name
    # 判断用户名或密码不能为空
    if not (user_name and user_password):
        tk.messagebox.showwarning(title='警告', message='用户名或密码不能为空')
    # 判断用户名和密码是否匹配
    elif user_name in name_list:
        if user_password == result[name_list.index(user_name)][1]:
            global window
            tk.messagebox.showinfo(title='欢迎您', message='       登录成功！请手动关闭所有页面！\r\n当前登录账号为：' + user_name)
            global user_name_logined
            user_name_logined = user_name
            global chVarDis
            global conf
            if chVarDis.get() == 1:
                conf.set("login","user_name",user_name)
                conf.set("login","password",user_password)
                conf.write(open("MPL.ini", "w"))

        else:
            tk.messagebox.showerror(title='错误', message='密码输入错误')
    # 账号不在数据库中，则弹出是否注册的框
    else:
        is_signup = tk.messagebox.askyesno(title='提示', message='该账号不存在，是否现在注册？')
        if is_signup:
            user_register()


# 注册函数
def user_register():
    # 确认注册函数
    def register_confirm():
        # 获取输入框内的内容
        name = new_name.get()
        password = new_password.get()
        password_confirm = new_password_confirm.get()
        playername = new_player_name.get()
        # 连接该数据库
        try:
            conn = pymysql.connect(host="localhost", user="root", password=dbmysql, database="serverlist", charset="utf8mb4")
            curs = conn.cursor()
        except Exception as wrong:
            main.messageboxwrong("错误:数据库连接失败，请检查网络设置", wrong)

        # 注册账号操作
        try:
            # 执行SQL语句，创建user数据表
            #curs.execute(test_sql)
            # 向user数据表中插入语句
            insert_sql = "INSERT INTO user(name, password, player_name) VALUES ('%s', '%s', '%s')" % (name, password, playername)
            # 读取user数据表中的name和password字段值
            read_sql = f'''select * from user where name = "{name}" and password = "{password}" and player_name = "{playername}"'''
            user_data = curs.execute(read_sql)
            # 判断注册账号和密码
            if not (name and password):
                tk.messagebox.showwarning(title='警告', message='注册账号或密码不能为空')
            elif password != password_confirm:
                tk.messagebox.showwarning(title='警告', message='两次密码输入不一致，请重新输入')
            else:
                if user_data.real:
                    tk.messagebox.showwarning(title='警告', message='该注册账号或玩家名已存在')
                else:
                    curs.execute(insert_sql)
                    tk.messagebox.showinfo(title='恭喜您', message='      注册成功！\r\n注册账号为：' + name + '\r\n玩家名为：' + playername)
            # 提交到数据库执行
            conn.commit()
            curs.close()
        except IOError:
            conn.rollback()
        # 关闭数据库连接
        conn.close()
        window_sign_up.destroy()

    # 注册窗口
    window_sign_up = tk.Toplevel(window)
    window_sign_up.iconbitmap(get_path("picture/ico.ico"))
    window_sign_up.geometry('350x200')
    window_sign_up.title('欢迎注册')
    window_sign_up.resizable(False, False)

    # 注册账号及标签、输入框
    new_name = tk.StringVar()
    tk.Label(window_sign_up, bg='green', text='注册账号：').place(x=50, y=10)
    tk.Entry(window_sign_up, textvariable=new_name).place(x=150, y=10)


    # 注册密码及标签、输入框
    new_password = tk.StringVar()
    tk.Label(window_sign_up, bg='green', text='密      码：').place(x=50, y=50)
    tk.Entry(window_sign_up, textvariable=new_password, show='*').place(x=150, y=50)

    # 重复密码及标签、输入框
    new_password_confirm = tk.StringVar()
    tk.Label(window_sign_up, bg='green', text='确认密码：').place(x=50, y=90)
    tk.Entry(window_sign_up, textvariable=new_password_confirm, show='*').place(x=150, y=90)

    # 玩家名
    new_player_name = tk.StringVar()
    tk.Label(window_sign_up, bg="green", text="玩家名：").place(x=50, y=130)
    tk.Entry(window_sign_up, textvariable=new_player_name).place(x=150, y=130)

    # 确认注册按钮及位置
    bt_confirm_sign_up = tk.Button(window_sign_up, bg='green', text='确认注册', command=register_confirm)
    bt_confirm_sign_up.place(x=150, y=160)



# 注册和登录按钮
bt_register = tk.Button(window, bg='yellow', text='注册', command=user_register)
bt_register.place(x=120, y=100)
bt_login = tk.Button(window, bg='yellow', text='登录', command=user_login)
bt_login.place(x=80, y=100)

# 主循环
window.mainloop()