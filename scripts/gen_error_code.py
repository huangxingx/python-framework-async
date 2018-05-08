#!/usr/bin/env python
# -*- coding: utf-8 -*-

# @author: x.huang
# @date:18-1-18


import os
import sys
import logging

cur_dir = os.path.dirname(__file__)
src_dir = os.path.join(os.path.dirname(cur_dir), 'webar')

sys.path.insert(0, src_dir)

ErrorCodeFilePath = os.path.join(os.path.dirname(cur_dir), 'errorCode.md')
logging.basicConfig(level=logging.INFO)


def write_msg_2_file(file_path):
    head = 'code | msg |\n---- | ------ |\n'
    body = gen_error_code_msg()
    msg = head + body
    with open(file_path, 'w') as f:
        f.write(msg)


def gen_error_code_msg():
    import yxexceptions
    exception_list = list()
    for item in dir(yxexceptions):
        if item.endswith('Exception') and item != 'YXException':
            exception_obj = getattr(yxexceptions, item)
            exception_list.append(exception_obj)
    msg_list = list()
    repeat_list = list()
    error_code_list = list()
    sorted_exception_list = sorted(exception_list, key=lambda e: e.error_code)
    for exception in sorted_exception_list:
        error_code = exception.error_code
        if error_code in error_code_list:
            repeat_list.append(error_code)
        error_code_list.append(error_code)
        msg_item = '{} | {} |\n'.format(error_code, exception.error_msg)
        msg_list.append(msg_item)

    logging.info(''.join(msg_list))
    if repeat_list:
        repeat_list = [str(i) for i in repeat_list]
        logging.error('repeat_list:' + ' '.join(repeat_list))
    return ''.join(msg_list)


def main():
    error_code_path = ErrorCodeFilePath
    write_msg_2_file(error_code_path)


if __name__ == '__main__':
    main()
