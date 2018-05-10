#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:10/05/18


import hashlib


def gen_md5(s):
    if not isinstance(s, bytes):
        s = s.encode('utf-8')
    md5 = hashlib.md5(s)
    return md5.hexdigest()


if __name__ == '__main__':
    print(gen_md5('123'))
