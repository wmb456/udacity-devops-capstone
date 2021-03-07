import requests
from os import getenv

service_address = getenv('COWSAY_SERVICE_ADDRESS', '127.0.0.1:8080')
service_url = f'http://{service_address}'

def test_index():

    response = requests.get(service_url)
    assert response.status_code == 200

def test_get_speakers():

    response = requests.get(f'{service_url}/speakers')
    assert response.status_code == 200
    assert 'cow' in response.text

def test_say_invalid_method():

    response = requests.get(f'{service_url}/say')
    assert response.status_code == 405

def test_post_say_missing_properties():

    response = requests.post(f'{service_url}/say')
    assert response.status_code == 400

def test_post_say():

    test_message = 'ZXCVBNMASDFGHJKLQWERTYUIOP'
    form_data = {
        'speaker': 'cow',
        'message': test_message
    }
    response = requests.post(f'{service_url}/say', data=form_data)
    assert response.status_code == 200
    assert test_message in response.text





