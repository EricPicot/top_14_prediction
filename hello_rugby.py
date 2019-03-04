#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar  3 20:23:07 2019

@author: ericpicot
"""

import pandas as pd
import numpy as np

print("hello world")

a =[x**2 for x in range(5)]
path = "/Users/ericpicot/Documents/top_14_prediction"
a = pd.DataFrame(a)
a.to_csv(path+"/crone_test.csv", mode ="a")
print("to_csv = done")
