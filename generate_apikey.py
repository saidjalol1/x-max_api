import secrets


api_key_storage = []


def generate_api_key():
    api_key = secrets.token_hex(64)
    api_key_storage.append(api_key)
    print(api_key)
    return api_key

def generate_super_key():
    super_key  = secrets.token_hex(32)
    print(super_key)
    return super_key

def generate_token_for_user():
    token = secrets.token_hex(16)
    return token

generate_api_key()
generate_super_key()
