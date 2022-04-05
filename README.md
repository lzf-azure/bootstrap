# bootstrap
Bootstrap scripts for LZ Project creation

# Manual prerequisite steps Github
* manualy create GH Organization for the project (testt-projectid-name)
* `export GH_ORGANIZATION=testt-projectid-name`
* manually create the Github GH_PAT with sufficient OAUTH rights in Settings -> Developer Settings -> Personal Access Token
* `export GH_PAT=ghp_lRydJ...`

# Manual setup TFE
* set up your TFE user token
`export TFE_USER_TOKEN=123.atlasv1.456`
* create a new TFE Organization, eg `lzf-test-123`
This will be the organization, where TFE will be hosting the workspaces for the GH repositories
* create the Terraform Enterprise Organization Token TFE_ORG_TOKEN as Organization -> Settings -> API Token -> Create Organization Token.
This token will allow the python script to access the TFE API on behalf of the TFE Organization
* `export TFE_ORG_TOKEN=asdf.gsgf.gad`
* create TFE connection to GH (OAUTH Token): TFE -> Organization Settings -> Providers -> Add VCS Provider -> github.com(custom). You will need to also create the GH Application to which it is linked, and copy the Client ID and Client Secret back to TFE. Ultimately, GH will issue and OAUTH token for TFE, which will be referenced by TFE_GH_OAUTH_TOKEN_ID in the bootstrap script. At this step, you will need to grant access to the GH organization created above. 
Note: if the repo is forked, then the upstream organization must also grant access.
* `export TFE_GH_OAUTH_TOKEN_ID=ot-...` 


# Start the bootstrap script
* install python venv and the dependencies
```python
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```
* and now run the bootstrapping
```bash
./bootstrap.py -g testt-123-myproject -i 123 -n myproject -t lzf-test-123
```
