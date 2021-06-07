import asyncio
import os
import time


#
# today = date.today()
# date = today.strftime("%b-%d-%Y")
# filepath = 'TempDataFiles/' + str(date) + '/' + str(19129388) + '/'
# targetFilePath = 'TempDataFiles/' + str(date) + '/' + str(19129388) + '/' + 'Target/'


def pollFiles(watchdir, movedir, interval):
    """
    polls a directory at a given interval to see if files exist. If they do, moves them to a queue for hdf5 storage

    :param watchdir: Directory to watch
    :param movedir: Directoy to move
    :param interval: Interval in seconds
    :return:
    """
    asyncio.run(do_stuff_periodically(interval, checkDir, watchdir, movedir))


async def checkDir(watch, target):
    """
    Moves files if they exist in a directoy
    :param watch: Directory to watch
    :param target: Directory to move to
    :return:
    """
    str = '\033[92m' + time.asctime() + ': Checking ' + watch + '\033[0m\n'
    files = [file for file in os.listdir(watch)
             if os.path.isfile(os.path.join(watch, file))]
    if not files:
        str += '\033[92m' + ' ' * 4 + 'No files found.' + '\033[0m\n'
    else:
        str += '\033[93m' + ' ' * 4 + 'Files found. Moving...'+ '\033[0m\n'
        for i in files:
            os.rename(watch + i, target + i)
    print(str)


async def do_stuff_periodically(interval, periodic_function, watch, target):
    """
    periodically does stuff
    :param interval: Time between function calls
    :param periodic_function: Function to call
    :param watch: Watch directory
    :param target: Target directory
    :return:
    """
    while True:
        await asyncio.gather(
            asyncio.sleep(interval),
            periodic_function(watch, target),
        )
