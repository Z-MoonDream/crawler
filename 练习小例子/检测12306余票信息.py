import requests

headers = {
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36 Edg/81.0.416.50'
}

session = requests.Session()
main_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
session.get(main_url,headers=headers)


url ='https://kyfw.12306.cn/otn/leftTicket/query'


city = {
    '北京北':'VAP',
    '北京':'BJP',
    '重庆':'CQW'
}
t = input('enter a time:(yyyy-mm-dd):')
start = city[input('enter a start city :')]
end = city[input('enter a end city:')]
params={
    'leftTicketDTO.train_date':t,
    'leftTicketDTO.from_station':  start,
    'leftTicketDTO.to_station': end,
    'purpose_codes': 'ADULT',
}
json_data_list = session.get(url=url,headers=headers,params=params).json()['data']['result']

# json_data_list = session.get(url=url,headers=headers,params=params).text
print(json_data_list)

