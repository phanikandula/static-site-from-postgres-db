import os
from peewee import *

database = PostgresqlDatabase(os.environ['DEMO_DB_NAME'], **{'host': os.environ['DEMO_DB_SERVER'], 'user': os.environ['DEMO_DB_NAME'], 'password': os.environ['DEMO_DB_PASSWORD']})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class SpatialRefSys(BaseModel):
    auth_name = CharField(null=True)
    auth_srid = IntegerField(null=True)
    proj4text = CharField(null=True)
    srid = IntegerField(unique=True)
    srtext = CharField(null=True)

    class Meta:
        table_name = 'spatial_ref_sys'
        primary_key = False

class Usa(BaseModel):
    capital_name = CharField()
    state_id = AutoField()
    state_name = CharField(unique=True)

    class Meta:
        table_name = 'usa'

