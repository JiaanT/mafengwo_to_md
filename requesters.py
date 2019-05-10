from bs4 import BeautifulSoup
import requests
import re

base_url = 'http://www.mafengwo.cn'
suzhou_url = 'http://www.mafengwo.cn/mdd/cityroute/10207_254.html'
nanjing_url = 'http://www.mafengwo.cn/mdd/cityroute/10684_122.html'

headers = {
    "Host" : "www.mafengwo.cn",
    "Connection" : "keep-alive",
    "Pragma" : "no-cache",
    "Cache-Control" : "no-cache",
    "Accept" : "*/*",
    "X-Requested-With" : "XMLHttpRequest",
    "User-Agent" : "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.78 Safari/537.36",
    "Referer" : "http://www.mafengwo.cn/gonglve/ziyouxing/mdd_10065/",
    "Accept-Language" : "en,zh-CN;q=0.8,zh;q=0.6",
}

r = requests.get(nanjing_url, headers=headers)
soup = BeautifulSoup(r.text, features="html.parser")


places_dict = {a.get_text(): {'mfw_url': base_url + a.get('href')} for a in soup.select('.p-link')}

md_str = ''

for place, place_dict in places_dict.items():
  r = requests.get(place_dict['mfw_url'], headers=headers)
  soup = BeautifulSoup(r.text, features="html.parser")
  place_dict['time'] = soup.select('.baseinfo.clearfix .item-time .content')[0].get_text()
  place_dict['ticket'] = soup.select('body > div.container > div:nth-child(7) > div.mod.mod-detail > dl:nth-child(4) > dd')[0].get_text().replace('\n', ' ')
  place_dict['opening'] = soup.select('body > div.container > div:nth-child(7) > div.mod.mod-detail > dl:nth-child(5) > dd')[0].get_text().replace('\n', ' ')
  place_dict['image_url'] = soup.select('body > div.container > div:nth-child(7) > div.row.row-picture.row-bg > div > a > div > div.pic-big > img')[0].get('src')
  place_dict['location'] = re.search('市.*区', soup.select('body > div.container > div:nth-child(7) > div.mod.mod-location > div.mhd > p')[0].get_text())[0].replace('市', '')
  md_str += '### ' + place + '  `' + place_dict['location'] + '`\n'
  md_str += '- 游玩时间：' + place_dict['time'] + '\n'
  md_str += '- 门票：' + place_dict['ticket'] + '\n'
  md_str += '- 开放：' + place_dict['opening'] + '\n'
  md_str += '- 蚂蜂窝：[' + place + '](' + place_dict['mfw_url'] + ')\n\n'
  md_str += '![' + place + '](' + place_dict['image_url'] + ')\n\n\n\n'

print(md_str)