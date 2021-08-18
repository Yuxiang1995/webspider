import requests
import re
import os
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
name = "城市老人"
num = 0
num_1 = 0
num_2 = 0
x = 50      #图片数量 x*60
set_1 = set()
for i in range(int(x)):
    name_1 = r"D:\Yuxiang Zhong\dataset"
    name_2 = os.path.join(name_1,'city_oldman')
    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+name+'&pn='+str(i*20)
    res = requests.get(url,headers=headers)
    htlm_1 = res.content.decode()
    a = re.findall('"objURL":"(.*?)",',htlm_1)
    if not os.path.exists(name_2):
        os.makedirs(name_2)
    for b in a:
        try:
            b_1 = re.findall('https:(.*?)&',b)
            b_2 = ''.join(b_1)
            if b_2 not in set_1:
                num = num + 1
                img = requests.get(b, headers=headers)
                f = open(os.path.join(name_2,name+str(num)+'.jpg'),'ab')
                print('---------正在下载第'+str(num)+'张图片----------')
                f.write(img.content)
                f.close()
                set_1.add(b_2)
            elif b_2 in set_1:
                num_1 = num_1 + 1
                continue
        except Exception as e:
            print('---------第'+str(num)+'张图片无法下载----------')
            num_2 = num_2 +1
            continue
print('下载完成,总共下载{}张,成功下载:{}张,重复下载:{}张,下载失败:{}张'.format(num+num_1+num_2,num,num_1,num_2))
