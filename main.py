import tkinter as tk
from tkinter import ttk
import sqlite3

# 初始化设置
window = tk.Tk()
window.title("学生信息管理系统")
window.geometry('930x500')
window.minsize(930, 400)

# 绑定的变量
search_name = tk.StringVar()  # 搜索 - 名字输入框的值
search_sub = tk.StringVar()  # 搜索 - 专业输入框的值

# 数据库
db = "students.db"


# ####################################
# 数据库相关操作
# ####################################

# 数据库 - 按条件查询学生信息
def getData(name, sub):
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    sql = "select * from student"
    if name and sub:
        sql = "select * from student where name like '%" + \
            name+"%' and sub like '%"+sub+"%'"
    elif name:
        sql = "select * from student where name like '%"+name+"%'"
    elif sub:
        sql = "select * from student where sub like '%"+sub+"%'"

    cur.execute(sql)
    res = cur.fetchall()
    cur.close()
    print("查询获取：", res)
    return res


# ####################################
# 业务
# ####################################

# 清空列表中的数据
def clearTree():
    x = table.get_children()
    for item in x:
        table.delete(item)


# 像列表中添加数据
def addData(data):
    if str(type(data)) == "<class 'list'>":
        for item in data:
            table.insert("", "end", values=item)
    else:
        table.insert("", "end", values=data)


# 显示所有学生信息
def showData():
    data = getData(None, None)
    clearTree()
    addData(data)


# 搜索按钮被点击
def onSearch():
    data = getData(search_name.get(), search_sub.get())
    clearTree()
    addData(data)


# 点击新增按钮
def clickNew():
    top = tk.Toplevel(master=window)
    top.grab_set()
    top.title('新增学生信息')


# 点击编辑按钮
def clickEdit():
    top = tk.Toplevel()
    top.title('编辑学生信息')


# 点击删除按钮
def onDel():
    top = tk.Toplevel()
    top.title('确定删除？')


# ####################################
# 画主界面UI
# ####################################
tk.Label(window).grid(row=0)
# 新增按钮
tk.Button(window, text='新增', font=('Arial', 12),
          width=10, height=1, command=clickNew).grid(row=1, column=1)
# 编辑按钮
tk.Button(window, text='编辑', font=('Arial', 12),
          width=10, height=1, command=clickEdit).grid(row=1, column=2)
# 删除按钮
tk.Button(window, text='删除', font=('Arial', 12),
          width=10, height=1, command=onDel).grid(row=1, column=3)

tk.Label(window, text=' | ', font=('Arial', 18),
         fg="#aaa").grid(row=1, column=4)
# 搜索框 - 名字
tk.Label(window, text='姓名:', font=('Arial', 14),
         fg="#222").grid(row=1, column=5)
tk.Entry(window, show=None, font=('Arial', 12), width=15, textvariable=search_name).grid(
    row=1, column=6)
# 搜索框 - 年龄
tk.Label(window, text=' 专业:', font=('Arial', 14),
         fg="#222").grid(row=1, column=7)
tk.Entry(window, show=None, font=('Arial', 12),
         width=15, textvariable=search_sub).grid(row=1, column=8)
tk.Label(window).grid(row=1, column=9)
# 搜索按钮
tk.Button(window, text="搜索", font=('Arial', 12),
          width=10, height=1, command=onSearch).grid(row=1, column=10)
# 列表
tk.Label(window).grid(row=2)
table = ttk.Treeview(window, show='headings', columns=(
    'id', '姓名', '性别', '学号', '专业'))
table.column("id", width=100, anchor='center')

table.column('姓名', width=200, anchor='center')
table.column('性别', width=200, anchor='center')
table.column('学号', width=200, anchor='center')
table.column('专业', width=200, anchor='center')

table.heading("id", text="ID")
table.heading("姓名", text="姓名")
table.heading("性别", text="性别")
table.heading("学号", text="学号")
table.heading("专业", text="专业")

table.grid(row=3, column=1, columnspan=10)


# INIT
showData()

window.mainloop()
