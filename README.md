# static-site-from-postgres-db

## Create DB on remote/cloud service
I used elephantsql.com to create a postgres DB using free tier.

Coped server name, user and default database name and password over into local file that's outside git repo.
```
export DEMO_DB_NAME='foo'
export DEMO_DB_PASSWORD='bar'
export DEMO_DB_SERVER='fooserver'
```

During development, I source this file.

## How to generate peewee models file.
```
python -m pwiz -e postgresql -H $DEMO_DB_SERVER -P $DEMO_DB_PASSWORD -u $DEMO_DB_NAME $DEMO_DB_NAME > models.py
```

Update the generated models.py file to use env vars instead of hardcoded credentials.

## Commands to use repo
```
bash$ fab --list
Available tasks:

  build-website       Get all states and capitals and generate new index.html
  dev-add-state       Provide CLI way to add new entries into remote DB.
  dev-show-states     Prints a list of all states and capitals retrieved from remote db.
  dev-trigger-build   Provides a way to trigger build on remote netlify server using webhook.

```
