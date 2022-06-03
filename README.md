# PIPE

Exchange files between devices in the same local wifi network

<hr>

**Download page:**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Download-page.png)

<hr>

**Upload page:**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Upload-page.png)

<hr>

**Get help:**

`python master.py -h/--help`

<hr>

**Run server with distributing a file:**

`python master.py -f photo.png`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/File-distribution-screenshot.png)

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/The-file-download-page-is-open-via-a-link-with-the-specified-code.png)

<hr>

**Run server without distributing a file (If you only need to get the file from another device):**

`python master.py`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Run-server-without-distributing-a-file.png)

<hr>

**Run server with custom port (default 5000):**

`python master.py 5001`

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Run-server-with-custom-port.png)

<hr>

**Upload files to server**

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Upload-file-to-server.png)

![](https://github.com/LookiMan/PIPE/blob/master/screenshots/Successfully-uploaded-file-to-server.png)

<hr>

**Run sass (for the development):**

`cd static/assets`

`sass --watch scss\style.scss:css\style.css`
