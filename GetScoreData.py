"""
目的：爬取某教育网站高考山东理工大学2021、2022、2023年各专业录取最低分、
        最低录取名次和选科要求数据分析
"""
import requests
from bs4 import BeautifulSoup
import csv

file_ojb=open('ScoreData.csv','w',newline='',encoding='utf-8-sig')
csv_obj=csv.writer(file_ojb)
csv_obj.writerow(['年份','专业名','最低录取分','平均录取分','最高录取分','排名'])

url = 'https://www.dxsbb.com/news/33038.html'
hd = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
res = requests.get(url, headers=hd)
res.encoding = 'utf-8'
soup =  BeautifulSoup(res.text, 'html.parser')
div = soup.find_all('div', attrs={'class': 'tablebox'})
for k in range (0,3):
    Year = 2023 - k
    # print("{}年山东理工大学各专业录取信息".format(z)+'-'*100)
    tr = div[k].find_all('tr')
    for i in tr[1:]:
        td = i.find_all('td')
        majortype = td[3].text
        if majortype != '普通类':
            continue
        majorName = td[4].text
        minSocer = td[5].text
        avgSocer = td[6].text
        maxSocer = td[7].text
        benline = td[8].text
        ranking = td[9].text
        ranking = ranking.replace('--', '暂无排名')
        print(majortype,majorName)
        csv_obj.writerow([Year, majorName, minSocer, avgSocer, maxSocer,ranking])


print('Get Success!')