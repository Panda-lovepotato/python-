import requests
import json

def main(data_path, sthjt_json):
    url = 'https://page.henan.gov.cn/api/stt-weather'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
    }
    #发送请求
    response = requests.post(url=url, headers=headers)
    response.encoding = 'utf-8'
    dic = eval(response.text)
    # print(dic)
    #判断网站数据是否更新
    if dic['obj'][0]['updateTime'] != sthjt_json['updatetime']:
        #保存数据，并更新json文件
        with open(data_path, 'a', encoding='utf-8') as fp:
            fp.write(json.dumps(dic, ensure_ascii=False) + '\n')
        sthjt_json['updatetime'] = dic['obj'][0]['updateTime']
        sthjt_json['saved_data'].append(dic['obj'][0]['updateTime'])
    return


if __name__ == '__main__':
    sthjt_path = 'sthjt.json'
    data_path = 'data.txt'
    #加载sthjt.json
    with open(sthjt_path, 'r') as fp:
        sthjt_json = json.loads(fp.read())
    #主函数
    main(data_path, sthjt_json)
    #保存sthjt.json
    with open(sthjt_path, 'w') as fp:
        fp.write(json.dumps(sthjt_json))
