#! /usr/bin/env python
"""
Scripts fetch sources from repositories (Also clones the repositories) 
and make markdown sources available for the webpage
"""
from __future__ import print_function
import sys
import argparse
import os
from git import Repo
from operator import itemgetter
from operator import attrgetter
from datetime import datetime
from pathlib import Path

def get_commit_infos(commits):
    authors = set()
    last_change = None
    first_change = None
    for commit in commits:
        committed_date, author = attrgetter("committed_date", "author")(commit)
        if last_change is None or last_change < committed_date:
            last_change = committed_date
        if first_change is None or committed_date < first_change:
            first_change = committed_date
        authors.add(author.name)
    return authors, first_change, last_change

def create_page(title, authors, md_text, date, lastmod, weight):
    # refs = map(lambda ref: "[" + ref + "](" + ref + ")", references)
    items = [
        "---",
        "contributors: %s"%authors,
        "title: \"%s\""%title,
        "date: %s"%date,
        "lastmod: %s"%lastmod,
        "draft: false",
        "images: []",
        "menu:",
        "  docs:",
        "    parent: \"overview\"",
        "weight: %s"%weight,
        "toc: true",
        "---",
        md_text,
    ]
    return "\n".join(items)

remote_url = "https://github.com/ObserveRTC/sfu-observer-js.git"
local_dir = "./repositories/sfu-observer-js"
content_dir = "../content"

def fetch():
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        Repo.clone_from(remote_url, local_dir)
    repo = Repo(local_dir)
    repo.remotes.origin.pull()

    user_manual_file = os.path.join(local_dir, "docs", "user-manual.md")
    user_manual_md = Path(user_manual_file).read_text()

    md_texts = [
        user_manual_md,
    ]

    all_commits = []
    for file in os.listdir(local_dir):
        if file.endswith(".md") is False:
            continue
        commits = list(repo.iter_commits('--all', paths=file))
        all_commits.extend(commits)
    authors, first_change, last_change = get_commit_infos(all_commits)
    date = datetime.fromtimestamp(first_change)
    lastmod = datetime.fromtimestamp(last_change)
    md_text = "\n\n".join(md_texts)

    integration_page = create_page("SFU Integrations",
        authors, 
        md_text,
        date, 
        lastmod,
        "1040"
    )
    return integration_page


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    # parser.add_argument(
    #     "input", nargs="?", default="-",
    #     metavar="INPUT_FILE", type=argparse.FileType("r"),
    #     help="path to the input file (read from stdin if omitted)")

    # args = parser.parse_args()
    target_dir = os.path.join(content_dir, "docs", "overview", "sfu-integrations")
    integration_page = fetch()
    
    print(integration_page, file=open(os.path.join(target_dir, "index.md"), 'w+'))

if __name__ == "__main__":
    main()