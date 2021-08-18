import requests
import re
import os
import time
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'}
name = "children"
num = 0
num_1 = 0
num_2 = 0
x = 20      #页面数量  图片数量≈x*120
set_1 = set()
for i in range(int(x)):
    name_1 = r"D:\Yuxiang Zhong\dataset"
    name_2 = os.path.join(name_1,'chinese_children')
    url = "https://www.vcg.com/creative-image/zhongguoertong/?page=" + str(i)
    res = requests.get(url, headers=headers)
    html = res.text
    a = re.findall('\"url800\":\"(.*?)jpg', html)
    if not os.path.exists(name_2):
        os.makedirs(name_2)
    for b in a:
        try:
            imgUrl = 'http:' + b + 'jpg'
            print(imgUrl)
            if imgUrl not in set_1:
                num = num + 1
                img = requests.get(imgUrl, headers=headers)
                f = open(os.path.join(name_2, name + str(num) + '.jpg'), 'ab')
                print('---------正在下载第' + str(num) + '张图片----------')
                f.write(img.content)
                f.close()
                set_1.add(b)
            else:
                num_1 = num_1 + 1
                continue
        except Exception as e:
            print('---------第' + str(num) + '张图片无法下载----------')
            num_2 = num_2 + 1
            continue
print('下载完成,总共下载{}张,成功下载:{}张,重复下载:{}张,下载失败:{}张'.format(num + num_1 + num_2, num, num_1, num_2))