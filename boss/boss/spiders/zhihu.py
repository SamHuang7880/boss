# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
import re
from boss.items import BossItem

class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    #start_urls = ['http://www.zhihu.com/']
       
    def start_requests(self):       #用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request('https://www.zhihu.com/signin?next=%2F',meta={'cookiejar':1},callback=self.parse)]

    def parse(self, response):
     
        # 响应Cookie
        Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print(Cookie1)
        
        print('登录中')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        return [FormRequest.from_response(response,
                                          url='https://www.zhihu.com/signin?next=%2F',   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          formdata={'username':'13715257880','password':'Sam1234567'},
                                          callback=self.next,
                                          )]
        #print(response.body)
        print(response.meta['cookiejar'])
    def next(self,response):
        a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
        print(a)
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('https://www.zhihu.com/people/a-le-7880',meta={'cookiejar':True},callback=self.next2)
    
    def next2(self,response):
        # 请求Cookie
        Cookie2 = response.request.headers.getlist('Cookie')
        print(Cookie2)

        #body = response.body  # 获取网页内容字节类型
        #unicode_body = response.body_as_unicode()  # 获取网站内容字符串类型

        #a = response.xpath('/html/head/title/text()').extract()  #得到个人中心页面
        t = response.xpath('//text()').extract()
        txt = re.sub(r'[a-zA-Z",:{}\\.(\)!;%&?$@#><+|*/[\]_=-]', "", str(t))
        txt = txt.replace(" ", "")
        txt = txt.replace("'","")
        print(txt)
        item = BossItem()
        item['txt'] = txt
        return item
    
