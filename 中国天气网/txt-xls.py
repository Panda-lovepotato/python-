from pprint import pprint
import xlwt
import json
import datetime

def main(city_path, data_path, xls_path):
    #创建excel
    x1 = xlwt.Workbook(encoding='utf-8')
    #创建所有表格
    std_name_lis = ['温度', '相对湿度', '降雨量', '风力', '风向']
    sheet_lis = []
    for i in std_name_lis:
        sheet_lis.append(x1.add_sheet(i))

    #对应字典
    std_name_dic = {'温度': 'od22', '相对湿度': 'od27', '降雨量': 'od26', '风力': 'od25', '风向': 'od24'}
    #读取data.txt数据
    std_data = {}
    with open(data_path, 'r', encoding='utf-8') as fp:
        lis = fp.readlines()
    #获取城市名称
    city_name_lis =[]
    with open(city_path, 'r', encoding='utf-8') as fp:
        city_json = json.loads(fp.read())
    for i in city_json.keys():
        city_name_lis.append(i)
        std_data[i] = {}
    #格式存储数据
    for i in lis:
        dat = json.loads(i)
        updateTime = dat['od']['od0']
        updateTime = datetime.date(int(updateTime[0:4]), int(updateTime[4:6]), int(updateTime[6:8]))
        updateTime -= datetime.timedelta(days=1)
        for j in dat['od']['od2'][::-1]:
            if j['od21'] == '00':
                updateTime += datetime.timedelta(days=1)
            std_data[dat['od']['od1']][updateTime.strftime("%Y%m%d")+j['od21']] = j
    # pprint(std_data)
    #填充表格第一栏
    for i in sheet_lis:
        i.write(0, 0, 'updateTime')
        for j in range(len(city_name_lis)):
            i.write(0, j+1, city_name_lis[j])
    #获取时间列表，填充表格第一列
    date_lis = []
    for i in std_data['郑州'].keys():
        date_lis.append(i)
    for i in range(len(std_name_lis)):
        for j in range(len(date_lis)):
            sheet_lis[i].write(j+1, 0, date_lis[j])
    #填充表格数据,第i个表第j行第k列
    for i in range(len(std_name_lis)):
        for j in range(len(date_lis)):
            for k in range(len(city_name_lis)):
                try:
                    sheet_lis[i].write(j+1, k+1, std_data[city_name_lis[k]][date_lis[j]][std_name_dic[std_name_lis[i]]])
                except:
                    sheet_lis[i].write(j+1, k+1, '--')

    #保存excel
    x1.save(xls_path)
    return


if __name__ == '__main__':
    city_path = 'city.json'
    data_path = 'data.txt'
    xls_path = 'weather.xls'
    main(city_path, data_path, xls_path)
