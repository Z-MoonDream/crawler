# 需求：
# 前5页的每一家企业的详情数据进行爬取
# 难点用不到数据解析(BeautifulSoup)都是动态加载出来的也就是ajax包

import requests



headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.50'
}

# data字典中可以加入表单数据模拟提交表单666
for i in range(1,6):
    data={
        'method': 'getXkzsList',
        'page':str(i)

    }
    url = "http://125.35.6.84:81/xk/itownet/portalAction.do"
    response = requests.post(url=url,data=data,headers=headers)

    for index in response.json()['list']:
        id = index['ID']
        url ='http://125.35.6.84:81/xk/itownet/portalAction.do'

        data = {
            'method': 'getXkzsById',
            'id': id,
        }
        response = requests.post(url=url,data=data,headers=headers).json()
        print('企业名称',response['epsName'])
        print('许可证编号',response['productSn'])
        print('许可项目',response['certStr'])
        print('企业住址',response['epsAddress'])
        print('生产地址',response['epsProductAddress'])
        print('社会信用代码',response['businessLicenseNumber'])
        print('法定代表人',response['businessPerson'])
        print('企业负责人',response['legalPerson'])
        print('质量负责人',response['qualityPerson'])
        print('发证机关',response['qfManagerName'])
        print('签发人',response['xkName'])
        print('日常监督管理机构',response['rcManagerDepartName'])
        print('日常监督管理人员',response['rcManagerUser'])
        print('有效期至',response['xkDate'])
        print('发证日期',response['xkDateStr'])
        print('状态','正常')
        print('举报电话','12331')
        print('\n')
        print(response['epsName'],'爬取完毕')


