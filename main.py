import os
from re import search

from dotenv import load_dotenv

from github import get_files, search_repos

load_dotenv()

from math import ceil
import time
import requests
import json


query = "stars:<2 created:2026-02-12T10:00:00Z..2026-02-12T10:10:00Z"

size = 15

count = search_repos(query)["total_count"]
print(f"Found {count} results...")

searched = []

for p in range(1, ceil(count/size) + 1):
    print(f"Loading Page {p}")
    page = search_repos(query, p, size)



    for repo in page["items"]:
        time.sleep(1)

        name = repo["full_name"]
        branch = repo.get("default_branch", "main")
        language = repo.get("language")

        if name in searched:
            print("Already searched")
            continue

        searched.append(name)

        print(f"Scraping {name}...  ", end="")

        tmp = True
        while tmp:
            try:
                files = get_files(name)
            except:
                print("failed", end="")
                time.sleep(5)
                continue

            tmp = False

        secrets = []

        for file in files:
            path: str = file["path"]

            if path.endswith(".env"):
                secrets.append(path)

        if len(secrets) == 0:
            print([])
            continue

        with open("secrets.csv", "a") as f:
            print(secrets)

            for sec in secrets:
                f.write(f"{name},{branch},{language},https://github.com/{name}/blob/{branch}/{sec}\n")