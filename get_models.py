import requests
import os

if(not 'models' in os.listdir()):
    os.mkdir('./models')


def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream=True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)


if __name__ == "__main__":
    print('Downloading 1/4 ...')
    download_file_from_google_drive(
        '1HSkg0FCerQ0ueCyIbaPiINgbMEZ67-HX', './models/art.npy')
    print('Downloading 2/4(300MB) ...')
    download_file_from_google_drive(
        '1jkqCth4aV1kU5a_fMcCgjRPXJ1tVJqE5', './models/article.hdf5')
    print('Downloading 3/4(300MB) ...')
    download_file_from_google_drive(
        '1GMrRTY_gvyNxfbg26CFJ_ql86xug0GML', './models/colour.hdf5')
    print('Downloading 4/4(300MB) ...')
    download_file_from_google_drive(
        '1zVBDJlw3UuE2A4TtPjuc2etYizR1wZVm', './models/gender.hdf5')
    print('Done!!!')
