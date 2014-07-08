Foundling Server

Current URL: http://ec2-107-20-106-161.compute-1.amazonaws.com/

You should create your own foundling_globals.py and populate it with your:

aws_public_key

aws_secret_key

mongo_db

foundling_aws_base_url

Right now its possible to save files to Amazon S3, and retreive a JSON object containing all of the foundlings (geo-tagged sounds, with a URL for the WAV file, and the latitude and longitude for where they were recorded).

Deployment instructions to come

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
