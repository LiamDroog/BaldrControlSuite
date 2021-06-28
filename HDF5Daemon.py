import asyncio
import os
import time
import numpy as np
import HDF5Methods as h5m

"""
########################################################################################################################
IMPORTANT:
            Diagnostic files that are saved MUST HAVE AN ENTRY NAMED 'diagnosticname' w/o the apostrophes
            This is to give it's associated dataset within the shot h5 file a proper name. Otherwise it's all nameless
            and it'll crash
            # TODO:
                    don't crash if nameless
"""
def pollFiles(watchdir, movedir):
    """
    runs a poll every so often to check if files exist in a directory, and moves them if they do

    :param watchdir: Directory to watch
    :param movedir: Directory to move to
    :return: None
    """
    asyncio.run(do_stuff_periodically(checkDir, watchdir, movedir))


async def checkDir(watch, target):
    """
    Checks watch directory for new files. If they exist, finds corresponding hdf5 file in the target directory
    to write file data to. based off of file numbers, and as such requires input files to be named with
    the last four characters of the filename to be the number padded with zeros to the left:
    ie, shot 1 = shotname_0001.hdf5

    :param watch: watch directory
    :param target: target directory with hdf5 files
    :return:
    """
    str = '\033[94m' + time.asctime() + ': Checking ' + watch + '\033[0m\n'
    npyfiles = [file for file in os.listdir(watch)
                if os.path.isfile(os.path.join(watch, file))]

    h5files = [file for file in os.listdir(target)
               if os.path.isfile(os.path.join(target, file))]
    # if len(h5files) > len(npyfiles):
    #     str += '\033[94m' + ' ' * 4 + 'No files to write found.' + '\033[0m\n'
    #     print(str)
    #     return
    if not npyfiles or not h5files:
        str += '\033[94m' + ' ' * 4 + 'No files found.' + '\033[0m\n'
    else:
        str += '\033[96m' + ' ' * 4 + 'Files found. Converting to hdf5...' + '\033[0m\n'

        for i in npyfiles:
            readname = i.split('.')[0]
            readfilenum = int(readname[-4:])
            for j in h5files:
                writename = j.split('.')[0]
                writefilenum = int(writename[-4:])
                if readfilenum == writefilenum:
                    await writedata(i, j, watch, target)
                    os.remove(os.path.join(watch, i))
    print(str)


async def do_stuff_periodically(periodic_function, watch, target):
    """
    periodically does stuff

    :param periodic_function: target function
    :param watch: watch directory
    :param target: target directory
    :return:
    """
    while True:
        await asyncio.gather(
            asyncio.sleep(1),
            periodic_function(watch, target),
        )


async def writedata(npy, hdf5, npydir, hdfdir):
    """
    Writes data fron npy file to hdf5 dataset

    :param npy: Target npy file
    :param hdf5: Target hdf5 file
    :param npydir: Directory of npy file
    :param hdfdir: Directory of hdf5 file
    :return:
    """
    data = np.load(os.path.join(npydir, npy), allow_pickle=True).item()
    datasetname = data['diagnosticname']
    h5m.createDataset(filename=os.path.join(hdfdir, hdf5), name=datasetname, data=data['data'])
    h5m.setMetadataFromDict(filename=os.path.join(hdfdir, hdf5), path=datasetname, dict=data['metadata'])
