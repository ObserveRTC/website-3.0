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
        "  tutorials:",
        "    parent: \"docker\"",
        "weight: %s"%weight,
        "toc: true",
        "---",
        md_text,
    ]
    return "\n".join(items)

remote_url = "https://github.com/ObserveRTC/docker-compose.git"
local_dir = "./repositories/docker-compose"
content_dir = "../content"

def main():
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        Repo.clone_from(remote_url, local_dir)
    repo = Repo(local_dir)
    repo.remotes.origin.pull()

    tutorial_dirs = []
    for entry in os.listdir(local_dir):
        dir_path = os.path.join(local_dir, entry)
        if os.path.isdir(dir_path) is False or entry.startswith("observer-") is False:
            continue
        tutorial_dirs.append(entry)
    weight = 1000
    for tutorial_dir in tutorial_dirs:
        repo_path = os.path.join(local_dir, tutorial_dir)
        content_path = os.path.join(content_dir, "tutorials", "docker", tutorial_dir)
        md_texts = []
        all_commits = []
        found = False
        for entry in os.listdir(repo_path):
            if entry.lower().startswith("readme.md") is False:
                continue
            found = True
            file_path = os.path.join(repo_path, entry)
            md_text = Path(file_path).read_text()
            md_texts.append(md_text)
            inrepo_path = os.path.join(tutorial_dir, entry)
            commits = list(repo.iter_commits('--all', paths=inrepo_path))
            all_commits.extend(commits)
        if found is False:
            print("Did not find readme in dir", entry)
            continue
        authors, first_change, last_change = get_commit_infos(all_commits)
        date = datetime.fromtimestamp(first_change)
        lastmod = datetime.fromtimestamp(last_change)
        md_text = "\n\n".join(md_texts)
        if not os.path.exists(content_path):
            os.makedirs(content_path)
        
        tutorial_title = tutorial_dir.replace("-", " ").title()
        page = create_page(tutorial_title,
            authors, 
            md_text,
            date, 
            lastmod,
            str(weight)
        )
        weight = weight + 10
        print(page, file=open(os.path.join(content_path, "index.md"), 'w+'))

if __name__ == "__main__":
    main()