from merge_webhook import MergeRequest
import argparse
import json

# Insert your secret token
SECRET_TOKEN = ''

def ReleaseEngine():
    
    with open('buildParams.json') as f:
        cfg = json.load(f)
        merge_status = cfg.get('status')
    
    if merge_status != 'merged':
        print('Wrong merge request status!')
        exit(1)
    else:
        try:
            mr = MergeRequest(cfg)
            mr.start_process()
            print ('Merge Request received. Installation completed without errors.')
            exit(0)
        except Exception as e:
            print('Exception! Message: ', str(e))
            print('Rollback')
            exit(1)


# START
if __name__ == '__main__':
    ReleaseEngine()