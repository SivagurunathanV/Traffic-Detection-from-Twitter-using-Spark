import unittest

from nose.tools import *
from streetaddress import StreetAddressFormatter, StreetAddressParser
from nltk import ne_chunk, pos_tag, word_tokenize
from commonregex import CommonRegex
import csv
import re
import requests
import time

class TestStreetAddress(unittest.TestCase):
    def setUp(self):
        self.addr_parser = StreetAddressParser()
        self.addr_formatter = StreetAddressFormatter()


    def test_success_abbrev_street_avenue_etc(self):
        text = "Disabled truck in Queens OnTheB q e on I 278 WB at Broadway stop and go traffic back to Northern Blvd delay of 2 mins traffic"
        addr = self.addr_parser.parse(text)
        print(addr)
        str = "Mon May 07 05:00:00 +0000 2018"
        ts = time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(str, '%a %b %d %H:%M:%S +0000 %Y'))
        print(ts)
        # chuncked = ne_chunk(pos_tag(word_tokenize(text)))
        # print(chuncked)
        # parsed_text = []
        # regexp = "[0-9]{1,3} .+, .+, [A-Z]{2} [0-9]{5}"
        # address = re.findall(regexp, text)
        # print(address)
        # for chunk in chuncked:
        #     if hasattr(chunk,'label'):
        #         # parsed_text.append(chunk.label(), ' '.join(c[0] for c in chunk))
        #         parsed_text.append(' '.join(c[0] for c in chunk))
        #
        # for parsed_text_word in parsed_text:
        #     parser = CommonRegex(parsed_text_word)
        #     print(parser.street_addresses)

        # with open('/Users/sivagurunathanvelayutham/PycharmProjects/BigDataProjects/src/twitter_traffic_data_static.csv') as file:
        #     reader = csv.reader(file)
        #     for row in reader:
        #         parsed_text = CommonRegex(row[1])
        # eq_(self.addr_formatter.abbrev_street_avenue_etc(addr['street_full']), 'Baker St')

