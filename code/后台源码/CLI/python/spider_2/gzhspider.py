# -*- coding: utf-8 -*-

# 整体思路是通过抓取搜狗的微信文章搜索引擎来完成，数据插入数据库表wxnum中
# http://weixin.sogou.com/
# 2017-07-15 by sehnji5

import logging
import random, re, os, sys, time, math, cookielib, json
import matplotlib.pyplot as plt # plt 用于显示图片
import urllib2
from datetime import datetime
from urllib import quote

import MySQLdb
import requests
from PIL import Image
from lxml import etree
from pyquery import PyQuery as pq
from wechatsogou import *

import config
from filecache import WechatCache
from ruokuaicode import RClient

reload(sys)
sys.setdefaultencoding('utf-8')
logger = logging.getLogger()

def printf(msg=''):
    try:
        return raw_input(msg)
    except NameError:
        return input(msg)

try:
    import StringIO

    def readimg(content):
        return Image.open(StringIO.StringIO(content))
except ImportError:
    import tempfile


    def readimg(content):
        f = tempfile.TemporaryFile()
        f.write(content)
        return Image.open(f)

class weixin_spider:
    def __init__(self, kw, num):
        self._cache = WechatCache(config.cache_dir, 60 * 60)
        self._session = self._cache.get(config.cache_session_name) if self._cache.get(
            config.cache_session_name) else requests.session()

        dama_name = 'yyNoMoon'
        dama_pswd = '09181024'
        dama_soft_id = '85372'
        dama_soft_key = '5ad8e22e3cc346618166acc91f8da27b'
        self._ocr = RClient(dama_name, dama_pswd, dama_soft_id, dama_soft_key)

        self._agent = [
            "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
            "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
            "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
            "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
            "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
            "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
            "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
            "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
            "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
            "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
            "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
        ]

        #关键字
        self.kw = kw
        # 第几页
        self.page = num
        # 搜狗微信搜索链接
        self.sogou_search_url = 'http://weixin.sogou.com/weixin?query=%s&_sug_type_=&_sug_=n&type=1&page=%d&ie=utf8' % (
        quote(self.kw), self.page)

    #预计此处会做出用户扫码登录，已获取完整信息
    #def login_sougou(self):
    #    basic_url = 'https://open.weinxin.qq.com/connect/confirm?uuid=0017w8PrRrSRda27'
    #    return self.s.get(basic_url, headers=self.headers, timeout=self.timeout).content

    #微信关键字搜索公众号（因为暂时写死的URL是公众号的URL）
    def get_search_result_by_kw(self):
        ' 调用搜狗微信搜索 '
        global pages
        global cookies

        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
        }
        if (self.page == 1):
            print "第一次加载从文件加载Cookie"
            jar = cookielib.MozillaCookieJar()
            # 试着载入cookie
            # 提一个问题，为什么要加入ignore_discard属性？
            try:
                jar.load('cookie.txt', ignore_discard=False, ignore_expires=False)
            except:
                pass

            r = self._session.get(self.sogou_search_url, cookies=jar, headers=headers)

            # 将CookieJar转为字典：
            cookies = requests.utils.dict_from_cookiejar(jar)
            print "全局变量Cookies为："
            print cookies
            # print cookies
        else:
            print "第一页之后从全局变量Cookies中加载Cookie"
            print "全局变量Cookies为："
            print cookies
            # 将字典转为CookieJar：
            jar = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
            r = self._session.get(self.sogou_search_url, cookies=jar, headers=headers)

        print self._session.cookies

        return r.text

    #得到页面中的微信公众号那一串list（暂时未使用）
    def get_wx_num_by_sougou_search_html(self, sougou_search_html):
        doc = pq(sougou_search_html)
        return doc('ul[class="news-list2"]')

    #解析一条微信公众号信息，返回字典信息
    def parse_one_wx_num(self,li):
        url = li.xpath('div/div[1]/a/@href')
        img = li.xpath('div/div[1]/a/img/@src')
        name = self._get_elem_text(li.xpath('div/div[2]/p[1]')[0])
        info = self._get_elem_text(li.xpath('div/div[2]/p[2]')[0])
        info = info.encode('utf8', 'ignore')  # 改变info编码，否则正则匹配会失败
        # print info
        info = re.split('微信号：|月发文|篇|平均阅读', info)
        # print info[1]
        try:
            wechatid = info[1]
        except IndexError:
            wechatid = ''
        try:
            post_perm = int(info[2])
        except IndexError:
            post_perm = 0
        try:
            read_count = int(info[3])  # 将4改成了3，不知道为什么他会写成4
        except IndexError:
            read_count = 0
        qrcode = li.xpath('div/div[3]/span/img[1]/@src')
        jieshao = self._get_elem_text(li.xpath('dl[1]/dd')[0])
        renzhen = li.xpath('dl[2]/dd/text()')
        pubarticle = li.xpath('dl[3]/dd/text()')  # 添加了一个最近发布的文章,判断公众号是否发表过文章
        if (len(pubarticle) == 0):
            pubarticle = '否'
        else:
            pubarticle = '是'

        return {
            'url': url[0],
            'img': img[0],
            'name': name.replace('red_beg', '').replace('red_end', ''),
            'wechatid': wechatid,
            'post_perm': post_perm,
            'read_count': read_count,
            'qrcode': qrcode[0] if qrcode else '',
            'introduction': jieshao.replace('red_beg', '').replace('red_end', ''),
            'authentication': renzhen[0] if renzhen else '',
            'pubarticle': pubarticle
        }

    #若被封，则尝试解封
    def _jiefeng(self):
        """对于出现验证码，识别验证码，解封

        Args:
            ruokuai: 是否采用若快打码平台

        Raises:
            WechatSogouVcodeException: 解封失败，可能验证码识别失败
        """
        self.log('vcode appear, using _jiefeng')
        codeurl = 'http://weixin.sogou.com/antispider/util/seccode.php?tc=' + str(time.time())[0:10]
        coder = self._session.get(codeurl)
        if hasattr(self, '_ocr'):
            result = self._ocr.create(coder.content, 3060)
            img_code = result['Result']
        else:
            # 显示验证码，人工识别输入
            im = readimg(coder.content)
            plt.imshow(im)  # 显示图片
            plt.axis('off')  # 不显示坐标轴
            plt.show()

            img_code = printf("please input code: ")
        post_url = 'http://weixin.sogou.com/antispider/thank.php'
        post_data = {
            'c': img_code,
            'r': quote(self._vcode_url),   #经过对比发现只需要weixin.sogou.com后面的一段字符，但全部用上好像也行
            'v': 5
        }
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
            'Host': 'weixin.sogou.com',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2f' + quote(
                self._vcode_url.replace('http://weixin.sogou.com/', ''))
        }
        rr = self._session.post(post_url, post_data, headers=headers)
        remsg = eval(rr.content)
        if remsg['code'] != 0:
            logger.error('cannot jiefeng because ' + remsg['msg'])
        # 修改全局变量Cookies
        snuid = json.loads(rr.text).get('id')
        cookies['SNUID'] = snuid
        print "尝试解封后修改全局变量Cookies的值，修改后Cookies为："
        print cookies

        print "得到的rr是：" + json.loads(rr.text).get('msg')

        self._cache.set(config.cache_session_name, self._session)
        print('ocr ', remsg['msg'].decode('utf8'))

    #日志记录
    def log(self, msg):
        ' 自定义log函数 '
        print u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)

    # 得到元素的文本
    def _get_elem_text(self, elem):
        """抽取lxml.etree库中elem对象中文字

        Args:
            elem: lxml.etree库中elem对象

        Returns:
            elem中文字
        """
        rc = []
        for node in elem.itertext():
            rc.append(node.strip())
        return ''.join(rc)

    # 判断公众号是否已经存在(从数据库中查询相同微信号的数据，微信号与公众号一一对应作为主键)
    def gzh_is_exist(self, wx_num_info):
        select_gzh_sql = "select count(wx_num) from wxnum where wx_num='" + wx_num_info["wechatid"]+"'"
        try:
            cursor.execute(select_gzh_sql)
            same_article_num = cursor.fetchall()
            return same_article_num[0][0]
        except:
            print "查找相同公众号失败"
            return 0
    # 公众号已经存在,更新原数据的链接、公众号的名字、简介、认证、是否发布过文章以及添加时间
    def update_gzh_info(self, wx_num_info):
        wx_num = wx_num_info["wechatid"]
        wx_num_url = wx_num_info["url"]
        wx_num_name = wx_num_info["name"].encode('utf8', 'ignore')
        fun_intro = wx_num_info["introduction"].encode('utf8', 'ignore')
        authentication = wx_num_info["authentication"].encode('utf8', 'ignore'),
        pubarticle = wx_num_info["pubarticle"].encode('utf8', 'ignore')
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        print "authentication = "+str(authentication[0])

        update_sql = ("UPDATE wxnum SET wx_num_link='%s', wx_num_name='%s', fun_intro='%s', authentication='%s', pubarticle='%s', add_time='%s' "
                      "WHERE wx_num='%s'" % (wx_num_url, wx_num_name, fun_intro, authentication[0], pubarticle, addDate, wx_num))

        cursor.execute(update_sql)
        db.commit()
        print "更新完成"

    # 公众号不存在数据库中，直接插入存储进入数据库
    def insert_gzh_info(self, wx_num_info):
        # 插入数据库时间
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构造sql语句
        insert_wx_num = (
        "INSERT INTO wxnum(wx_num,wx_num_link,wx_num_name,fun_intro,authentication,pubarticle,add_time,keyword) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
        data_wx_num = (wx_num_info["wechatid"], wx_num_info["url"], wx_num_info["name"].encode('utf8', 'ignore'),
                       wx_num_info["introduction"].encode('utf8', 'ignore'), wx_num_info["authentication"],
                       wx_num_info["pubarticle"].encode('utf8', 'ignore'), addDate.encode('utf8', 'ignore'),
                       self.kw.encode('utf8','ignore'))

        # 插入数据库
        try:
            cursor.execute(insert_wx_num, data_wx_num)
            db.commit()
            print "插入成功\n"
        except:
            print ("插入失败")

    def run(self):
        ' 爬虫入口函数 需要登录，否则只能爬取前一百条'
        # self.login_sougou()
        global pages
        self.log(u'搜索网址为：%s' % self.sogou_search_url)
        self.log(u'开始获取，微信公众号关键字为：%s' % self.kw)
        self.log(u'开始调用sougou搜索引擎')
        sougou_search_html = self.get_search_result_by_kw()

        self.log(u'获取该关键字的搜索结果第%d页' % self.page)
        self.log(u'获取第%d页成功，开始抓取该页面的公众号' % self.page)
        page = etree.HTML(sougou_search_html)
        lis = page.xpath('//ul[@class="news-list2"]/li')

        numtext = page.xpath('//*[@id="pagebar_container"]/div/text()')
        try:
            numtext = numtext[0].encode('utf8','ignore')
            num = re.split('找到约|条结果',numtext)
            print "查询到" + num[1] + "条结果"
            pages = math.ceil(int(num[1].replace(',',''))/10.0)
        except:
            print "查询文章数错误，pages = "+str(pages)

        while('ç¨æ·æ¨å¥½ï¼æ¨çè®¿é®è¿äºé¢ç¹ï¼ä¸ºç¡®è®¤æ¬æ¬¡è®¿é®ä¸ºæ­£å¸¸ç¨æ·è¡ä¸ºï¼éè¦æ¨åå©éªè¯ã' in sougou_search_html):
            self.log("发现页面被封")
            #设置被封的URL
            self._vcode_url = self.sogou_search_url
            self.log("请求网址："+self._vcode_url+"时被封，开始尝试解封")
            #运行解封函数
            self._jiefeng()
            self.log("解封程序运行完成，再一次访问页面")
            #重新访问页面
            sougou_search_html = self.get_search_result_by_kw()
            page = etree.HTML(sougou_search_html)
            lis = page.xpath('//ul[@class="news-list2"]/li')
            numtext = page.xpath('//*[@id="pagebar_container"]/div/text()')
            try:
                numtext = numtext[0].encode('utf8', 'ignore')
                num = re.split('找到约|条结果', numtext)
                print "查询到" + num[1] + "条结果"
                pages = math.ceil(int(num[1].replace(',', '')) / 10.0)
            except:
                print "查询文章数错误，pages = " + str(pages)

        for li in lis:
            wx_num_info = self.parse_one_wx_num(li)
            print wx_num_info

            if(self.gzh_is_exist(wx_num_info)>0):
                print "数据库有相同的公众号，更新相关链接"
                self.update_gzh_info(wx_num_info)
            else:
                print "数据库没有相同的公众号，直接存入数据库"
                self.insert_gzh_info(wx_num_info)


# main
if __name__ == '__main__':
    global pages
    pages = 1
    print('连接到mysql服务器...')
    db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
    print('连接上了!')
    cursor = db.cursor()
    pageNum = 1
    while(pageNum<=pages):
        weixin_spider('国寿', pageNum).run()
        time.sleep(10)
        pageNum = pageNum + 1

    #正则匹配地名，设置能够查询到的公众号的地名级别（省，市，县区）
    #os.system("python E:\Internship\爬虫python脚本\version1.0\learn\getlevel.py")