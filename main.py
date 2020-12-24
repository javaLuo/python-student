import tkinter as tk
from tkinter import ttk
import sqlite3
import tkinter.messagebox as messagebox


# ####################################
# 数据库相关操作
# ####################################
class DB:
    def __init__(self, db):
        self.db = db

    # 数据库 - 按条件查询学生信息
    def getData(self, name, sub):
        conn = sqlite3.connect(self.db)
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
        conn.close()
        return res

    # 数据库 - 插入一条数据
    def insertData(self, name, sex, num, sub):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        sql = 'insert into student (name, sex, num, sub) values (?,?,?,?)'
        val = (name, sex, num, sub)
        cur.execute(sql, val)
        conn.commit()

        cur.close()
        conn.close()

    # 数据库 - 修改一条数据
    def updateData(self, id, name, sex, num, sub):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        sql = 'update student set name=?, sex=?, num=?, sub=? where id=?'
        val = (name, '男' if sex == 1 else '女', num, sub, id)

        cur.execute(sql, val)
        conn.commit()

        cur.close()
        conn.close()

    # 数据库 - 删除一条数据
    def onDeleteData(self, id):
        conn = sqlite3.connect(self.db)
        cur = conn.cursor()

        sql = 'delete from student where id=?'
        val = (id)

        cur.execute(sql, val)
        conn.commit()

        cur.close()
        conn.close()


class Main:
    def __init__(self, master, db):  # 初始化
        self.root = master
        self.db = db
        self.root.title("学生信息管理系统")
        self.root.geometry('930x500')
        self.root.minsize(930, 400)
        self.root.resizable(0, 0)

        # 绑定的变量
        self.search_name = tk.StringVar()  # 搜索 - 名字输入框的值
        self.search_sub = tk.StringVar()  # 搜索 - 专业输入框的值
        self.form_name = tk.StringVar()  # 表单 - 名字
        self.form_sex = tk.IntVar()  # 表单 - 性别
        self.form_num = tk.StringVar()  # 表单 - 学号
        self.form_sub = tk.StringVar()  # 表单 - 专业
        self.dataNow = None  # 当前列表选中的数据

        self.initUI()
        self.showData()

    def initUI(self):  # 画UI
        tk.Label(self.root).grid(row=0)
        # 新增按钮
        tk.Button(self.root, text='新增', font=('Arial', 12),
                  width=10, height=1, command=self.clickNew).grid(row=1, column=1)
        # 编辑按钮
        tk.Button(self.root, text='编辑', font=('Arial', 12),
                  width=10, height=1, command=self.clickEdit).grid(row=1, column=2)
        # 删除按钮
        tk.Button(self.root, text='删除', font=('Arial', 12),
                  width=10, height=1, command=self.onDel).grid(row=1, column=3)

        tk.Label(self.root, text=' | ', font=('Arial', 18),
                 fg="#aaa").grid(row=1, column=4)
        # 搜索框 - 名字
        tk.Label(self.root, text='姓名:', font=('Arial', 14),
                 fg="#222").grid(row=1, column=5)
        tk.Entry(self.root, show=None, font=('Arial', 12), width=15, textvariable=self.search_name).grid(
            row=1, column=6)
        # 搜索框 - 年龄
        tk.Label(self.root, text=' 专业:', font=('Arial', 14),
                 fg="#222").grid(row=1, column=7)
        tk.Entry(self.root, show=None, font=('Arial', 12),
                 width=15, textvariable=self.search_sub).grid(row=1, column=8)
        tk.Label(self.root).grid(row=1, column=9)
        # 搜索按钮
        tk.Button(self.root, text="搜索", font=('Arial', 12),
                  width=10, height=1, command=self.onSearch).grid(row=1, column=10)
        # 列表
        tk.Label(self.root).grid(row=2)
        table = ttk.Treeview(self.root, show='headings', columns=(
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

        self.table = table
        self.table.bind('<ButtonRelease-1>', self.treeviewClick)

    def addData(self, data):  # 像列表中添加数据
        if str(type(data)) == "<class 'list'>":
            for item in data:
                self.table.insert("", "end", values=item)
        else:
            self.table.insert("", "end", values=data)

    def showData(self):  # 显示所有学生信息
        data = self.db.getData(None, None)
        self.clearTree()
        self.addData(data)

    def onSearch(self):  # 搜索按钮被点击
        data = self.db.getData(self.search_name.get(), self.search_sub.get())
        self.clearTree()
        self.addData(data)

    def clearTree(self):  # 清空列表中的数据
        x = self.table.get_children()
        for item in x:
            self.table.delete(item)

    # 真正保存 新增
    def onSaveNew(self):
        formName = self.form_name.get()
        formSex = self.form_sex.get() or 0
        formNum = self.form_num.get()
        formSub = self.form_sub.get()
        if not formName:
            messagebox.showwarning('提示', '请填写姓名')
            return
        elif not formNum:
            messagebox.showwarning('提示', '请填写学号')
            return
        elif not formSub:
            messagebox.showwarning('提示', '请填写专业')
            return
        self.db.insertData(formName, '男' if formSex ==
                           1 else '女', formNum, formSub)
        self.showData()  # 刷新数据
        self.top.destroy()  # 销毁窗口
        messagebox.showinfo('提示', '添加成功')

    # 真正保存 编辑
    def onUpdate(self):
        self.db.updateData(self.dataNow[0], self.form_name.get(
        ), self.form_sex.get(), self.form_num.get(), self.form_sub.get())
        self.showData()  # 刷新数据
        self.top.destroy()  # 销毁窗口
        self.dataNow = None
        messagebox.showinfo('提示', '修改成功')

    # 点击新增按钮
    def clickNew(self):
        self.form_name.set('')
        self.form_sex.set(0)
        self.form_num.set('')
        self.form_sub.set('')
        self.tool_createModal("新增学生信息", 'new')

    # 选中某一条数据
    def treeviewClick(self, event):
        if self.table.selection():
            self.dataNow = self.table.item(self.table.selection()[0], "values")

    # 点击编辑按钮
    def clickEdit(self):
        if self.dataNow:
            print(self.dataNow)
            self.form_name.set(self.dataNow[1])
            self.form_sex.set(1 if self.dataNow[2] == '男' else 0)
            self.form_num.set(self.dataNow[3])
            self.form_sub.set(self.dataNow[4])
            self.tool_createModal("编辑学生信息，ID:"+self.dataNow[0], 'update')
        else:
            messagebox.showwarning("提示", "请先选择一个学生信息")

    # 点击删除按钮
    def onDel(self):
        if self.dataNow:
            isSure = messagebox.askokcancel("提示", "确定删除吗？")
            if isSure:
                self.db.onDeleteData(self.dataNow[0])
                self.showData()
                self.dataNow = None
        else:
            messagebox.showwarning("提示", "请先选择一个学生信息")

    # 工具 - 创建子窗口 用于新增/编辑
    # title - 模态框标题
    # type - 类型 new新增/update编辑
    def tool_createModal(self, title, type):
        top = tk.Toplevel(master=self.root)
        top.grab_set()
        top.title(title)
        top.geometry('200x200')
        top.resizable(0, 0)
        top.resizable(width=False, height=False)
        # 姓名框
        tk.Label(top, text='姓名:', font=('Arial', 14),
                 fg="#222").grid(row=1, column=1)
        tk.Entry(top, show=None, font=('Arial', 12), width=15,
                 textvariable=self.form_name).grid(row=1, column=2, columnspan=2)
        # 性别选择
        tk.Label(top, text='性别:', font=('Arial', 14),
                 fg="#222").grid(row=2, column=1)
        tk.Radiobutton(top, text="男", value=1,
                       variable=self.form_sex).grid(row=2, column=2)
        tk.Radiobutton(top, text="女", value=0,
                       variable=self.form_sex).grid(row=2, column=3)
        # 学号
        tk.Label(top, text='学号:', font=('Arial', 14),
                 fg="#222").grid(row=3, column=1)
        tk.Entry(top, show=None, font=('Arial', 12), width=15,
                 textvariable=self.form_num).grid(row=3, column=2, columnspan=2)
        # 专业
        tk.Label(top, text='专业:', font=('Arial', 14),
                 fg="#222").grid(row=4, column=1)
        tk.Entry(top, show=None, font=('Arial', 12), width=15,
                 textvariable=self.form_sub).grid(row=4, column=2, columnspan=2)
        # 保存按钮
        onSubmit = self.onSaveNew if type == 'new' else self.onUpdate
        tk.Button(top, text='保存', font=('Arial', 12), width=10,
                  height=1, command=onSubmit).grid(row=5, column=1, columnspan=2)

        self.top = top


if __name__ == '__main__':
    root = tk.Tk()
    Main(root, DB("students.db"))
    root.mainloop()
