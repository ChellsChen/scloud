#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-09-23 17:48:25
# @Author  : 陈小雪 (shell_chen@yeah.net)
# @Version : $Id$

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Date       : 2015-06-09 15:21:13
# Author     : 陈小雪
# E-mail     : shell_chen@yeah.net
# Version    : 1.0.1
"""
发布流程:
1. 运行pulish.py脚本,
    参数 -f:filename
         -tags:tags
         -title:tile
         -p: dirpath
         -c: fileclass

2. 初始化待发布文章信息:
    id : 文章id
    title :文章标题
    tags : 文章标签
    class : 文章所属类别
    publishtime: 发布时间
    dirpath : 发布的路径

3. 加载json文件
    tagsfile: 标签下对应的文件
    classfile:  分类文章
    indexfile:  文章信息

4. 发布过程
    将file.md转换成file.html文件
    copy file.html文件到发布路径所在目录
    将待发布文章信息保存到各json对象中

"""

import os
import json
import logging
import time
import sys
from markdown import markdown

reload(sys)
sys.setdefaultencoding( "utf-8" )

class BlogData(object):
    def __init__(self, path):
        self.path = path

        self.indexfile = os.path.join(path, "index.json")
        self.classflie = os.path.join(path, "class.json")
        self.tagsfile = os.path.join(path, "tags.json")

        self.loads()

    def getid(self):
        return int(time.time() - 1419598800)

    def loads(self):
        self.indexs = self._loads(self.indexfile)
        self.classes = self._loads(self.classflie)
        self.tags = self._loads(self.tagsfile)

    def dumps(self):
        self._dumps(self.indexs, self.indexfile)
        self._dumps(self.classes, self.classflie)
        self._dumps(self.tags, self.tagsfile)

    def _loads(self, filename):
        tmp = None
        if os.path.isfile(filename):
            try:
                tmp = json.load(open(filename))
            except:
                tmp = None
                print "load pickle:%s error!" %filename
        return tmp

    def _dumps(self, obj, filename):
        d = json.dumps(obj)
        with open(filename,"w") as fp:
            fp.write(d)

    def add(self, Id, infos, tex):
        mtime = ctime = time.time()
        infos["ctime"] = ctime
        infos["mtime"] = mtime
        self.setinfo(Id,infos, tex)
        return str(Id)

    def update(self, Id, infos, tex):
        mtime = time.time()
        cinfo = self.indexs.get(Id)
        if cinfo is None:
            return "-1"
        infos["mtime"] = mtime

        self.setinfo(Id, infos, tex)
        return str(Id)

    def delete(self, ID):
        infos = self.indexs.get(ID)
        if not infos:
            return "-1"

        cls = infos.get("class")
        cls_index = self.classes[cls]
        if cls:
            cls_index = self.classes[cls]
            cls_index.remove(ID)

            if len(cls_index) == 0:
                del self.classes[cls]
            else:
                self.classes[cls] = cls_index

        del self.indexs[ID]

        self.dumps()

        return str(ID)

    def setinfo(self, Id, infos, tex):
        dirpath = os.path.join(self.path, str(Id))

        if not self.write(Id, tex):
            return

        self.tagsadd(infos.get("tags"))
        self.clsadd(Id, infos.get("class"))
        self.indexadd(Id,infos)
        self.dumps()

    def write(self, Id, context):
        dirpath = os.path.join(self.path, str(Id))

        if not os.path.isdir(dirpath):
            try:
                os.mkdir(dirpath)
            except:
                logging.exception("mkdir %s fail"%dirpath)
                return False

        fpdir = os.path.join(dirpath, "index.html")
        with open(fpdir, "w") as fp:
            fp.write(markdown(context))

        return True

    def tagsadd(self, tags):
        if tags is None:
            return
        if self.tags is None:
            self.tags = [ ]

        for t in tags:
            if t not in self.tags:
                self.tags.append(t)

    def clsadd(self, Id, cls):
        if cls is None:
            cls = "undefine"

        if not self.classes:
            self.classes = { }

        c = self.classes.get(cls)
        if not c:
            self.classes[cls] = [Id]
        else:
            c.append(Id)

    def indexadd(self, Id, info):
        if not self.indexs:
            self.indexs = { }
        self.indexs[Id] = info

if __name__ == "__main__":
    bd = BlogData("/home/cxx/shell/blog/store")
    bd.add('bbcc', "bbbbbbbccc",["bbb"],"bbb")













