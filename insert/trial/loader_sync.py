import os
import time

from psycopg2.pool import ThreadedConnectionPool

import config

tcp = ThreadedConnectionPool(1, 10, config.DSN)


def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    if os.path.exists(startdir) == False:
        logger.error('Cannot use connection')
        raise OSError(2, 'No such file or directory', startdir)

    return [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]


def process_files(files):
    for file in files:
        save_file(file)


def save_file(file):
    conn = tcp.getconn()
    cur = conn.cursor()
    with open(file, encoding='utf-8') as tsv:
        cur.copy_from(tsv, 'geoname', null='')
        conn.commit()
    tcp.putconn(conn)


if __name__ == '__main__':
    t0 = time.time()
    files = get_files(config.DIRECTORY)
    process_files(files)
    print(time.time() - t0), "seconds wall time"
