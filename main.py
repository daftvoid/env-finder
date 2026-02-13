import os
from dotenv import load_dotenv

from github import get_files

load_dotenv()

from math import ceil
import time
import requests
import json

files = get_files("daftvoid/env-finder")
print(files)