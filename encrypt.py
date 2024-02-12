from cryptography.fernet import Fernet
import json
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('-key', required = True, type=str, help='decryption key')
args = parser.parse_args()
key = args.key
cipher_suite = Fernet(key)

with open('cfg/config.json', 'r') as config:
    data = json.load(config)
    encrypted_data = cipher_suite.encrypt(json.dumps(data).encode())
    
    with open('/home/ubuntu/.config/webhook/config_encrypted', 'wb') as config_json:        
        config_json.write(encrypted_data)