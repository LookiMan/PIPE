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

<hr>

**Activate virtual environment**

Linux: `source ./env/bin/activate`

Windows: `./env/Scripts/Activate.ps1`

<hr>

**Upgrade pip**

`python -m pip install --upgrade pip`

<hr>

**Install requirements:**

`python -m pip install -r requirements.txt`

<hr>

**Install node.js:**

[Download node.js from website](https://nodejs.org/en/download)

<hr>

**Install node.js requirements (Webpack and other libraries from package.json):**

`npm install -D --legacy-peer-deps`

<hr>

**Install Sass from compile scss to css (If you don't want to install Webpack)**

`npm install -g sass`

<hr>

**If you don't install Webpack replace next line in `/app/templates/base.html`**

`<script type="text/javascript" src="{{ url_for('static', filename='assets/dist/bundle.js') }}" async></script>`

**to**

`<script type="text/javascript" src="{{ url_for('static', filename='assets/js/app.js') }}" async></script>`

**and remove first line from `/app/static/assets/js/app.js`**:

`import '../scss/style.scss';`

<hr>

**Create an .env environment file using .env.ini as a template:**

`cp .env.ini .env`

<hr>

**Migrate:**

`alembic upgrade head`

<hr>

**Build assets use webpack:**

`npm run build`

<hr>

**Build styles use sass (If webpack Webpack not installed)**

`sass ./app/static/assets/scss/style.scss:./app/static/assets/dist/bundle.css`

<hr>

## Usage:

**Get help:**

`python run.py -h/--help`

<hr>

**Start server:**

`python run.py`

<hr>

**Clear all media files:**

`flask command clear`

<hr>

## Development:

**Start development server:**

`python run.py --debug`

<hr>

**Watch assets use Webpack:**

`npm run watch`

<hr>

**Watch styles use sass (If Webpack not installed)**

`sass --watch ./app/static/assets/scss/style.scss:./app/static/assets/dist/bundle.css`

<hr>

**Make migrations:**

`alembic revision --autogenerate -m "migration comment"`

<hr>
