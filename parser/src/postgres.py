from playhouse.db_url import connect
from peewee import (
    Model, TextField,
    CharField, FixedCharField,
    IntegerField, DoubleField,
    BooleanField, DateTimeField
)


def get_postgres_connection():
    psql_db = connect(
        url='postgresext://guest:q1w2e3r4@rc1b-s3a3dtlkkxb1qz6y.mdb.yandexcloud.net:6432/db',
        sslmode='require',
        sslrootcert='CA.pem'
    )
    return psql_db


class TechnoMoscow(Model):
    name = CharField(primary_key=True)
    website = CharField(null=True)
    tel = CharField(null=True)
    category = TextField(null=True)
    description = TextField(null=True)

    class Meta:
        table_name = 'techno_moscow'


class CompaniesInfo(Model):
    short_name = CharField(null=True)
    full_name = TextField(null=True)
    inn = FixedCharField(12, primary_key=True)
    ogrn = FixedCharField(15)
    region = IntegerField(null=True)
    okved_name = TextField(null=True)
    okved_0 = IntegerField(null=True)
    okved_1 = IntegerField(null=True)
    okved_2 = IntegerField(null=True)
    city = CharField(null=True)
    street = CharField(null=True)
    house = CharField(null=True)
    corpus = CharField(null=True)
    apartment = CharField(null=True)
    latitude = DoubleField(null=True)
    longitude = DoubleField(null=True)
    website = CharField(null=True)
    tel = CharField(null=True)
    email = CharField(null=True)
    moscow_support = BooleanField(null=True)
    reg_date = DateTimeField(null=True)
    
    class Meta:
        table_name = 'companies_info'

