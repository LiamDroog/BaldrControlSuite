import os
from datetime import date
import numpy as np
import asyncio, time
import HDF5Methods as h5m


def pollFiles(watchdir, movedir):
    asyncio.run(do_stuff_periodically(checkDir, watchdir, movedir))


async def checkDir(watch, target):
    str = '\033[94m' + time.asctime() + ': Checking ' + watch + '\033[0m\n'
    npyfiles = [file for file in os.listdir(watch)
                if os.path.isfile(os.path.join(watch, file))]

    h5files = [file for file in os.listdir(target)
               if os.path.isfile(os.path.join(target, file))]

    if len(h5files) > len(npyfiles):
        str += '\033[94m' + ' ' * 4 + 'No files to write found.' + '\033[0m\n'
        print(str)
        return
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
    while True:
        await asyncio.gather(
            asyncio.sleep(1),
            periodic_function(watch, target),
        )


async def writedata(npy, hdf5, npydir, hdfdir):
    data = np.load(os.path.join(npydir, npy), allow_pickle=True).item()
    datasetname = data['diagnosticname']
    h5m.createDataset(filename=os.path.join(hdfdir, hdf5), name=datasetname, data=data['data'])
    h5m.setMetadataFromDict(filename=os.path.join(hdfdir, hdf5), path=datasetname, dict=data['metadata'])
