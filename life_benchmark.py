#!/usr/bin/python
# -*- coding:utf-8 -*-

import computer
import time

class Timer:
    def __enter__(self):
        self.start_time = time.clock()

    def __exit__(self, *args):
        self.runtime = time.clock() - self.start_time

c = computer.LifeComputer(20, 20)
c.fill_random()
t = Timer()

for i in range(50):
    with t:
        c.compute(10)
    print t.runtime

