#!/usr/bin/env python3


from github import Github
from decouple import config
import argparse
import logging

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)


logging.info(f"Bootstrapping started")

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--organization", required=True)
parser.add_argument("-i", "--projectId", required=True)
parser.add_argument("-n", "--projectName", required=True)
args = parser.parse_args()

logging.info(f"Args: {args}")
 

github = Github(config("GH_PAT"))

# set the marker
logging.info(f"Adding repo description")
projectOrg = github.get_organization(args.organization)
projectOrg.edit(description="Bootstrapped by LZF")

# fork the lzf-seed into this new org
# find the reference to the repo to copy
lzfSeedRepo = github.get_repo("lzf-azure/lzf-seed")
projectLzfRepoName = f"lzf-{args.projectId}-{args.projectName}"
logging.info(f"will fork repository: {lzfSeedRepo.full_name} into : {args.organization}/{projectLzfRepoName}")
projectLzfRepo = lzfSeedRepo.create_fork(organization=args.organization)

# set the properties of the new repo
projectLzfRepo.edit(name=projectLzfRepoName)
projectLzfRepo.edit(delete_branch_on_merge=True)
projectLzfRepo.enable_vulnerability_alert()






