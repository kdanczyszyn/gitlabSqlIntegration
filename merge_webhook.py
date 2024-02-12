import git
import os
import shutil
from cfg.database import SQLDatabase, SQLProcessingError
import json
import requests
from datetime import datetime


class MergeRequest:
    def __init__(self, cfg : dict) -> None:
        self.source_branch = cfg.get('sourcebranch')
        self.target_branch = cfg.get('targetbranch')
        self.mergeiid = cfg.get('mergeiid')
        self.merge_status = cfg.get('mergestatus')
        self.repo_name = cfg.get('repo_name')
        self.project_id = cfg.get('project_id')
        self.token = ''

    def get_modified_files(self, repo_path : str) -> str:
        """
        Args: repo_path : str
        Description: function makes get request to gitlab to fetch changes
        Return: local_path : str (path with changed files)
        """
        release = datetime.now().strftime("R%y.%m")
        local_path = f'/path/gitlabSqlIntegration/{self.repo_name}/{release}'
        if os.path.exists(local_path):
            shutil.rmtree(local_path)
        os.makedirs(local_path, exist_ok=True)
                
        
        url = f"http://gitlab.foo.com/api/v4/projects/{self.project_id}/merge_requests/{self.mergeiid}/changes"
        headers = {'PRIVATE-TOKEN': self.token}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:            
            try:
                changes = response.json()['changes']
                
                items = [file['old_path'] for file in changes if not file['deleted_file']]
                for item in items:
                    print(item)
                    shutil.copy(os.path.join(repo_path, item), os.path.join(local_path, os.path.basename(item)))
            except Exception: 
                print('exception')
                raise Exception

        return local_path        

    def start_process(self) -> None:
        """
        Args: None 
        Description: main process of deploying changes starts here.
            1. Download repo
            2. Get Changes
            3. Start _write_to_database
        Return: None, function _write_to_database() raises Exception if needed
        """        
        repo_path = f'/path/gitlabSqlIntegration/{self.repo_name}/repo/'
        changed_files = self.get_modified_files(repo_path) # get changes 
        
        # start deploying
        # create SQLDatabase object, initalization needed here due to Mocked tests
        db = SQLDatabase(self.repo_name, self.target_branch)     
        
        self._write_to_database(changed_files_path = changed_files, db = db)

    def _write_to_database(self, changed_files_path : str, db : SQLDatabase) -> None:  
        """
        Args: changed_files_path : str, 
                db : SQLDatabase
        Description: Run scripts in database, Raise Exception "SQLProcessingError" if any error during execution occurs
        Return: None        
        """     
        conn = db.connect()
        cursor = conn.cursor()
        files = os.listdir(changed_files_path)
        try:            
            for filename in files:
                if filename.endswith('.sql'):
                    print("Processing ", filename)
                    with open(os.path.join(changed_files_path, filename), 'r') as f:
                        code = f.read()
                        cursor.execute(code) # process each file                
            conn.commit() # end transaction
        except Exception as e:
            cursor.rollback() # rollback entire transaction in case of any error
            raise SQLProcessingError(f'Error processing SQL file: {filename}, {str(e)}.')
        finally:
            conn.close()
