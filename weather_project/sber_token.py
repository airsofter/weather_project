import os
import uuid
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key


load_dotenv()

SBER_AUTHORIZATION = os.getenv('SBER_AUTHORIZATION')

env_path = Path(__file__).resolve().parent / '.env'


def get_sber_token(sber_authoriztion):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    rq_uid = str(uuid.uuid4())
    payload = 'scope=GIGACHAT_API_PERS'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': rq_uid,
        'Authorization': f'Basic {sber_authoriztion}'
    }
    response = requests.post(url, headers=headers, data=payload, verify=False)
    set_key(
        env_path, 'SBER_TOKEN',
        response.json()['access_token']
    )
    set_key(
        env_path, 'SBER_TIME_TOKEN',
        str(response.json()['expires_at'])
    )
    load_dotenv(dotenv_path=env_path, override=True)

    return
