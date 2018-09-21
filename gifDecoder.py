#coding=utf-8
import io
import os
import sys
import json
import zipfile
from PIL import Image
import Tkinter as tk
import urllib2

inputPath = os.path.expanduser('~') + '/Desktop/gifInput/'
outputPath = os.path.expanduser('~') + '/Desktop/gifZips'

def getInput(path):
    print  inputPath + path
    return inputPath + path

def getOutput(path):
    print  outputPath + '/' + path
    return outputPath + '/' + path

# 压缩指定目录下的所有文件
def zip_ya(startdir, file_news):

    z = zipfile.ZipFile(file_news,'w',zipfile.ZIP_DEFLATED) #参数一：文件夹名
    for dirpath, dirnames, filenames in os.walk(startdir):
        fpath = dirpath.replace(startdir,'') #这一句很重要，不replace的话，就从根目录开始复制
        fpath = fpath and fpath + os.sep or ''#这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
        for filename in filenames:
            z.write(os.path.join(dirpath, filename),fpath+filename)
        print ('压缩成功')
    z.close()


# 分析gif图片
def analyseImage(path):
 
    im = Image.open(path)
    results = {
        'size': im.size,
        'mode': 'full',
    }
    try:
        while True:
            if im.tile:
                tile = im.tile[0]
                update_region = tile[1]
                update_region_dimensions = update_region[2:]
                if update_region_dimensions != im.size:
                    results['mode'] = 'partial'
                    break
            im.seek(im.tell() + 1)
    except EOFError:
        pass
    return results


#解析gif图片
def processImage(path, dir):
   
    mode = analyseImage(path)['mode']
    
    im = Image.open(path)
    
    i = 1
    p = im.getpalette()
    last_frame = im.convert('RGBA')
    
    try:
        while True:
           
            if not im.getpalette():
                im.putpalette(p)
        
            new_frame = Image.new('RGBA', im.size)
          
            if mode == 'partial':
                new_frame.paste(last_frame)
    
            new_frame.paste(im, (0,0), im.convert('RGBA'))
            new_frame.save('%s/%d.png' % (dir, i), 'PNG')

            i += 1
            
            last_frame = new_frame
            im.seek(im.tell() + 1)
    except EOFError:
        pass


#读取gif图片
def readGif(src, gifNumber):

    gifName = gifNumber + 'origin.gif'
    
    response = urllib2.urlopen(src)
    cat_img = response.read()
    with open(getOutput(gifName), 'wb') as f:
        f.write(cat_img)

    pngDir = getOutput(gifNumber)
    #创建存放每帧图片的文件夹
    os.mkdir(pngDir)

    processImage(getOutput(gifName), pngDir)

    startdir = pngDir  #要压缩的文件夹路径
    file_news = startdir + '.zip' # 压缩后文件夹的名字
    zip_ya(startdir, file_news)


#读取json文件中gif的地址
def loadJson(filename):
    f = io.open(filename, encoding='utf-8')
    setting = json.load(f)
    arr = []
    for key in setting:
        url = str(setting[key]['Address'])
        url.strip('\n')
        
        if(url.endswith('gif')):
            item = {'id': str(key), 'url': url}
            arr.append(item);

    return arr


# 搜索当前文件夹中的json文件
def searchJson(file_dir):
    jsonFiles = []
    
    for root, dirs, files in os.walk(file_dir):
        print(root) #当前目录路径
        print(dirs) #当前路径下所有子目录
        print(files) #当前路径下所有非目录子文件
        for file in files:
            if(str(file).endswith('json')):
                jsonFiles.append(getInput(str(file)));

    return jsonFiles


#检查输出文件夹
def checkOutput():
    if os.path.exists(outputPath):
        del_dir_tree(outputPath)
    os.makedirs(outputPath)


#删除输出文件夹
def del_dir_tree(path):
    ''' 递归删除目录及其子目录,　子文件'''
    if os.path.isfile(path):
        os.remove(path)
       
    elif os.path.isdir(path):
        for item in os.listdir(path):
            itempath = os.path.join(path, item)
            del_dir_tree(itempath)
        os.rmdir(path) # 删除空目录


# 主函数
def start():
    jsonFiles = searchJson(inputPath)
    checkOutput()
    print jsonFiles
    for jsonFile in jsonFiles:
        gifs = loadJson(jsonFile)
        for i in range(0, len(gifs)):
            #print i, gifs[i]
            readGif(gifs[i]['url'], gifs[i]['id'])

start()
