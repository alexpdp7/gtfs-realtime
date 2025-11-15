#!/usr/bin/env python3
import argparse
import datetime
import pathlib
import time
import urllib.request


parser = argparse.ArgumentParser()
parser.add_argument("url")
parser.add_argument("output", type=pathlib.Path)
args = parser.parse_args()

previous = None
output: pathlib.Path = args.output

while True:
    time.sleep(5)
    with urllib.request.urlopen(args.url) as f:
        content = f.read()
    if content == previous:
        continue
    previous = content
    now = datetime.datetime.now()
    path = output / now.strftime("%Y") / now.strftime("%m") / now.strftime("%d") / now.isoformat(timespec="seconds")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)
