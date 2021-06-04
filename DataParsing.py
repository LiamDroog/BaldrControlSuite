import multiprocessing
from CameraDaemon import pollFiles
import os


class DataDaemon:
    def __init__(self, watchdir, movedir, interval):
        cwd = os.path.dirname(__file__)
        os.chdir(cwd)
        self.p = multiprocessing.Process(target=pollFiles, args=(watchdir, movedir, interval))

    def main(self):
        self.p.start()

    def kill(self):
        self.p.terminate()
        self.p.join()


