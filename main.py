try:
    import git
except:
    tmp = "Please make sure you have completed the setting of git(name and Email)"
import os
import subprocess
import shutil
from tkinter import *
import tkinter as tk
from tkinter import simpledialog as sd
from functools import partial
import re
from tkinter import filedialog
from tkinter import simpledialog as sd
import json
from PIL import ImageTk,Image
import PIL
import tkinter.font as tkFont


def gitCheck():
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    cmd = "git config user.email"
    try:
        r = os.popen(cmd)
        text = r.read()
        r.close()
    except :
        return False
    if email_pattern.match(text.strip()):
        return True
    return False
  
def download(text, dic):
    if not gitCheck():
        text.set('Please make sure you have completed the setting of git(name and Email )')
        return
    if os.path.isdir("./TerrariaMapGit"):
        repo = git.Repo('./TerrariaMapGit')
        g = repo.git
        g.pull()
    else:
        repo = git.Repo.clone_from(url="https://github.com/x55662306/TerrariaMapGit", to_path="./TerrariaMapGit")

    if not os.path.isdir('worlds'):
        os.makedirs('worlds')

    shutil.copy('.\\TerrariaMapGit\\' + dic['world_name'] + '.wld', '.\\worlds\\' + dic['world_name'] + '.wld')
    shutil.copy('.\\TerrariaMapGit\\' + dic['world_name'] + '.wld.bak', '.\\worlds\\' + dic['world_name'] + '.wld.bak')

    text.set('Download Complete!!')
    
    return repo

def upload(text, dic):

    if not gitCheck():
        text.set('Please make sure you have completed the setting of git(name and Email )')
        return
    if not os.path.isdir("./TerrariaMapGit"):
        os.makedirs("worlds")
    shutil.copy('.\\worlds\\' + dic['world_name'] + '.wld', '.\\TerrariaMapGit\\' + dic['world_name'] + '.wld')
    shutil.copy('.\\worlds\\' + dic['world_name'] + '.wld.bak', '.\\TerrariaMapGit\\' + dic['world_name'] + '.wld.bak')
    repo = git.Repo('./TerrariaMapGit')
    g = repo.git
    g.add("--all")
    try:
        g.commit("-m auto update")
    except:
        pass
    g.push()
              
    text.set('Upload Complete!!')

def startGame(dic):
    filepath = dic['terraria_path']
    p = subprocess.Popen('cmd /c start ' + filepath)

def selectExe(exePath, dic):
    exePath.set(filedialog.askdirectory(initialdir = "/",title = "Select file"))
    files  = os.listdir(exePath.get())
    for f in files:
        if f == 'Terraria.exe' or f == 'Terraria.url':
            exePath.set(exePath.get() + '\\' + f)
            break
    with open("x87654321_config.json", "w") as f: 
        dic['terraria_path'] = exePath.get().replace('/', '\\')
        json.dump(dic, f)

def askWorldName(worldName, dic):
    name = sd.askstring("世界的名字", "輸入你的世界名稱")
    if name is not None:
        worldName.set(name)

        
    with open("x87654321_config.json", "w") as f: 
        dic['world_name'] = worldName.get()
        json.dump(dic, f)

def change_auto_download(downloadVar, dic):
    with open("x87654321_config.json", "w") as f: 
        dic['auto_download'] = downloadVar.get()
        json.dump(dic, f)
        

def change_auto_start(startVar, dic):
    with open("x87654321_config.json", "w") as f: 
        dic['auto_start'] = startVar.get()
        json.dump(dic, f)
    
def main():
    
    dic = {}
    try:
        with open("x87654321_config.json", 'r', encoding='utf-8') as f:
            dic = json.load(f)
    except:
        with open("x87654321_config.json", "w", encoding='utf-8') as f: #a+ Opens a file for both appending and reading
            dic = {'terraria_path': 'C:\\Users\\User\Desktop\\Terraria\\Terraria.exe', 'world_name': 'test', 'auto_download': 0, 'auto_start': 0}
            json.dump(dic, f)
    
    
        
    # 建立主視窗和 Frame（把元件變成群組的容器）
    window = tk.Tk()
    window.title("bToro")
    window.configure(bg='lightgray')
    window.geometry("500x500")
    
    fontStyle_label = tkFont.Font(family="Lucida Grande", size=10,weight=tkFont.BOLD)
    fontStyle_button = tkFont.Font(family="Fixdsys", size=13)
    
    top_frame = tk.Frame(window)
    top_frame.configure(bg='lightgray')
    
    # 將元件分為 top/bottom 兩群並加入主視窗
    top_frame.pack()
    top_frame.configure(bg='lightgray')
    bottom_frame = tk.Frame(window,bg='lightgray')
    bottom_frame.pack(side=tk.BOTTOM)

    im=PIL.Image.open("terraria_img.png")
    im = im.resize((250,250),Image.ANTIALIAS)
    img=ImageTk.PhotoImage(im)
    panel=tk.Label(window,image=img,bg='lightgray').pack()

    text = tk.StringVar()
    text.set("Get started")
    try:
        text.set(tmp)
    except:
        pass
    statusLabel = tk.Label(top_frame, textvariable=text,font = fontStyle_label)
    statusLabel.configure(bg='lightgray')
    statusLabel.pack()

    exePath = tk.StringVar()
    worldName = tk.StringVar()
    worldName.set('test')
    nameButton = tk.Button(top_frame,activebackground = 'gray', text='更改世界名稱',font = fontStyle_button, fg='black', command=partial(askWorldName, worldName, dic))    
    nameButton.pack()

    
    fileButton = tk.Button(top_frame,activebackground = 'gray', text='更改Terraria.exe路徑',font = fontStyle_button, fg='black', command=partial(selectExe, exePath, dic))
    fileButton.pack()
    

    
    # 以下為 bottom 群組
    
    bottom_button = tk.Button(bottom_frame,activebackground = 'gray',text='Upload', fg='black',font = fontStyle_button, command=partial(upload, text, dic))
    bottom_button2 = tk.Button(bottom_frame,activebackground = 'gray', text='Download', fg='black',font = fontStyle_button, command=partial(download, text, dic))

    


    bottom_button3 = tk.Button(bottom_frame,activebackground = 'gray', text='Start Game', font = fontStyle_button,fg='black', command=partial(startGame, dic))
    bottom_button3.pack(side=tk.TOP)   
    bottom_button.pack(side=tk.LEFT)
    bottom_button2.pack(side=tk.RIGHT)
    
    if dic['auto_download'] == 1:
        download(text, dic)
    if dic['auto_start'] == 1:
        startGame(dic)
    
    startVar = tk.IntVar()
    startVar.set(dic['auto_start'])
    downloadVar = tk.IntVar()
    downloadVar.set(dic['auto_download'])
    check_auto_download = tk.Checkbutton(window,bg='lightgray', text='auto download', variable=downloadVar, onvalue=1, offvalue=0,font = fontStyle_label,
                    command=partial(change_auto_download, downloadVar, dic))
                                         
    check_auto_download.pack()
    
    check_auto_start = tk.Checkbutton(window, bg='lightgray',text='auto start game', variable=startVar, onvalue=1, offvalue=0,font = fontStyle_label,
                    command=partial(change_auto_start, startVar, dic))
    check_auto_start.pack()

    # 運行主程式
    window.mainloop()

if __name__ == '__main__':
    main()





