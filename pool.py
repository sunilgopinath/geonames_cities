import os
import concurrent.futures
import psycopg2
import csv

def save_file(filename):
    with open(filename, encoding='utf-8') as tsv:
            for row in csv.reader(tsv, delimiter='\t'):
                print("hello")


def save_to_db(con):
    cur = con.cursor()

# Create a pool of processes. By default, one is created for each CPU in your machine.
with concurrent.futures.ProcessPoolExecutor() as executor:
    # Get a list of files to process
    files = [os.path.join(dirpath, f) for dirpath, _, filenames in os.walk('../all20') for f in filenames]
    conn = psycopg2.connect("host=localhost dbname=geonames_sunil user=geonames_user")

    # Process the list of files, but split the work across the process pool to use all CPUs!
    for a in executor.map(save_file, files):
        print(a)