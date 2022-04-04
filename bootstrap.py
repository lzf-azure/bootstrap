#!/usr/bin/env python3


from re import A
from github import Github
from decouple import config
import argparse
import logging
from datetime import datetime
import pyterprise


logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', level=logging.INFO)


logging.info(f"Bootstrapping started")

parser = argparse.ArgumentParser()
parser.add_argument("-o", "--organization", required=True)
parser.add_argument("-i", "--projectId", required=True)
parser.add_argument("-n", "--projectName", required=True)
parser.add_argument("-t", "--tfeOrganization", required=True)
args = parser.parse_args()

logging.info(f"Args: {args}")
now = datetime.now() # current date and time
current_timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
 
def setupGithub(args, current_timestamp):
    logging.info(f"Setting up the github connection")
    github = Github(config("GH_PAT"))

    # set the marker
    logging.info(f"Adding repo description for organization {args.organization}")
    projectOrg = github.get_organization(args.organization)
    projectOrg.edit(description=f"Bootstrapped by LZF on {current_timestamp}")

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

def setupTfe(args, current_timestamp):
    logging.info(f"Setting up the TFE connection for {args.tfeOrganization}")
    client = pyterprise.Client()
    client.init(config("TFE_ORG_TOKEN"), url='https://app.terraform.io')
    org = client.set_organization(id=args.tfeOrganization)

    logging.info(f"Existing TFE Workspaces: {org.list_workspaces()}")
    # workspaceName = f"lzf-{args.projectId}-{args.projectName}"



# setupGithub(args, current_timestamp)
setupTfe(args, current_timestamp )




