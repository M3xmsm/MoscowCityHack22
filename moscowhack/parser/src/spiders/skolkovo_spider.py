import pandas as pd
import scrapy
from structlog import get_logger
from w3lib.html import remove_tags
from moscowhack.backend.postgres import SkolkovoProm, get_postgres_connection

logger = get_logger()


class SkolkovoSpider(scrapy.Spider):
    name = 'skolkovo'
    df = pd.read_csv(
        'MoscowCityHack22/parser/skolkovo_prom_orn_good.csv',
         converters={'id': str}
    )
    ids = df['id'].values.tolist()
    start_urls = ['https://navigator.sk.ru/orn/' + id for id in ids]
    psql_db = get_postgres_connection()
    psql_db.bind([SkolkovoProm])

    def send_to_db(self, record):
        with self.psql_db:
            SkolkovoProm.insert(
                name=record['name'],
                inn=record['inn'],
                ogrn=record['ogrn'],
                description=record['description']
            ).execute()

    def parse(self, response):
        for companies in response.css('div.page-content'):

            company_name = companies.css('div.page-header__column')
            company_description = companies.css('div.page-section__main-text')
            company_card = companies.css('div.page-section__column.page-section__column_33')

            name = None
            inn = None
            ogrn = None
            description = None
            try:
                name = company_name.css('p.page__subtitle::text').get()
                inn = company_card.css('div.contact-item__text-2::text')[1].get()
                ogrn = company_card.css('div.contact-item__text-2::text')[2].get()
                description = company_description.css('p::text').getall()
            except:
                name = None
                inn = None
                ogrn = None
                description = None

            profile_info = {
                'name': name,
                'inn': inn,
                'ogrn': ogrn,
                'description': description
            }
            self.send_to_db(profile_info)
            yield profile_info
