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

def log(message:str, level:str=f"info", end="\n"):

    levelcolor = ""

    if level.lower() == "info":
        levelcolor = f"{Back.LIGHTCYAN_EX}{Fore.BLACK}"
    if level.lower() == "error":
        levelcolor = f"{Back.RED}{Fore.BLACK}"
    if level.lower() == "results":
        levelcolor = f"{Back.YELLOW}{Fore.BLACK}"


    print(f"{Fore.WHITE}[{datetime.now().strftime("%H:%M:%S")}]{Fore.RESET} {levelcolor} {level.upper().ljust(10)}{Fore.RESET}{Back.RESET} {message}", end=end)

query = "stars:<2 created:2026-02-13T11:40:00Z..2026-02-13T11:45:00Z"

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


        tmp = True
        while tmp:
            log(f"Scraping {name}...  ".ljust(70))

            try:
                files = get_files(name)
            except:
                log("Failed to fetch Files","error")
                time.sleep(5)
                continue

            tmp = False

        secrets = []

        for file in files:
            path: str = file["path"]

            if file["type"] == "tree": continue
            if file.get("size", 0) == 0: continue

            if ".env" in path and not "example" in path:
                secrets.append(file)

        if len(secrets) == 0:
            continue

        with open("secrets.csv", "a") as f:
            log(f"Found Secrets for {name}", "results")

            for sec in secrets:
                path = sec["path"]
                f.write(f"{name},{branch},{language},https://github.com/{name}/blob/{branch}/{path},{sec["sha"]}\n")