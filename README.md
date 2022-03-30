# bootstrap
Bootstrap scripts for LZ Project creation

# Manual prerequisite steps
* manualy create GH Organization for the project (testt-projectid-name)
* `export GH_ORGANIZATION=testt-projectid-name`
* manually create the GH_PAT with sufficient OAUTH rights in Settings -> Developer Settings -> Personal Access Token
* `export GH_PAT=ghp_lRydJ...


# Start the bootstrap script
* install python venv and the dependencies
```python
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
```
* and now run the bootstrapping
```bash
./bootstrap.py -o testt-123-myproject -i 123 -n myproject
```
