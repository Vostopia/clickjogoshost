ClickJogos Client
=================
Server for hosting a vostopia game on heroku using
ClickJogos Connect (http://connect.clickjogos.uol.com.br/docs/). Intended
for hosting on Heroku (http://www.heroku.com).


Environment Variables
---------------------
The following environment variables should be set:

* DATABASE_URL - heroku-style url to database (set automatically by heroku postgres)
* CLICKJOGOS_KEY - public clickjogos key
* CLICKJOGOS_SECRET - private clickjogos key
* AWS_ACCESS_KEY_ID - amazon aws access key (used to upload assets to s3)
* AWS_SECRET_ACCESS_KEY - amason aws secret key (used to upload assets to s3)
* AWS_STORAGE_BUCKET_NAME - amazon s3 bucket name to upload assets to
* DJANGO_SECRET_KEY - secret key to this django instance

Optional:
* REDISCLOUD_URL - url to redis, used for sessions to avoid to store the session data in the database (set automatically by the rediscloud addon)
* AWS_STORAGE_BUCKET_PREFIX - prefix (path) to add to all items uploaded s3


Heroku Addons
-----------
* rediscloud - used for sessions
* heroku-postgresql - We're using the basic (hobby-basic) plan.


Getting Started
---------------
Get clickjogoshost from github
> git clone git@github.com:Vostopia/clickjogoshost.git

> cd clickjogoshost

Create heroku app. This should also create a git remote called heroku in your current git repo
> heroku apps:create clickjogoshost-test

Add postgres and rediscloud addons
> heroku addons:add heroku-postgresql:hobby-basic --app clickjogoshost-test
> heroku addons:add rediscloud --app clickjogoshost-test

Set clickjogos key and secret for your clickjogos sso integration
> heroku config:set CLICKJOGOS_KEY="..." CLICKJOGOS_SECRET="..." --app clickjogoshost-test

Create an amazon aws account, and create a a s3 bucket and set the configuration parameters to the heroku app
> heroku config:set AWS_ACCESS_KEY_ID="..." AWS_SECRET_ACCESS_KEY="..." AWS_STORAGE_BUCKET_NAME="..." --app clickjogoshost-test

Create a (long) random string and use as django secret
> heroku config:set DJANGO_SECRET_KEY="..."

Deploy the project to heroku
> git push heroku master

Create the database tables
> heroku run python manage.py syncdb --app clickjogoshost-test
> heroku run python manage.py migrate --app clickjogoshost-test

Create a superuser (for uploaing webplayers)
> heroku run python manage.py createsuperuser --app clickjogoshost-test

Go to the admin interface on http://clickjogoshost-test.herokuapp.com/admin and log in with the newly created superuser.
In the admin interface, you can add a "webplayer", where you can upload a unity3d file, and an image to show if the user is not logged in.