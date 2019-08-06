import requests
from lxml import html
import os

etree = html.etree
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

# 修改book选取小说
book = '/mh/wmdx'
# 修改baseDir改变根文件夹
baseDir = '/home/opengwe/Desktop/Books'
domain = 'http://www.4399dmw.com'

def getText(url):
    res = requests.get(url, headers)
    res.encoding = res.apparent_encoding
    return res.text

def getElements(text, xpath):
    html = etree.HTML(text)
    return html.xpath(xpath)

def mkDir(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def saveImage(url, path):
    res = requests.get(url)
    with open(path, 'wb') as f:
        f.write(res.content)

def savePage(novelName, chapter, images):
    folder = '{}/{}/{}/'.format(baseDir, novelName, chapter)
    mkDir(folder)
    for img in images:
        name = img.split('/')[-1]
        saveImage(img, folder+name)

if __name__ == '__main__':
    novelText = getText(domain + book)
    novelName = getElements(novelText, '//div[@class="curtain__info-tit"]/text()')[0]
    chapters = getElements(novelText, '//div[@class="listing__free-content"][1]/div[@class="listing__free-box"][1]//a')
    for chapr in chapters:
        chapterName = chapr.xpath('text()')[0]
        chapterText = getText(domain + chapr.xpath('@href')[0])
        images = getElements(chapterText, '//div[@class="m-img m-img-all"]//img/@data-src')
        savePage(novelName, chapterName, images)
        print('已完成\t%s\t%s' % (novelName, chapterName))