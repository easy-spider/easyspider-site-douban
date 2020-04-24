#!/bin/bash
scrapyd-deploy -p douban -v 1.0 --build-egg=easyspider_douban.egg
rm -rf release/
mkdir -p release/
mv *.egg build *.egg-info setup.py -t release/
