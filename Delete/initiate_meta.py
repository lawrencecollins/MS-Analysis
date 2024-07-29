import unidec
import matplotlib.pyplot as plt
import numpy as np
import os
from unidec.metaunidec.mudeng import MetaUniDec


class Meta2(MetaUniDec):
    def __init__(self):
        Meta2.__init__(self)
        self.filename = None
        self.dirname = None
        self.path = None
        self.chromdat = None
        self.tic = None
        self.ticdat = None
        self.spectra = None
        self.massdat = None
        self.mzdata = None
        self.procdata = None
        self.config.default_high_res()
        self.unidec_eng = unidec.UniDec()

if __name__ == "__main__":
    test_dir = "D:\\WORK\\Meta2_test_dir"
    input_file = "D:\WORK\Meta2_test_dir\\Meta2_input_file.xlsx"