from cryptography.fernet import Fernet
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-key', required = True, type=str, help='decryption key')
args = parser.parse_args()
key = args.key
cipher_suite = Fernet(key)

with open('/path/to/config_encrypted', 'rb') as config:
    encrypted_data = config.read()
    decrypted_data = cipher_suite.decrypt(encrypted_data)
    decoded_json = decrypted_data.decode('utf-8')
    json_data = json.loads(decoded_json)
    
    with open('cfg/config.json', 'w') as config_json:        
        json.dump(json_data, config_json)
