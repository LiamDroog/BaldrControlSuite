import multiprocessing
from HDF5Daemon import pollFiles
import os


class HDF5Writer:
    """
    Used to spawn instances of a file directory watchdog. Only one should be run at a time to ensure
    deadlocks do not occur.
    """
    def __init__(self, watchdir, targetdir):
        """

        :param watchdir: Directory to watch for new files
        :param targetdir: Directory to write files to
        """
        # spawns in wrong directory w/o this for some reason. quick fix though
        cwd = os.path.dirname(__file__)
        os.chdir(cwd)
        # spawn process
        self.p = multiprocessing.Process(target=pollFiles, args=(watchdir, targetdir))

    def start(self):
        self.p.start()

    def kill(self):
        self.p.terminate()
        self.p.join()

