import tkinter
import tkinter.filedialog
from Search.search import search
import os

root = tkinter.Tk()
path = tkinter.StringVar(root, value='')
keyword = tkinter.StringVar(root, value='')
result = tkinter.StringVar(root, value='')


def DoSearch(thePath, text):
    if thePath == '':
        result.set("请输入搜索路径")
    elif text == '':
        result.set("请输入搜索内容")
    else:
        if os.path.exists(thePath):
            result.set("do searching...")
            temp = search(thePath, text)
            result.set(temp)
        else:
            result.set("路径错误")


def GetSearchPath():
    temp = tkinter.filedialog.askdirectory()
    if temp:
        path.set(temp)


inputPathLabel = tkinter.Label(root, text="输入搜索目录:")
inputKeyLabel = tkinter.Label(root, text="搜索内容:")

inputPathEntry = tkinter.Entry(root, width=70, textvariable=path)
inputKeyEntry = tkinter.Entry(root, width=70, textvariable=keyword)

browserButton = tkinter.Button(root, text="浏览", command=lambda: GetSearchPath())
searchButton = tkinter.Button(root, text="搜索", command=lambda: DoSearch(inputPathEntry.get(), inputKeyEntry.get()))

resultLabel = tkinter.Label(root, textvariable=result)


inputPathLabel.grid(row=0, column=0)
inputPathEntry.grid(row=0, column=1)
browserButton.grid(row=0, column=2)

inputKeyLabel.grid(row=1, column=0)
inputKeyEntry.grid(row=1, column=1)
searchButton.grid(row=1, column=2)

resultLabel.grid(row=2, column=0)

root.mainloop()
