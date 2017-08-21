# -*- encoding:utf-8 -*-

#-------------------------------------------------------------------------------------------------------
#
#  管理员点击某条文章，如果发现文章的连接失效，那么可以点击更新链接按钮进行更新
#  前端传来的是一个文章的id，首先根据id找到那条文章，得到它的名字、时间戳等
#  然后将文章的名字作为关键字进行查找，爬取最开始的一条数据，如果时间戳相等，则将它的各种URL更新到数据库
#
#-------------------------------------------------------------------------------------------------------

import random, time, re, logging, json
import MySQLdb
import requests, cookielib, config
from lxml import etree
from datetime import datetime
from PIL import Image
from urllib import quote
from filecache import WechatCache
from ruokuaicode import RClient
import matplotlib.pyplot as plt # plt 用于显示图片

import sys
reload(sys)
sys.setdefaultencoding("utf-8")
logger = logging.getLogger()

def printf(msg=''):
    try:
        return raw_input(msg)
    except NameError:
        return input(msg)

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

class update_URL_by_id:
    def __init__(self, id):
        self.id = id
        self._cache = WechatCache(config.cache_dir, 60 * 60)
        self._session = self._cache.get(config.cache_session_name) if self._cache.get(
            config.cache_session_name) else requests.session()
        #self._session = requests.session()
        self.update_success = False
        self.load_cookie = False
        self.article_info = []
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
        dama_name = 'yyNoMoon'
        dama_pswd = '09181024'
        dama_soft_id = '85372'
        dama_soft_key = '5ad8e22e3cc346618166acc91f8da27b'
        self._ocr = RClient(dama_name, dama_pswd, dama_soft_id, dama_soft_key)

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

    # 若被封，则尝试解封
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
            'r': quote(self._vcode_url),  # 经过对比发现只需要weixin.sogou.com后面的一段字符，但全部用上好像也行
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

    def get_info_by_id(self):
        sql = "select article_id,article_title,article_time from article where article_id="+str(self.id)
        cursor.execute(sql)
        info = cursor.fetchall()
        return info

    def search_article_by_title(self):
        global cookies
        print "search article by title..."
        info = self.get_info_by_id()
        self.article_info = info
        article_title = self.article_info[0][1]
        article_title = article_title.replace('《','').replace('》','')
        self.searchURL = "http://weixin.sogou.com/weixin?oq=&query=" + article_title + "&_sug_type_=1&sut=0&lkt=0%2C0%2C0&s_from=input&ri=0&_sug_=n&type=2&sst0=1501463616231&page=1&ie=utf8&p=40040108&dp=1&w=01015002&dr=1"
        headers = {
            "User-Agent": self._agent[random.randint(0, len(self._agent) - 1)],
        }
        if (self.load_cookie == False):
            print "第一次加载从文件加载Cookie"
            jar = cookielib.MozillaCookieJar()
            # 试着载入cookie
            try:
                jar.load('cookie.txt', ignore_discard=False, ignore_expires=False)
            except:
                pass
            r = self._session.get(self.searchURL, cookies=jar, headers=headers)

            # 将CookieJar转为字典：
            cookies = requests.utils.dict_from_cookiejar(jar)
            self.load_cookie = True
            print "全局变量Cookies为："
            print cookies
        else:
            print "之后从全局变量Cookies中加载Cookie"
            print "全局变量Cookies为："
            print cookies
            # 将字典转为CookieJar：
            jar = requests.utils.cookiejar_from_dict(cookies, cookiejar=None, overwrite=True)
            r = self._session.get(self.searchURL, cookies=jar, headers=headers)

        return r.text

    # 解析一条微信文章信息，返回字典信息
    def parse_one_wx_article(self, li):
        print "parse one article..."
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

    def updateURL(self, wx_article_info):
        article_url = wx_article_info["article"]["url"]
        article_gzh_name = wx_article_info["gzh"]["name"].encode('utf8', 'ignore')
        article_gzh_url = wx_article_info["gzh"]["article_list_url"]
        addDate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        update_sql = ("UPDATE article SET article_url='%s', article_gzh_name='%s', article_gzh_url='%s', add_time='%s' "
                      "WHERE article_id=%d" % (
                          article_url, article_gzh_name, article_gzh_url, addDate, self.id))

        cursor.execute(update_sql)
        db.commit()

    def run(self):
        sougou_search_html = self.search_article_by_title()
        page = etree.HTML(sougou_search_html)
        lis = page.xpath('//ul[@class="news-list"]/li')

        if ('ç¨æ·æ¨å¥½ï¼æ¨çè®¿é®è¿äºé¢ç¹ï¼ä¸ºç¡®è®¤æ¬æ¬¡è®¿é®ä¸ºæ­£å¸¸ç¨æ·è¡ä¸ºï¼éè¦æ¨åå©éªè¯ã' in sougou_search_html):
            print("发现页面被封")
            # 设置被封的URL
            self._vcode_url = self.searchURL
            self.log("请求网址：" + self._vcode_url + "时被封，开始尝试解封")
            # 运行解封函数
            self._jiefeng()
            self.log("解封程序运行完成，再一次访问页面")
            # 重新访问页面
            sougou_search_html = self.search_article_by_title()
            page = etree.HTML(sougou_search_html)
            lis = page.xpath('//ul[@class="news-list"]/li')

        print self.article_info[0][1]
        print self.article_info[0][2]

        for li in lis:
            wx_article_info = self.parse_one_wx_article(li)
            #print wx_article_info

            article_title = wx_article_info["article"]["title"].encode('utf8', 'ignore')
            article_time = wx_article_info["article"]["time"]

            print article_title
            print article_time

            #有可能文章的标题有细小改变不能匹配，比如多加了一些书名号或者空格等等，所以去掉空格之后再匹配或直接匹配时间戳
            if(article_title.replace(' ','') == self.article_info[0][1].replace(' ','') or article_time == int(self.article_info[0][2])):
                print "find the same article, updating..."
                self.updateURL(wx_article_info)
                self.update_success = True
                break

        #如果因为某种原因更新不成功（搜索到其他公众号转发的该文章，原文章被删除），则选择相似的第一篇文章更新进来
        #if self.update_success == False:
        #    wx_article_info = self.parse_one_wx_article(lis[0])
        #    self.updateURL(wx_article_info)
        #    self.update_success = True

        return self.update_success



# main
if __name__ == '__main__':
    print('connect to mysql server...')
    db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
    print('connect mysql success!')
    cursor = db.cursor()
    if update_URL_by_id(86).run() == True:
        print 'update success...'
    else:
        print 'update failed, please try again...'