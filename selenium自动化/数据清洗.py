# -*- coding: utf-8 -*-

cookie_list = [
{
    "domain": ".zhipin.com",
    "expirationDate": 1903171523,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__a",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "50115059.1587810474..1587810474.5.1.5.5",
    "id": 1
},
{
    "domain": ".zhipin.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "__c",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1587810474",
    "id": 2
},
{
    "domain": ".zhipin.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "__g",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "-",
    "id": 3
},
{
    "domain": ".zhipin.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "__l",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "l=%2Fwww.zhipin.com%2F&r=&friend_source=0&friend_source=0",
    "id": 4
},
{
    "domain": ".zhipin.com",
    "expirationDate": 1588041924,
    "hostOnly": false,
    "httpOnly": false,
    "name": "__zp_stoken__",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "81574WdK5sSLo2o8JwPF3oIKZHXWY%2FXYV5p8KJI4Ypt7bhAb13K4amXSsIany4nuVZwfe%2F0ZutjkJNfi2trLddJsRMxqUgtKaEgVoStWchIxOcw6aHQLeNKN%2FoEmDTmHE8Uw",
    "id": 5
},
{
    "domain": ".zhipin.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "1587811525",
    "id": 6
},
{
    "domain": ".zhipin.com",
    "expirationDate": 1619347524,
    "hostOnly": false,
    "httpOnly": false,
    "name": "Hm_lvt_194df3105ad7148dcf2b98a91b5e727a",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "1587349207,1587551222,1587781653,1587787385",
    "id": 7
},
{
    "domain": ".zhipin.com",
    "hostOnly": false,
    "httpOnly": false,
    "name": "lastCity",
    "path": "/",
    "sameSite": "unspecified",
    "secure": false,
    "session": true,
    "storeId": "0",
    "value": "100010000",
    "id": 8
},
{
    "domain": "www.zhipin.com",
    "expirationDate": 1901968247,
    "hostOnly": true,
    "httpOnly": false,
    "name": "_uab_collina",
    "path": "/job_detail",
    "sameSite": "unspecified",
    "secure": false,
    "session": false,
    "storeId": "0",
    "value": "158660824783282301024173",
    "id": 9
}
]

cookie = ';'.join(line['name'] + line['value']for line in cookie_list)
print(cookie)
