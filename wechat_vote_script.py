#!/usr/bin/env python
# encoding: utf-8

# File name:    wechat_vote_script.py
# Author:       Coder_Dong
# Version:      1.00
# Date:         12, Jul, 2020
# Description:  wechat vote script

import requests
import re
from time import sleep

VOTE_HEADER = {
	    	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
		          'application/signed-exchange;v=b3;q=0.9',
	    	'Accept-Encoding': 'gzip, deflate',
	    	'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
	    	'Cache-Control': 'max-age=0',
		'Cookie': 'PHPSESSID=1cb643e770dae659f5b9a1f11904f407; _currentUrl_=czozNDoiL01lbWJlci9pbmRleC5waHA%2FbT1QdWJsaWMmYT1sb2dpbiI7',
		'Host': 'celou.net.cn',
		'Proxy-Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 '
		              'Safari/537.36 QBCore/3.53.1159.400 QQBrowser/9.0.2524.400 Mozilla/5.0 (Windows NT 6.1; WOW64) '
		              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 '
	    	              'NetType/WIFI WindowsWechat',
}

status_info = {r'\u6295\u7968\u5931\u8d25\uff0c\u5728\u89c4\u5b9a\u65f6\u95f4\u5185\u4e0d\u80fd\u91cd\u590d\u6295\u7ed9\u540c\u4e00\u4e2a\u4eba':
"投票失败，在规定时间内不能重复投给同一个人",
r"\u8be5\u9009\u624b\u6295\u7968\u8fc7\u591a,\u8bf715\u5206\u949f\u540e\u518d\u6295":
"该选手投票过多,请15分钟后再投"}

class WeChatVote(object):
    def __init__(self, vote_url, IP_FILE_PATH):
        self.vote_url = vote_url
        self.proxies = {'http': None,
                        "https": None
                        }
        self.IP_FILE_PATH = IP_FILE_PATH

    def vote(self, response, proixes):
        """
            check the response info if the stautus code
        """
        try:
            status_info = re.search(r'"info":"(.*?)"', response).group(1)
            status_code = re.search(r'"status":(.*?), ', response).group(1)
        except AttributeError as e:
            status_code = None
            status_info = None
        if not status_code:
            print('投票失败')
        elif status_code == '1':
            print(proixes['http'], '投票成功')
        else:
            reason = status_info[info]
            print(proixes['http'], '投票失败', reason)
            

    def load_ip(self):
        """
            load ip
        """
        with open(self.IP_FILE_PATH, 'r', encoding='utf-8') as f:
            ips = f.readlines()
        return ips

    def connect(self, url, proxies):
        """
            connect to url
        """
        
        try:
            resp = requests.get(url, headers = VOTE_HEADER, proxies = proxies)
            if resp.status_code == 200:
                return resp.text
            else:
                return None
        except Exception as e:
            return None

    def run(self):
        ips = self.load_ip()
        for ip in ips:
            sleep(30)
            self.proxies['http'] = re.sub('\n', '', ip)
            self.proxies['https'] = self.proxies['http']
            response = self.connect(self.vote_url, self.proxies)
            if response is "Error" or text is None:
                print('Error')
            else:
                self.vote(response, proxies)
vote_url = 'http://celou.net.cn/Home/index.php?m=Index&a=vote&vid=198403&id=1429&tp='
IP_FILE = './ips.txt'
vote = WeChatVote(vote_url, IP_FILE)
vote.run()
