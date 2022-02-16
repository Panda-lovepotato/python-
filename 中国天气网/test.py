#! /usr/bin/python3

from http import server
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from time import sleep
from pprint import pprint
import json


def main():
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {
            'browser':'ALL',
            'performance':'ALL',
    }
    caps['perfLoggingPrefs'] = {
        'enableNetwork' : True,
        'enablePage' : False,
        'enableTimeline' : False
    }

    
    options = webdriver.chrome.options.Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-extensions')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--disable-single-click-autofill')
    options.add_argument('--disable-autofill-keyboard-accessory-view[8]')
    options.add_argument('--disable-full-form-autofill-ios')
    options.add_experimental_option('w3c',False)
    options.add_experimental_option('perfLoggingPrefs',{
        'enableNetwork':True,
        'enablePage':False,
        })

    service = webdriver.chrome.service.Service(r'C:\Users\song\Documents\Code\pfile\中国天气网\chromedriver.exe')
    #webdriver.Chrome函数，返回driver对象
    driver = webdriver.Chrome(options=options, desired_capabilities=caps, service=service)
    driver.get('http://www.weather.com.cn/weather1d/101180101.shtml')
    sleep(5)


    perfs = driver.get_log('performance')
    # pprint(perfs)
    for row in perfs:
        log_data = row
        log_json = json.loads(log_data['message'])
        log = log_json['message']
        if log['method'] == 'Network.responseReceived' and 'http://d1.weather.com.cn/sk_2d/101180101.html?' in json.dumps(log):
            requestId = log['params']['requestId']
            try:
                response_body = driver.execute_cdp_cmd('Network.getResponseBody',{'requestId': requestId})
                pprint(response_body)

            except:
                print('response.body is null')
    driver.quit()
    return

if __name__ == '__main__':
    main()
