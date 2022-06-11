import scrapy
from structlog import get_logger


logger = get_logger()


class TechnoMoscowSpider(scrapy.Spider):
    name = 'technomoscow'
    start_urls = ['https://technomoscow.ru/resident/']

    def parse(self, response):
        for companies in response.css('a.resident-item'):
            logger.info('company', name = companies.css('div.resident-item__title::text').get())
            full_link = 'https://technomoscow.ru' + companies.css('a.resident-item').attrib['href']
            yield {
                'name': companies.css('div.resident-item__title::text').get(),
                'type': companies.css('div.resident-item__footer-name::text').get(),
                'full_link': full_link
            }
            yield response.follow(full_link, callback = self.parse_profile)

    # def parse_next_page(self, response):
    #     for link in response.css('a.resident-item'):
    #         companies = response.css('a.resident-item')
    #         full_link = 'https://technomoscow.ru' + companies.css('a.resident-item').attrib['href']
    #         yield response.follow(full_link, callback = self.parse_profile)
    
    def parse_profile(self, response):
        profile = response.css('div.resident__descr')
        needed_divs = profile.css('div.resident__text-col')
        logger.info('Profile', name=profile.css('span.resident__title-text::text').get())

        # website_1 = None
        # if profile.css('a.resident__label-val') is not None:
        #     try: 
        #         website_1 = profile.css('a.resident__label-val').attrib['href']
        #     except Exception as e:
        #         logger.error('Error', exception=str(e))
        #         website_1 = None

        # website_2 = None
        # if profile.css('a') is not None:     
        #     try:
        #         website_2 = profile.css('a').attrib['href']
        #     except Exception as e:
        #         logger.error('Error', exception=str(e))
        #         website_2 = None
    
        # yield {
        #     'website_1': website_1,
        #     'website_2': website_2
        # }


        try:
            yield {
                'website': profile.css('a.resident__label-val').attrib['href'],
                'tel': profile.css('a.resident__label-val')[1].attrib['href'].replace('tel:', ''),
                'description': needed_divs.css('p').getall()
            }
        except:
            try:
                yield {
                    'website': profile.css('a').attrib['href'],
                    'tel': profile.css('a')[1].attrib['href'].replace('tel:', ''),
                    'description': needed_divs.css('p').getall()
                }
            except:
                try:
                    yield {
                        'website': profile.css('a').attrib['href'],
                        'tel': None,
                        'description': needed_divs.css('p').getall()
                    }
                except:
                    try:
                        yield {
                            'website': None,
                            'tel': None,
                            'description': needed_divs.css('p').getall()
                        }
                    except:
                        yield {
                            'website': None,
                            'tel': None,
                            'description': None
                        }
        finally:
            yield {
                'website': None,
                'tel': None,
                'description': None
            }
