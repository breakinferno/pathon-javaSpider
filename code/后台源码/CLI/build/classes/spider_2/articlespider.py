# -*- coding: utf-8 -*-

# 整体思路是通过抓取搜狗的微信文章搜索引擎来完成，数据插入数据库表article中
# http://weixin.sogou.com/
# 2017-07-15 by sehnji5

import logging, config
import random, re, sys, time, math, json, cookielib
import matplotlib.pyplot as plt # plt 用于显示图片
import MySQLdb
import requests
from PIL import Image
from lxml import etree
from wechatsogou import *
from filecache import WechatCache
from ruokuaicode import RClient
from datetime import datetime
from urllib import quote

reload(sys)
sys.setdefaultencoding('utf-8')

def list_or_empty(content, contype=None):
    if isinstance(content, list):
        if content:
            return contype(content[0]) if contype else content[0]
        else:
            if contype:
                if contype == int:
                    return 0
                elif contype == str:
                    return ''
                elif contype == list:
                    return []
                else:
                    raise Exception('only cna deal int str list')
            else:
                return ''
    else:
        raise Exception('need list')

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

# wechatsogou实例
wechats = WechatSogouApi()
logger = logging.getLogger()

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
        self.sogou_search_url = 'http://weixin.sogou.com/weixin?query=%s&_sug_type_=&_sug_=n&type=2&page=%d&ie=utf8' % (
        quote(self.kw), self.page)

    #微信关键字搜索文章（暂时写死的URL是微信文章的URL）
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
            try:
                jar.load('cookie.txt', ignore_discard=False, ignore_expires=False)
            except:
                pass

            r = self._session.get(self.sogou_search_url, cookies=jar, headers=headers)

            # 将CookieJar转为字典：
            cookies = requests.utils.dict_from_cookiejar(jar)
            #print "全局变量Cookies为："
            #print cookies
            # print cookies
        else:
            print "第一页之后从全局变量Cookies中加载Cookie"
            #print "全局变量Cookies为："
            #print cookies
            # 将字典转为CookieJar：
            jar = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
            r = self._session.get(self.sogou_search_url, cookies=jar, headers=headers)

        print self._session.cookies

        return r.text

    #解析一条微信文章信息，返回字典信息
    def parse_one_wx_article(self,li):
        url = li.xpath('div[1]/a/@href')
        if url:
            title = li.xpath('div[2]/h3/a')
            imgs = li.xpath('div[1]/a/img/@src')
            abstract = li.xpath('div[2]/p')
            time = li.xpath('div[2]/div/span/script/text()')
            gzh_info = li.xpath('div[2]/div/a')[0]
        else:
            url = li.xpath('div/h3/a/@href')
            title = li.xpath('div/h3/a')
            imgs = []
            spans = li.xpath('div/div[1]/a')
            for span in spans:
                img = span.xpath('span/img/@src')
                if img:
                    imgs.append(img)
            abstract = li.xpath('div/p')
            time = li.xpath('div/div[2]/span/script/text()')
            gzh_info = li.xpath('div/div[2]/a')[0]

        if title:
            title = self._get_elem_text(title[0]).replace("red_beg", "").replace("red_end", "")
        else:
            title = ''
        if abstract:
            abstract = self._get_elem_text(abstract[0]).replace("red_beg", "").replace("red_end", "")
        else:
            abstract = ''
        time = list_or_empty(time)
        time = re.findall('timeConvert\(\'(.*?)\'\)', time)
        time = list_or_empty(time, int)
        gzh_article_url = gzh_info.xpath('@href')
        gzh_headimage = gzh_info.xpath('@data-headimage')
        gzh_qrcodeurl = gzh_info.xpath('@data-encqrcodeurl')
        gzh_name = gzh_info.xpath('text()')  # 修改了获取发布公众号的名字
        gzh_wechatid = gzh_info.xpath('@data-username')
        gzh_isv = gzh_info.xpath('@data-isv')
        gzh_avgpublish = gzh_info.xpath('@data-avgpublish')
        gzh_avgread = gzh_info.xpath('@data-avgread')

        return {
            'article': {
                'title': title,
                'url': list_or_empty(url),
                'imgs': imgs,
                'abstract': abstract,
                'time': time
            },
            'gzh': {
                'article_list_url': list_or_empty(gzh_article_url),
                'headimage': list_or_empty((gzh_headimage)),
                'qrcodeurl': list_or_empty((gzh_qrcodeurl)),
                'name': list_or_empty(gzh_name),
                'wechatid': list_or_empty(gzh_wechatid),
                'isv': list_or_empty(gzh_isv, int),
                'avgpublish': list_or_empty(gzh_avgpublish, int),
                'avgread': list_or_empty(gzh_avgread, int)
            }
        }

    #若被封，则尝试解封
    def _jiefeng(self):
        """对于出现验证码，识别验证码，解封
        """
        global cookies

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
        #修改全局变量Cookies
        snuid = json.loads(rr.text).get('id')
        cookies['SNUID'] = snuid
        print "尝试解封后修改全局变量Cookies的值，修改后Cookies为："
        print cookies

        print "得到的rr是："+json.loads(rr.text).get('msg')

        self._cache.set(config.cache_session_name, self._session)
        print('ocr ', remsg['msg'].decode('utf8'))

    #日志记录
    def log(self, msg):
        ' 自定义log函数 '
        print u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)

    #得到元素的文本
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

    #判断文章已经存在(从数据库中查询相同名字且发表时间相同的文章数量，基本可以排除在相同时间戳有人发表相同名字的文章)
    def article_is_exist(self,wx_article_info):
        article_title = wx_article_info["article"]["title"].encode('utf8','ignore')
        article_time = wx_article_info["article"]["time"]
        select_article_sql = "select count(article_id) from article where article_title='"+article_title+"' and article_time='"+str(article_time)+"'"
        try:
            cursor.execute(select_article_sql)
            same_article_num = cursor.fetchall()
            return same_article_num[0][0]
        except:
            print "查找同名文章失败"
            return 0
    # 文章已经存在,更新原数据的链接、发布公众号的名字、发布公众号的链接、添加时间
    def update_article_info(self, wx_article_info):
        article_title = wx_article_info["article"]["title"].encode('utf8','ignore')
        article_time = wx_article_info["article"]["time"]
        article_url = wx_article_info["article"]["url"]
        article_gzh_name = wx_article_info["gzh"]["name"].encode('utf8','ignore')
        article_gzh_url = wx_article_info["gzh"]["article_list_url"]
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update_sql = ("UPDATE article SET article_url='%s', article_gzh_name='%s', article_gzh_url='%s', add_time='%s' "
        "WHERE article_title='%s' AND article_time='%s'" % (
        article_url, article_gzh_name, article_gzh_url, addDate, article_title, article_time))

        cursor.execute(update_sql)
        db.commit()
        print "更新完成"

    #文章不存在数据库中，直接插入存储进入数据库
    def insert_article_info(self, wx_article_info):
        # 插入数据库时间
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 构造sql语句
        insert_wx_article = (
        "INSERT INTO article(article_title,article_url,article_abstract,article_time,article_gzh_name,article_gzh_url,article_gzh_headimg,add_time,keyword) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)")
        data_wx_article = (
        wx_article_info["article"]["title"].encode('utf8', 'ignore'), wx_article_info["article"]["url"],
        wx_article_info["article"]["abstract"].encode('utf8', 'ignore'), wx_article_info["article"]["time"],
        wx_article_info["gzh"]["name"].encode('utf8', 'ignore'), wx_article_info["gzh"]["article_list_url"],
        wx_article_info["gzh"]["headimage"], addDate.encode('utf8', 'ignore'),self.kw.encode('utf8', 'ignore'))

        try:
            cursor.execute(insert_wx_article, data_wx_article)
            db.commit()
            print "插入成功\n"
        except:
            print ("插入失败")

    def run(self):
        ' 爬虫入口函数 需要登录，否则只能爬取前一百条'
        # self.login_sougou()
        global pages
        self.log(u'搜索网址为：%s' % self.sogou_search_url)
        self.log(u'开始获取，微信文章关键字为：%s' % self.kw)
        self.log(u'开始调用sougou搜索引擎')
        sougou_search_html = self.get_search_result_by_kw()
        #chardet.detect(sougou_search_html)['encoding']
        #print sougou_search_html
        self.log(u'获取该关键字的搜索结果第%d页' % self.page)
        self.log(u'获取第%d页成功，开始抓取该页面的文章' % self.page)
        page = etree.HTML(sougou_search_html)
        lis = page.xpath('//ul[@class="news-list"]/li')
        #print lis
        numtext = page.xpath('//*[@id="pagebar_container"]/div/text()')
        #print numtext
        try:
            numtext = numtext[0].encode('utf8','ignore')
            num = re.split('找到约|条结果',numtext)
            print "查询到" + num[1] + "条结果"
            pages = math.ceil(int(num[1].replace(',',''))/10.0)
        except:
            print "查询文章数错误，pages = "+str(pages)

        if('ç¨æ·æ¨å¥½ï¼æ¨çè®¿é®è¿äºé¢ç¹ï¼ä¸ºç¡®è®¤æ¬æ¬¡è®¿é®ä¸ºæ­£å¸¸ç¨æ·è¡ä¸ºï¼éè¦æ¨åå©éªè¯ã' in sougou_search_html):
            self.log("发现页面被封")
            #设置被封的URL
            self._vcode_url = self.sogou_search_url
            self.log("请求网址："+self._vcode_url+"时被封，开始尝试解封")
            #运行解封函数
            self._jiefeng()
            self.log("解封程序运行完成，再一次访问页面")
            #重新访问页面
            sougou_search_html = self.get_search_result_by_kw()
            print "重新请求："+self.sogou_search_url
            print sougou_search_html
            page = etree.HTML(sougou_search_html)
            lis = page.xpath('//ul[@class="news-list"]/li')
            #print sougou_search_html
            numtext = page.xpath('//*[@id="pagebar_container"]/div/text()')
            #print lis
            try:
                numtext = numtext[0].encode('utf8', 'ignore')
                num = re.split('找到约|条结果', numtext)
                print "查询到"+num[1]+"条结果"
                #pages = math.ceil(int(num[1].replace(',', '')) / 10.0)
                pages = 100
            except:
                print "查询文章数错误，pages = " + str(pages)


        # 1.怎么判断是否是最后一页，如果地址栏page大于了最大页数它会一直返回最后一页，所以如果没有被封每次拿取到的li都不会为0
        # 2.怎么判断是否被封了，需要输入验证码验证
        for li in lis:
            wx_article_info = self.parse_one_wx_article(li)
            print wx_article_info

            #如果有相同的文章，则更新原数据的链接、发布公众号的名字、发布公众号的链接、添加时间
            if(self.article_is_exist(wx_article_info)>0):
                print "数据库有相同的文章，更新相关链接"
                self.update_article_info(wx_article_info)
            else:
                print "数据库没有相同的文章，直接存入数据库"
                self.insert_article_info(wx_article_info)

# main
if __name__ == '__main__':
    global pages
    global cookies
    pages = 1
    print('连接到mysql服务器...')
    db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
    print('连接上了!')
    cursor = db.cursor()
    pageNum = 1
    while(pageNum<=pages):
        print ("pages = " + str(pages))
        weixin_spider('国寿', pageNum).run()
        time.sleep(10)
        pageNum = pageNum + 1