"""
##################################################
Writes contents of single hdf5 file to an
excel xlsx file. Does not run all that quickly :/
##################################################
# Author:   Liam Droog
# Email:    droog@ualberta.ca
# Year:     2021
# Version:  V.1.0.0
##################################################
"""

import xlsxwriter as xlsx
import h5py
import time
import os


# note this does not utilize HDF5Methods as we want to access this file *once*

# Full path to target hdf5 file
# ######################################
hFile = 'C:/Users/Liam/PycharmProjects/BaldrControlHub py3.8/DataFiles/Jun-07-2021/shot0002.hdf5'
# ######################################

print('Please be patient. This will take a few seconds...')
st = time.time()
filename = hFile.split('/')[-1].split('.')[0]

outputdir = os.path.join('/'.join(hFile.split('/')[:-1]), 'xlsx output')

if not os.path.exists(outputdir):
    os.makedirs(outputdir)

with h5py.File(hFile, 'r') as h5f:
    workbook = xlsx.Workbook(os.path.join(outputdir, filename + '.xlsx'))
    e_notation = workbook.add_format({'num_format': '0.00E+00'})
    for i in h5f.keys():
        wksheet = workbook.add_worksheet(i[:31])
        row = 0
        col = 0
        # create worksheet for metadata + data
        for key, val in h5f[i].attrs.items():
            wksheet.write(row, col, key)
            wksheet.write(row, col + 1, val)
            row += 1
        datsheet = workbook.add_worksheet(i[:27] + 'data')
        writedata = h5f[i][()]
        for j in range(len(writedata)):
            for k in range(len(writedata[j])):
                m = writedata[j][k]
                datsheet.write(j, k, m, e_notation)
        workbook.close()
print('Saved ' + filename + '.xlsx')
print('Conversion took %2.2f seconds.' % (time.time() - st))
