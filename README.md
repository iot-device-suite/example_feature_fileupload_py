# Feature Fileupload
Simple example script to download all by the iot devices uploaded files. 

## Setup
- Install the needed python packages in a venv
```sh
python -m venv venv
source venv/bin/activate
pip install requests boto3 environs
```
- copy the `.env.template`
```sh
cp .env.template .env
```
- Put your (technical) user account credentials in `.env` file. Be aware that this example only works without activated MFA of the according account.


## Run
```sh
python src/main.py
```
