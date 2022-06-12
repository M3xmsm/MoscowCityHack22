import pandas as pd
import scrapy
from structlog import get_logger
from w3lib.html import remove_tags
from src.postgres import SkolkovoProm, get_postgres_connection


logger = get_logger()


class SkolkovoSpider(scrapy.Spider):
    name = 'skolkovo'
    df = pd.read_csv('/Users/mariabukhtiyarova/Documents/git/MoscowCityHack22/parser/skolkovo_prom_orn_good.csv', converters={'id': str})
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
            
            profile_info =  {
                'name': name,
                'inn': inn,
                'ogrn': ogrn,
                'description': description
            }
            self.send_to_db(profile_info)
            yield profile_info


            # logger.info('company', name = companies.css('div.resident-item__title::text').get())
    #         full_link = 'https://technomoscow.ru' + companies.css('a.resident-item').attrib['href']
    #         meta = {
    #             'name': companies.css('div.resident-item__title::text').get(),
    #             'category': companies.css('div.resident-item__footer-name::text').get(),
    #         }
    #         yield response.follow(full_link, callback=self.parse_profile, meta=meta)

    # def parse_profile(self, response):
    #     profile = response.css('div.resident__descr')
    #     needed_divs = profile.css('div.resident__text-col')

    #     website = None
    #     tel = None
    #     description = None

    #     try:
    #         raw_description = needed_divs.css('p').getall()
    #         full_description = ' '.join(raw_description)
    #         description = remove_tags(full_description).replace('\r\n', '').replace('\t', '')
    #     except:
    #         description = None

    #     try: 
    #         website = profile.css('a.resident__label-val').attrib['href']
    #         tel =  profile.css('a.resident__label-val')[1].attrib['href'].replace('tel:', '')
    #     except: 
    #         try:
    #             website = profile.css('a').attrib['href']
    #             tel = profile.css('a')[1].attrib['href'].replace('tel:', '')
    #         except:
    #             try:
    #                 website = profile.css('a').attrib['href']
    #                 tel = None     
    #             except:
    #                 website = None
    #                 tel = None

    #     profile_info =  {
    #             'website': website,
    #             'tel': tel,
    #             'description': description
    #         }
    #     profile_info.update(response.meta)
    #     self.send_to_db(profile_info)
    #     logger.info('Profile', **profile_info)
    #     yield profile_info
            