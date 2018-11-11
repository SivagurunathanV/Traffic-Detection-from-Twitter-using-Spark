import json

import requests
from elasticsearch import Elasticsearch
from streetaddress import StreetAddressParser
import time

addr_parser = StreetAddressParser()
headers = {'content-type': 'application/json'}
elasticsearch_index_uri = 'http://localhost:9200/twitter_traffic_nyc_demo/tweet'
mapping = {
    "mappings": {
        "tweet": {
            "properties": {
                "text": {
                    "type": "keyword"
                },
                "timestamp": {
                    "type": "date",
                    "format": "yyyy-MM-dd HH:mm:ss"
                },
                "location": {
                    "type": "geo_point"
                },
            }
        }
    }
}
es = Elasticsearch()
es.indices.create(index='twitter_traffic_nyc_demo', body=mapping, ignore=400)


def index_to_elasticsearch(x):
    print('=================================================================================')
    json_data = json.loads(x)
    doc = {
        'text': json_data['text'],
        'location': get_google_results(json_data['text']),
        'timestamp':  time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(json_data['created_at'], '%a %b %d %H:%M:%S +0000 %Y'))
    }
    print(json.dumps(doc))
    requests.post(elasticsearch_index_uri, data=json.dumps(doc), headers=headers)


def get_google_results(txt):
    address = addr_parser.parse(txt)
    geocode_url = "https://maps.googleapis.com/maps/api/geocode/json?address={}".format(address)
    results = requests.get(geocode_url)
    results = results.json()
    if len(results['results']) == 0:
        output = {
            "lat": None,
            "lon": None
        }
    else:
        answer = results['results'][0]
        output = {
            "lat": answer.get('geometry').get('location').get('lat'),
            "lon": answer.get('geometry').get('location').get('lng')
        }

    return output
