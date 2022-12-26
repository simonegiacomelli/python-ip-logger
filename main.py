import datetime
import json
import os
from pathlib import Path
from time import sleep
from typing import Callable, Optional
import urllib
import urllib.request


def get_ip_httpbin() -> Optional[str]:
    try:
        res_str = urllib.request.urlopen('http://httpbin.org/ip').read().decode('utf-8')
        ip_obj = json.loads(res_str)
        ip = ip_obj['origin']
        return ip
    except:
        return None


# credits Jazz Weisman https://stackoverflow.com/a/73195814/316766
def read_n_to_last_line(file, n=1):
    """Returns the nth before last line of a file (n=1 gives last line)"""
    num_newlines = 0
    with open(file, 'rb') as f:
        try:
            f.seek(-2, os.SEEK_END)
            while num_newlines < n:
                f.seek(-2, os.SEEK_CUR)
                if f.read(1) == b'\n':
                    num_newlines += 1
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
    return last_line


def append_text(file, content):
    with open(file, 'a') as f:
        f.write(content)


def log_changed_ip(get_ip: Callable, time_provider: Callable, changes_filename: str = 'ip_changes.tsv'):
    changes_file = Path(changes_filename)
    last_ip = None
    current_ip = get_ip()
    if current_ip is None:
        return
    if changes_file.exists():
        last_line = read_n_to_last_line(changes_file)
        last_ip = last_line.split('\t')[0]
        if last_ip == current_ip:
            return
    print(f'ip changed to: {current_ip} from {last_ip}')

    now = time_provider()
    append_text(changes_file, f'{current_ip}\t{now}\n')


def main():
    execution_log = Path('execution_log.txt')

    def log(msg):
        line = f'{datetime.datetime.now().isoformat()} {msg}'
        print(line)
        append_text(execution_log, f'{line}\n')

    def check():
        return datetime.datetime.now().hour

    log('startup')
    last_check = check()
    while True:
        current_check = check()
        if last_check != current_check:
            last_check = current_check
            log('still checking')
        log_changed_ip(
            get_ip=get_ip_httpbin,
            time_provider=lambda: datetime.datetime.now().isoformat()
        )
        sleep(10)


if __name__ == '__main__':
    main()
