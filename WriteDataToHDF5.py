import multiprocessing
from HDF5Daemon import pollFiles
import os


class HDF5Writer:
    def __init__(self, watchdir, targetdir):
        cwd = os.path.dirname(__file__)
        os.chdir(cwd)
        self.p = multiprocessing.Process(target=pollFiles, args=(watchdir, targetdir))

    def start(self):
        self.p.start()

    def kill(self):
        self.p.terminate()
        self.p.join()

