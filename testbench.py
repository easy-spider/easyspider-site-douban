#!/usr/bin/env python
from scrapy.cmdline import execute
import time
import datetime
import os

"""
    spidername: 选择使用的爬虫，可选项有 'moviesearch'、‘booksearch’、‘musicsearch’
    keyword: 搜索的关键字, eg '欧美'、'诺兰'、'陈奕迅'等
    pages： 爬取页数，范围需要在[1,100(建议)]之间
"""

test_list = [
    {"spidername": "moviesearch", "keyword": "欧美", "pages": 1},
    {"spidername": "booksearch", "keyword": "中国", "pages": 1},
    {"spidername": "musicsearch", "keyword": "美国", "pages": 1},
]

if __name__ == "__main__":
    testbench_start_time = time.time()
    testbench_start_date = datetime.datetime.now()
    dir_name = (
        f"{testbench_start_date.year}{testbench_start_date.month}{testbench_start_date.day}"
        f"{testbench_start_date.hour}{testbench_start_date.minute}{testbench_start_date.second}"
    )
    os.system(f"mkdir -p log/{dir_name}")
    for test in test_list:
        start_date = datetime.datetime.now()
        file_name = (
            f"log/{dir_name}/report_{test['spidername']}_{test['keyword']}_{test['pages']}"
            f"_{start_date.hour}{start_date.minute}{start_date.second}.log"
        )

        start_time = time.time()
        last_finish_time = time.time()
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(
                f"Test start at {start_date.hour}:{start_date.minute}:{start_date.second}\n"
            )
        for cur_page in range(1, test["pages"] + 1):
            os.system(
                f"python3 ./run.py {test['spidername']} {test['keyword']} {cur_page}"
            )
            cur_time = time.time()
            cur_date = datetime.datetime.now()
            with open(file_name, "a", encoding="utf-8") as f:
                f.write(
                    f"cur_page {cur_page}, "
                    f"finish time {cur_date.hour}:{cur_date.minute}:{cur_date.second}, "
                    f"spent time {(cur_time - last_finish_time) / 60}\n"
                )
            last_finish_time = time.time()

        end_time = time.time()
        test["time"] = (end_time - start_time) / 60
        with open(file_name, "a", encoding="utf-8") as f:
            f.write(f"Testbench Finished, it takes {test['time']} mins")

    testbench_end_time = time.time()
    print(
        f"Testbench Finished, it takes {(testbench_end_time - testbench_start_time) / 60} mins"
    )
    with open(f"log/{dir_name}/overall.log", "a", encoding="utf-8") as f:
        f.write(f"Finish total {len(test_list)} tests\n")
        for i, test in enumerate(test_list):
            f.write(
                f"Test {i + 1} spider {test['spidername']} keyword {test['keyword']} pages {test['pages']}, "
                f"takes {test['time']} mins\n"
            )
        f.write(
            f"Testbench takes {(testbench_end_time - testbench_start_time) / 60} mins"
        )
