import os

import boto3
from environs import Env
import requests


env = Env()
env.read_env()  # read .env file, if it exists

DOWNLOAD_PREFIX = env("DOWNLOAD_PREFIX")
BASE_URL = env("BASE_URL")
USERNAME = env("USERNAME")
PASSWORD = env("PASSWORD")


# authenticate
logn = boto3.client('cognito-idp', region_name="eu-central-1")
res = logn.initiate_auth(
            ClientId='58cn4ra5bg54m30jnklhludn9n',
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': USERNAME,
                'PASSWORD': PASSWORD
            }
        )
jwt_token = res.get("AuthenticationResult").get("IdToken")

headers = {
    "Authorization": f"Bearer {jwt_token}"
}

# get all files
files = requests.get(f"{BASE_URL}/fileupload/v1/file-upload/files", headers=headers).json().get("content")
# alternative get only the files for a specific device
# files = requests.get(f"{BASE_URL}/fileupload/v1/file-upload/device/<deviceUid>", headers=headers).json().get("content")

for count, file in enumerate(files):
    print("#############################################")
    print(f"Downloading file {count}/{len(files)}")
    print(f"{file=}")

    file_id = file.get("fileId")
    device_uid = file.get("deviceUid")
    device_file_name = file.get("deviceFileName")
    created_at = file.get("createdAt")

    # get corresponding device_name
    device_name = requests.get(f"{BASE_URL}/feature/registry_manager/{device_uid}", headers=headers).json().get("Item", {}).get("device_name")
    print(f"{device_name=}")

    download_path = f"{DOWNLOAD_PREFIX}/{device_name}/{created_at}"
    download_file = f"{download_path}/{device_file_name}"
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    # get presigned url to download file
    presigned_url = requests.get(f"{BASE_URL}/fileupload/v1/file-upload/file/{file_id}/download", headers=headers).json().get("downloadUrl")

    with requests.get(presigned_url, stream=True) as r:
        r.raise_for_status()
        with open(download_file, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

    # delete the file from the database
    # requests.delete(f"{URL}/fileupload/v1/file-upload/file/{file_id}", headers=headers)
    print("#############################################")





