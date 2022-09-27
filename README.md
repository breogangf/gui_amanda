# gui_amanda
Graphic Interface to interact with Amanda

# Configuration

## Environment Variables
Create an `.env` file in the root level with the followings keys:
```sh
HOSTNAME=<hostname>
TARGET_AUDIENCE=<target_audience>
KEY_PATH=<path>/key.json
PROJECT_NAME=<project_name>
SUBSCRIPTION_ASSETS=<subscription_assets_name>
SUBSCRIPTION_JOBS=<subscription_jobs_name>
```
## Install Dependencies
To intall the dependencies, you should run the command `pip install -r requirements.txt`

# Creating an installer
For creating an installer to launch the followings:

* For Mac: `pyinstaller --paths lib/python3.9/site-packages --paths .env --clean main.py`
* For UNIX: TODO
* For Win: TODO