import argparse
import os
import sys
import time

FILE_NAME = './out.txt'


def is_process_running(process_id):
    """uses the in-built os command to check the status of 
       a process

    """
    try:
        os.kill(process_id, 0)
        return True
    except OSError:
        return False


def readFile(file):
    """reads in a file which contains the process id

    """
    try:
        f = open(file)
        s = f.readline()
        i = int(s.strip())
        return i
    except OSError as err:
        print("OS error: {0}".format(err))
    except ValueError:
        print("Could not convert data to an integer.")
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise


def checkProcess(process_id, time_limit):
    """Monitors the current process id (of the loader to see if it is still running)
       and prints a message if it has exceeded the time limit.

    """
    # set an arbitrary time limit
    t_end = time.time() + 60 * time_limit
    while time.time() < t_end:
        if not is_process_running(process_id):
            print("process {0} terminated".format(process_id))
            return

    # could be an external integration (slack, pager duty)
    print("process {0} still running. Kill?".format(process_id))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("--time", "-t", type=int, required=True)
    args = parser.parse_args()

    file_name = FILE_NAME
    time_limit = args.time

    process_id = readFile(file_name)

    if id:
        checkProcess(process_id, time_limit)
