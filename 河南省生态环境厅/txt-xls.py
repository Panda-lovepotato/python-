import xlwt
import json

def main(data_path, xls_path):
    #创建excel
    x1 = xlwt.Workbook(encoding='utf-8')
    #创建所有表格
    std_name_lis = ['aqi', 'pm25', 'pm10', 'no2', 'so2', 'co', 'o3', 'primaryPoll', 'status']
    sheet_lis = []
    for i in std_name_lis:
        sheet_lis.append(x1.add_sheet(i, cell_overwrite_ok=True))

    #读取data.txt数据
    with open(data_path, 'r', encoding='utf-8') as fp:
        lis = fp.readlines()
    #获取城市名称
    city_name_lis =[]
    obj = json.loads(lis[0])['obj']
    for i in obj:
        city_name_lis.append(i['cityName'])
    #填充表格第一栏
    for i in sheet_lis:
        i.write(0, 0, 'updateTime')
        for j in range(len(city_name_lis)):
            i.write(0, j+1, city_name_lis[j])
    #遍历data.txt，填充表格数据,第i行第j列第k个元素
    line = 0
    for i in lis:
        obj = json.loads(i)['obj']
        line += 1
        for j in obj:
            for k in range(len(std_name_lis)):
                column = city_name_lis.index(j['cityName'])
                sheet_lis[k].write(line, 0, j['updateTime'])
                sheet_lis[k].write(line, column+1, j[std_name_lis[k]])
            
            # sheet_lis[i].write(j+1, 0, obj[0]['updateTime'])
            # for k in range(len(city_name_lis)):
            #     if obj[k]['cityName'] == city_name_lis[k]:
            #         sheet_lis[i].write(j+1, k+1, obj[k][std_name_lis[i]])
            #     else:
            #         print('error!!!')

    #保存excel
    x1.save(xls_path)
    return


if __name__ == '__main__':
    data_path = 'data.txt'
    xls_path = 'sthjt.xls'
    main(data_path, xls_path)
