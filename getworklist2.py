import urllib.request
import tkinter
import re
import time
import conf as cf
import json as js
from tkinter import *
import sys
import os

global DOWNLOADING_SONG_NAME
global percent
DOWNLOADING_SONG_NAME=''
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
'''	
    try:
		req = urllib.request.Request(website,headers=USER_AGENT)
		html = urllib.request.urlopen(req)
		html_content = html.read().decode('utf8')
		#print(html_content)
		return html_content
	except urllib.error.HTTPError as err:
		print(err.msg)
'''

def get_object_element(reg,content):
	object_element_list=re.findall(reg,content)
	return object_element_list

def download_work(url_dict):
    URL_DOWNLOAD={}
    global DOWNLOADING_SONG_NAME
    global percent
    path="E:\\"+cf.UserID+"\\"
    os.mkdir(path)
    for key in url_dict:
        url=url_dict[key]
        content=download_url(url)
        #time.sleep(0.3)
        if len(get_object_element(cf.ADD_REG_EXP4,content))!= 0:
                content_part=get_object_element(cf.ADD_REG_EXP4,content)[0]
        try:
                DOWNLOADING_SONG_NAME=str(key)
                urllib.request.urlretrieve(content_part,"E:\\"+cf.UserID+"\\" + file_name_check(str(key)) + ".mp3",callbackfunc)
        except urllib.error.HTTPError as reason:
                print(reason)
 
    print(URL_DOWNLOAD)
 
def callbackfunc(blocknum, blocksize, totalsize):
    '''回调函数
    @blocknum: 已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
    '''
    global DOWNLOADING_SONG_NAME
    global percent
    percent = 100.0 * blocknum * blocksize / totalsize
    if percent > 100:
        percent = 100
    print('<---"%s"--->进度 = %-6.2f%%\r' % (DOWNLOADING_SONG_NAME,percent))

def run():
    URL_DICT={}
    pagenum=0
    print('<---------------------------数据爬取中,即将开始下载--------------------------->\r')
    for i in range(25):
        sys.stdout.write('<---------------------------{0}秒/剩余时间25秒--------------------------->\r'.format(i + 1))
        sys.stdout.flush()
        time.sleep(1)
    while len(get_work_list(cf.SONG_URL1,cf.SONG_URL2,cf.SONG_URL3,str(pagenum),str(get_userid(cf.UserID))))!=2:
        
        CONTENT_JSON=get_work_list(cf.SONG_URL1,cf.SONG_URL2,cf.SONG_URL3,str(pagenum),str(get_userid(cf.UserID)))
        CONVERT_CONTENT=js.loads(CONTENT_JSON)
        pagenum+=1
        for i in range(len(CONVERT_CONTENT)):
            URL_OF_SONG=cf.MAIN_URL+'/s/'+CONVERT_CONTENT[i].get('enworkid')
            NAME_OF_SONG=CONVERT_CONTENT[i].get('songname')
            URL_DICT[NAME_OF_SONG]=URL_OF_SONG
    
    download_work(URL_DICT)

def file_name_check(name):
    str1='\/：:*?？"<>|'
    name_array=list(name)
    for i in name_array:
        if i in str1:
            name_array[name_array.index(i)]='~'
    result_str = ('').join(name_array)
    return result_str
def clicl_btn():
    userid=v2.get()
    root.withdraw()
    if userid == '':
        messagebox('请输入主播ID！')
    else:
        cf.UserID=userid
        
        run()

root = tkinter.Tk()
root.title('请输入主播ID')
root.geometry('300x100') 
root.attributes("-alpha", 0.95)
root.iconbitmap('K:\Python\DLLs\py.ico')
v2 = StringVar()
#设置entry为只读属性
Label(root, text="主播ID：").pack()
#默认情况下下Entry的状态为normal
Entry(root, width=30,textvariable=v2).pack()
v2.set("")
#将输入的内容用密文的形式显示
Button(root, text="确定",width=30, command = clicl_btn).pack()

root.mainloop()
#run()