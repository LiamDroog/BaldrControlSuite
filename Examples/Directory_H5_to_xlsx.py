"""
##################################################
Writes all hdf5 files in directory to xlsx files.
Will be slow as heck even with multiprocessing.
You have been warned.
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
import multiprocessing


def converter(dirs, hDir):
    outputdir = os.path.join(hDir, 'xlsx output')
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for file in range(len(dirs)):
        st = time.time()
        filename = dirs[file].split('.')[0]
        with h5py.File(os.path.join(hDir, dirs[file]), 'r') as h5f:
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
        print('Saved ' + filename + '.xlsx in %2.2f seconds. Completion: %2.2f percent ' % ((time.time() - st),
                                                                                            ((file + 1) / len(
                                                                                                dirs)) * 100))


if __name__ == '__main__':
    totalst = time.time()

    # Inputs
    # ######################################
    # Full path to target directory
    hDir = 'C:/Users/Liam/PycharmProjects/BaldrControlHub py3.8/DataFiles/Jun-07-2021'
    # number of processes to run
    chunk_num = 5
    # ######################################


    # get list of all h5 files within dir:
    dirs = [file for file in os.listdir(hDir) if os.path.isfile(os.path.join(hDir, file))]

    if dirs == []:
        print('No hdf5 files found.')
    else:
        for i in range(len(dirs)):
            if dirs[i][-5:] != '.hdf5':
                dirs.pop(i)

    chunk_len = int(len(dirs) / chunk_num)
    chunked_data = [dirs[x:x + chunk_len] for x in range(0, len(dirs), chunk_len)]
    print('#' * 80)
    convertstr = 'Converting ' + str(len(dirs)) + ' hdf5 files to .xlxs files'
    print(convertstr.center(80))
    print(str('Utilizing ' + str(chunk_num) + ' processes.').center(80))
    print('Please be patient. This will take some time...'.center(80))
    print('#' * 80)

    processes = []
    for i in range(len(chunked_data)):
        p = multiprocessing.Process(target=converter, args=(chunked_data[i], hDir,))
        processes.append(p)
        p.start()
        time.sleep(0.5)
    for i in processes:
        i.join()

    print('#' * 80)
    print('All files converted. Time taken: %4.2f seconds' % (time.time() - totalst))
    print('#' * 80)
