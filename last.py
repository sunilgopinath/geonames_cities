import psycopg2
import os
import csv
from psycopg2.pool import ThreadedConnectionPool
import io
import sys
import time

DSN = "postgresql://geonames_user@localhost/geonames_sunil"
tcp = ThreadedConnectionPool(1, 10, DSN)


class IteratorFile(io.TextIOBase):
    """ given an iterator which yields strings,
    return a file like object for reading those strings """

    def __init__(self, it):
        self._it = it
        self._f = io.StringIO()

    def read(self, length=sys.maxsize):

        try:
            while self._f.tell() < length:
                self._f.write(next(self._it) + "\n")
                
        except StopIteration as e:
            # soak up StopIteration. this block is not necessary because
            # of finally, but just to be explicit
            pass

        except Exception as e:
            print("uncaught exception: {}".format(e))
            
        finally:
            self._f.seek(0)
            data = self._f.read(length)

            # save the remainder for next read
            remainder = self._f.read()
            self._f.seek(0)
            self._f.truncate(0)
            self._f.write(remainder)
            return data

    def readline(self):
        return next(self._it)

def get_files(startdir):
    """Walks through the directory where the 'single line' files are kept and
       passes that value through to the process_files function

    """
    if os.path.exists(startdir) == False:
        logger.error('Cannot use connection')
        raise OSError(2, 'No such file or directory', startdir)

    return  [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk(startdir) for f in filenames]

def process_files(files):
    for file in files:
        save_file(file)

def foo(files, con):
    page_size = 4000
    page = []
    for file in files:
        with open(file, encoding='utf-8') as tsv:
            for row in csv.reader(tsv, delimiter='\t'):
                page.append(
                    (int(row[0]), row[1], float(row[4]), float(row[5]), row[8], row[10], row[11]) 
                )
                if len(page) >= page_size:
                    save_foo_files(page, conn)
                    page = []

    save_foo_files(page, conn)

def save_foo_files(rows, conn):
    cur = conn.cursor()
    f = IteratorFile(("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(x[0], x[1], x[2], x[3], x[4],x[5],x[6]) for x in rows))
    cur.copy_from(f, 'cities',null='')
    conn.commit()
        
def save_file(file):
    conn = tcp.getconn()
    cur = conn.cursor()
    with open(file, encoding='utf-8') as tsv:
        cur.copy_from(tsv, 'geoname',null='')
        conn.commit()
    tcp.putconn(conn)

if __name__ == '__main__':
    t0 = time.time()
    files = get_files('../all20')
    conn = psycopg2.connect("host=localhost dbname=geonames_sunil user=geonames_user")
    foo(files, conn)
    conn.close()
    print(time.time() - t0), "seconds wall time"