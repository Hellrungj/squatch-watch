# SQUATCH WATCH REVIEW

*Created: 11/9/2018*

*Made by John J. Hellrung*

## Introduction

This is for review of the squatch watch project.

The following is a recount of the event that happened during the project.

*11/9 - Day One*

* Installed zip file
* Creadted a folder called `squatch_watch`
* Unziped and moved files to `squatch_watch` folder
* Checked verson of python version -command: `python -V` -result: `2.7.12`
* Ran `virtualenv venv` to make a virtual environment for the project
* Ran `source venv/bin/activate` to activated virtual environment for the project
* Ran `pip install -r requirements.txt`to install all the requred dependences for the project
* Run `python manage.py runserver`to run the server
* `ISSUE:` When running `python manage.py runserver`

```bash
$ python manage.py runserver
  File "manage.py", line 14
    ) from exc
         ^
SyntaxError: invalid syntax
```

* `Resolved:` Found [Reddit Django Post](https://www.reddit.com/r/django/comments/8srdai/can_someone_help_me_fix_this_error_from_exc/) and then use python 3. Current using `3.5.2`
* Run `python3 manage.py runserver`to run the server
* `ISSUE:` When running `python3 manage.py runserver`

```bash
$ python3 manage.py runserver
Performing system checks...

Unhandled exception in thread started by <function check_errors.<locals>.wrapper at 0x7faf946cba60>
Traceback (most recent call last):
  File "/usr/local/lib/python3.5/dist-packages/django/utils/autoreload.py", line 228, in wrapper
    fn(*args, **kwargs)
  File "/usr/local/lib/python3.5/dist-packages/django/core/management/commands/runserver.py", line 125, in inner_run
    self.check(display_num_errors=True)
  File "/usr/local/lib/python3.5/dist-packages/django/core/management/base.py", line 359, in check
    include_deployment_checks=include_deployment_checks,
  File "/usr/local/lib/python3.5/dist-packages/django/core/management/base.py", line 346, in _run_checks
    return checks.run_checks(**kwargs)
  File "/usr/local/lib/python3.5/dist-packages/django/core/checks/registry.py", line 81, in run_checks
    new_errors = check(app_configs=app_configs)
  File "/usr/local/lib/python3.5/dist-packages/django/core/checks/urls.py", line 16, in check_url_config
    return check_resolver(resolver)
  File "/usr/local/lib/python3.5/dist-packages/django/core/checks/urls.py", line 26, in check_resolver
    return check_method()
  File "/usr/local/lib/python3.5/dist-packages/django/urls/resolvers.py", line 254, in check
    for pattern in self.url_patterns:
  File "/usr/local/lib/python3.5/dist-packages/django/utils/functional.py", line 35, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
  File "/usr/local/lib/python3.5/dist-packages/django/urls/resolvers.py", line 405, in url_patterns
    patterns = getattr(self.urlconf_module, "urlpatterns", self.urlconf_module)
  File "/usr/local/lib/python3.5/dist-packages/django/utils/functional.py", line 35, in __get__
    res = instance.__dict__[self.name] = self.func(instance)
  File "/usr/local/lib/python3.5/dist-packages/django/urls/resolvers.py", line 398, in urlconf_module
    return import_module(self.urlconf_name)
  File "/usr/lib/python3.5/importlib/__init__.py", line 126, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
  File "<frozen importlib._bootstrap>", line 986, in _gcd_import
  File "<frozen importlib._bootstrap>", line 969, in _find_and_load
  File "<frozen importlib._bootstrap>", line 958, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 673, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 665, in exec_module
  File "<frozen importlib._bootstrap>", line 222, in _call_with_frames_removed
  File "/mnt/c/Users/hellrungj/Desktop/squatch_watch/squatch_watch/urls.py", line 17, in <module>
    from django.urls import path
ImportError: cannot import name 'path'
```
* `Resolved:` Found [stackoverflow Django Post](https://stackoverflow.com/questions/47563013/unable-to-import-path-from-django-urls) and then I ran `pip3 install --upgrade django`.
* Ran `python3 manage.py runserver`to run the server
* Opened Chrome at http://127.0.0.1:8000/ and application worked
* Stoped the server and Ran `python3 manage.py mirgate` to mirgate
* `python3 manage.py createsuperuser`to create superuser
* Opened Chrome at http://127.0.0.1:8000/admin and login with new superuser and application worked redirected me to the admin panel
* Created a route for monsters app in `url.py` and a `url.py` for monsters app 
* Created a `layout.html`, `index.html`, `details.html`, `upload.html` page
* Started index, details and upload_csv view linking it them to their template
* Created a route for each page in the monsters `urls.py`
* Tested each template with url -result `Working`
* Worked on upload_csv to created a simple upload action
    * Modifed the `setting.py` to include `MEDIA_URL` and `MEDIA_ROOT` for uploading files
    * Modifed the `squatch_watch\url.py` and added debuging features.
    * Modifed the upload_csv action in `squatch_watch\view.py` to check if there is a post request then upload and then display upload page
    * Modifed the `upload.html` page with a choose file button and upload button and a link along with a link the shows up if a file has been uploaded
    * Tested the upload action with uploading a sample csv from the sample folder in the project. -Result: The page was rerender with a new link of the filepath of the uploaded file and the filesystem now inculdes the uploaded file in the media folder
* Worked on making models for the database
    * Made a tables for Researcher, Monster, Sighting and MonsterReport based on the follow instuctions:

``` text
MonsterReport: refers to a single CSV report that is comprised of many sightings
Sighting: an instance of a researcher spotting a monster at a specific time and location
Researcher: the human credited with finding the monster (unique across all sightings)
Monster: the monster spotted (unique across all sightings)
```

Here is a schema for the following data:

``` Text
MonsterReport
    |
Sighting - Monster
    |
Researcher

```

    * Modifed the `admin.py` to inculde the models in the admin pages
    * Ran `python3 manage.py makemigrations monsters` to make migration for the monster model
    * Ran `python3 manage.py migrate` to migrate to the new migration
    * Tested the admin pages and the four tables show and all field are working
 