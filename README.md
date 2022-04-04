# bootstrap
Bootstrap scripts for LZ Project creation

# Manual prerequisite steps
* manualy create GH Organization for the project (testt-projectid-name)
* `export GH_ORGANIZATION=testt-projectid-name`
* manually create the Github GH_PAT with sufficient OAUTH rights in Settings -> Developer Settings -> Personal Access Token
* `export GH_PAT=ghp_lRydJ...`
* manually create the Terraform Enterprise Organization Token TFE_ORG_TOKEN as Organization -> Settings -> API Token -> Create Organization Token
* `export TFE_ORG_TOKEN=asdf.gsgf.gad`


# Start the bootstrap script
* install python venv and the dependencies
```python
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```
* and now run the bootstrapping
```bash
./bootstrap.py -o testt-123-myproject -i 123 -n myproject -t lzf-test-123
```
