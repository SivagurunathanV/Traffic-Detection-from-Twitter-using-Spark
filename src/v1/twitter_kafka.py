from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import SimpleProducer, KafkaClient, SimpleClient
import json
import re
# import os
# os.environ['PYSPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.2 pyspark-shell'

access_token = '307283104-wudCmyxuxa4WCSJEaD1AdQIY1C5CqiNhAgkwfOLN'
access_token_secret = '1M72Md4lP9zPyV0WPhJJq4Tfhxorpolg4JpB34EQe4wu6'
consumer_key = 'IYOY5AAXSvl2jktD5Qqq1ziDC'
consumer_secret = 'aV2phJEBufvXm0dfXkusTqrm54frZVY3bGxL9TC2QthWOp8v7a'

hashtags = ["traffic nyc", "#traffic #nyc", "#traffic #ny", "#traffic #newyorkcity", "#traffic #newyork",
            "#accident #newyorkcity",
            "#roadblock #newyorkcity", "#accident #newyork", "#roadblock #newyork", "#accident #nyc",
            "#roadblock #nyc", "#accident #ny", "#roadblock #ny"]


# hashtags=["#traffic #cleaveland","#traffic #cleaveland", "#traffic #cleaveland", "#traffic #accident #cleaveland","#traffic #roadblock #cleaveland"]
# hashtags=["#traffic", "#traffic #accident","#traffic #roadblock"]

class StdOutListener(StreamListener):
    def on_data(self, data):
        status = json.loads(data)
        try:
            processed_String = ' '.join(
                re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|(\ART )", " ", status['text']).split())
            processed_String = ' '.join(processed_String.split('\n'))
            print(status['text'])
            print(str(status['user']['location']).encode('utf-8'))
            print(status['created_at'])
            print(processed_String)
            new_data = {'text': processed_String, 'location': str(status['user']['location']).encode('utf-8'),
                        'created_at': status['created_at']}
            new_data = json.dumps(new_data)
            producer.send_messages("trafficnyc", new_data.encode("utf-8"))
            print('--------------------------------------------------')
            return True
        except:
            print('----------------------------------------------------')

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    kafka = SimpleClient("localhost:9092")
    producer = SimpleProducer(kafka)
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)
    stream.filter(track="#WorldLaughterDay", languages=["en"],
                  follow=['42640432'])  # ,locations=[-74.1687,40.5722,-73.8062,40.9467])
