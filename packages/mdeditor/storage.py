#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2015-09-23 17:55:59
# @Author  : 陈小雪 (shell_chen@yeah.net)
# @Version : $Id$

import os
import json
import time
from shutil import rmtree

class STORAGE(object):
    def __init__(self, path):
        self.path = path

        self.config_path = os.path.join(self.path, "config")

        self.load_config()

    def get(self, Id):
        tex_path = os.path.join(self.path, str(Id))
        if not os.path.isdir(tex_path):
            return False

        md_path = os.path.join(tex_path, "index.md")
        with open(md_path, "r") as md_fp:
            md_tex = md_fp.read()

        return md_tex

    def add(self, Id, title, tags, tex):
        Id_path = os.path.join(self.path, str(Id))
        c_time = time.time()

        os.mkdir(Id_path, 0777)

        tpl_path = os.path.join(Id_path, "index.md")
        with open(tpl_path, "w") as fp:
            fp.write(tex)

        self.update_config(Id, title, tags, c_time)

        return True

    def update(self, Id, title, tags, md, html, post = 1):
        tex_path = os.path.join(self.path, str(Id))
        md_path = os.path.join(tex_path, "index.md")
        html_path = os.path.join(tex_path, "index.html")
        c_time = time.time()

        if not os.path.isdir(tex_path):
            return False

        with open(md_path, "w") as md_fp:
            md_fp.write(md)

        with open(html_path, "w") as html_fp:
            html_fp.write(html)

        self.update_config(Id, title, tags, c_time, post)

        return True

    def delete(self, Id):
        tex_path = os.path.join(self.path, str(Id))
        if not os.path.isdir(tex_path):
            return

        title, tags, c_time = self.index.get(str(Id))

        for tag in tags:
            stags = self.tags.get(tag)
            stags.remove(str(Id))
            self.tags[tag] = stags

        del self.index[str(Id)]
        rmtree(tex_path, True)

        self.save_config()

        return True

    def __loads(self, path):
        buf = None
        try:
            with open(path, "r") as fp:
                try:
                    buf = json.loads(fp.read())
                except:
                    pass
        except:
            buf = {}

        return buf

    def load_config(self):
        data = self.__loads(self.config_path)
        tags = data.get("tags")
        if not tags:
            tags = {}

        index = data.get("index")
        if not index:
            index = {}

        self.tags = tags
        self.index = index

    def get_config(self):
        return {"tags": self.tags, "index":self.index}

    def save_config(self):
        config = self.get_config()
        with open(self.config_path, "w") as fp:
            fp.write(json.dumps(config))

    def update_config(self, Id, title, tags, c_time, post = 1):
        self.index[str(Id)] = (title, tags, c_time, post)
        Id = str(Id)

        for t in tags:
            tag_ids = self.tags.get(t)
            if tag_ids is None:
                tag_ids = []

            if Id not in tag_ids:
                tag_ids.append(Id)

            self.tags[t] = tag_ids

        for tag, Ids in self.tags.items():
            if tag not in tags:
                if Id in Ids:
                    idindex = Ids.index(Id)
                    del Ids[idindex]

            if len(Ids) == 0:
                del self.tags[tag]

            else:
                self.tags[tag] = Ids

        self.save_config()

def get_tex_info(tex):
    lines = tex.split("\n")

    title_mark = "#"
    tags_mark = "tags:"
    title = ""
    tags = ""

    for i, line in enumerate(lines):
        if i >= 10:
            break

        line = str(line.strip())

        if not line:
            continue

        if line.startswith(title_mark):
            if title:
                continue
            hs = line.split(" ",1)
            if len(hs) < 2:
                continue
            title = hs[1].strip()

        if line.startswith(tags_mark):
            tags = line.split(":", 1)[1]
            tags = tags.split(",")
            tags = map(lambda x: x.strip(), tags)
            break

    if not title:
        title = "undefine"

    if not tags or not tags[0]:
        tags = ["undefine"]

    return (title, tags)
























