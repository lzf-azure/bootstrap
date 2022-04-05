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
parser.add_argument("-i", "--projectId", required=True)
parser.add_argument("-n", "--projectName", required=True)
parser.add_argument("-g", "--ghOrganization", required=True)
parser.add_argument("-t", "--tfeOrganization", required=True)
args = parser.parse_args()

logging.info(f"Args: {args}")
now = datetime.now() # current date and time
current_timestamp = now.strftime("%m/%d/%Y, %H:%M:%S")
 
def setupGithub(args, current_timestamp):
    logging.info(f"Setting up the github connection")
    github = Github(config("GH_PAT"))

    # set the marker
    logging.info(f"Adding repo description for organization {args.ghOrganization}")
    projectOrg = github.get_organization(args.ghOrganization)
    projectOrg.edit(description=f"Bootstrapped by LZF on {current_timestamp}")

    # fork the lzf-seed into this new org
    # find the reference to the repo to copy
    lzfSeedRepo = github.get_repo("lzf-azure/lzf-seed")
    projectLzfRepoName = f"lzf-{args.projectId}-{args.projectName}"
    logging.info(f"will fork repository: {lzfSeedRepo.full_name} into : {args.ghOrganization}/{projectLzfRepoName}")
    # TODO: forking is not a good option, as TFE rights must be secured on the upstream repo as well
    # Solution: use clone and push copy instead 
    projectLzfRepo = lzfSeedRepo.create_fork(organization=args.ghOrganization)

    # set the properties of the new repo
    projectLzfRepo.edit(name=projectLzfRepoName)
    projectLzfRepo.edit(delete_branch_on_merge=True)
    projectLzfRepo.enable_vulnerability_alert()

def setupTfe(args, current_timestamp):
    logging.info("Logging in to TFE org: %s", args.tfeOrganization)
    client = pyterprise.Client()
    client.init(config("TFE_USER_TOKEN"), url='https://app.terraform.io')
    org = client.set_organization(id=args.tfeOrganization)

    logging.info("Existing TFE Workspaces:  %s", len(org.list_workspaces()))
    projectLzfRepoName = f"lzf-{args.projectId}-{args.projectName}"

    vcs_options = {
        "identifier": f"{args.ghOrganization}/{projectLzfRepoName}",
        # "identifier": "abaxsoraszem/conntest",
        "oauth-token-id": config("TFE_GH_OAUTH_TOKEN_ID"),
        "branch": "main"
    }

    logging.info(f"Creating workspace for VCS {vcs_options}")
    org.create_workspace(name=projectLzfRepoName,
                        vcs_repo=vcs_options,
                        auto_apply=False,
                        queue_all_runs=False,
                        working_directory='/',
                        trigger_prefixes=['/'])
    workspace = org.get_workspace(projectLzfRepoName)

    logging.info("Adding variables to access github from terraform provider")
    workspace.create_variable(key='GITHUB_TOKEN', value=config("GH_PAT"), sensitive=True, category='env')
    workspace.create_variable(key='GITHUB_OWNER', value=args.ghOrganization, sensitive=False, category='env')
    workspace.create_variable(key='projectId', value=args.projectId, sensitive=False, category='terraform')  
    workspace.create_variable(key='projectName', value=args.projectName, sensitive=False, category='terraform')  

    logging.info("Workspace runs: %s", len(workspace.list_runs()))

    logging.info("Running intial TFE apply on workspace %s. Dont forget to apply manually", projectLzfRepoName)
    workspace.run()



# setupGithub(args, current_timestamp)
setupTfe(args, current_timestamp )




