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
USER_AGENT={}
USER_AGENT['User-Agent']=cf.Mobile_User_Agent

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
    req = urllib.request.Request(website,headers=USER_AGENT)
    req.add_header=('Referer','http://www.changba.com/u/'+cf.UserID)
    req.add_header=('User-Agent',cf.Mobile_User_Agent)
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
    print('<---------------------------下载文件存放在：%s 中......' % cf.PATH)
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
    print('<---------------------------下载完成！共计下载歌曲：%s'% str(len(sum([i[2] for i in os.walk(cf.PATH)],[]))))
 
def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    cf.percent = 100.0 * blocknum * blocksize / totalsize
    if cf.percent > 100:
        cf.percent = 100
    print('                                                                                                                                                          \r', end='')
    print(('<---"%s"--->进度 = %-6.2f%%--->\r' % (cf.DOWNLOADING_SONG_NAME,cf.percent)), end='')

def run():
    pagenum=0
    print('<---------------------------数据爬取中,即将开始下载--------------------------->')
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
    #print(cf.PATH)
    print('<---------------------------正在下载\'%s\'的歌曲--------------------------->' % cf.UserName)
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
    root.withdraw()
    if userid == '':
        tkinter.messagebox.askokcancel('请输入主播ID')
    else:
        cf.UserID=userid
        cf.PATH=v2.get()+'/'+cf.UserName
        run()
        
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
    content=get_object_element(cf.ADD_REG_EXP6,html_content)[0]
    content_clean=file_name_check(content)
    name=content_clean[0:content_clean.index('安')]
    return name



#创建输入窗口
root = tkinter.Tk()
root.title('请输入主播ID')
root.geometry('300x140') 
#root.attributes("-alpha", 0.95)
root.iconbitmap('K:\Python\DLLs\py.ico')
v1 = StringVar()
l1=Label(root, text="主播ID：",justify=LEFT).grid(column=3, row=1, sticky=W)
Entry(root, width=30,textvariable=v1,justify=LEFT).grid(column=3, row=2, sticky=W)
v1.set("")
v2=StringVar()
l2=Label(root, text="存储位置：",justify=LEFT).grid(column=3, row=3, sticky=W)
v2.set('E:\\')
Entry(root, width=30,textvariable=v2,justify=LEFT).grid(column=3, row=4, sticky=W)
Button(root, text="路径",width=5,command = get_path).grid(column=4, row=4, sticky=W)
Button(root, text="确定",width=30, command = clicl_btn).grid(column=3, row=6, sticky=W)

root.mainloop()