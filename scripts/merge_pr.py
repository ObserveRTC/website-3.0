import argparse
import json
import requests
import subprocess
from git import Repo
from github import Github

def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-p','--project', help='The github project', required=True, type=str)
    parser.add_argument('-r','--repo', help='The github repository', required=True, type=str)
    parser.add_argument('-t','--token', help='The github token', required=True, type=str)
    parser.add_argument('-b','--branch', help='The name of the new branch', required=True, type=str)
    parser.add_argument('-cm','--commitmessage', help='The name of the new branch', required=True, type=str)
    parser.add_argument('-ti','--title', help='The title of the new PR', required=True, type=str)
    parser.add_argument('-bm','--bodymessage', help='The body message of the new PR', required=True, type=str)

    args = parser.parse_args()
    
    repo = Repo("../.git")
    main_branch_name = "main"  
    new_branch_name = args.branch
    current = repo.create_head(new_branch_name)
    current.checkout()
     
    master = repo.heads.main
    repo.git.pull('origin', master)
    #creating file
    if repo.index.diff(None) or repo.untracked_files:
        repo.git.add(A=True)
        repo.git.commit(m=args.commitmessage)
        repo.git.push('--set-upstream', 'origin', current)
        print('Changes detected, (hopefully) PR is created and merged')
    else:
        print('no changes detected, no pr is created')
        exit(0)

    g = Github(args.token)

    repo = g.get_repo("ObserveRTC/website-3.0")
    body = args.bodymessage

    pr = repo.create_pull(title=args.title, body=body, head=new_branch_name, base=main_branch_name)
    print("Created PR with name {} for branch {}".format(args.title, new_branch_name))
    base = repo.get_branch(main_branch_name)
    head = repo.get_branch(new_branch_name)

    merge_to_master = repo.merge(main_branch_name, head.commit.sha, args.commitmessage)
    print("PR {} for branch {} is merged into {}".format(args.title, new_branch_name, main_branch_name))
    
    try:
        ref = repo.get_git_ref(f"heads/{new_branch_name}")
        ref.delete()
        print("Branch {} is deleted".format(new_branch_name))
    except UnknownObjectException:
        print('No such branch', new_branch_name)
    

if __name__ == "__main__":
    main()