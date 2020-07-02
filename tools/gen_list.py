import os

def ReadFileDir(path, pattern = ".json"):
    file = []
    pfile = []
    dirs = os.listdir(path)                    # 获取指定路径下的文件
    for i in dirs:                             # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == pattern:   # 筛选json文件
            file.append(i)
            pfile.append(os.path.join(path,i))
    return file, pfile

def RemoveFile(path):
    if os.path.exists(path):  # 如果文件存在
        os.remove(path)  
        #os.unlink(path)
    else:
        print('no such file:%s'%path)  # 则返回文件不存在


if __name__ == '__main__':
    # the xml file dir
    path = 'hxlx'
    _, pfile = ReadFileDir(path, '.xml')

    # save file
    path = 'image_list.txt'
    RemoveFile(path)
    f = open(path, 'a')
    for i, file in enumerate(pfile):
        line = file.split('.')[0]+'.jpg ' + file
        f.write("{}\n".format(line))
    f.close()