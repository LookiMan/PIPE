# PIPE

Exchange files between devices in the same local wifi network

<hr>

**Download page:**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Download-page.png)

<hr>

**Upload page:**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Upload-page.png)

<hr>

# Usage:

**Create virtual environment**

`python -m venv "env"`

**Activate virtual environment**

Windows: `./env/Scripts/Activate.ps1`

Linux: `source ./env/bin/activate`

**Upgrade pip**

`python -m pip install --upgrade pip`

**Install requirements:**

`python -m pip install -r requirements.txt`

**Install nodejs requirements:**

`npm install -D --legacy-peer-deps`

**Make migrations:**

`alembic revision --autogenerate -m "init"`

**Migrate:**

`alembic upgrade head`

**Get help:**

`python run.py -h/--help`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Help-text.png)

<hr>

**Run server with distributing a file:**

`python run.py -f photo.png`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/File-distribution-screenshot.png)

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/The-file-download-page-is-open-via-a-link-with-the-specified-code.png)

<hr>

**Run server without distributing a file (If you only need to get the file from another device):**

`python run.py`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Run-server-without-distributing-a-file.png)

<hr>

**Run server with custom port (default 5000):**

`python run.py 5001`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Run-server-with-custom-port.png)

<hr>

**Upload files to server**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Upload-file-to-server.png)

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Successfully-uploaded-file-to-server.png)

<hr>

**Build assets:**

`npm run build`

**Watch assets (for the development):**

`npm run watch`


**Clear all media files:**

`flask command clear`
