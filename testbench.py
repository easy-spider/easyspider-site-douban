#!/usr/bin/env python
import time
import os

if __name__ == "__main__":
    spidername = "moviesearch"
    keyword = "欧美"
    pages = 10
    start_time = time.time()
    for cur_page in range(1, pages + 1):
        os.system(f"python3 ./run.py {spidername} {keyword} {cur_page}")
    end_time = time.time()
    print(f"Testbench Finished, it takes {(end_time-start_time)/60} mins")
