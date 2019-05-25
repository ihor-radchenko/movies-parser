from scrapy.commands import ScrapyCommand
from connection import session
from models import Country
import json
import os
import urllib


class Command(ScrapyCommand):

    def run(self, args, opts):
        with open(os.getcwd() + '/../sql/countries.json', encoding='utf-8') as json_countries:
            countries = json.load(json_countries)
            for country in countries:
                if not session.query(Country).filter(Country.name == country.get('name')).first():
                    flag_file_name = os.path.basename(country.get('flag'))
                    urllib.request.urlretrieve(country.get('flag'), os.getcwd() + '/../resources/flags/' + flag_file_name)
                    session.add(Country(
                        name=country.get('name'),
                        alpha_2_code=country.get('alpha2Code'),
                        alpha_3_code=country.get('alpha3Code'),
                        population=country.get('population'),
                        flag_file_name=flag_file_name,
                        flag_external_url=country.get('flag')
                    ))
                    session.commit()

    def short_desc(self):
        return 'Import countries from json to database.'
