#! /usr/bin/python3


import re
import json
import requests
from lxml import etree
from pprint import pprint
from time import sleep


class Source_Code:
    source_code = ''
    response_encoding = 'UTF-8'
    def __init__(self, url):
        headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
        }
        response = requests.get(url=url, headers=headers)
        response.encoding = self.response_encoding
        self.source_code = response.text
    def ana_xpath(self, data_path):
        tree = etree.HTML(self.source_code)
        return tree.xpath(data_path)
    def ana_re(self, re_pattern):
        matchObj = re.search(re_pattern, self.source_code)
        return matchObj.group(1)



def main(city_path, data_path):
    with open(city_path, 'r', encoding='utf-8') as fp:
        city = json.loads(fp.read())
    for key, value in city.items():
        #创建对象，执行ana_re方法|找到observe24h_data，然后删除对象
        url = 'http://www.weather.com.cn/weather1d/' + value + '.shtml'
        weather1d = Source_Code(url)
        observe24h_data = json.loads(weather1d.ana_re('observe24h_data = (.*);'))
        del weather1d
        observe24h_data['od']['od1'] = key
        with open(data_path, 'a', encoding='utf-8') as fp:
            fp.write(json.dumps(observe24h_data, ensure_ascii=False) + '\n')
        sleep(1)
    return


if __name__ == '__main__':
    city_path = 'city.json'
    data_path = 'data.txt'
    main(city_path, data_path)