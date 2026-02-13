from datetime import datetime
import os
from re import search

from dotenv import load_dotenv

from github import get_files, search_repos

load_dotenv()

from math import ceil
import time
from colorama import Fore
from colorama import Back

def log(message:str, level:str=f"{Back.LIGHTCYAN_EX}{Fore.BLACK}INFO{Back.RESET}{Fore.RESET}", end="\n"):
    print(f"{Fore.WHITE}[{datetime.now().strftime("%H:%M:%S")}]{Fore.RESET} {level.ljust(15)} {message}", end=end)

query = "stars:<2 created:2026-02-12T11:00:00Z..2026-02-12T11:10:00Z"

size = 15

count = search_repos(query)["total_count"]
log(f"Found {count} results...")

searched = []

for p in range(1, ceil(count/size) + 1):
    log(f"Loading Page {p}")
    page = search_repos(query, p, size)



    for repo in page["items"]:
        time.sleep(1)

        name = repo["full_name"]
        branch = repo.get("default_branch", "main")
        language = repo.get("language")

        if name in searched:
            log("Already searched")
            continue

        searched.append(name)

        log(f"Scraping {name}...  ".ljust(50), end="")

        tmp = True
        while tmp:
            try:
                files = get_files(name)
            except:
                log("Failed to fetch Files",f"{Back.RED}{Fore.BLACK}ERROR{Back.RESET}{Fore.RESET}", end="")
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

            log(f"Found Secrets for {name}", f"{Back.MAGENTA}{Fore.BLACK}SECRETS{Back.RESET}{Fore.RESET}")

            for sec in secrets:
                f.write(f"{name},{branch},{language},https://github.com/{name}/blob/{branch}/{sec}\n")