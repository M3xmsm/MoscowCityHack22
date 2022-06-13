from peewee import (
    Model, TextField,
    CharField, FixedCharField,
    IntegerField, DoubleField,
    BooleanField, DateTimeField
)
from playhouse.db_url import connect
from playhouse.postgres_ext import ArrayField


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


class MoscowProducts(Model):
    short_name = CharField(null=True)
    full_name = TextField(null=True)
    inn = FixedCharField(12)
    ogrn = FixedCharField(15)
    register_number = CharField(null=True)
    product_name = TextField(null=True)
    okpd2 = CharField(null=True)
    tnved = CharField(null=True)
    name_of_regulations = TextField(null=True)
    okved_name = TextField(null=True)
    okved_0 = IntegerField(null=True)

    class Meta:
        table_name = 'moscow_products'


class SkolkovoProm(Model):
    name = CharField(primary_key=True)
    inn = FixedCharField(12)
    ogrn = FixedCharField(15)
    description = TextField(null=True)

    class Meta:
        table_name = 'skolkovo_prom'

class AnalyticsDataTry(Model):
    inn = FixedCharField(12, primary_key=True)                    
    num_products = IntegerField(null=True)          
    has_products = BooleanField(null=True)          
    available_data_count = IntegerField(null=True)   
    missing_data = ArrayField(CharField)         
    similar_producers_num = IntegerField(null=True) 
    
    class Meta:
        table_name = 'analyticsdatatry'

        