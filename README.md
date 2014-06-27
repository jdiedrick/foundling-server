Foundling Server:

You should create your own foundling_globals.py and populate it with your:

aws_public_key

aws_secret_key

mongo_db

Right now its possible to save files to Amazon S3, and retreive a JSON object containing all of the foundlings (geo-tagged sounds, with a URL for the WAV file, and the latitude and longitude for where they were recorded).

Deployment instructions to come

To-do:

Write JSON to MongoDB from client (iOS)

Receive WAV from client (iOS)

Generate web-based map (most of this code was backed up)

--

Setting up the server on Amazon AWS:

Create a python virtual env:

virtualenv foundling-server --no-site-packages

Use that virtual environment as your default python:

source foundling-server/bin/activate

If you're using an Ubuntu instance on Amazon S3 (like I chose), make sure to install python dev before trying to install requirements.txt with pip

sudo aptitude install python-dev

You might need to "sudo aptitude update" first if you can't run the previous command (I didn't have to)

http://stackoverflow.com/questions/5786017/why-cant-i-install-greenlet-just-a-basic-python-package

Install your requirements.txt

pip install -r requirements.txt
