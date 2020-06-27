# -*- coding: utf-8 -*-
import requests
import time
from fake_useragent import UserAgent
from lxml import etree
headers = {
    'User-Agent': str(UserAgent().random),
    'Host': 'search.51job.com',
    'Pragma': 'no-cache',
    'Upgrade-Insecure-Requests': '1',

}
