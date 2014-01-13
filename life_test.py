#!/usr/bin/python
# -*- coding:utf-8 -*-

import computer

def test_computer_basics():
    c = computer.LifeComputer(3,4)
    assert c.width == 3
    assert c.height == 4
    assert c.array.shape == (5, 6)

    c.set_size(width=5)
    assert c.width == 5
    assert c.array.shape == (7, 6)

    c.set_size(height=1)
    assert c.height == 1
    assert c.array.shape == (7, 3)
