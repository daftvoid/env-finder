from datetime import datetime, timezone, timedelta

from dotenv import load_dotenv

from github import get_files, search_repos

load_dotenv()

from math import ceil
import time
from util import log

size = 15

searched = []

# stats
repos_scraped = 0
secrets_found = 0
errors = 0


while True:
    basetime = datetime.now(timezone.utc)

    now = basetime - timedelta(seconds=30)
    before = now - timedelta(seconds=59)

    query = f"stars:<2 language:Python language:JavaScript language:TypeScript created:{before.strftime("%Y-%m-%dT%H:%M:%SZ")}..{now.strftime("%Y-%m-%dT%H:%M:%SZ")}"

    log(f"Querying \"{query}\"")

    count = search_repos(query)["total_count"]
    log(f"Found {count} matching repositories...")

    for p in range(1, ceil(count/size) + 1):
        log(f"Loading Page {p}/{ceil(count/size)}")
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
                    errors += 1
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

            repos_scraped += 1

            if len(secrets) == 0:
                continue

            secrets_found += len(secrets)

            with open("secrets.csv", "a") as f:
                log(f"Found Secrets for {name}", "results")

                for sec in secrets:
                    path = sec["path"]
                    f.write(f"{name},{branch},{language},https://github.com/{name}/blob/{branch}/{path},{sec["sha"]}\n")


    log(f"Repos scraped: {repos_scraped} - Secrets: {secrets_found} - Errors: {errors} - ", "stats")