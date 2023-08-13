# PIPE

Small flask app from exchanging files between devices in the same local network

## Screenshots:

**Download page:**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Download-page.png)

**Upload page:**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Upload-page.png)

**Upload files to server**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Upload-file-to-server.png)


## Configuration:

**Create virtual environment**

`python -m venv "env"`

**Activate virtual environment**

Linux: `source ./env/bin/activate`

Windows: `./env/Scripts/Activate.ps1`

**Upgrade pip**

`python -m pip install --upgrade pip`

**Install requirements:**

`python -m pip install -r requirements.txt`

**Install node.js requirements:**

`npm install -D --legacy-peer-deps`

**Create an .env environment file using .env.ini as a template**

`cp .env.ini .env`

**Migrate:**

`alembic upgrade head`

**Build assets:**

`npm run build`

## Usage:

**Get help:**

`python run.py -h/--help`

**Start server:**

`python run.py`

**Clear all media files:**

`flask command clear`

## Development:

**Start development server:**

`python run.py --debug`

**Watch assets:**

`npm run watch`

**Make migrations:**

`alembic revision --autogenerate -m "migration comment"`
