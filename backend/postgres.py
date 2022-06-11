from playhouse.db_url import connect
from peewee import Model, TextField, CharField


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
    category = CharField(null=True)
    description = TextField(null=True)

    class Meta:
        table_name = 'techno_moscow'


def main():
    psql_db = get_postgres_connection()
    psql_db.bind([MoscowCompanies])

    with psql_db:
        MoscowCompanies.create(
            company_name=...,
            company_url=...,
            description=...,
        )