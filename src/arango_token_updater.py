import base64
import argparse
import os
import requests


def base64_encode_string(token):
    '''Encode token to base64'''
    encoded_bytes = base64.b64encode(token.encode("utf-8"))
    return str(encoded_bytes, "utf-8")


def get_arango_jwt_token(uri, usr, passwd):
    """Return base64-encoded arangoDB jwt token"""
    response = requests.post(
        f'http://{uri}/_open/auth',
        headers={'Content-Type': 'application/json'},
        json={
            "username": usr,
            "password": passwd
        },
        timeout=5
    )
    
    return base64_encode_string(response.json()['jwt'])


def patch_secret(secret, token):
    bash_command = f"kubectl patch secret {secret} -p=\"(\\\"data\\\": (\\\"token\\\": \\\"{token}\\\"))\" -n kube-prometheus-stack"
    os.system(bash_command
              .replace("(", "{")
              .replace(")", "}")
    )


def main():
    parser = argparse.ArgumentParser(description='ArangoDB Token updater')
    parser.add_argument(
        '--secret',
        type=str,
        required=True,
        help='Secret name for arangodb token'
    )
    arg = parser.parse_args()
    
    user = os.getenv('USERNAME')
    passwd = os.getenv('PASSWORD')
    uri = os.getenv('URI')
    
    token = get_arango_jwt_token(uri, user, passwd)
    
    patch_secret(arg.secret, token)
      

if __name__ == '__main__':
    main()
