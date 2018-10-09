#!/usr/bin/env python3
# -*- coding:utf-8 -*-

'微信公众号爬取'

import requests
import ssl
from functools import wraps
import json


class WeiXin:
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat"
    }

    url = "https://mp.weixin.qq.com/mp/getappmsgext?f=json&mock=&uin=Mjk0NDI3MDI4Mg%253D%253D&key=0c77658d63cf1c58690b3e804078adb688eab2429879af02a782ed84855b33de324f327a026615838f9765501d0d737f600253ad64be801bed7bc41e6a75b457e93151401ed7ee624790c19cf58a2ab5&pass_ticket=Jzusnw%25252FSf4DnyHvPn%25252FAUdWgQJ%25252BEyKd8MWjED3JoFBgV7zsIWGg7C5UeREOXnwetg&wxtoken=777&devicetype=iMac%26nbsp%3BMacBookPro12%2C1%26nbsp%3BOSX%26nbsp%3BOSX%26nbsp%3B10.12.6%26nbsp%3Bbuild(16G1510)&clientversion=12031110&appmsg_token=967_%252FOCmLoVA6ndBWd%252BV2403Vy0vZBrwFvmTEjO6PDYrX3VlaRjN079XqFH89AGXg4qqZVYG289eiLyrP2LA&x5=0&f=json"
    params = "r=0.6694553794717748&__biz=MjM5OTE0NjU2MA%3D%3D&appmsg_type=9&mid=2652358043&sn=99caeae43680829119b03f12a2e033d0&idx=1&scene=0&title=%25E8%2580%2581%25E5%2585%25AC%25E8%25AF%25B4%25EF%25BC%259A%25E8%2580%2581%25E5%25A9%2586%25EF%25BC%258C%25E6%2588%2591%25E6%25B2%25A1%25E9%2592%25B1%25E4%25BA%2586...%25E4%25B8%2587%25E4%25B8%2587%25E6%25B2%25A1%25E6%2583%25B3%25E5%2588%25B0%25E5%25A5%25B3%25E4%25BA%25BA%25E5%259B%259E%25E5%25A4%258D%25E5%25A4%25AA%25E6%259C%2589%25E6%2589%258D%25E4%25BA%2586%25EF%25BC%2581&ct=1533089400&abtest_cookie=&devicetype=iMac%20MacBookPro12%2C1%20OSX%20OSX%2010.12.6%20build(16G1510)&version=12031110&is_need_ticket=0&is_need_ad=0&comment_id=394152106258694144&is_need_reward=0&both_ad=0&reward_uin_count=0&send_time=&msg_daily_idx=1&is_original=0&is_only_read=1&req_id=0110vEYgeBpxdO4k18D7035i&pass_ticket=Jzusnw%25252FSf4DnyHvPn%25252FAUdWgQJ%25252BEyKd8MWjED3JoFBgV7zsIWGg7C5UeREOXnwetg&is_temp_url=0&item_show_type=undefined&tmp_version=1"
    def sslwrap(func):
        @wraps(func)
        def bar(*args, **kw):
            kw['ssl_version'] = ssl.PROTOCOL_TLSv1
            return func(*args, **kw)

        return bar

    ssl.wrap_socket = sslwrap(ssl.wrap_socket)

    def crawel(self):
        response = requests.post(url=self.url, data=self.params, headers=self.headers, verify=False)

        data = response.json()

        print(data)
        print(data["appmsgstat"]["read_num"])

if __name__ == '__main__':
    WeiXin().crawel()
