#!/bin/bash
scrapyd-deploy -p douban -v 1.0 --build-egg=easyspider_douban.egg
rm -rf release/
mkdir -p release/
rm -rf build
mv *.egg *.egg-info setup.py -t release/