#遇见   ！！！   表示有待更改
import os
import json
from zipfile import ZipFile as OpenZipFile
from shutil import copy2 as FileCopy
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import askyesnocancel, showerror, askyesno, showinfo
from tkinter.filedialog import askdirectory
#===================================================
defaultCatalogue = os.getenv("HOMEDRIVE", default = "C:") + os.getenv("HOMEPATH", default = "\\Users\\admin") + "\\Desktop"
TempPath = os.getenv("TEMP", default = None)
DataPath = os.getenv("LOCALAPPDATA", default = None) + "\\OvercookedTool"
SaveBackupsPath = os.getenv("LOCALAPPDATA", default = None) + "\\OvercookedTool" + "\\SaveBackups"
bSaved = True#！！！
WorkingMode = 2
numberList = list("0123456789")
ROOTFileList = ["OvercookedTool.dll", "OVERCOOKED.dll", "OvercookedTool.exe", "OvercookedTool.pdb", "OvercookedTool.runtimeconfig.json", "OvercookedTool.runtimeconfig.dev.json", "OvercookedTool.deps.json", "DATA.dll", "dependent.dll"]
#---------------------------------------------------
class RootClass():#每一个页面的基本框架
    def __init__(self):
        self.frame = tk.Frame(root.rootWindow, relief="flat", bg = "white")

    def Show(self):
        self.frame.grid(row=0,column=2,sticky = "N")
#---------------------------------------------------
class GlobalFrame():
    def __init__(self):
        #根窗口初始化
        self.rootWindow = tk.Tk()
        self.rootWindow.state("zoomed")
        self.rootWindow.title("胡闹厨房存档管理器")
        if not os.path.exists(TempPath + "\\Overcooked2.ico"):
            self.CodeBinaryFile(os.getcwd() + "\\OVERCOOKED.dll", TempPath + "\\Overcooked2.ico")
        self.rootWindow.iconbitmap(TempPath + "\\Overcooked2.ico")
        self.rootWindow.protocol('WM_DELETE_WINDOW', self.CloseRootWindow)
        self.rootWindow["bg"] = "white"
        #self.rootWindow.attributes("-topmost",True,"-toolwindow",True,"-alpha",0.2)
        #完整性验证
        for i in ROOTFileList:
            if not os.path.exists(os.getcwd() + "\\" + i):
                tk.messagebox.showerror(title="项目不完整", message="缺少" + i)
                os._exit(0)
        #NET安装
        while True:
            test = subprocess.Popen([os.getcwd() + "\\OvercookedTool.exe", "decrypt", "dependent.dll", "test.txt", "1"], stderr = subprocess.PIPE)
            test.wait()
            if test.stderr.read()[:60] != b'':
                tk.messagebox.showerror(title="缺少插件", message="您的电脑未安装dotnet-sdk-3.1.412-win-x64")
                answer = tk.messagebox.askyesno(title="缺少插件", message='选"是":自动安装\n选"否":退出')
                if answer == True:
                    NETsetup = os.getcwd() + "\\dotnet-sdk-3.1.412-win-x64.exe"
                    if os.path.exists(NETsetup):
                        subprocess.call(NETsetup)
                    else:
                        tk.messagebox.showerror(title="项目不完整", message="未找到dotnet-sdk-3.1.412-win-x64.exe")
                        os._exit(0)
                else:
                    os._exit(0)
            else:
                os.remove("test.txt")
                break
        self.progressbar = ttk.Progressbar(self.rootWindow, orient = "horizontal", mode = "indeterminate", length = 200)
        self.progressbar.start(interval = 10)
        self.progressbar.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.UnzipSaveFiles()
        #以下是存储的文件检测，用于第一次启动
        if not os.path.exists(DataPath):
            os.makedirs(SaveBackupsPath)
        if not os.path.exists(DataPath + "\\savePathList2.json"):
            self.savePathList2 = []
            with open(DataPath + "\\savePathList2.json","w") as f:
                f.write(json.dumps(self.savePathList2))
        if not os.path.exists(DataPath + "\\savePathList3.json"):
            self.savePathList3 = []
            with open(DataPath + "\\savePathList3.json","w") as f:
                f.write(json.dumps(self.savePathList3))
        if not os.path.exists(DataPath + "\\remarks.json"):
            self.remarks = {}
            with open(DataPath + "\\remarks.json","w") as f:
                f.write(json.dumps(self.remarks))
        if not os.path.exists(DataPath + "\\backups.json"):
            self.backups = {}
            with open(DataPath + "\\backups.json","w") as f:
                f.write(json.dumps(self.backups))
        self.Load()

    def Save(self):
        with open(DataPath + "\\savePathList2.json","w") as f:
            f.write(json.dumps(self.savePathList2))
        with open(DataPath + "\\savePathList3.json","w") as f:
            f.write(json.dumps(self.savePathList3))
        with open(DataPath + "\\remarks.json","w") as f:
            f.write(json.dumps(self.remarks))
        with open(DataPath + "\\backups.json","w") as f:
                f.write(json.dumps(self.backups))

    def Load(self):
        with open(DataPath + "\\savePathList2.json","r") as f:
            self.savePathList2 = json.load(f)
        with open(DataPath + "\\savePathList3.json","r") as f:
            self.savePathList3 = json.load(f)
        with open(DataPath + "\\remarks.json","r") as f:
            self.remarks = json.load(f)
        with open(DataPath + "\\backups.json","r") as f:
            self.backups = json.load(f)

    def CodeBinaryFile(self, inputFile, outputFile):#对文件进行转化防止白嫖
        output = b""
        with open(inputFile,'rb') as f:
            length = len(f.read())
            for i in range(length+2):
                f.seek(-i+1,2)
                dataNow = f.read(1)
                output += dataNow
                #print('\r' + str(int(i/length*100)) + "%",dataNow, end = '')#百分比显示
        with open(outputFile,'wb') as f:
            f.write(output)

    def CloseRootWindow(self):
        if not bSaved:
            bRepliy = tk.messagebox.askyesnocancel(title="未保存退出", message="您没有对刚刚的修改进行保存，是否保存并退出？\n选 是：保存并退出\n选 否：直接退出\n选 取消：不执行任何操作")
            if bRepliy == None:
                return
            elif bRepliy == True:
                self.Save()
        self.rootWindow.destroy()

    def Web(self,url):#"关于"界面的"去看看"会跳到这里打开浏览器
        path = os.getcwd()
        if " " in path:
            for i in path.split(" ")[0][::-1]:
                if i == "\\":
                    break
                path = path.split(" ")[0][:-1]
        file = path + "\\temp.url"
        with open(file,"w") as f:
            f.write("[InternetShortcut]\nURL=" + url + "\n")
        os.system("start " + file)
        os.remove(file)

    def MakeBackup(self, gameSave, path, decodeString, reason):#reason包括:delete/cover/user
        number = 0
        part = path + "\\" + os.path.splitext(os.path.basename(gameSave))[0] + "#" + reason + "^"
        backupFile = "0"
        while os.path.exists(backupFile):
            backupFile = part + str(number) + ".json"
            number += 1
        subprocess.call([os.getcwd() + "\\OvercookedTool.exe", "decrypt", gameSave, backupFile, decodeString])

    def UnzipSaveFiles(self):
        if not os.path.exists(TempPath + "\\tool.zip"):
            self.CodeBinaryFile(os.getcwd() + "\\DATA.dll", TempPath + "\\tool.zip")
        if not os.path.exists(SaveBackupsPath + "\\0"):
            with OpenZipFile(TempPath + "\\tool.zip") as ZipF:
                ZipF.extractall(path = SaveBackupsPath)

root = GlobalFrame()
#---------------------------------------------------
class InterfaceManagement():#左侧边栏界面
    def __init__(self):
        self.bChoosePath=False
        self.bChooseSaveFolder=False
        self.bChooseSaveFiles=False
        self.bSettings=False
        self.bAbout=False
        self.bOnCycle = False
        self.frame = tk.Frame(root.rootWindow, relief="flat", bg = "deepskyblue")
        description1 = tk.Label(self.frame,width=25,height=2,justify="center",text="本工具仅支持Windows系统",fg="white",bg = "deepskyblue",font=('华文行楷',16))
        description1.grid(row=0,column=0,sticky = "N")
        self.button1 = tk.Button(self.frame,width=16,height=2, font=("微软雅黑",20), relief = "flat", activebackground = "white", activeforeground = "deepskyblue", text="选择存档包",command=lambda:SwitchingInterface("chooseSaveFolder"))
        self.button2 = tk.Button(self.frame,width=16,height=2, font=("微软雅黑",20), relief = "flat", activebackground = "#00DFFF", activeforeground = "white", text="选择存档")
        self.button5 = tk.Button(self.frame,width=16,height=2, font=("微软雅黑",20), relief = "flat", activebackground = "white", activeforeground = "deepskyblue", text="设置",command=lambda:SwitchingInterface("settings"))
        self.button6 = tk.Button(self.frame,width=16,height=2, font=("微软雅黑",20), relief = "flat", activebackground = "white", activeforeground = "deepskyblue", text="关于",command=lambda:SwitchingInterface("about"))
        self.button1.grid(row=1,column=0)
        self.button5.grid(row=5,column=0)
        self.button6.grid(row=6,column=0)
        self.dynamicString = tk.StringVar()
        self.dynamicString.set(" ")
        self.description3 = tk.Label(self.frame,width=19,height=2,justify="center",textvariable = self.dynamicString,fg="#00BFFF",bg = "deepskyblue",font=('Harlow Solid Italic',20))
        self.description3.place(rely = 0.8)
    
    def Refresh(self):
        self.button1.config(bg = "deepskyblue", fg = "white")
        self.button2.config(bg = "deepskyblue", fg = "white")
        self.button5.config(bg = "deepskyblue", fg = "white")
        self.button6.config(bg = "deepskyblue", fg = "white")
        self.button2.grid_forget()
        if self.bChooseSaveFolder:
            self.button1.config(bg = "white", fg = "deepskyblue")
        if self.bChooseSaveFiles:
            self.button2.config(bg = "#00DFFF")
            self.button2.grid(row=2,column=0)
        if self.bSettings or self.bChoosePath:
            self.button5.config(bg = "white", fg = "deepskyblue")
        if self.bAbout:
            self.button6.config(bg = "white", fg = "deepskyblue")
        root.rootWindow.update()
    
    def Show_description3Color(self, nowColor, which = "fg"):
        tempStr = "#"
        for i in nowColor:
            if i > 255:
                i = 255
            elif i < 0:
                i = 0
            a = TransferBase_str(inputStr = str(i), inputBase = 10, outputBase = 16)
            if len(a) == 1:
                a = "0" + a
            tempStr += a
        self.description3[which] = tempStr

    def Message(self, message, time_Second = 2, inputBGColor = [0, 255, 0], inputFGColor = [255, 255, 255], outputColor = [0, 191, 255]):
        self.millisecond = 10
        self.time_Second = time_Second
        self.inputFGColor = inputFGColor
        self.inputBGColor = inputBGColor
        self.outputColor = outputColor
        self.dynamicString.set(message)
        self.Show_description3Color(inputFGColor, "fg")
        self.Show_description3Color(inputBGColor, "bg")
        self.timeNumber = -1
        if not self.bOnCycle:
            root.rootWindow.after(1000, self.Refresh_Message)
            self.bOnCycle = True

    def Refresh_Message(self):
        self.timeNumber += 1
        nowColor = [0,0,0]
        for i in range(len(self.inputBGColor)):
            nowColor[i] = int( ((self.outputColor[i] - self.inputBGColor[i]) / (self.time_Second * (1000 / self.millisecond))) * self.timeNumber + self.inputBGColor[i])
        self.Show_description3Color(nowColor, "bg")
        for i in range(len(self.inputFGColor)):
            nowColor[i] = int( ((self.outputColor[i] - self.inputFGColor[i]) / (self.time_Second * (1000 / self.millisecond))) * self.timeNumber + self.inputFGColor[i])
        self.Show_description3Color(nowColor, "fg")
        if not self.timeNumber / (1000 / self.millisecond) > self.time_Second:
            root.rootWindow.after(self.millisecond, self.Refresh_Message)
        else:
            self.bOnCycle = False

    def Show(self):
        self.frame.grid(row=0,column=0,sticky = "N", ipady=root.rootWindow.winfo_height()/3+1)
        root.rootWindow.update()
#===================================================
class Settings_choosePath(RootClass):
    def __init__(self):
        super().__init__()
        self.currentSaveFolder = "无"#会用于最终输出
        self.bExistTypedSaveFolder = False
        self.AutoFindSaveFolder()
        row = 0
        prompt1_1 = tk.Label(self.frame,width=20,height=3,justify="left",text="请选择存档的路径",fg="black",bg = "white",font=('微软雅黑',25))
        prompt1_1.grid(row=row,column=0,sticky = "E")
        row += 1
        prompt2_0 = tk.Label(self.frame,width=20,height=3,justify="left",text="自动搜索结果:",fg="black",bg = "white",font=('宋体',15))
        prompt2_0.grid(row=row,column=0,sticky = "E")
        prompt2_1 = tk.Label(self.frame,height=3,justify="left",text=self.preSaveFolder1,fg="black",bg = "white",font=('宋体',15))
        prompt2_1.grid(row=row,column=1,sticky = "W")
        self.useAutoSaveFolder = tk.Button(self.frame, text="使用自动搜索结果", command=self.OnUseAutoSaveFolder, relief = "flat",width=16,height=2, font=('宋体',9), activebackground = "#00FFFF")
        self.useAutoSaveFolder.grid(row=row,column=2)
        row += 1
        prompt3_0 = tk.Label(self.frame,width=20,height=3,justify="left",text="或输入:",fg="black",bg = "white",font=('宋体',15))
        prompt3_0.grid(row=row,column=0,sticky = "E")
        self.promptEntry = tk.Entry(self.frame, bd = 5,width=100, font = ('微软雅黑',13), fg = "grey", bg = "#00DFFF", relief = "flat",validate ="focusin",validatecommand=self.DeleteEntryStrings)
        self.promptEntry.insert(0,"在这里输入一个存档路径")
        self.promptEntry.grid(row=row,column=1,sticky = "E")
        prompt3_2 = tk.Button(self.frame, text="选择目录", command=self.OnInputSaveFolder, bg = "#00DFFF", relief = "flat",width=10,height=1, font=('宋体',15), activebackground = "#00FFFF")
        prompt3_2.grid(row=row,column=2,sticky = "W")
        row += 1
        prompt4_0 = tk.Label(self.frame,width=20,height=3,justify="left",text="当前输入的目录为:",fg="black",bg = "white",font=('宋体',15))
        prompt4_0.grid(row=row,column=0,sticky = "E")
        self.dynamicString1 = tk.StringVar()
        prompt4_1 = tk.Label(self.frame,height=3,justify="left",textvariable=self.dynamicString1,fg="black",bg = "white",font=('宋体',15))
        prompt4_1.grid(row=row,column=1,sticky = "W")
        self.useTypedSaveFolder = tk.Button(self.frame, text="使用输入路径", command=self.OnUseTypedSaveFolder, relief = "flat",width=13,height=1, font=('宋体',13), activebackground = "#00FFFF")
        self.useTypedSaveFolder.grid(row=row,column=2,sticky = "W")
        row += 1
        prompt5_0 = tk.Label(self.frame,width=20,height=3,justify="left",text="当前使用的目录为:",fg="black",bg = "white",font=('宋体',15))
        prompt5_0.grid(row=row,column=0,sticky = "E")
        self.dynamicString2 = tk.StringVar()
        self.dynamicString2.set("无")
        prompt5_1 = tk.Label(self.frame,height=3,justify="left",textvariable=self.dynamicString2,fg="black",bg = "white",font=('宋体',15))
        prompt5_1.grid(row=row,column=1,sticky = "W")
        row += 1
        self.useSaveFolder = tk.Button(self.frame,width=10,height=3, font=('宋体',15),text="确定", relief = "flat",command=lambda:SwitchingInterface("settings",1), activebackground = "#00FFFF")
        self.useSaveFolder.grid(row=row,column=2)
        tk.Button(self.frame,width=10,height=3, font=('宋体',15),text="取消", relief = "flat",command=lambda:SwitchingInterface("settings"),bg = "#00DFFF", activebackground = "#00FFFF").grid(row=row,column=0)
        self.Refresh()

    def AutoFindSaveFolder(self):
        if WorkingMode == 2:
            autoPath = os.getenv("LOCALAPPDATA", default = None) + "Low\\Team17\\Overcooked2"
        elif WorkingMode == 3:
            autoPath = os.getenv("LOCALAPPDATA", default = None) + "Low\\Team17\\Overcooked All You Can Eat"
        if os.path.exists(autoPath):
            self.bExistAutoSaveFolder = True
            self.preSaveFolder1 = autoPath
        else:
            self.preSaveFolder1 = "未找到存档路径"
            self.bExistAutoSaveFolder = False

    def OnInputSaveFolder(self):
        saveFolder = tk.filedialog.askdirectory(title = "选择一个目录作为存档载入目录", initialdir = defaultCatalogue, parent = root.rootWindow)
        self.promptEntry.delete(0, "end")
        self.promptEntry.insert(0,saveFolder)

    def GetEntry(self):#每过一秒就获取一次输入栏中的路径
        if not interfaceManagement.bChoosePath:return
        saveFolder = self.promptEntry.get()
        if os.path.exists(saveFolder):
            self.dynamicString1.set(saveFolder)
            self.preSaveFolder2 = saveFolder
            self.bExistTypedSaveFolder = True
        else:
            self.dynamicString1.set("路径不存在")
            self.bExistTypedSaveFolder = False
        self.Refresh()
        root.rootWindow.after(1000, self.GetEntry)

    def OnUseAutoSaveFolder(self):
        self.currentSaveFolder = self.preSaveFolder1
        self.dynamicString2.set(self.currentSaveFolder)
        self.Refresh()

    def OnUseTypedSaveFolder(self):
        self.currentSaveFolder = self.preSaveFolder2
        self.dynamicString2.set(self.currentSaveFolder)
        self.Refresh()

    def DeleteEntryStrings(self):
        self.promptEntry.delete(0,12)

    def Refresh(self):
        if self.bExistAutoSaveFolder:
            self.useAutoSaveFolder.config(state = "normal", bg = "#00DFFF")
        else:
            self.useAutoSaveFolder.config(state = "disabled", bg = "#EEEEEE")
        if self.bExistTypedSaveFolder:
            self.useTypedSaveFolder.config(state = "normal", bg = "#00DFFF")
        else:
            self.useTypedSaveFolder.config(state = "disabled", bg = "#EEEEEE")
        if self.currentSaveFolder!="无":
            self.useSaveFolder.config(state = "normal", bg = "#00DFFF")
        else:
            self.useSaveFolder.config(state = "disabled", bg = "#EEEEEE")
        root.rootWindow.update()

    def Show(self):
        self.GetEntry()#用于重复执行
        super().Show()
#---------------------------------------------------
class Settings(RootClass):#设置界面
    def __init__(self):
        self.frame = tk.Frame(root.rootWindow, relief="flat", bg = "white")
        prompt0_0 = tk.Label(self.frame,height=3,justify="left",text="当前使用的存档路径",fg="black",bg = "white",font=('微软雅黑',20, 'bold'))
        prompt0_0.grid(row = 0,column = 0, columnspan = 2)#, sticky = "E")
        frame_path = tk.Frame(self.frame, relief="flat", bg = "white")
        frame_path.grid(row=1,column=0, columnspan = 5)
        scrollbar1= tk.Scrollbar(frame_path)
        scrollbar2 = tk.Scrollbar(frame_path, orient="horizontal")
        self.pathListBox = tk.Listbox(frame_path,selectmode = "browse",height =5,width = 100,selectbackground = "#00DFFF",xscrollcommand = scrollbar2.set, yscrollcommand = scrollbar1.set)
        for i in NowSavePathList:
            self.pathListBox.insert("end", i)
        scrollbar1.config(command = self.pathListBox.yview)
        scrollbar2.config(command = self.pathListBox.xview)
        temp = tk.Label(frame_path, text = " ", width=20, bg = "white")
        temp.grid(row=0,column=0)
        self.pathListBox.grid(row=0,column=1,columnspan = 2)
        scrollbar1.grid(row=0,column=3,rowspan = 2, sticky = "N", ipady = 20)
        scrollbar2.grid(row=1,column=1,columnspan = 2, sticky = "W", ipadx = 330)
        deleteButton = tk.Button(frame_path,width=10,height=1, font=("微软雅黑",15), bg = "#00DFFF", text="删除", relief = "flat",command=self.DeleteSavePath, activebackground = "#00FFFF")
        deleteButton.grid(row=2,column=1,sticky = "W")
        addButton = tk.Button(frame_path,width=10,height=1, font=("微软雅黑",15), bg = "#00DFFF", text="添加…", relief = "flat",command=lambda:SwitchingInterface("choosePath"), activebackground = "#00FFFF")
        addButton.grid(row=2,column=2,sticky = "E")
        prompt2_0 = tk.Label(self.frame,height=3,justify="left",text="选择目录时的默认目录:",fg="black",bg = "white",font=('微软雅黑',15, 'bold'))
        prompt2_0.grid(row=2,column=0,sticky = "E")
        self.dynamicString = tk.StringVar()
        self.dynamicString.set(defaultCatalogue)
        prompt2_1 = tk.Label(self.frame,height=3,justify="left",textvariable=self.dynamicString,fg="black",bg = "white",font=('宋体',15))
        prompt2_1.grid(row=2,column=1,sticky = "W")
        changeDefaultCatalogue = tk.Button(self.frame, text="更改", command=self.ChangeDefaultCatalogue, relief = "flat",width=13,height=1, font=('宋体',15), bg = "#00DFFF", activebackground = "#00FFFF")
        changeDefaultCatalogue.grid(row=2,column=2,sticky = "W")
        self.workingModeChosen = tk.IntVar()
        self.radiobutton2 = tk.Radiobutton(self.frame, relief = "groove", bg = "white", font=('微软雅黑','12'), command = self.WorkingModeChange, variable = self.workingModeChosen, value = 2, text = "胡闹厨房2")
        self.radiobutton3 = tk.Radiobutton(self.frame, relief = "groove", bg = "white", font=('微软雅黑','10'), command = self.WorkingModeChange, variable = self.workingModeChosen, value = 3, text = "胡闹厨房-全都好吃")
        if WorkingMode == 2:
            self.radiobutton2.select()
        elif WorkingMode == 3:
            self.radiobutton3.select()
        self.choseWorkingMode = tk.Label(self.frame,height=3,justify="left",text="模式",bg = "white",font=('微软雅黑',15, 'bold'))
        self.choseWorkingMode.grid(row = 3, column = 0)
        self.radiobutton2.grid(row = 3, column = 1, sticky = "W")
        self.radiobutton3.grid(row = 3, column = 2, sticky = "W")
        self.information = tk.Button(self.frame, text="使用的常见Q&A", command=lambda:tk.messagebox.showinfo(title = "常见Q&A", message = "一、选择存档包部分\n\t1.备注有什么用?\n\t答:备注可以方便区分不同的存档包\n二、选择存档部分\n\t1.覆盖游戏存档是什么意思?\n\t答:本工具会独立一份你的存档出来到工具里,一般更改存档时会同步修改独立出来的部分和你的存档, 但是在增加存档时就需要这个覆盖功能进行手动同步\n\t2.为什么我的存档变黄了?\n\t答:存档变黄的意思就是这个存档只存在于工具中,游戏无法识别,如果需要游戏识别,可以使用覆盖游戏存档,这样就不会变黄了"), relief = "flat",width=20,height=2, font=('宋体',15, "bold"), bg = "#00DFFF", activebackground = "#00FFFF")
        self.information.grid(row = 4, column = 1)
        self.Version = tk.Label(self.frame,width=15,height=2,justify="center",text="v0.3.1 - Beta version",fg="cornflowerblue",bg = "white",font=('Harlow Solid Italic',20))
        self.Version.grid(row = 99, column = 99)
    
    def WorkingModeChange(self):
        global WorkingMode
        if WorkingMode != self.workingModeChosen.get():
            WorkingMode = self.workingModeChosen.get()
            SwitchWorkingMode()

    def ChangeDefaultCatalogue(self):
        global defaultCatalogue
        a = tk.filedialog.askdirectory(title = "选择一个目录作为选择目录时的默认目录", initialdir = defaultCatalogue, parent = root.rootWindow)
        if a:
            defaultCatalogue = a
            self.dynamicString.set(defaultCatalogue)

    def DeleteSavePath(self):
        for i in range(self.pathListBox.size()):
            if self.pathListBox.selection_includes(i):
                NowSavePathList.pop(i)
        Refresh_Path()

    def Show(self):
        super().Show()
#---------------------------------------------------
class About(RootClass):#关于界面
    def __init__(self):
        super().__init__()
        prompt1 = tk.Label(self.frame,bg = "white",font=('方正舒体',35), text = "要是好用就支持一下我吧ヾ(@^▽^@)ノ")
        white1 = tk.Frame(self.frame, width=20, bg = "white")
        white2 = tk.Frame(self.frame, height=50, bg = "white")
        prompt2 = tk.Label(self.frame,bg = "white",font=('Tw Cen MT Condensed',25), text = "\tGitHub:\thttps://github.com/StaryDreamer/OvercookedSaveTool")
        prompt3 = tk.Label(self.frame,bg = "white",font=('华文琥珀',25), text = "            B站：https://www.bilibili.com/video/BV1Fq4y1Y7gu")
        prompt4 = tk.Label(self.frame,bg = "white",font=('华文琥珀',25), text = "            Q群：     156986240")
        prompt5 = tk.Label(self.frame,bg = "white",font=('华文新魏',40), text = "\t感谢你的使用~")
        prompt6 = tk.Label(self.frame,bg = "white",font=('华文彩云',25), text = "\t\t2022.4")
        Button1 = tk.Button(self.frame,width=10,height=1, font=("微软雅黑",15), bg = "gold", text="去看看→", relief = "flat",command=lambda:root.Web("https://github.com/StaryDreamer/OvercookedSaveTool"), activebackground = "#FFF700")
        Button2 = tk.Button(self.frame,width=10,height=1, font=("微软雅黑",15), bg = "gold", text="去看看→", relief = "flat",command=lambda:root.Web("https://www.bilibili.com/video/BV1Fq4y1Y7gu/"), activebackground = "#FFF700")
        Button1.grid(row=1,column=2, sticky = "W")
        Button2.grid(row=2,column=2, sticky = "W")
        white1.grid(row = 0, column = 0)
        prompt1.grid(row = 0, column = 1, columnspan = 2, sticky = "W")
        prompt2.grid(row = 1, column = 1, sticky = "W")
        prompt3.grid(row = 2, column = 1, sticky = "W")
        prompt4.grid(row = 3, column = 1, sticky = "W")
        white2.grid(row = 4, column = 0)
        prompt5.grid(row = 5, column = 1, sticky = "W")
        prompt6.grid(row = 6, column = 2, sticky = "W")
    
    def Show(self):
        super().Show()
#---------------------------------------------------
class Main_chooseSaveFolder(RootClass):
    def FindDecodeString(self, inputPath):
        decodeString = ""
        for strNum in range(0,-len(inputPath),-1):
            if inputPath[strNum] == "\\":
                break
            elif inputPath[strNum] in numberList:
                decodeString += inputPath[strNum]
        return decodeString[::-1]#反转字符串

    def __init__(self):
        super().__init__()
        self.bAim1 = False
        self.aim1 = -1
        self.saveFolderList = []
        '''
        saveFolderList的数据结构(括号内是当前位置说明，请去除)：
                [(总列表)
                    [(存档文件夹1)
                        [(存档文件夹1第一项)
                            该存档文件夹路径,
                            商店,
                            好友代码,
                            数字(Steam：1, Epic：2, 其它：3),
                            解密秘钥,
                        ],
                        (存档文件夹1第二项)存档1,
                        (存档文件夹1第三项)存档2,
                        ……,
                    ],
                    [(存档文件夹2)
                        [(存档文件夹2第一项)
                            该存档文件夹路径,
                            商店,
                            好友代码,
                            数字(Steam：1, Epic：2, 其它：3),
                            解密秘钥,
                        ],
                        (存档文件夹2第二项)存档1,
                        (存档文件夹2第三项)存档2,
                        ……,
                    ],
                    ……,
                ]
        '''
        for current in NowSavePathList:#以下是存档寻找及商店确定，本行是对每个输入的路径循环
            #以下是输入的路径处理
            temp = self.FindSaveFiles(current)
            if temp!=[]:
                self.saveFolderList.append(temp)
            #以上是输入的路径处理，以下是 在输入的路径里 寻找过的 可能是存档文件夹的文件夹 的处理
            for i in self.FindSaveFolder(current):
                temp = self.FindSaveFiles(i)
                if temp!=[]:
                    self.saveFolderList.append(temp)
            #按330行的列表 的数据结构 进行添加
            if WorkingMode == 2:
                for i in self.saveFolderList:
                    temp = i[0][0] + "\\steam_autocloud.vdf"
                    if os.path.exists(temp):
                        i[0].append("Steam")
                        with open(temp,'r') as f:
                            i[0].append(f.read()[39:-4])
                        i[0].append(1)
                        #下面是Steam的解密秘钥添加
                        i[0].append(self.FindDecodeString(i[0][0]))
                    else:
                        temp = subprocess.Popen([os.getcwd() + "\\OvercookedTool.exe", "decrypt", i[0][0] + "\\Meta_SaveFile.save", TempPath + "\\a.txt", "Epic.OnlineServices.EpicAccountId"], stdout = subprocess.PIPE)
                        temp.wait()
                        if temp.stdout.read() == b"":#b"It was not possible to find any compatible framework version\r\nThe framework 'Microsoft.NETCore.App', version '3.1.0' was not found.\r\n  - The following frameworks were found:\r\n      5.0.12 at [C:\\Program Files\\dotnet\\shared\\Microsoft.NETCore.App]\r\n\r\nYou can resolve the problem by installing the specified framework and/or SDK.\r\n\r\nThe specified framework can be found at:\r\n  - https://aka.ms/dotnet-core-applaunch?framework=Microsoft.NETCore.App&framework_version=3.1.0&arch=x64&rid=win10-x64\r\n"
                            i[0].append("Epic")
                            i[0].append("")
                            i[0].append(2)
                            i[0].append("Epic.OnlineServices.EpicAccountId")
                        else:
                            i[0].append("???")
                            i[0].append("")
                            i[0].append(3)
                            i[0].append(self.FindDecodeString(i[0][0]))
            elif WorkingMode == 3:
                for i in self.saveFolderList:
                    temp = current + "\\steam_autocloud.vdf"
                    i[0].append("Steam")
                    if os.path.exists(temp):
                        with open(temp,'r') as f:
                            i[0].append(f.read()[39:-4])
                    else:
                        i[0].append("")
                    i[0].append(1)
                    #下面是Steam的解密秘钥添加
                    i[0].append(self.FindDecodeString(i[0][0]))
        #文件列表准备完毕，开始构建图形界面
        chooseSaveFolder_prompt0_0 = tk.Label(self.frame,width=20,height=3,justify="left",text="请选择要编辑的存档文件夹",fg="black",bg = "white",font=('微软雅黑',30))
        chooseSaveFolder_prompt0_0.grid(row = 0,column = 0,columnspan = 2, rowspan = 2)
        if NowSavePathList == []:
            chooseSaveFolder_prompt0_0.config(text = "诶呀,这里什么也没有呢~ 到设置中添加一个路径吧",width = 50)
            return
        self.prompt0_5 = tk.Button(self.frame,width=20,height=1,text="添加备注", font=('微软雅黑',15), state = "disabled", bg = "#EEEEEE", activebackground = "lightseagreen", command = self.AddRemarks, relief = "flat")
        self.prompt0_5.grid(row = 0,column = 5)
        self.Entry = tk.Entry(self.frame, bd = 5,width=49, font = ('微软雅黑',13), fg = "grey", bg = "#00DFFF", relief = "flat",validate ="focusin",validatecommand=self.DeleteEntryStrings)
        self.Entry.insert(0,"在这里输入备注")
        self.Entry.grid(row=0,column=3,sticky = "S")
        self.Refresh1()

    def FindSaveFiles(self, path):
        tL = []
        fileList = os.listdir(path)
        for i in range(len(fileList)):#筛选存档
            if fileList[i][-5:]!=".save":
                tL.append(i)
        for i in range(len(tL)):
            fileList.pop(tL[i] - i)
        for i in range(len(fileList)):#补全路径
            fileList[i] = path+"\\"+fileList[i]
        tL = []
        for i in range(len(fileList)):#去除文件夹
            if os.path.isdir(fileList[i]):
                tL.append(i)
        for i in range(len(tL)):
            fileList.pop(tL[i] - i)
        if fileList == []:#无存档特殊情况处理
            return []
        fileList.insert(0,[path])
        return fileList
    
    def FindSaveFolder(self, path):#返回指定目录的存档文件夹
        fileList = os.listdir(path)#得到指定目录的文件列表
        tL = []
        for i in range(len(fileList)):#补全路径
            fileList[i] = path+"\\"+fileList[i]
        for i in range(len(fileList)):#去除文件项
            if os.path.isfile(fileList[i]):
                tL.append(i)
        for i in range(len(tL)):
            fileList.pop(tL[i] - i)
        return fileList
    
    def AddRemarks(self):
        root.remarks[self.saveFolderList[self.aim1][0][0]] = self.Entry.get()
        self.Refresh1()
    
    def Combobox_Selected(self, event):#event不知道怎么用，就没用
        temp = ""
        for i in self.Combobox1_3.get():#获取选中项的数字
            if i == ":":
                break
            elif i == "-":
                self.bAim1 = False
                self.Refresh2()
                return
            elif i in numberList:
                temp += i
        self.aim1 = int(temp)-1#使数字与文件列表下标匹配
        self.bAim1 = True
        self.Refresh2()
    
    def DeleteEntryStrings(self):
        self.Entry.delete(0,8)
    
    def Refresh1(self):
        row1 = 2
        row2 = 2
        row3 = 2
        tempList = ["-在这里选择备注增加到哪个存档-"]
        for i in range(len(self.saveFolderList)):#根据__init__的文件列表生成按钮
            if self.saveFolderList[i][0][0] in root.remarks:#添加备注
                tempRemarks = root.remarks[self.saveFolderList[i][0][0]]
            else:
                tempRemarks = "无"
                root.remarks[self.saveFolderList[i][0][0]] = tempRemarks
            column = 2*self.saveFolderList[i][0][3]-1#为每列的空格预留空间
            temp = ""
            #下方是 按商店分竖列 进行按钮摆放，每放一次就将本列的行(row)数加一
            if column == 1:
                temp += "\n该存档所属账户的好友代码：" + self.saveFolderList[i][0][2]
                row = row1
                row1 += 1
            elif column == 3:
                row = row2
                row2 += 1
            else:
                row = row3
                row3 += 1
            temp += "\n备注：" + tempRemarks
            name = "【" + self.saveFolderList[i][0][1] + "】" + self.saveFolderList[i][0][0][0:3] + "…" + self.saveFolderList[i][0][0][-36:]#路径可能过长，截取前3后36
            tempList.append(str(i+1) + ":" + name)#这是添加备注时下拉列表的内容，在491行使用
            tempButton = tk.Button(self.frame,width=50,height=4, font=('宋体',15), bg = "#00DFFF", text=name + temp, justify = "center", relief = "flat",command=SwitchingInterfaceClosure("chooseSaveFiles", i, name + temp), activebackground = "#00FFFF")
            tempButton.grid(row=row,column=column)
            tempLabel = tk.Label(self.frame, text = " ",bg = "white")
            tempLabel.grid(row=row,column=column+1)
        self.Combobox1_3 = ttk.Combobox(self.frame,width=48, font = ('微软雅黑',13), state = "readonly")
        self.Combobox1_3.bind("<<ComboboxSelected>>",self.Combobox_Selected)
        self.Combobox1_3["value"] = tuple(tempList)
        self.Combobox1_3.current(self.aim1+1)
        self.Combobox1_3.grid(row=1,column=3,sticky = "N")
        root.rootWindow.update()
    
    def Refresh2(self):
        if self.bAim1:
            self.prompt0_5.config(state = "normal", bg = "lightgreen")
        else:
            self.prompt0_5.config(state = "disabled", bg = "#EEEEEE")
        root.rootWindow.update()

    def Show(self):
        super().Show()
#---------------------------------------------------
class Main_chooseSaveFiles():#这个类的鼠标滚动事件绑定比较乱,建议用搜索寻找bind函数来归类查看
    def __init__(self):
        self.bModify = False
        self.bAdministrateBackup = False
        self.bAdjustOrder = False
        self.bAddRemarks = False
        self.bAddSave = False
        self.bMultipleChoiceMode = False
        
        #一级界面放置
        self.rootFrame = tk.Frame(root.rootWindow, relief="flat", bg = "#00DFFF")

        #工具栏
        self.toolsFrame = tk.Frame(self.rootFrame, relief="flat", bg = "#009FFF")
        self.adjustOrderButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="调整顺序", command = self.InterfaceManagementClosure("adjustOrder"))
        self.addRemarksButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="添加备注", command = self.InterfaceManagementClosure("addRemarks"))
        self.addSaveButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="增加存档", command = self.InterfaceManagementClosure("addSave"))
        self.pasteButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="粘贴", command = self.OnPaste)
        self.copyButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="复制", command = self.OnCopy)
        self.deleteButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="删除", command = self.OnDelete)
        self.coverButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="覆盖游戏存档", command = self.OnCover)
        self.multipleChoiceModeButton = tk.Button(self.toolsFrame, width=8, height=1, font=('微软雅黑',10), bg = "lightgreen", activebackground = "lightseagreen", relief = "flat", text="多选", command = self.InterfaceManagementClosure("multipleChoiceMode"))
        self.adjustOrderButton.grid(row = 0,column = 0)
        self.addRemarksButton.grid(row = 0,column = 1)
        self.addSaveButton.grid(row = 0,column = 2)
        self.pasteButton.grid(row = 0,column = 3)
        self.copyButton.grid(row = 1, column = 0)
        self.deleteButton.grid(row = 1, column = 1)
        self.coverButton.grid(row = 1, column = 2)
        self.multipleChoiceModeButton.grid(row = 1,column = 3)
        
        #下方界面
        #这里为了实现框架可滚动需要先将框架放置在画布上，再用滚动条滚动画布以便滚动框架，画布和滚动条都放在rootFrame上
        self.scrollbarOfFrame= tk.Scrollbar(self.rootFrame)
        self.canvas = tk.Canvas(self.rootFrame, height = root.rootWindow.winfo_height(), bg = "#00DFFF", bd = 0, width = 270)
        self.frame = tk.Frame(self.canvas, relief="flat", bg = "#00DFFF")
        self.frame.bind("<MouseWheel>", self.OnMouseWheel)
        self.frame.grid(row = 0,column = 0)
        self.title = tk.Label(self.frame,height=3,justify="left",fg="black",bg = "#00DFFF",font=('微软雅黑',10))
        self.backupsButton = tk.Button(self.frame,width=16,height=2, font=("微软雅黑",20), text = "存档的备份", bg = "#00DFFF",fg = "white", relief = "flat", activebackground = "#00FFFF", activeforeground = "white")
        self.mataSaveFileButton = tk.Button(self.frame, width=22, height = 3, font=('微软雅黑',15), text = "根存档",command = self.SwitchClosure("Meta_SaveFile#sys.json"), bg = "#00DFFF",fg = "white", relief = "flat", activebackground = "#00FFFF", activeforeground = "white")
        self.title.grid(row = 0, column = 0)
        self.title.bind("<MouseWheel>", self.OnMouseWheel)
        self.backupsButton.grid(row = 1, column = 0, sticky = "E")
        self.backupsButton.bind("<MouseWheel>", self.OnMouseWheel)
        self.mataSaveFileButton.grid(row = 2, column = 0)
        self.mataSaveFileButton.bind("<MouseWheel>", self.OnMouseWheel)
        #根字典定义
        self.IndefinitePartRefresh()
        
        #二级界面放置
        self.secondary_rootFrame = tk.Frame(root.rootWindow, relief="flat", bg = "white")
        self.secondary_canvas = tk.Canvas(self.secondary_rootFrame, height = root.rootWindow.winfo_height(), bg = "#FFFFFF", bd = 0, width = 270)#！！！
        self.secondary_scrollbarOfFrame= tk.Scrollbar(self.secondary_rootFrame)
        self.secondary_frame = tk.Frame(self.secondary_canvas, relief="flat", bg = "#FFFFFF")
        self.adjustOrder_frame = tk.Frame(self.secondary_frame, relief="flat", bg = "white")
        self.addRemarks_frame = tk.Frame(self.secondary_frame, relief="flat", bg = "white")
        self.addSave_frame = tk.Frame(self.secondary_frame, relief="flat", bg = "white")
        self.multipleChoiceMode_frame = tk.Frame(self.secondary_frame, relief="flat", bg = "white")
        
        #二级_多选界面放置
        self.secondary_button = tk.Button(self.multipleChoiceMode_frame, width=10, height=3, font=('宋体',15), text="确定", relief = "flat", command = self.InterfaceManagementClosure("multipleChoiceMode"), bg = "#00DFFF")
        self.secondary_button.grid(row = 1, column = 3)
        
        #二级_增加存档界面放置
        self.secondary_addSave_bSelected = False
        self.secondary_addSave_aim = 0
        self.secondary_addSave_title = tk.Label(self.addSave_frame, height=3, font=('微软雅黑',25), text = "增加新的存档", bg = "white")
        self.secondary_addSave_title.grid(row = 0, column = 0, sticky = "W")
        self.secondary_addSave_label1 = tk.Label(self.addSave_frame, height=3, font=('微软雅黑',15), bg = "white")
        self.secondary_addSave_label2 = tk.Label(self.addSave_frame, height=3, font=('微软雅黑',15), bg = "white")
        self.secondary_addSave_label1.grid(row = 2, column = 0, sticky = "W")
        self.secondary_addSave_label2.grid(row = 4, column = 0, sticky = "W")
        self.secondary_addSave_chosenStr = tk.StringVar()
        self.secondary_addSave_radiobutton1 = tk.Radiobutton(self.addSave_frame, relief = "groove", bg = "white", font=('微软雅黑','12','bold'), variable = self.secondary_addSave_chosenStr)
        self.secondary_addSave_radiobutton2 = tk.Radiobutton(self.addSave_frame, relief = "groove", bg = "white", fg='black', font=('微软雅黑','10'), variable = self.secondary_addSave_chosenStr)
        self.secondary_addSave_radiobutton1.grid(row = 3, column = 0, sticky = "W")
        self.secondary_addSave_radiobutton2.grid(row = 5, column = 0, sticky = "W")
        tempList = ["-在这里选择增加哪个部分存档-"]
        count = 1
        for i in self.frameDict:
            infoList = self.frameDict[i]["info"]
            tempList.append(str(count) + ":" + infoList[0] + " " + infoList[1])#这是添加备注时下拉列表的内容
            count += 1
        self.secondary_addSave_combobox = ttk.Combobox(self.addSave_frame, width=48, font = ('微软雅黑',13), value = tuple(tempList), state = "readonly")
        self.secondary_addSave_combobox.bind("<<ComboboxSelected>>",self.Combobox_Selected)
        self.secondary_addSave_combobox.current(self.secondary_addSave_aim)
        self.secondary_addSave_combobox.grid(row=1,column=0,sticky = "S")
        self.ensureButton = tk.Button(self.addSave_frame, width=10, height=3, font=('宋体',15),text="确定", relief = "flat", command = lambda:self.OnEnsure(), activebackground = "#00FFFF")
        self.ensureButton.grid(row = 10, column = 1)
        
        #二级界面滚动条相关#！！！！
        self.secondary_canvas.grid(row = 0, column = 0, sticky = "N")
        #self.secondary_scrollbarOfFrame.grid(row = 0, column = 1, ipady = 450, sticky = "N")#ipady须更改，没放(因为没做“求每个框架的height”)！！！
        self.secondary_canvas.create_window((0,0), window = self.secondary_frame, anchor = "nw", height = 500)#height须更改！！！
        self.secondary_canvas.configure(yscrollcommand = self.secondary_scrollbarOfFrame.set, scrollregion=self.secondary_canvas.bbox("all"))
        self.secondary_canvas.bind("<MouseWheel>", self.Secondary_onMouseWheel)
        self.secondary_scrollbarOfFrame.config(command = self.secondary_canvas.yview)
        self.secondary_frame.grid(row = 0,column = 0)

    def OnMouseWheel(self, event):
        offset = int((-event.delta)/100)
        self.canvas.yview_scroll(offset,'units')

    def Secondary_onMouseWheel(self, event):
        pass
    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓工具部分
    def OnPaste(self):
        '''
        self.copyList:
            [
            源目录，
                [
                    文件1源名称，
                    文件1目标名称（后面添加）
                ]，
                [
                    文件2源名称，
                    文件2目标名称（后面添加）
                ]……
            ]
        '''
        try:a = self.copyList[0]
        except:return
        if self.copyMode != WorkingMode:return
        bExistSameSave = False
        sameCount = 0
        for i in range(len(self.copyList)):
            if i == 0:continue
            if self.copyList[i][0] == "Meta_SaveFile#sys.json":
                self.copyList[i].append("Meta_SaveFile#sys.json")
            elif os.path.exists(self.currentSavePath + "\\" + self.copyList[i][0]):#处理相同档位的存档
                tL = self.copyList[i][0][::-1].split("_", 1)
                part1 = tL[1][::-1]
                tL = tL[0][::-1].split("#", 1)
                number = sameCount
                part2 = tL[1]
                save = part1 + "_" + str(number) + "#" + part2
                while os.path.exists(self.currentSavePath + "\\" + save):
                    save = part1 + "_" + str(number) + "#" + part2
                    number += 1
                bExistSameSave = True
                self.copyList[i].append(save)
                sameCount = number
            else:
                self.copyList[i].append(self.copyList[i][0])
        if bExistSameSave:
            answer = tk.messagebox.askyesno(title="提示", message="发现相同档位的存档，粘贴操作会自动将相同档位的档位数字后延\n是否继续？")
            if answer == False:
                return
        copyedItem = 0
        for i in range(len(self.copyList)):
            if i == 0:
                path = self.copyList[i]
                continue
            fromPath = path + "\\" + self.copyList[i][0]
            toPath = self.currentSavePath + "\\" + self.copyList[i][1]
            if fromPath != toPath:
                FileCopy(fromPath, toPath)
                copyedItem += 1
        interfaceManagement.Message(message = "粘贴完成\n已粘贴" + str(copyedItem) + "个项")
        self.Hide()
        self.IndefinitePartRefresh()
        self.LocalRefresh()

    def OnCopy(self):
        if self.now != []:
            self.copyList = [self.currentSavePath, [self.now]]
        else:
            tL = self.chosenString.get().split("\n", 1)
            if len(tL) == 1:return
            self.copyedString.set("当前已复制项为:\n" + tL[1])
            self.copyList = [self.currentSavePath]
            for i in self.chosenList:
                if i == None:
                    continue
                self.copyList.append([i[1]])
        self.copyMode = WorkingMode
        interfaceManagement.Message(message = "复制完成\n已复制" + str(len(self.copyList)-1) + "个项")

    def OnDelete(self):
        if self.now != []:
            self.chosenList = [["", self.now]]
        message = "此操作不可撤销!!!\n是否继续？"
        for i in self.chosenList:
            if i != None:
                if "Meta_SaveFile#sys.json" in i:
                    message += "(不会删除根存档)"
        answer = tk.messagebox.askyesno(title = "提示", message = message)
        if answer == False:return
        path = self.currentSavePath
        tempA = len(self.chosenList)
        for i in self.chosenList:
            if i == None or i[1] == "Meta_SaveFile#sys.json":
                tempA -= 1
                continue
            os.remove(path + "\\" + i[1])
            gameSave = main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList][0][0] + "\\" + i[1].split("#")[0] + ".save"#这一行是把各种东西合并,好玩。具体拆解见下方OnCover函数的倒数几行
            if os.path.exists(gameSave):
                encodeStrings = main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList][0][4]
                root.MakeBackup(gameSave = gameSave, path = self.currentSavePath, decodeString = encodeStrings, reason = "delete")
                os.remove(gameSave)
                if gameSave in main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList]:
                    main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList].remove(gameSave)
        if tempA == 0:
            interfaceManagement.Message(message = "无删除项", inputBGColor = [255, 0, 0])
        else:
            interfaceManagement.Message(message = "删除完成\n已删除" + str(tempA) + "个项")
        self.Hide()
        self.IndefinitePartRefresh()
        self.LocalRefresh()

    def OnCover(self):
        if self.now != []:
            self.chosenList = [["", self.now]]
        message = "此操作不可撤销!!!\n是否继续？"
        answer = tk.messagebox.askyesno(title = "提示", message = message)
        if answer == False:return
        path = main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList][0][0]
        encodeStrings = main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList][0][4]
        tempA = len(self.chosenList)
        for i in self.chosenList:
            if i == None:
                tempA -= 1
                continue
            tL = i[1].split("#")
            outputFile = tL[0] + ".save"
            gameSave = path + "\\" + outputFile
            if os.path.exists(gameSave):
                root.MakeBackup(gameSave = gameSave, path = self.currentSavePath, decodeString = encodeStrings, reason = "cover")
            subprocess.call([os.getcwd() + "\\OvercookedTool.exe", "encrypt", self.currentSavePath + "\\" + i[1], gameSave, encodeStrings])
            main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList].append(gameSave)
        if tempA == 0:
            interfaceManagement.Message(message = "无覆盖项", inputBGColor = [255, 0, 0])
        else:
            interfaceManagement.Message(message = "覆盖完成\n已覆盖" + str(tempA) + "个项")
        self.Hide()
        self.IndefinitePartRefresh()
        self.LocalRefresh()
    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓增加存档部分
    def OnAddSave(self):
        if WorkingMode == 2:
            self.secondary_addSave_label1.config(fg = "gold", text = "高端大气上档次作者自己玩的超厉害无敌帅的")
            self.secondary_addSave_radiobutton1.config(text = "三星大存档", value = "2#3")
            self.secondary_addSave_label2["text"] = "平平无奇的"
            self.secondary_addSave_radiobutton2.config(text = "普通新存档", value = "2#0", state = "normal")
        elif WorkingMode == 3:
            self.secondary_addSave_label1.config(fg = "black", text = "平平无奇的")
            self.secondary_addSave_radiobutton1.config(text = "普通新存档", value = "3#0")
            self.secondary_addSave_label2["text"] = "无聊透顶糟糕的"
            self.secondary_addSave_radiobutton2.config(text = "辅助模式新存档", value = "", state = "disabled")
        self.secondary_addSave_radiobutton1.select()
        self.Refresh_ensureButton()

    def Refresh_ensureButton(self):
        if self.secondary_addSave_bSelected:
            self.ensureButton.config(state = "normal", bg = "#00DFFF")
        else:
            self.ensureButton.config(state = "disabled", bg = "#EEEEEE")

    def Combobox_Selected(self, event):#event不知道怎么用，就没用
        temp = ""
        for i in self.secondary_addSave_combobox.get():#获取选中项的数字
            if i == ":":
                break
            elif i == "-":
                self.secondary_addSave_bSelected = False
                self.Refresh_ensureButton()
                return
            elif i in numberList:
                temp += i
        self.secondary_addSave_aim = int(temp)#使数字与文件列表下标匹配
        self.secondary_addSave_bSelected = True
        self.Refresh_ensureButton()

    def OnEnsure(self):
        tL = []
        for i in self.frameDict.keys():
            tL.append(i)
        firstItem = tL[self.secondary_addSave_aim - 1]
        tL = self.secondary_addSave_chosenStr.get().split("#")
        currentPath = SaveBackupsPath + "\\0\\" + str(tL[0])
        for i in os.listdir(currentPath):
            if i.split("_")[0] == firstItem:
                tempStr = i.split("#")[0]
                break
        saveList = os.listdir(self.currentSavePath)
        count = 0
        currentSysFile = tempStr + "_" + str(count) + "#sys.json"
        while currentSysFile in saveList:
            count += 1
            currentSysFile = tempStr + "_" + str(count) + "#sys.json"
        outputFile = self.currentSavePath + "\\" + currentSysFile
        FileCopy(currentPath + "\\" + tempStr + "#" + tL[1] + ".json", outputFile)
        self.Hide()
        self.IndefinitePartRefresh()
        self.LocalRefresh()
    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓多选部分
    def OnMultipleChoiceMode(self):
        self.canvas["width"] = 380
        self.multipleChoiceModeButton["text"] = "确定"
        self.originalList = [tk.StringVar()]
        self.chosenList = [None]
        self.checkbuttonList = [tk.Checkbutton(self.frame, variable = self.originalList[0], onvalue = "1", offvalue = "", padx = 20, pady = 20, activebackground = "#00FFFF", relief = "groove", bg = "#00DFFF")]
        self.selectAllButton = tk.Button(self.frame, command = self.SelectAll, text = "全选", font=('微软雅黑',10), fg="white", bg = "#00FFFF", relief = "groove")
        self.selectAllButton.grid(row = 1, column = 1)
        self.selectAllButton.bind("<MouseWheel>", self.OnMouseWheel)
        self.reverseSelectionButton = tk.Button(self.frame, command = self.ReverseSelection, text = "反选", font=('微软雅黑',10), fg="white", bg = "#00FFFF", relief = "groove")
        self.reverseSelectionButton.grid(row = 1, column = 2)
        self.reverseSelectionButton.bind("<MouseWheel>", self.OnMouseWheel)
        self.checkbuttonList[0].grid(row = 2, column = 1)
        self.checkbuttonList[0].bind("<MouseWheel>", self.OnMouseWheel)
        count = 1
        for index in self.frameDict:
            for buttonCount in range(len(self.frameDict[index]["buttons"])):
                if len(self.originalList)-1 < count:
                    self.originalList.append(tk.StringVar())
                    self.chosenList.append(None)
                self.checkbuttonList.append(tk.Checkbutton(self.frameDict[index]["own"], variable = self.originalList[count], onvalue = index + "#" + str(buttonCount), offvalue = "", padx = 20, pady = 20, activebackground = "#00FFFF", relief = "groove", bg = "#00DFFF"))
                self.checkbuttonList[-1].grid(row = count, column = 1 ,sticky = "W")
                self.checkbuttonList[-1].bind("<MouseWheel>", self.OnMouseWheel)
                count += 1
        self.chosenString = tk.StringVar()
        self.copyedString = tk.StringVar()
        self.multipleChoiceModeLabel1 = tk.Label(self.multipleChoiceMode_frame, justify = "left", textvariable = self.chosenString, fg = "black", bg = "white", font = ('宋体',15))
        self.multipleChoiceModeLabel1.grid(row = 0,column = 0, sticky = "N")
        self.Refresh_chosenString()
        self.multipleChoiceModeLabel2 = tk.Label(self.multipleChoiceMode_frame, justify = "left", textvariable = self.copyedString, fg = "black", bg = "white", font = ('宋体',15))
        self.multipleChoiceModeLabel2.grid(row = 0,column = 1, sticky = "N")

    def SelectAll(self):
        for checkbutton in self.checkbuttonList:
            checkbutton.select()

    def ReverseSelection(self):
        for checkbutton in self.checkbuttonList:
            checkbutton.toggle()
    
    def Refresh_chosenString(self):#每过0.5秒就刷新当前选中项提示
        if not self.bMultipleChoiceMode:return
        for i in range(len(self.originalList)):#根据原始数据导出结果
            if self.originalList[i].get() == "1":
                self.chosenList[i] = ["根存档", "Meta_SaveFile#sys.json"]
            elif self.originalList[i].get() == "":
                self.chosenList[i] = None
            else:
                tL = self.originalList[i].get().split("#")
                self.chosenList[i] = self.frameDict[tL[0]]["buttons"][int(tL[1])]["info"]
        string = "当前选中项为:"
        for i in self.chosenList:
            if i == None:
                continue
            string += "\n" + i[0]
        self.chosenString.set(string)
        root.rootWindow.after(500, self.Refresh_chosenString)
    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓刷新
    def IndefinitePartRefresh(self):
        try:
            a = self.frameDict["CoopSlot"]
            for i in self.frameDict:
                self.frameDict[i]["own"].destroy()
        except Exception as e:pass
        #不定项部分
        if WorkingMode == 2:
            self.frameDict = {
                            "CoopSlot":{
                                        "info":["主线", ""],
                                        "own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),
                                        "buttons":[],#{"info":[text,file], "own":tk.Botton()}
                                        }, 
                            "DLC2":{
                                        "info":["海滩"," Surf 'n' Turf"],
                                        "own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),
                                        "buttons":[],#{"info":[text,file], "own":tk.Botton()}
                                    }, 
                            "DLC3":{
                                        "info":["节庆更新", ""],
                                        "own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),
                                        "buttons":[],#{"info":[text,file], "own":tk.Botton()}
                                    }, 
                            "DLC5":{
                                        "info":["野营", " Campfire Cook Off"],
                                        "own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),
                                        "buttons":[],#{"info":[text,file], "own":tk.Botton()}
                                    }, 
                            "DLC7":{
                                        "info":["黑暗城堡", " Night of the Hangry Horde"],
                                        "own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),
                                        "buttons":[],#{"info":[text,file], "own":tk.Botton()}
                                    }, 
                            "DLC8":{
                                        "info":["马戏团", " Carnival of Chaos"],
                                        "own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),
                                        "buttons":[],#{"info":[text,file], "own":tk.Botton()}
                                    }, 
                            }
        elif WorkingMode == 3:
            tempL = ["OC1#1代主线#", "CoopSlot#2代主线#", "DLC202#凯文生日#", "BAG#冒险故事#the ever peckish rises", "DLC102#1代冰雪节日#festive seasoning", "DLC101#1代古老遗迹#the lost morsel", "DLC13#2代中秋节#", "DLC11#2代盛大游行(狂欢一夏)#sun's out buns out", "DLC10#2代春节#", "DLC9#2代冬季(僵尸面包)#winter wonderland", "DLC8#2代马戏团#carnival of chaos", "DLC7#2代黑暗城堡#night of the hangry horde", "DLC5#2代野营#campfire cook off", "DLC4#2代农历新年#", "DLC3#2代冰雪(巧克力奶)#kevin's christmas cracker", "DLC2#2代海滩#surf'n'turf", "DLC203#世界美食节#"]
            self.frameDict = {}
            for i in tempL:
                tL = i.split("#")
                self.frameDict[tL[0]] = {"info":[tL[1], tL[2]],"own":tk.Frame(self.frame, relief="flat", bg = "#00DFFF"),"buttons":[]} 
        row = 3
        for i in self.frameDict:
            self.frameDict[i]["own"].grid(row = row, column = 0, columnspan = 3, sticky = "W")
            self.frameDict[i]["own"].bind("<MouseWheel>", self.OnMouseWheel)
            row += 1
            temp = tk.Label(self.frameDict[i]["own"], height=3, justify="left", fg="black", bg = "#00DFFF", font=('微软雅黑',10), text = 43*"_" + "\n" + self.frameDict[i]["info"][0] + self.frameDict[i]["info"][1])
            temp.grid(row = 0, column = 0, sticky = "W")
            temp.bind("<MouseWheel>", self.OnMouseWheel)

    def ResetButtons(self):
        for index in self.frameDict:
            for button in self.frameDict[index]["buttons"]:
                if button["warning"]:
                    button["own"]["bg"] = "#D5D500"
                else:
                    button["own"]["bg"] = "#00DFFF"

    def Refresh_toolsFrame(self):
        self.adjustOrderButton.config(state = "normal", bg = "lightgreen")
        self.addRemarksButton.config(state = "normal", bg = "lightgreen")
        self.addSaveButton.config(state = "normal", bg = "lightgreen")
        self.pasteButton.config(state = "normal", bg = "lightgreen")
        self.copyButton.config(state = "normal", bg = "lightgreen")
        self.deleteButton.config(state = "normal", bg = "lightgreen")
        self.coverButton.config(state = "normal", bg = "lightgreen")
        self.multipleChoiceModeButton.config(state = "normal", bg = "lightgreen")
        self.adjustOrderButton.config(state = "disabled", bg = "#EEEEEE")#！！！
        self.addRemarksButton.config(state = "disabled", bg = "#EEEEEE")#！！！
        if self.bAdministrateBackup or not self.bChosedSomething:
            self.copyButton.config(bg = "#EEEEEE", state = "disabled")
            self.deleteButton.config(bg = "#EEEEEE", state = "disabled")
            self.coverButton.config(bg = "#EEEEEE", state = "disabled")
        if self.bMultipleChoiceMode:
            self.adjustOrderButton.config(bg = "#EEEEEE", state = "disabled")
            self.addRemarksButton.config(bg = "#EEEEEE", state = "disabled")
            self.addSaveButton.config(bg = "#EEEEEE", state = "disabled")
            self.pasteButton.config(bg = "#EEEEEE", state = "disabled")

    def SetButtons(self):#按钮放置
        row = 1
        for index in self.frameDict:
            for button in self.frameDict[index]["buttons"]:
                button["own"].grid(row = row, column = 0, sticky = "E")
                button["own"].bind("<MouseWheel>", self.OnMouseWheel)
                row += 1
            if self.frameDict[index]["buttons"] == []:
                self.frameDict[index]["own"].grid_forget()
                self.canvasCount1 += 1
        self.row = row
        self.now = []
    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓界面管理
    def InterfaceManagement(self, to, *others):#工具界面管理
        if to == "adjustOrder"and self.bAdjustOrder == False:
            self.Hide()
            self.bAdjustOrder = True
            self.adjustOrder_frame.grid(row=0,column=0,sticky = "N")
        if to == "addRemarks" and self.bAddRemarks == False:
            self.Hide()
            self.bAddRemarks = True
            self.addRemarks_frame.grid(row=0,column=1,sticky = "N")
        if to == "addSave"and self.bAddSave == False:
            self.Hide()
            self.bAddSave = True
            self.OnAddSave()
            self.addSave_frame.grid(row=0,column=2,sticky = "N")
        if to == "multipleChoiceMode":
            if self.bMultipleChoiceMode == True:
                self.Hide()
            elif self.bMultipleChoiceMode == False:
                self.Hide()
                self.bMultipleChoiceMode = True
                self.multipleChoiceMode_frame.grid(row=0,column=3,sticky = "N")
                self.bChosedSomething = True
                self.OnMultipleChoiceMode()
        self.now = []
        self.ResetButtons()
        self.Refresh_toolsFrame()

    def InterfaceManagementClosure(self, to, *others):
        def aaa():
            self.InterfaceManagement(to, *others)
        return aaa

    def Switch(self, inputItem):#存档编辑和备份界面管理
        if self.bMultipleChoiceMode:#多选模式按钮无反应
            return
        elif inputItem == self.currentSavePath:
            if self.bAdministrateBackup == False:
                self.Hide()
                self.now = []
                self.backupsButton.config(bg = "#00FFFF")
                main_secondary_administrateBackup.Show(inputItem)
                self.bAdministrateBackup = True
                self.ResetButtons()
        elif inputItem == "Meta_SaveFile#sys.json":
            if self.now != "Meta_SaveFile#sys.json":
                self.Hide()
                self.now = "Meta_SaveFile#sys.json"
                self.mataSaveFileButton.config(bg = "#00FFFF")
                self.bModify = True
                main_secondary_modify.Show(inputItem)
                self.ResetButtons()
        else:
            nowButtonDict = self.frameDict[inputItem[0]]["buttons"][inputItem[1]]
            file = nowButtonDict["info"][1]
            if self.now != file:
                self.Hide()
                self.now = file
                self.ResetButtons()
                if nowButtonDict["warning"]:
                    nowButtonDict["own"]["bg"] = "#00D580"
                else:
                    nowButtonDict["own"]["bg"] = "#00FFFF"
                main_secondary_modify.Show(file)
                self.bModify = True
        self.bChosedSomething = True
        self.Refresh_toolsFrame()

    def SwitchClosure(self, inputItem):
        def aaa():
            self.Switch(inputItem)
        return aaa

    def Hide(self):
        if self.bModify:
            self.bModify = False
            if self.now == "Meta_SaveFile#sys.json":
                self.mataSaveFileButton.config(bg = "#00DFFF")
            main_secondary_modify.frame.grid_forget()
        if self.bAdministrateBackup:
            self.bAdministrateBackup = False
            self.backupsButton.config(bg = "#00DFFF")
            main_secondary_administrateBackup.frame.grid_forget()
        if self.bAdjustOrder:
            self.bAdjustOrder = False
            self.adjustOrder_frame.grid_forget()
        if self.bAddRemarks:
            self.bAddRemarks = False
            self.addRemarks_frame.grid_forget()
        if self.bAddSave:
            self.bAddSave = False
            self.addSave_frame.grid_forget()
        if self.bMultipleChoiceMode:
            self.bMultipleChoiceMode = False
            self.canvas["width"] = 270
            self.multipleChoiceModeButton["text"] = "多选"
            for i in self.checkbuttonList:
                i.destroy()
            self.multipleChoiceModeLabel1.destroy()
            self.multipleChoiceModeLabel2.destroy()
            self.selectAllButton.destroy()
            self.reverseSelectionButton.destroy()
            self.multipleChoiceMode_frame.grid_forget()
            self.chosenList = [None]
    #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓首次刷新处理(后面也会调用)
    def LoadSysSaveTimeData(self, currentPath):
        file = currentPath + "\\" + "sysSaveTimeData.data"
        if not os.path.exists(file):
            self.sysSaveTimeData = {}
            with open(file, "w") as f:
                f.write(json.dumps(self.sysSaveTimeData))
        else:
            with open(file,"r") as f:
                self.sysSaveTimeData = json.load(f)
        return file
        
    def SaveSysSaveTimeData(self, file):
        with open(file,"w") as f:
            f.write(json.dumps(self.sysSaveTimeData))

    def DecodeSaveFolder(self):
        for i in main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList]:#这里的indexOfSaveFolderList是main_chooseSaveFolder.SaveFolderList的索引,指示应该解析哪个存档
            if str(type(i)) == "<class 'list'>":
                decodeStrings = i[4]
                pathNumber = root.backups.setdefault(i[0], len(root.backups)+1)#这里是: 如果存在main…,就将值赋给pathNumber, 如果不存在,就将main…设为键,default的那一堆设为值存储并赋给pathNumber
                currentPath = SaveBackupsPath + "\\" + str(pathNumber)#随便说一嘴,这里是存档备份路径 + 反斜杠 + 上面的数字, 下面会用到currentPath
                if not os.path.exists(currentPath):
                    os.makedirs(currentPath)
                dataFile = self.LoadSysSaveTimeData(currentPath)
                continue
            outputFile = currentPath + "\\" + os.path.splitext(os.path.basename(i))[0] + "#root.json"
            sysFile = outputFile[:-9] + "sys.json"
            #下面的try是为了在版本更新时防止问题
            try:
                a = self.sysSaveTimeData[i]
            except:
                self.sysSaveTimeData[i] = os.path.getmtime(i)
            if not os.path.exists(outputFile):
                #这里是解码的代码: 工具 解码 须解码文件 输出路径 解密密钥
                temp = subprocess.Popen([os.getcwd() + "\\OvercookedTool.exe", "decrypt", i, outputFile, decodeStrings], stdout = subprocess.PIPE)
                temp.wait()
                if temp.stdout.read() == b'Decryption failed\r\nWrong key?\r\n':
                	return False#@特殊情况：当没有正确密钥导致无法解码时，返回False
                FileCopy(outputFile, sysFile)
                self.sysSaveTimeData[i] = os.path.getmtime(i)
            elif self.sysSaveTimeData[i] != os.path.getmtime(i):
                temp = subprocess.Popen([os.getcwd() + "\\OvercookedTool.exe", "decrypt", i, outputFile, decodeStrings], stdout = subprocess.PIPE)
                temp.wait()
                if temp.stdout.read() == b'Decryption failed\r\nWrong key?\r\n':
                	return False#@特殊情况：当没有正确密钥导致无法解码时，返回False
                self.sysSaveTimeData[i] = os.path.getmtime(i)
        self.SaveSysSaveTimeData(dataFile)
        return currentPath
    
    def CompareFunction_BaseOnSaveNumber(self, inputStr):
        tL = inputStr.split("_")
        if tL[0] == "CoopSlot":
            return int(tL[2].split("#")[0])
        else:
            return int(tL[3].split("#")[0])

    def AnalyseSaveName(self, path):#获取给用户看的信息
        nameList = os.listdir(path)
        tL = []
        for i in range(len(nameList)):#保留所有sys
            if nameList[i][-8:-5]!="sys":
                tL.append(i)
        for i in range(len(tL)):
            nameList.pop(tL[i] - i)
        if 'Meta_SaveFile#sys.json' in nameList:
            nameList.remove('Meta_SaveFile#sys.json')
        if 'Meta_SaveFile#root.json' in nameList:
            nameList.remove('Meta_SaveFile#root.json')
        print("[line 1282] nameList:", nameList)
        nameList = sorted(nameList, key = self.CompareFunction_BaseOnSaveNumber)
        for i in nameList:
            tL = i.split("_")
            if tL[0] == "CoopSlot":
                saveNumber = str(int(tL[2].split("#")[0])+1)
            else:
                saveNumber = str(int(tL[3].split("#")[0])+1)
            text = "[" + self.frameDict[tL[0]]["info"][0] + "]档位" + saveNumber
            nowButtonsList = self.frameDict[tL[0]]["buttons"]
            gameSave = main_chooseSaveFolder.saveFolderList[self.indexOfSaveFolderList][0][0] + "\\" + os.path.basename(i.split("#")[0]) + ".save"
            if os.path.exists(gameSave):
                nowButtonsList.append({"info":[text, i], "warning":False, "own":tk.Button(self.frameDict[tL[0]]["own"], command=self.SwitchClosure([tL[0], len(nowButtonsList)]), text=text, bg = "#00DFFF", state = "normal", width=22, height = 3, font=('微软雅黑',15), fg = "white", justify = "left", relief = "flat", activebackground = "#00FFFF", activeforeground = "white")})
            else:
                nowButtonsList.append({"info":[text, i], "warning":True, "own":tk.Button(self.frameDict[tL[0]]["own"], command=self.SwitchClosure([tL[0], len(nowButtonsList)]), text=text, bg = "#D5D500", activebackground = "#00D580", state = "normal", width=22, height = 3, font=('微软雅黑',15), fg = "white", justify = "left", relief = "flat", activeforeground = "white")})

    def Show(self, indexOfSaveFolderList, titleStrings):#因为每次Show都可能是新的存档包,所以要初始化
        self.indexOfSaveFolderList = indexOfSaveFolderList
        self.titleStrings = titleStrings
        self.now = []
        self.currentScrollbarPosition = 0
        self.IndefinitePartRefresh()
        #标题处理↓
        tempList = self.titleStrings.split("\n", 1)
        tempList_0 = tempList[0].split("…", 1)
        tempList_0[1] = tempList_0[1][-22:]
        tempList[0] = "…".join(tempList_0)
        self.title["text"] = "\n".join(tempList)
        self.toolsFrame.grid(row=0, column=0, columnspan = 2, sticky = "N")
        self.canvas.grid(row = 1, column = 1, sticky = "N")
        self.scrollbarOfFrame.grid(row = 1, column = 0, ipady = 450, sticky = "N")
        self.currentSavePath = self.DecodeSaveFolder()#存档的读取、备份和计算
        if self.currentSavePath == False:
        	return False#@特殊情况：当没有正确密钥导致无法解码时，返回False。Ctrl + F @ 可以找到下一级
        #按钮命令更新
        self.backupsButton["command"] = self.SwitchClosure(self.currentSavePath)
        root.Save()
        self.secondary_rootFrame.grid(row = 0,column = 5, sticky = "N")
        self.LocalRefresh()
        return True#@特殊情况：见上方@

    def LocalRefresh(self):
        self.AnalyseSaveName(self.currentSavePath)
        self.canvasCount1 = 0
        self.SetButtons()
        #滚动条相关↓
        self.canvas.create_window((0,0),window=self.frame,anchor="nw", height = (272*self.row + 264*(6-self.canvasCount1) + 958)*1)#我也不知道为什么要乘以0.4,前面的数据都是计算出来的实际大小,但是显示出来就过长了,试出来0.36这个数字很合适,但是在只有根存档时又太短,只好用0.4了
        self.canvas.configure(yscrollcommand = self.scrollbarOfFrame.set, scrollregion=self.canvas.bbox("all"))
        self.canvas.bind("<MouseWheel>", self.OnMouseWheel)
        self.scrollbarOfFrame.config(command = self.canvas.yview)
        self.canvasCount1 = 0
        self.bChosedSomething = False
        self.Refresh_toolsFrame()
        self.rootFrame.grid(row = 0, column = 1, sticky = "N")
#---------------------------------------------------
class Main_secondary_modify():
    def __init__(self):
        self.frame = tk.Frame(main_chooseSaveFiles.secondary_frame, relief="flat", bg = "white")
        self.COMING = tk.Label(self.frame,width=50,height=3,justify="left",text="这里是存档修改，随缘制作~",fg="black",bg = "white",font=('微软雅黑',30))
        self.COMING.grid(row = 0,column = 0)

    def Show(self, activeFile):
        self.activeFile = activeFile
        self.frame.grid(row=0,column=5,sticky = "N")
#---------------------------------------------------
class Main_secondary_administrateBackup():
    def __init__(self):
        self.frame = tk.Frame(main_chooseSaveFiles.secondary_frame, relief="flat", bg = "white")
        self.COMING = tk.Label(self.frame,width=50,height=3,justify="left",text="这里是备份查看,资源管理器凑合一下~",fg="black",bg = "white",font=('微软雅黑',30))
        self.COMING.grid(row = 0,column = 0)

    def Show(self, activeSaveBackupFolder):        
        self.activeSaveBackupFolder = activeSaveBackupFolder
        self.frame.grid(row=0,column=5,sticky = "N")
        subprocess.call([os.getenv("windir", default = None) + "\\explorer.exe", self.activeSaveBackupFolder])
#===================================================
def SwitchingInterface(to, *others):
    if interfaceManagement.bChoosePath:
        if others == (1,) and settings_choosePath.currentSaveFolder not in NowSavePathList:#if的and的前一个判断是判定用户点击“确定”，and的后一个判断是防止出现重复路径
            NowSavePathList.append(settings_choosePath.currentSaveFolder)
        Refresh_Path()
        settings_choosePath.frame.grid_forget()
        interfaceManagement.bChoosePath = False
    if interfaceManagement.bChooseSaveFolder:
        interfaceManagement.bChooseSaveFolder = False
        main_chooseSaveFolder.frame.grid_forget()
    if interfaceManagement.bChooseSaveFiles:
        interfaceManagement.bChooseSaveFiles = False
        main_chooseSaveFiles.Hide()
        main_chooseSaveFiles.rootFrame.grid_forget()
    if interfaceManagement.bSettings:
        interfaceManagement.bSettings = False
        settings.frame.grid_forget()
    if interfaceManagement.bAbout:
        interfaceManagement.bAbout = False
        about.frame.grid_forget()
    if to == "choosePath":
        interfaceManagement.bChoosePath = True
        settings_choosePath.Show()        
    if to == "chooseSaveFolder":
        interfaceManagement.bChooseSaveFolder = True
        main_chooseSaveFolder.Show()
    if to == "chooseSaveFiles":
        root.progressbar.place(relx = 0.5, rely = 0.5, anchor = "center")
        root.progressbar.start(interval = 50)
        root.rootWindow.update()
        interfaceManagement.bChooseSaveFiles = True
        tempOutput = main_chooseSaveFiles.Show(others[0], others[1])
        if tempOutput == False:
        	SwitchingInterface("chooseSaveFolder")
        	tk.messagebox.showerror(title="存档处理错误", message="无法找到正确的解密秘钥\n如果是非官方存档文件，请正确命名存档文件夹")
        root.progressbar.stop()
        root.progressbar.place_forget()
    if to == "settings":
        interfaceManagement.bSettings = True
        settings.Show()
    if to == "about":
        interfaceManagement.bAbout = True
        about.Show()
    interfaceManagement.Refresh()
    root.Save()

def SwitchingInterfaceClosure(to, *input):
    def aaa():
        SwitchingInterface(to, *input)
    return aaa

def Refresh_Path():#在设置中添加或者删除路径时刷新
    settings.pathListBox.delete(0,"end")
    for i in NowSavePathList:
        settings.pathListBox.insert("end", i)
    global main_chooseSaveFolder
    main_chooseSaveFolder = Main_chooseSaveFolder()

def TransferBase_str(inputStr = "", inputBase = 10, outputBase = 16):
    if inputStr == "" or inputStr == "0":return "0"#遇见0或空，直接返回0
    numberList = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"#顺便初始化
    if inputStr[0] == "-":
        inputStr = inputStr[1:]
        b = True
    else:
        b = False
    number = 0#这是输入字符串转换成整型的临时存储
    for i in range(len(inputStr)):
        number += numberList.index(inputStr[-(i+1)]) * inputBase**i#对输入倒序取值,再找到在numberList中对应的下标,表示这个位对应的数,再乘以这个位对应表示的大小,得到这一位实际的数
    number = int(number)#防止出问题
    #字符串转整型结束,开始整型转字符串
    outputStr = ""
    while number > 0:#除基倒取余法
        temp = number
        number //= outputBase
        outputStr += numberList[temp - (number * outputBase)]
    outputStr = outputStr[::-1]
    if b:
        return "-" + outputStr
    else:
        return outputStr

def SwitchWorkingMode():
    global NowSavePathList
    global main_chooseSaveFolder
    global settings
    global settings_choosePath
    if WorkingMode == 2:
        NowSavePathList = root.savePathList2
    elif WorkingMode == 3:
        NowSavePathList = root.savePathList3
    a = b = c = False
    try:
        main_chooseSaveFolder
        a = True
    except Exception:
        pass
    try:
        settings
        b = True
    except Exception:
        pass
    try:
        settings_choosePath
        c = True
    except Exception:
        pass
    if a:
        main_chooseSaveFolder.frame.destroy()
    if b:
        settings.frame.destroy()
    if c:
        settings_choosePath.frame.destroy()
    main_chooseSaveFolder = Main_chooseSaveFolder()
    settings_choosePath = Settings_choosePath()
    settings = Settings()
    d = False
    try:
        interfaceManagement
        d = True
    except Exception:pass
    if d:
        SwitchingInterface("settings")
#===================================================
SwitchWorkingMode()
interfaceManagement = InterfaceManagement()
main_chooseSaveFiles = Main_chooseSaveFiles()
main_secondary_administrateBackup = Main_secondary_administrateBackup()
main_secondary_modify = Main_secondary_modify()
about = About()
#===================================================
root.progressbar.place_forget()
root.progressbar.stop()
if NowSavePathList == []:
    SwitchingInterface("choosePath")
else:
    SwitchingInterface("chooseSaveFolder")
interfaceManagement.Show()
root.rootWindow.mainloop()
#OP Wingdings 2
#ENGLISH Bauhaus 93
#color:#FFFFFF/white >>> #C8FFFF >>> #80FFFF >>> #00FFFF >>> #00DFFF >>> #00BFFF/deepskyblue >>> #009FFF
'''modify准备
def DecodeJsonSaveFile(file):#输入文件路径,输出获取的数据
    with open(file,"r") as f:
        temp = f.read()
    count = 0
    while temp[-1]==chr(0):#这里有一个过于离谱的发现：存档解密后文件最后的空格数量不定，结果read后发现结尾的空格全部无法显示，研究半天发现它们都等于chr(0)???
        temp = temp[0:-1]
        count += 1
    rootDictionary = json.loads(temp)
    dataList = [json.loads(rootDictionary['m_Entries'][-2]['m_JSON'])["m_Value"]]
    for i in rootDictionary['m_Entries']:
        if i==0 or i==1:
            continue
        term = json.loads(i['m_JSON'])
        tempDictionary = {}
        for i in range(len(term['m_Value'])):
            tempDictionary[term['m_Key'][i]] = term['m_Value'][i]
        dataList.append(tempDictionary)
    #数据结构：
    #[是否解锁新游戏＋,[第一关的数据],[第二关的数据],…]
    return json.loads(temp)
'''
'''
window.geometry()   设定主窗口的大小以及位置，当参数值为 None 时表示获取窗口的大小和位置信息。
window.quit()   关闭当前窗口
window.update() 刷新当前窗口
window.iconbitmap() 设置窗口左上角的图标（图标是.ico文件类型）
window.config(background ="grey")
window.minsize(50,50)   设置窗口被允许调整的最小范围，即宽和高各50
window.maxsize(400,400) 设置窗口被允许调整的最大范围，即宽和高各400
window.attributes("-alpha",0.5) 用来设置窗口的一些属性，比如透明度（-alpha）、是否置顶（-topmost）即将主屏置于其他图标之上、是否全屏（-fullscreen）全屏显示等
window.state("normal")  用来设置窗口的显示状态，参数值 normal（正常显示），icon（最小化），zoomed（最大化），
window.withdraw()   用来隐藏主窗口，但不会销毁窗口。
window.iconify()    设置窗口最小化
window.deiconify()  将窗口从隐藏状态还原
window.winfo_screenwidth()
window.winfo_screenheight() 获取电脑屏幕的分辨率（尺寸）
window.winfo_width()
window.winfo_height()   获取窗口的大小，同样也适用于其他控件，但是使用前需要使用 window.update() 刷新屏幕，否则返回值为1
window.protocol("协议名",回调函数) 启用协议处理机制，常用协议有 WN_DELETE_WINDOW，当用户点击关闭窗口时，窗口不会关闭，而是触发回调函数。
root_window["bg"] = "white"



log:
v0.1 发布

v0.2 修复了无法开启的问题

v0.3 修复了进入存档包会一直加载的问题（即找不到密钥时不报错）
     修复了steam存档和epic存档识别不清的问题

v0.3.1 修复了无法复制根存档的问题
       修复了密钥正确时也会报错的问题

v0.3.2 修复了世界美食节更新导致的全都好吃模式无法查看存档的问题
'''
