# 
# Author: Fangda
# Date: 2017-10-26
# A simple mobile weibo crawler  
#


# import binascii
# import base64
# import re


from urllib.parse import urlencode
from bs4 import BeautifulSoup
import urllib
import json  
import requests


# import time
# r = requests.post('https://requestb.in/167wbct1', data={"ts":time.time()})
# print(r.status_code)
# print(r.content)


class MWeiboLogin:
    
    def __init__(self):
        self.session=requests.Session()

    def userlogin(self,
                    username="",
                    password="",
                    verbose=True):
        """
        login module for moblie weibo
        param 
        username:weibo username
        password:weibo password
        verbose: print login process status code when True
        """
        # set headers
        headers={
        'Origin': 'https://passport.weibo.cn',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Referer': 'https://passport.weibo.cn/signin/login?entry=mweibo',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8,zh;q=0.6,zh-CN;q=0.4',
        }

        # setup crawl session
        self.session.headers=headers
        
        # login settings
        payload={
            'username':username,
            'password':password,
            'savestate':'1',
            'r':'http://weibo.cn/?featurecode=20000320',
            'oid':'4166716080362935',
            'luicode':'20000061',
            'lfid':'4166716080362935',
            'ec':'0',
            'pagerefer':'',	
            'entry':'mweibo',
            'wentry':'',
            'loginfrom':'',	
            'client_id':'',	
            'code':'',	
            'qq':''	,
            'mainpageflag':1,
            'hff':'',	
            'hfp':'',	
        }

        # visit any mobile weibo to get corresponding cookies 
        resp = self.session.get("https://weibo.cn/pub/")
        if resp.status_code == 200:
            if verbose:
                print("正在登陆",resp.status_code)
        else:
            raise Exception("登陆错误")
        #soup=BeautifulSoup(resp.content)

        # login page, keep if in case of furture use
        # resp = self.session.get("https://passport.weibo.cn/signin/login?entry=mweibo&r=http%3A%2F%2Fweibo.cn%2F&backTitle=%CE%A2%B2%A9&vt=")
        # print(resp.status_code)

        url_mweibologin = 'https://passport.weibo.cn/sso/login'
        resp=self.session.post(url_mweibologin,data=payload)
        if resp.status_code == 200:
            if verbose:
                print("解析地址",resp.status_code)
        else:
            raise Exception("登陆错误")
        
        # parse auth pages url in result
        res_json=json.loads(resp.content.decode())
        weiboList=res_json['data']['crossdomainlist']

        # get cookie from a series of pages
        for item in weiboList:
            resp=self.session.get(weiboList[item])
            if resp.status_code == 200:
                if verbose:
                    print("解析地址",resp.status_code)
            else:
                raise Exception("登陆错误")
        
        if verbose:
            print("登陆成功")
    
    def crawl(self,data, url="https://weibo.cn/"):
        resp=self.session.get(url,params=data)
        return resp
        # soup=BeautifulSoup(resp.content,"lxml")
        # a=resp.content.decode("utf-8")
        # with open('mytextt.html',"w",encoding="utf-8") as f:
        #     f.write(a)

            


if __name__='__main__':
    # instantiate login
    crawler=MWeiboLogin()

    crawler.userlogin()
    crawler.crawl(url="https://requestb.in/1nn7ht71",data={"page":2})
    print("success")

