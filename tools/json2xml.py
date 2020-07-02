
import os
import json
from lxml.etree import Element, SubElement, tostring, ElementTree
from xml.dom import minidom
import cv2


def ReadFileDir(path, pattern=".json"):
    file = []
    dirs = os.listdir(path)                    # 获取指定路径下的文件
    for i in dirs:                             # 循环读取路径下的文件并筛选输出
        if os.path.splitext(i)[1] == pattern:   # 筛选json文件
            file.append(i)
    return file


def ReadJson(path):
    with open(path, 'r') as load_f:
        load_dict = json.load(load_f)
    return load_dict


def subElement(root, tag, text):
    ele = SubElement(root, tag)
    if text != "":
        ele.text = text
    return ele


def saveXML(root, filename, indent="\t", newl="\n", encoding="utf-8"):
    rawText = tostring(root)
    dom = minidom.parseString(rawText)
    with open(filename, 'w') as f:
        dom.writexml(f, "", indent, newl, encoding)


def LoadXML(filename):
    dom = minidom.parse(filename)
    # 得到文档元素对象
    root = dom.documentElement
    return root


def make_xml(image_name, width, height):
    node_root = Element('annotation')

    subElement(node_root, "folder", "widerface")
    subElement(node_root, "filename", image_name)
    node_source = subElement(node_root, "source", "")
    subElement(node_source, "database", "wider face Database")
    subElement(node_source, "annotation", "PASCAL VOC2007")
    subElement(node_source, "image", "flickr")
    subElement(node_source, "flickrid", "-1")

    node_owner = subElement(node_root, "owner", "")
    subElement(node_owner, "flickrid", "yanyu")
    subElement(node_owner, "name", "yanyu")
    subElement(node_root, "segmented", "0")

    node_size = subElement(node_root, "size", "")
    subElement(node_size, "width", str(width))
    subElement(node_size, "height", str(height))
    subElement(node_size, "depth", "3")

    return node_root


def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print(path + ' 创建成功')
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print(path+' 目录已存在')
        return False


def toxml():
    # json dir
    path = '/home/q/train/Data/images/hxlx'
    # save dir
    save_xml_dir = 'hxlx'
    mkdir(save_xml_dir)
    jsonfile = ReadFileDir(path)

    for i, v in enumerate(jsonfile):
        dict = ReadJson(os.path.join(path, v))

        if 'photo_id' in dict:
            image_id = dict['photo_id']
            image_name = image_id + ".jpg"
        else:
            continue
        if 'width' in dict:
            width = dict['width']
        else:
            continue
        if 'height' in dict:
            height = dict['height']
        else:
            continue

        node_root = make_xml(image_name, width, height)

        if 'croppers' in dict:
            croppers = dict['croppers']
            for i, crop_dict in enumerate(croppers):
                print(crop_dict)

                xmin = int(crop_dict['x'] * width)
                ymin = int(crop_dict['y'] * height)
                xmax = int((crop_dict['x'] + crop_dict['width']) * width)
                ymax = int((crop_dict['y'] + crop_dict['height']) * height)

                node_object = subElement(node_root, "object", "")
                subElement(node_object, "name", crop_dict["cropper_type"])
                subElement(node_object, "pose", 'Unspecified')
                subElement(node_object, "truncated", '1')
                subElement(node_object, "difficult", '0')
                node_bndbox = subElement(node_object, "bndbox", "")
                subElement(node_bndbox, "xmin", str(xmin))
                subElement(node_bndbox, "ymin", str(ymin))
                subElement(node_bndbox, "xmax", str(xmax))
                subElement(node_bndbox, "ymax", str(ymax))
                subElement(node_object, "has_lm", '0')

            # 保存xml文件
            saveXML(node_root, os.path.join(save_xml_dir, image_id + ".xml"))

def showXml(path, xmlpath):
    '''
    path: image dir
    xmlpath: xml path
    '''
    root = LoadXML(xmlpath)
    filename = root.getElementsByTagName("filename")

    fname = remap_fname(filename[0].firstChild.data)
    image_path = os.path.join(path, fname)
    image = cv2.imread(image_path)

    objects = root.getElementsByTagName("object")
    for object in objects:
        # name 元素
        xmin = object.getElementsByTagName("xmin")[0]
        ymin = object.getElementsByTagName("ymin")[0]
        xmax = object.getElementsByTagName("xmax")[0]
        ymax = object.getElementsByTagName("ymax")[0]


        x1 = int(xmin.childNodes[0].data)
        y1 = int(ymin.childNodes[0].data)
        x2 = int(xmax.childNodes[0].data)
        y2 = int(ymax.childNodes[0].data)
        cv2.rectangle(image, (x1, y1), (x2, y2), (255,0,0), 2)
    cv2.imshow('image', image)
    cv2.waitKey(0)

def remap_fname(s):
    ret = s
    if '--' in s[:6]:
        prefix = s.split('--')[0]
        n = len(prefix)
        idx = s[n:].index(prefix) + n - 1
        ret = s[:idx] + '/' + s[(idx + 1):]
    return ret

if __name__ == "__main__":
    toxml()
    exit()

    file = ReadFileDir('hxlx', pattern=".xml")
    for i, f in enumerate(file):
        filename = 'hxlx/' + f
        print (filename)
        # filename = '/home/q/train/pytorch/libfacedetection.train/data/WIDER_FACE_rect/annotations/0--Parade_0_Parade_marchingband_1_5.xml'
        path = '/home/q/train/Data/images/hxlx'
        # path = '/home/q/train/pytorch/libfacedetection.train/data/WIDER_FACE_rect/images'
        showXml(path, filename)  
