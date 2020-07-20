# coding=utf-8
import os
import time
from datetime import datetime, timedelta
import argparse
import logging
import sys

logging.basicConfig(stream=sys.stdout)
logger = logging.getLogger()


def pick_back_file_name(d: str, origin_file_name: str, bak_extension: str):
    index = 0
    while True:
        index += 1
        beijing_time = timedelta(hours=8) + datetime.utcnow()
        beijing_date = beijing_time.strftime('%Y-%m-%d')
        p = os.path.join(d, f'{origin_file_name}.{beijing_date}.{index}.bak')
        if not os.path.exists(p):
            return p


def clean_work(d: str, max_size: int, log_extension: str, bak_extension: str):
    f = [x for x in os.listdir(d)]
    f = [x for x in f if os.path.isfile(os.path.join(d, x))]
    logs = [x for x in f if x.lower().endswith(log_extension)]
    baks = [x for x in f if x.lower().endswith(bak_extension)]
    month_ago = datetime.utcnow() + timedelta(days=-30)
    expired_time = month_ago.timestamp()
    expired_baks = [x for x in baks if os.stat(os.path.join(d, x)).st_mtime < expired_time]
    # 删除旧备份
    for m in expired_baks:
        bak_file = os.path.join(d, m)
        os.remove(bak_file)
        print('删除', bak_file)
    # 迁移日志文件
    for log_ in logs:
        log_file = os.path.join(d, log_)
        if os.path.getsize(log_file) > max_size:
            bak_file_path = pick_back_file_name(d, log_, bak_extension)
            with open(log_file, mode='r+') as lf:
                # 把文件内容复制一份
                with open(bak_file_path, mode='w') as b:
                    b.writelines(lf.readlines())
                    print('备份', bak_file_path)
                # 清空文件内容
                lf.seek(0)
                lf.truncate()
                print('清空', log_file)

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, action='append')
    parser.add_argument('--log_extension', type=str, default='.log')
    parser.add_argument('--bak_extension', type=str, default='.bak')
    parser.add_argument('--max_size', type=int, default=1024 * 1024 * 5)

    args = parser.parse_args()
    print(args)

    command_path = args.path if args.path else []
    path_list = [x for x in command_path if os.path.exists(x)]
    print('日志目录：', path_list)

    while True:
        utc_now = datetime.utcnow()
        for path_to_clean in path_list:
            try:
                print(utc_now, '清理', path_to_clean)
                clean_work(path_to_clean,
                           max_size=args.max_size,
                           log_extension=args.log_extension.lower(),
                           bak_extension=args.bak_extension.lower())
            except Exception as e:
                print(e)
        print(utc_now, '等待中。。。')
        time.sleep(10)
