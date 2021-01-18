import sqlite3
import numpy as np
from ctypes import *
import sys
import os
import baf2sql
import matplotlib.pyplot as plt

analysis_dir = "example_analysis.d"


if sys.version_info.major == 2:
    # note: assuming a european Windows here...
    analysis_dir = unicode(analysis_dir, 'cp1252')
    
baf_fn = os.path.join(analysis_dir, "analysis.baf")
sqlite_fn = baf2sql.getSQLiteCacheFilename(baf_fn)
conn = sqlite3.connect(sqlite_fn)

# --- Count spectra
q = conn.execute("SELECT COUNT(*) FROM Spectra "
                 "WHERE LineMzId NOT NULL AND ProfileMzId NOT NULL")
row = q.fetchone()
N = row[0]
print("Specified BAF has {} spectra with line and profile data.".format(N))

# --- Plot TIC and BPC over MS^1 spectra
q = conn.execute("SELECT Rt, SumIntensity, MaxIntensity FROM Spectra s "
                 "JOIN AcquisitionKeys ak ON s.AcquisitionKey = ak.Id "
                 "WHERE ak.MsLevel = 0 "
                 "ORDER BY s.ROWID")
data = [ row for row in q ]
rt = [ row[0] for row in data ]
tic = [ row[1] for row in data ]
bpc = [ row[2] for row in data ]

# plt.figure()
# plt.plot(rt, tic)
# # plt.hold(True)
# plt.plot(rt, bpc, '--')
# plt.xlabel('retention time / s')
# plt.ylabel('intensity / a.u.')
# plt.legend(['TIC', 'BPC'])
# plt.show()


# --- Plot mean spectrum within time window

np_bpc = np.array(bpc, dtype = 'float')

# get time window around base-peak intensity 
rt_range = rt[np.nanargmax(np_bpc) - 5: np.nanargmax(np_bpc) + 6]

spec_vals = {'profile_mz':[], 'profile_int':[], 'line_mz':[], 'line_int':[]}

for i in rt_range: 

    q = conn.execute("SELECT LineMzId, LineIntensityId, ProfileMzId, ProfileIntensityId FROM Spectra "
                    "WHERE ABS(Rt - {}) < 1e-8".format(i))
                
    row = q.fetchone()

    bs = baf2sql.BinaryStorage(baf_fn)

    if not all(row) == False: # check for None values

        bs = baf2sql.BinaryStorage(baf_fn)

        profile_mz = bs.readArrayDouble(row[2])
        profile_int = bs.readArrayDouble(row[3])

        spec_vals['profile_mz'].append(profile_mz)
        spec_vals['profile_int'].append(profile_int)


        line_mz = bs.readArrayDouble(row[0])
        line_int = bs.readArrayDouble(row[1])

        # stem() can take quite some time, so we reduce data for this example:

        max_points = 100;

        if len(line_mz) > max_points:
            line_mz = line_mz[0:max_points]
            line_int = line_int[0:max_points]
        
        spec_vals['line_mz'].append(line_mz)
        spec_vals['line_int'].append(line_int)


# convert resulting spectra values into arrays
np_profile_mz = np.array(spec_vals['profile_mz'])
np_profile_int = np.array(spec_vals['profile_int'])

np_line_mz = np.array(spec_vals['line_mz'])
np_line_int = np.array(spec_vals['line_int'])

# take average of arrays 
mean_profile_mz = np.average(np_profile_mz, axis = 0)
mean_profile_int = np.average(np_profile_int, axis = 0)
mean_line_mz = np.average(np_profile_mz, axis = 0)
mean_line_int = np.average(np_profile_mz, axis = 0)

plt.figure(dpi = 120)
# plot profile spectrum
plt.plot(mean_profile_mz, mean_profile_int)

# # plot line spectrum
# plt.stem(line_mz, line_int)

plt.xlabel("m/z / Th")
plt.ylabel('intensity / a.u.')
plt.title("Mean Spectrum between {}s and {}s".format(rt_range[0], rt_range[-1]))
plt.show()

# --- export spectrum 
mean_data = np.array([mean_profile_mz, mean_profile_int]).T
np.savetxt("mean_data.txt", mean_data, delimiter = "\t")
help(baf2sql)
