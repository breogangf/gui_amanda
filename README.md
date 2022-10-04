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
To create an installer, you should launch the followings command:

For console:
```bash
pyinstaller main_console.py --paths <your_python_dependecies> --add-data '.env:.' --onefile --name amanda --clean -y
```
For window:
```bash
pyinstaller main_gui.py --windowed --paths <your_python_dependecies> --add-data '.env:.' --add-data 'images:images' --ico images/amanda.jpg --onefile --name amanda --clean -y
```

If you created a virtual environment, most likely the path will look like as `lib/python3.x/site-packages`, where `x` can be different depending of the minor version