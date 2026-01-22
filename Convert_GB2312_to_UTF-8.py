#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import chardet

if getattr(sys, 'frozen', False):
    SCRIPT_DIR = os.path.dirname(sys.executable)
else:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

TARGET_EXTS = {'.c', '.h', '.cpp'}

CLR = {
    'red':    '\033[31m',
    'green':  '\033[32m',
    'yellow': '\033[33m',
    'reset':  '\033[0m'
}

stats = {'total': 0, 'converted': 0, 'skipped': 0, 'error': 0}


def rel(path: str) -> str:
    """返回 SCRIPT_DIR 下的相对路径，前面再加个 . 以示区别"""
    return './' + os.path.relpath(path, SCRIPT_DIR).replace('\\', '/')


def detect_encoding(path: str) -> str:
    with open(path, 'rb') as f:
        raw = f.read()
    if not raw:
        return ''
    return chardet.detect(raw)['encoding'] or ''


def convert_if_gb2312(path: str) -> None:
    stats['total'] += 1
    enc = detect_encoding(path)
    if enc is None or enc.lower() != 'gb2312':
        stats['skipped'] += 1
        print(f"{CLR['reset']}[跳过]{CLR['reset']} {rel(path)}  编码：{enc}")
        return

    try:
        with open(path, 'r', encoding='gb2312') as f:
            text = f.read()
        with open(path, 'w', encoding='utf-8') as f:
            f.write(text)
        stats['converted'] += 1
        print(f"{CLR['green']}[转换]{CLR['reset']} {rel(path)}  GB2312 -> UTF-8")
    except Exception as e:
        stats['error'] += 1
        print(f"{CLR['red']}[失败]{CLR['reset']} {rel(path)}  转换失败：{e}")


def main():
    for root, _, files in os.walk(SCRIPT_DIR):
        for name in files:
            if os.path.splitext(name)[1].lower() in TARGET_EXTS:
                convert_if_gb2312(os.path.join(root, name))

    print('\n========== 转换完成 ==========')
    print(f'共扫描文件：{stats["total"]}')
    print(f'已转换(GB2312->UTF-8)：{stats["converted"]}')
    print(f'跳过：{stats["skipped"]}')
    print(f'失败：{stats["error"]}')
    print('==============================')
    input('\n按回车键退出...')


if __name__ == '__main__':
    main()