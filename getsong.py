import urllib.request
import tkinter
from tkinter import *
import re
import time
import conf as cf
import json as js
import sys
import os
from tkinter.filedialog import *
from tkinter.messagebox import *
import threading

class myThread (threading.Thread):
    def __init__(self, threadID, name,functions):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.functions=functions
    def run(self):
        self.functions()
# 链接代理
def	build_proxy():
	proxy = cf.PROXY
	proxy_support = urllib.request.ProxyHandler(proxy)
	opener = urllib.request.build_opener(proxy_support)
	urllib.request.install_opener(opener)

def get_userid(id):

    try:
        req=urllib.request.Request(cf.MAIN_URL+'/u/'+str(id))
        html = urllib.request.urlopen(req)
        html_content =html.read().decode('utf8')
        reg_content=get_object_element(cf.ADD_REG_EXP5,html_content)
        if len(reg_content)!=0:
            userid=reg_content[0].split("'")[1]
            return userid
    except urllib.error.HTTPError as err:
        print(err.msg)

def get_work_list(site_part1,site_part2,site_part3,pagenum,userid):
    website=site_part1+pagenum+site_part2+userid+site_part3
    try:
        req=urllib.request.Request(website)
        html = urllib.request.urlopen(req)
        html_content =html.read().decode('utf8')
        return html_content
    except urllib.error.HTTPError as err:
        print(err.msg)

def download_url(website):
    req = urllib.request.Request(website,headers=cf.FAKE_HEADER)
    #req.add_header=('Referer','http://www.changba.com/u/'+cf.UserID)
    #req.add_header=('User-Agent',cf.Mobile_User_Agent)
    try:
        html = urllib.request.urlopen(req)
        html_content = html.read().decode('utf8')
        return html_content
    except urllib.error.HTTPError as err:
        print(err.msg)

def get_object_element(reg,content):
	object_element_list=re.findall(reg,content)
	return object_element_list

def download_work(url_dict):
    print('下载文件存放在：%s 中......' % cf.PATH)
    v3.set('下载文件存放在：%s 中......' % cf.PATH)
    if os.path.exists(cf.PATH):
        for key in url_dict:
            url=url_dict[key]
            content=download_url(url)
            #time.sleep(0.3)
            if len(get_object_element(cf.ADD_REG_EXP4,content))!= 0:
                    content_part=get_object_element(cf.ADD_REG_EXP4,content)[0]
            try:
                    cf.DOWNLOADING_SONG_NAME=str(key)
                    urllib.request.urlretrieve(content_part,cf.PATH + '/'+file_name_check(str(key)) + ".mp3",callbackfunc)
            except urllib.error.HTTPError as reason:
                    print(reason)
    else:
        os.mkdir(cf.PATH)
        for key in url_dict:
            url=url_dict[key]
            content=download_url(url)
            #time.sleep(0.3)
            if len(get_object_element(cf.ADD_REG_EXP4,content))!= 0:
                    content_part=get_object_element(cf.ADD_REG_EXP4,content)[0]
            try:
                    cf.DOWNLOADING_SONG_NAME=str(key)
                    urllib.request.urlretrieve(content_part,cf.PATH +'/'+ file_name_check(str(key)) + ".mp3",callbackfunc)
            except urllib.error.HTTPError as reason:
                    print(reason)
    print('                                                                                          \r', end='')
    print('下载完成！共计下载歌曲：%s'% str(len(sum([i[2] for i in os.walk(cf.PATH)],[]))))
    v3.set('下载完成！共计下载歌曲：%s'% str(len(sum([i[2] for i in os.walk(cf.PATH)],[]))))
    time.sleep(3)
    v3.set('准备开始')

def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    cf.percent = 100.0 * blocknum * blocksize / totalsize
    if cf.percent > 100:
        cf.percent = 100
    print('                                                                                         \r', end='')
    print(('<---"%s"--->进度 = %-6.2f%%--->\r' % (redecode(cf.DOWNLOADING_SONG_NAME),cf.percent)), end='')
    v3.set('"%s"进度 = %-6.2f%%\r' % (redecode(cf.DOWNLOADING_SONG_NAME),cf.percent))
def run():
    pagenum=0
    print('<---------------------------数据爬取中,即将开始下载--------------------------->')
    v3.set('数据爬取中,即将开始下载')
    while len(get_work_list(cf.SONG_URL1,cf.SONG_URL2,cf.SONG_URL3,str(pagenum),str(get_userid(cf.UserID))))!=2:
        CONTENT_JSON=get_work_list(cf.SONG_URL1,cf.SONG_URL2,cf.SONG_URL3,str(pagenum),str(get_userid(cf.UserID)))
        CONVERT_CONTENT=js.loads(CONTENT_JSON)
        pagenum+=1
        for i in range(len(CONVERT_CONTENT)):
            URL_OF_SONG=cf.MAIN_URL+'/s/'+CONVERT_CONTENT[i].get('enworkid')
            NAME_OF_SONG=CONVERT_CONTENT[i].get('songname')
            cf.URL_DICT[NAME_OF_SONG]=URL_OF_SONG

    cf.UserName=get_username()
    cf.PATH=cf.PATH+cf.UserName
    print(redecode('<---------------------------正在下载\'%s\'的歌曲--------------------------->') % cf.UserName)
    v3.set('正在下载\'%s\'的歌曲' % cf.UserName)
    download_work(cf.URL_DICT)

def file_name_check(name):
    str1='\/：:*?？"<>|-!！。. _——，,'
    name_array=list(name)
    for i in name_array:
        if i in str1:
            name_array[name_array.index(i)]=''
    result_str = ('').join(name_array)
    return result_str

def clicl_btn():
    userid=v1.get()
    #root.withdraw()
    if v3.get()=='准备开始':
        if userid == '':
            tkinter.messagebox.askokcancel('请输入主播ID')
        else:
            cf.UserID=userid
            cf.PATH=v2.get()+'/'+cf.UserName
            get_data_thread=myThread(1,"get_data_thread",run)
            get_data_thread.setDaemon(True)
            get_data_thread.start()
    else:
        tkinter.messagebox.askokcancel('提示！','上一个任务正在进行中......')
        
        #run()
        
def get_path():
    choose_path=tkinter.filedialog.askdirectory()
    v2.set(choose_path)


 
def get_username():
    for i in cf.URL_DICT:
        website=cf.URL_DICT[i]
        break
    req=urllib.request.Request(website)
    html = urllib.request.urlopen(req)
    html_content =html.read().decode('utf8')
    if len(get_object_element(cf.ADD_REG_EXP6,html_content))!=0:
        content=get_object_element(cf.ADD_REG_EXP6,html_content)[0]
        content_clean=file_name_check(content)
        name=content_clean[0:content_clean.index('安')]
    else:
        print("未找到用户名称！")
        name='匿名'
    return name

def redecode(str):
    reture_str=str.encode("GBK", 'ignore').decode('gbk')
    return reture_str

root = tkinter.Tk()
root.title('请输入主播ID')
root.geometry('350x84')
#root.attributes("-alpha", 0.95)
#root.iconbitmap(r'C:\Users\Administrator\Desktop\QTPlayer.ico')
v1 = StringVar()
v1.set("")
l1=Label(root, text="主播ID：",justify=LEFT).grid(column=1, row=1, sticky=W)
Entry(root, width=30,textvariable=v1,justify=LEFT).grid(column=2, row=1, sticky=N+S+E+W)
v2=StringVar()
v2.set('E:\\')
Entry(root, width=30,textvariable=v2,justify=LEFT).grid(column=2, row=2, sticky=N+S+E+W)
l2=Label(root, text="存储位置：",justify=LEFT).grid(column=1, row=2, sticky=W)
Button(root, text="路    径",width=8,command = get_path).grid(column=3, row=2, sticky=W)
Label(root, text="",height=1,justify=LEFT).grid(column=1, row=3, sticky=W)
Button(root, text="开始下载",width=8, command = clicl_btn).grid(column=3, row=1, sticky=W)
v3=StringVar()
v3.set("准备开始")
Label(root,bg='lightgray',width=50,textvariable=v3,justify=LEFT).grid(columnspan=3,column=1, row=3,sticky=W)
labelframe = LabelFrame(root, text="This is a LabelFrame")
root.mainloop()


