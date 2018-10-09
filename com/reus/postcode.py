#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""地区邮政编码"""

import requests
from bs4 import BeautifulSoup
import pymysql
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
}

domain = "https://www.youbianku.cn"


class PostCode:
    """获取省份列表"""
    data = []

    def get_provinces(self):
        response = requests.get("https://www.youbianku.cn/province", headers=headers)
        raw_text = response.text.replace("&nbsp;", "")
        soup = BeautifulSoup(raw_text, "html.parser")
        zoom = soup.select(".field-content")
        if zoom is not None and len(zoom) > 0:
            for a in zoom:
                nodes = a.select("a")
                if nodes is not None and len(nodes) > 0:
                    url = nodes[0].extract().get("href")
                    province = nodes[0].string
                    url = domain + url
                    self.get_citys(url, province)
        self.write_file()

    """获取城市列表"""

    def get_citys(self, url, province):
        response = requests.get(url, headers=headers)
        raw_text = response.text.replace("&nbsp;", "")
        soup = BeautifulSoup(raw_text, "html.parser")
        tables = soup.select(".views-table")
        if tables is not None and len(tables) > 0:
            table = tables[0].select("tbody tr")
            if table is not None and len(table) > 0:
                for tr in table:
                    city = tr.select(".views-field-title a")[0].string
                    url = tr.select(".views-field-title a")[0].extract().get("href")
                    url = domain + url
                    code = tr.select(".views-field-field-postcode a")[0].string
                    self.get_countrys(url, province, city, code)

    """获取县列表"""

    def get_countrys(self, url, province, city, city_code):
        response = requests.get(url, headers=headers)
        raw_text = response.text.replace("&nbsp;", "")
        soup = BeautifulSoup(raw_text, "html.parser")
        tables = soup.select(".views-table")
        if tables is not None and len(tables) > 0:
            table = tables[0].select("tr")
            if table is not None and len(table) > 0:
                for tr in table:
                    country = tr.select(".views-field-title a")
                    if country is not None and len(country) > 0:
                        country = country[0].string.replace(province, "").replace(city, "")
                        code = tr.select(".views-field-field-postcode a")
                        if code is not None and len(code) > 0:
                            code = code[0].string
                        else:
                            code = city_code
                        if country.strip() == '' or code.strip() == '':
                            country = city
                        str = province + "," + city + "," + country + "," + code + "\n"
                        self.data.append(str)
                        print("{},{},{},{}".format(province, city, country, code))

    def write_file(self):
        fo = open("post_code.txt", "a")
        fo.writelines(self.data)
        fo.close()

    def update_mysql(self):
        # 连接数据库
        db = pymysql.connect("127.0.0.1", "root", "Weidai@123", "db_crawler")
        # 使用cursor()方法获得一个游标
        cursor = db.cursor()
        sql = "update tb_city_code_2 set post_code = %s where province_name = %s and county_name = %s"
        params = []
        fo = open("post_code.txt", "r")
        line = fo.readline()
        while line:
            lists = line.split(",")
            params.append((lists[3].strip(), lists[0], lists[2]))
            line = fo.readline()
        cursor.executemany(sql, params)
        db.commit()
        cursor.close()

    def get_post_province(self):
        url = "https://bic.11185.cn/ZxptRestPub/common/queryprovinces"
        array = []
        response = requests.get(url, headers=headers)
        data = json.loads(response.text)
        items = data['data']['items']
        for item in items:
            province_name = item['provName']
            province_code = item['distCd']
            self.get_post_city(province_name, province_code, array)
        self.write_post_file(array)

    def get_post_city(self, province_name, province_code, array):
        url = "https://bic.11185.cn/ZxptRestPub/common/querycitys?proviceCode={}".format(province_code)
        response = requests.post(url, headers=headers)
        data = json.loads(response.text)
        items = data['data']['items']
        for item in items:
            city_code = item['distCd']
            city_name = item['ctyName']
            self.get_post_country(province_name, province_code, city_name, city_code, array)
        return array

    def get_post_country(self, province_name, province_code, city_name, city_code, array):
        url = "https://bic.11185.cn/ZxptRestPub/common/querycountrys?cityCode={}".format(city_code)
        response = requests.post(url, headers=headers)
        data = json.loads(response.text)
        items = data['data']['items']
        for item in items:
            temp = Item()
            country_code = item['distCd']
            country_name = item['ctyName']
            temp.country_code = country_code
            temp.country_name = country_name
            temp.city_name = city_name
            temp.city_code = city_code
            temp.province_code = province_code
            temp.province_name = province_name
            array.append(temp)
        return array

    def write_post_file(self, array):
        fp = open("code_file.txt", "a")
        for item in array:
            temp = "{},{},{},{},{},{}\n".format(item.province_name, item.province_code, item.city_name, item.city_code,
                                                item.country_name, item.country_code)
            fp.write(temp)
        fp.close()


class Item:
    province_name = ''
    province_code = ''
    city_name = ''
    city_code = ''
    country_name = ''
    country_code = ''


if __name__ == "__main__":
    PostCode().get_post_province()
