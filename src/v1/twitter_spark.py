from pyspark.streaming import StreamingContext
from pyspark.sql.functions import *
from pyspark.sql.types import *
from pyspark.streaming.kafka import KafkaUtils
from pyspark.sql.session import SparkSession
import requests
import json
import os


os.environ['SPARK_SUBMIT_ARGS'] = '--packages org.apache.spark:spark-streaming-kafka-0-8-assembly_2.11:2.2.1'

headers = {'content-type': 'application/json'}
elasticsearch_index_uri = 'http://localhost:9200/twitter_nyc/tweet'


def index_to_elasticsearch(x):
    # timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('=================================================================================')
    json_data = json.loads(x)
    doc = {
        'text': json_data['text'],
        'location': json_data['location'],
        'timestamp': json_data['created_at']
    }
    requests.post(elasticsearch_index_uri, data=json.dumps(doc), headers=headers)


def process(time, rdd):
    print("****************")
    df = spark.read.json(rdd)
    df.show()


if __name__ == "__main__":
    spark = SparkSession.builder.master("local[*]").appName("stream").getOrCreate()
    ssc = StreamingContext(spark.sparkContext, 1)
    topic = 'trafficnyc'
    zkQuorum = 'localhost:2181'
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    print('---------------------------------------------------------')
    lines = kvs.map(lambda x: x[1])
    print('Number of incoming tweets in this batch : ' + str(lines.count()))
    lines.pprint()
    lines.foreachRDD(process)
    ssc.start()
    ssc.awaitTermination()
