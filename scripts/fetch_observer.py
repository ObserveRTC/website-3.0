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
import re
# https://stackoverflow.com/questions/5930542/check-image-urls-using-python-markdown
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

def create_page(title, authors, md_text, date, lastmod, weight, images, referneces):
    # refs = map(lambda ref: "[" + ref + "](" + ref + ")", references)
    items = [
        "---",
        "contributors: %s"%authors,
        "title: \"%s\""%title,
        "date: %s"%date,
        "lastmod: %s"%lastmod,
        "draft: false",
        "menu:",
        "  docs:",
        "    parent: \"overview\"",
        "weight: %s"%weight,
        "toc: true",
        "images: %s"%images,
        "---",
        md_text,
        "## References",
        "\n *".join(referneces)
    ]
    return "\n".join(items)

remote_url = "https://github.com/ObserveRTC/observer"
local_dir = "./repositories/observer"
content_dir = "../content"

def fetch():
    if not os.path.exists(local_dir):
        os.makedirs(local_dir)
        Repo.clone_from(remote_url, local_dir)
    repo = Repo(local_dir)
    repo.remotes.origin.pull()
    
    inside_repo_file = os.path.join("docs", "user-manual.md")
    source_file = os.path.join(local_dir, inside_repo_file)
    commits = list(repo.iter_commits('--all', paths=inside_repo_file))
    authors, first_change, last_change = get_commit_infos(commits)
    date = datetime.fromtimestamp(first_change)
    lastmod = datetime.fromtimestamp(last_change)
    md_text = Path(source_file).read_text()
    
    image_src_path = os.path.join(local_dir, "docs", "images")
    images = []
    lines = []
    for line in md_text.splitlines():
        match = re.search(r"!\[([\s\w\-]+)\]\(images\/([\w/\-\.]+)\)", line)
        if match is None:
            lines.append(line)
            continue
        image = match.group(2)
        alt = match.group(1)
        images.append(image)
        # print(alt, image)
        image_text = '{{{{< img-simple src=\"{image}\" alt=\"{alt}\" >}}}}'.format(image=image, alt=alt)
        lines.append(image_text)
        # text = '{{< img-simple src="observer-overview.png" alt="High-level sketch of the observer inputs and outputs" >}}'
    # !\[([\s\w\-]+)\]\(([\w/\-\.]+)\)
    
    user_manual_page = create_page("Observer",
        authors, 
        "\n".join(lines),
        date, 
        lastmod,
        "1020",
        "[\"" + "\", \"".join(images) + "\"]",
        ["[Schemas](https://github.com/ObserveRTC/schemas-2.0/tree/main/generated-schemas/samples/v2)"]
    )
    # {{< img-simple src="observer-overview.png" alt="High-level sketch of the observer inputs and outputs" >}}
    return user_manual_page, image_src_path, images

import shutil
def main():
    # parser = argparse.ArgumentParser(description=__doc__)

    # parser.add_argument(
    #     "input", nargs="?", default="-",
    #     metavar="INPUT_FILE", type=argparse.FileType("r"),
    #     help="path to the input file (read from stdin if omitted)")

    # args = parser.parse_args()
    target_dir = os.path.join(content_dir, "docs", "overview", "observer")
    user_manual_page, image_src_path, images = fetch()
    for image in images:
        shutil.copy(os.path.join(image_src_path, image), os.path.join(target_dir, image))
    print(user_manual_page, file=open(os.path.join(target_dir, "index.md"), 'w+'))

if __name__ == "__main__":
    main()