import multiprocessing
from DiagnosticDaemon import pollFiles
import os


class DataDaemon:
    """
    Instatiates a watchdog to poll input directory for files and moves them to target directory. Multiple can be
    instantiated (one per diagnostic) so long as they read from different directories. I suggest directories based off
    of the diagnostic name or serial number.
    """
    def __init__(self, watchdir, movedir, interval):
        """

        :param watchdir: Directory to watch for new files
        :param targetdir: Directory to write files to
        :param interval: Time interval between calls
        """
        cwd = os.path.dirname(__file__)
        os.chdir(cwd)
        self.p = multiprocessing.Process(target=pollFiles, args=(watchdir, movedir, interval))

    def start(self):
        self.p.start()

    def kill(self):
        self.p.terminate()
        self.p.join()


