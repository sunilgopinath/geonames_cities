import os, os.path

# path joining version for other paths
DIR = '/Users/sunilgopinath/Interview/aiohttp/demos/all20'
print(len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))]))