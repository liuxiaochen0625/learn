#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'地区编码'

import requests
from bs4 import BeautifulSoup
import re
import pymysql


class Example:
    domain = "http://www.mca.gov.cn"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    }
    reg = "window.location.href=\"(.*?)\";"
    db = pymysql.connect(host='127.0.0.1', user='root', passwd='mysql', db='xxl-job', port=3306)
    cursor = db.cursor()
    sql = "INSERT INTO tb_city_code_3(year,province_name,province_code,city_name,city_code,county_name,county_code) VALUES (%s,%s,%s,%s,%s,%s,%s)"

    def crawel(self, url, name):
        response = requests.get(url, headers=self.headers)
        raw_text = response.text.replace("&nbsp;", "")
        soup = BeautifulSoup(raw_text, "html.parser")

        zoom = soup.select("#zoom a")

        if zoom is not None and len(zoom) > 0:
            url = zoom[0]['href']
            response = requests.get(url, headers=self.headers)
            raw_text = response.text.replace("&nbsp;", "")
            soup = BeautifulSoup(raw_text, "html.parser")
        pattern = re.compile(r'window.location.href=\"(.*?)\";', re.I)
        match = pattern.search(raw_text)
        if match is not None:
            url = match.group(1)
            response = requests.get(url, headers=self.headers)
            raw_text = response.text.replace("&nbsp;", "")
            soup = BeautifulSoup(raw_text, "html.parser")

        trs = soup.select("tr")
        province = {}
        city = {}
        data = []
        for i in range(3, len(trs)):
            tds = trs[i].select("td")
            if (tds is None) or len(tds) < 3:
                continue
            code = tds[1].string
            country_name = tds[2].text
            if (code is None) or (country_name is None) or (code == '') or (country_name == ''):
                continue
            code = code.replace("\n", "").replace(" ", "")
            country_name = country_name.replace("\n", "").replace(" ", "")
            if code[0:1] not in ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'):
                continue
            if code.endswith("0000"):
                province[code] = country_name
            if code.endswith("00") and not code.endswith("0000"):
                city[code] = country_name
            province_code = code[0:2] + "0000"
            province_name = province.get(province_code)
            city_code = code[0:4] + "00"
            city_name = city.get(city_code)
            if city_name is None:
                city_code = province_code
                city_name = province_name
            data.append(
                (name, province_name, province_code, city_name, city_code, country_name,
                 code))
        print(data)
        self.cursor.executemany(self.sql, data)
        self.db.commit()

    def get_url(self, url):
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, "lxml")
        trs = soup.select(".artitlelist")
        for tr in trs:
            url = self.domain + tr['href']
            name = tr['title'][0:4]
            self.crawel(url, name)


if __name__ == "__main__":
    urls = ['http://www.mca.gov.cn/article/sj/xzqh//1980/?', 'http://www.mca.gov.cn/article/sj/xzqh//1980/?2',
            'http://www.mca.gov.cn/article/sj/xzqh//1980/?3']
    Example().get_url(urls[2])
