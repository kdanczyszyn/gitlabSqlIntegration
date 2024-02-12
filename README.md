# Overview
### Description
This project is used to create pipelines between GitLab repository and MSSQL Databases.  

### Process description
Pipelines are used to automaticly get merged code between specified branches and deploy them in the SQL Server.<br>
After successfull merge request, a payload is send through webhook to Jenkins job: job/deployPipeline/ (example in the end).<br>
If jenkins get the payload, a Pipeline script will be executed with data fetched from this payload.<br>
Repository is cloned directly from Jenkins onto the Linux machine that the build is executed on.<br>
Needed informations are stored in **buildParams.json** file on the server.<br>
```bash
def jsonParams = [
    sourcebranch: gitlabSourceBranch,
    targetbranch: gitlabTargetBranch,
    mergeiid: gitlabMergeRequestIid,
    status: gitlabMergeRequestState,
    repo_name: gitlabSourceRepoName.toLowerCase().replaceAll(' ', '-'),
    project_id: gitlabMergeRequestTargetProjectId
  ]

def jsonContent = new groovy.json.JsonBuilder(jsonParams).toPrettyString()

writeFile file: '/path/gitlabSqlIntegration/buildParams.json', text: jsonContent
```

**main.py** reads buildParams.json file and during the process uses its data to make a GET request to repository in order to get info about changed files from the merge request. Next, a script fetches those files from cloned local repository and move it to new folder named RYY.MM eg. R24.02  


### Decrypting /cfg/config.json
This file is not included in repository and is stored in /path/to/project/ directory.
It contains a configuration of SQL databases (servers, databases, users etc.) for each repository and branches.
Its encrypted using python library **cryptography.Fernet**.<br>
Key used to encrypt and decrypt the file is stored in jenkins global variables and also in the Keepass.<br>
If you would like to edit this file: <br>
```bash
cd /path/gitlabSqlIntegration
. /path/to/venv/bin/activate
python dectrypt -key insert_key #file is created in /cfg/ in project dir
python encrypt -key insert_key #file is saved in /path/to/config_encrypted.txt
```

### File Tree
```
.
├── buildParams.json
├── cfg
│   ├── database.py
├── decrypt.py
├── encrypt.py
├── main.py
├── merge_webhook.py
├── README.md
├── requirements.txt
└── tests
    ├── correct
    │   ├── create_table_test_table.sql
    │   └── insert.sql
    ├── rollback
    │   ├── create_table_test_table_failed.sql
    │   └── insert.sql
    └── test_merge_request_functions.py
```

# Contributing
### Configure project
```bash
git clone git@<your_link>
python -m venv venv  # put proper version of python (3.8 or higher)
source /venv/bin/activate
pip install -r requirements.txt
```

