#!/bin/bash
SECONDS=0
echo "Starting to load records..."
sh ./sql/install.sh
python insert/loader.py --e prod
sh ./sql/post_process.sh
echo "Finished loading records."
duration=$SECONDS
echo "Records loaded in $(($duration / 60)) minutes and $(($duration % 60)) seconds."