#!/bin/bash
scrapyd-deploy -p douban -v 1.0 --build-egg=easyspider_douban.egg
rm -rf release/easyspider_douban
mkdir -p release/easyspider_douban
mv *.egg build *.egg-info setup.py -t release/easyspider_douban
