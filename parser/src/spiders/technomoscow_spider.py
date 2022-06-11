import scrapy
from structlog import get_logger
from w3lib.html import remove_tags
from backend.postgres import TechnoMoscow, get_postgres_connection



logger = get_logger()


class TechnoMoscowSpider(scrapy.Spider):
    name = 'technomoscow'
    start_urls = ['https://technomoscow.ru/resident/']
    psql_db = get_postgres_connection()
    psql_db.bind([TechnoMoscow])


    def send_to_db(self, record):
        with self.psql_db:
            TechnoMoscow.create(
                name=record['name'],
                category=record['category'],
                website=record['website'], 
                tel=record['tel'],
                description=record['description']
            )

    def parse(self, response):
        for companies in response.css('a.resident-item'):
            # logger.info('company', name = companies.css('div.resident-item__title::text').get())
            full_link = 'https://technomoscow.ru' + companies.css('a.resident-item').attrib['href']
            meta = {
                'name': companies.css('div.resident-item__title::text').get(),
                'category': companies.css('div.resident-item__footer-name::text').get(),
            }
            yield response.follow(full_link, callback=self.parse_profile, meta=meta)

    def parse_profile(self, response):
        profile = response.css('div.resident__descr')
        needed_divs = profile.css('div.resident__text-col')

        website = None
        tel = None
        description = None

        try:
            raw_description = needed_divs.css('p').getall()
            full_description = ' '.join(raw_description)
            description = remove_tags(full_description).replace('\r\n', '').replace('\t', '')
        except:
            description = None

        try: 
            website = profile.css('a.resident__label-val').attrib['href']
            tel =  profile.css('a.resident__label-val')[1].attrib['href'].replace('tel:', '')
        except: 
            try:
                website = profile.css('a').attrib['href']
                tel = profile.css('a')[1].attrib['href'].replace('tel:', '')
            except:
                try:
                    website = profile.css('a').attrib['href']
                    tel = None     
                except:
                    website = None
                    tel = None

        profile_info =  {
                'website': website,
                'tel': tel,
                'description': description
            }
        profile_info.update(response.meta)
        logger.info('Profile', **profile_info)
        yield profile_info
            




def main():
    psql_db = get_postgres_connection()
    psql_db.bind([MoscowCompanies])

    with psql_db:
        MoscowCompanies.create(
            company_name=...,
            company_url=...,
            description=...,
        )