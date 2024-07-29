from UniDec import unidec
import matplotlib.pyplot as plt
import numpy as np







mass_range = [11500.0, 13000.0]
# load text file
eng = unidec.UniDec()
eng.open_file("mean_data.txt")

eng.process_data()
eng.run_unidec()
eng.pick_peaks()
eng.process_mass_data()

mass_dist_data = np.loadtxt("mean_data_unidecfiles/mean_data_mass.txt")

print(mass_dist_data.shape)
