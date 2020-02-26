import requests
import time
import json

DEFAULT_HEAD = '''Accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
Accept-Encoding:gzip, deflate
Accept-Language:zh-CN,zh;q=0.9
Cache-Control:max-age=0
Connection:keep-alive
Content-Type:application/x-www-form-urlencoded
Host:10.10.10.9
Origin:http://10.10.10.9
Referer:http://10.10.10.9/a70.htm
Upgrade-Insecure-Requests:1
User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36'''

DEFAULT_DATA =  {
    '0MKKey': '123456',
    'DDDDD':'',#此处填写学号
    'Login':'',
    'R1': '0',
    'R2':'',
    'R3': '0',
    'R6': '0',
    'buttonClicked':'',
    'cmd':'',
    'err_flag':'',
    'para': '00',
    'password':'',
    'redirect_url':'',
    'upass': '',
    'user':'',
    'username':''
}

class Client():
    def __init__(self, header=None, cookies=None):
        self.headers = DEFAULT_HEAD
        if not header is None:
            self.headers = headers 
        
        self.cookies = {}
        if not cookies is None:
            self.cookies = cookies

        self.session = requests.session()
        

    def _trans_head(self,):
        headers = {}
        raw_head = self.headers
        for raw in raw_head.split('\n'):
            headerkey, headerValue = raw.split(':', 1)
            headers[headerkey] = headerValue
        return headers
    
    def post(self, url, post_data):
        headers = self._trans_head()
        res = self.session.post(url,post_data,headers,cookies=self.cookies)
        # print(requests.utils.dict_from_cookiejar(res.cookies))
        self.cookies.update(res.cookies)
        # print(sself.cookies)
        if res.status_code >= 400:
            return None
        return res.text
    
    def get(self, url, param_data):
        headers = self._trans_head()
        res = self.session.get(url,params=param_data, headers=headers, cookies=self.cookies)
        self.cookies.update(res.cookies)
        # print(res.text)
        if res.status_code >= 400:
            return ""
        return res.text

class User():
    def __init__(self, url='http://10.10.10.9/', user_name='', passwd=''):
        self.url = url
        self.user_name = user_name
        self.passwd = passwd

        self.client = Client()
    
    def _trans_res(self, raw_res):
        start = raw_res.find('(')+1
        end = raw_res.rfind(')')
        res = json.loads(raw_res[start:end])
        return res
    
    def login(self,):
        para_data = DEFAULT_DATA
        para_data['DDDDD'] = self.user_name
        para_data['upass'] = self.passwd
        res = self.client.post(self.url, para_data)

        if "认证成功页" in res:
            print("登录成功！！")
            return
        else:
            print("登录失败，请重试！！")
            return
    
    def json_login(self, ):
        url = 'http://10.10.10.9/drcom/login'
        t = int(1000 * time.time())
        para_data = {
            'callback': 'dr1582689734168',
            'DDDDD': self.user_name,
            'upass': self.passwd,
            '0MKKey': 123456,
            'R1': 0,
            'R3': 0,
            'R6': 0,
            'para': '00',
            'v6ip':'', 
            '_': t
        }
        res = self.client.get(url,param_data=para_data)
        print(res)
    
    def get_info(self, method='loadOnlineDevice'):
        url = "http://10.10.10.9:801/eportal/"
        t = int(1000 * time.time())
        para_data = {
            'c': 'GetUserMsg',
            'a': method,
            'callback': 'jQuery111309017605431204194_1582689082082',
            'account': self.user_name,
            '_': int(1000 * time.time())
        }
        res = self.client.get(url, para_data)
        res = self._trans_res(res)
        for item in res['list']:
            print(item)
            # print()
        # return res['list']
    
    def logout(self, ):
        url = "http://10.10.10.9/drcom/logout"
        para_data = {
            'callback':'dr1582694731120',
            '_': int(1000 * time.time())
        }
        res = self.client.get(url, param_data=para_data)
        start = res.find('(') + 1
        end = res.rfind(')') 
        print(res[start:end])
        res = json.loads(res[start:end])
        if res['result'] == 1:
            print("登出成功!!")
            return
        else:
            print("登出失败，请重试")
            return


