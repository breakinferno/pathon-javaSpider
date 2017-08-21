# -*- coding: utf-8 -*-
import re
import time
import MySQLdb

import sys
reload(sys)
sys.setdefaultencoding('utf8')

def select_db():
    select_sql = 'select wx_num_name,authentication,wx_num from wxnum'
    cursor.execute(select_sql)
    places = cursor.fetchall()

    for place in places:
        get = match_key(place)
        if (get != ''):
            print place[0].encode('utf8', 'ignore')+" 判定为 "+get
            update_level(place[2], get)


def match_key(place):
    name = place[0].encode('utf8', 'ignore')
    if (place[1].encode('utf8', 'ignore') == '' or place[1].encode('utf8', 'ignore') == '\n'):
        # print name+"没有认证"
        auth = ''
    else:
        auth = place[1].encode('utf8', 'ignore')
        # print name+"的认证为："+auth
    placename = ''
    # 匹配地名
    pattern1 = re.compile(r'中国人寿财险(.*?)市中心支公司')
    pattern2 = re.compile(r'中国人寿财险(.*?)市支公司')
    pattern13 = re.compile(r'中国人寿财险(.*?)中心支公司')
    pattern3 = re.compile(r'中国人寿财险(.*?)支公司')
    pattern4 = re.compile(r'中国人寿财险(.*?)分公司')
    pattern5 = re.compile(r'中国人寿(.*?)中心支公司')
    pattern6 = re.compile(r'中国人寿(.*?)市支公司')
    pattern7 = re.compile(r'中国人寿(.*?)支公司')
    pattern12 = re.compile(r'中国人寿财险(.*?)中支')
    pattern8 = re.compile(r'中国人寿(.*?)分公司')
    pattern14 = re.compile(r'中国人寿（.*?）市')
    pattern9 = re.compile(r'中国人寿(.*?)省')
    pattern10 = re.compile(r'中国人寿(.*?)电销中心')
    pattern11 = re.compile(r'中国人寿(.*?)电话销售中心')
    pattern15 = re.compile(r'中国人寿(.*?)市(.*?)支公司')
    pattern16 = re.compile(r'中国人寿保险(.*?)分公司')
    pattern17 = re.compile(r'中国人寿财产(.*?)支公司')

    pattern_auth1 = re.compile(r'中国人寿保险股份有限公司(.*?)分公司')
    pattern_auth2 = re.compile(r'中国人寿财产保险股份有限公司(.*?)支公司')
    pattern_auth3 = re.compile(r'中国人寿财产保险股份有限公司(.*?)中心支公司')
    pattern_auth4 = re.compile(r'中国人寿财产保险股份有限公司(.*?)市(.*?)支公司')

    # match = re.match(pattern1, name)
    if re.match(pattern1, name):
        placename = re.match(pattern1, name).group(1)
    elif re.match(pattern2, name):
        placename = re.match(pattern2, name).group(1)
    elif re.match(pattern13, name):
        placename = re.match(pattern13, name).group(1)
    elif re.match(pattern15, name):
        placename = re.match(pattern15, name).group(2)
    elif re.match(pattern3, name):
        placename = re.match(pattern3, name).group(1)
    elif re.match(pattern4, name):
        placename = re.match(pattern4, name).group(1)
    elif re.match(pattern5, name):
        placename = re.match(pattern5, name).group(1)
    elif re.match(pattern6, name):
        placename = re.match(pattern6, name).group(1)
    elif re.match(pattern17, name):
        placename = re.match(pattern17, name).group(1)
    elif re.match(pattern7, name):
        placename = re.match(pattern7, name).group(1)
    elif re.match(pattern12, name):
        placename = re.match(pattern12, name).group(1)
    elif re.match(pattern16, name):
        placename = re.match(pattern16, name).group(1)
    elif re.match(pattern8, name):
        placename = re.match(pattern8, name).group(1)
    elif re.match(pattern14, name):
        placename = re.match(pattern14, name).group(1)
    elif re.match(pattern9, name):
        placename = re.match(pattern9, name).group(1)
    elif re.match(pattern10, name):
        placename = re.match(pattern10, name).group(1)
    elif re.match(pattern11, name):
        placename = re.match(pattern11, name).group(1)
    elif re.match(pattern_auth1, auth):
        placename = re.match(pattern_auth1, auth).group(1)
    elif re.match(pattern_auth2, auth):
        placename = re.match(pattern_auth2, auth).group(1)
    elif re.match(pattern_auth3, auth):
        placename = re.match(pattern_auth3, auth).group(1)
    elif re.match(pattern_auth4, auth):
        placename = re.match(pattern_auth4, auth).group(1)
    else:
        #print name + " 无法提取地名"
        #if (("俱乐部" in name) or ("投资" in name) or ("团队" in name) or ("VIP" in name)):
        #    print name + "含有不规范词汇"
        return ''

    match_city_sql = "select count(CityID) from s_city where CityName LIKE concat('%','" + placename + "','%')"
    match_district_sql = "select count(DistrictID) as count from s_district where DistrictName LIKE concat('%','" + placename + "','%')"
    match_provience_sql = "select count(ProvinceID) as count from s_province where ProvinceName LIKE concat('%','" + placename + "','%')"
    cursor2.execute(match_provience_sql)
    count = cursor2.fetchall()
    if count[0][0] > 0:
        return "省级"
    else:
        cursor2.execute(match_city_sql)
        count = cursor2.fetchall()
        if count[0][0] > 0:
            return "市级"
        else:
            cursor2.execute(match_district_sql)
            count = cursor2.fetchall()
            if count[0][0] > 0:
                return "县区级"
            else:
                return ''
                # print "地名："+placename+"无法识别"
                # if(placename == ''):
                #print name + " 提取出的地名" + placename + "无法识别"

def update_level(wx_num, level):
    update_sql = "update wxnum set level='"+level+"' where wx_num='"+wx_num+"'"
    cursor.execute(update_sql)
    db.commit()

# main
if __name__ == '__main__':
    print('连接到mysql服务器...')
    db = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='wechat', charset="utf8")
    db2 = MySQLdb.connect(host='localhost', user='root', passwd='09181024', db='places', charset="utf8")
    print('连接上了!')
    cursor = db.cursor()
    cursor2 = db2.cursor()
    select_db()