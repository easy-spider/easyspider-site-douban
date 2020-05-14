#!/usr/bin/env python
from scrapy.cmdline import execute
import time
import os

if __name__ == "__main__":
    spidername = "moviesearch"
    keyword = "欧美"
    pages = 100
    start_time = time.time()
    for cur_page in range(1, pages + 1):
        os.system(f"python3 ./run.py {spidername} {keyword} {cur_page}")
        # execute(
        #     [
        #         "scrapy",
        #         "crawl",
        #         spidername,
        #         f"-akeyword={keyword}",
        #         f"-apage={page_index}",
        #         "-sMONGO_URL=mongodb://localhost:27017/",
        #         "-sSPIDER_NAME=moviesearch",
        #         "-sTASK_ID=001",
        #         "-sJOB_ID=002",
        #     ]
        # )
    end_time = time.time()
    print(f"Testbench Finished, it takes {(end_time-start_time)/60} mins")
